#!/usr/bin/env python3
"""ternary-rom CLI: Model-to-GDS flow for mask-locked ternary inference chips.

Commands:
    ternary-rom analyze MODEL_PATH    Analyze model and show sensitivity report
    ternary-rom ternarize MODEL_PATH  Ternarize model weights
    ternary-rom netlist WEIGHTS_DIR   Generate structural Verilog from ternary weights
    ternary-rom cells PROCESS         Generate cell library files
    ternary-rom flow NETLIST_PATH    Run OpenROAD flow (generate Tcl or execute)
    ternary-rom info                 Show system info and supported processes
"""

import argparse
import os
import sys
from pathlib import Path


def _load_weights(path: str):
    """Load weights from .npy or .npz file.

    Returns dict of {name: np.ndarray}.
    """
    import numpy as np

    p = Path(path)
    if p.suffix == ".npz":
        data = dict(np.load(str(p)))
        # If keys look like array names, use directly.
        # If there's a single 'weights' key, expand it.
        if "weights" in data and len(data) == 1:
            w = data["weights"]
            if w.ndim == 3:
                # Assume shape (num_layers, rows, cols)
                return {f"layer_{i}": w[i] for i in range(w.shape[0])}
            return {"weights": w}
        return data
    elif p.suffix == ".npy":
        w = np.load(str(p))
        return {"weights": w}
    else:
        # Try loading as npz
        try:
            data = dict(np.load(str(p), allow_pickle=False))
            return data
        except Exception:
            raise ValueError(
                f"Unsupported file format: {path}. Use .npy or .npz"
            )


def _load_ternary_weights(path: str):
    """Load ternary weights from .npz file.

    Returns dict of {name: np.ndarray} with int8 dtype.
    """
    import numpy as np

    p = Path(path)
    if p.suffix != ".npz":
        raise ValueError(
            f"Ternary weights must be in .npz format, got: {path}"
        )
    data = dict(np.load(str(p), allow_pickle=False))
    result = {}
    for k, v in data.items():
        arr = np.asarray(v, dtype=np.int8)
        result[k] = arr
    return result


def cmd_analyze(args):
    """Analyze model weights for sensitivity to ternarization."""
    from ternary_rom.ternarize.sensitivity import SensitivityAnalyzer

    weights = _load_weights(args.model_path)
    analyzer = SensitivityAnalyzer()
    sensitivities = analyzer.analyze(weights)
    report = analyzer.generate_report(sensitivities)

    print(report)

    # Also save to file
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "sensitivity_report.md").write_text(report, encoding="utf-8")
    print(f"\nReport saved to: {out / 'sensitivity_report.md'}")


def cmd_ternarize(args):
    """Ternarize model weights."""
    import numpy as np
    from ternary_rom.ternarize.engine import Ternarizer

    weights = _load_weights(args.model_path)
    skip_layers = args.skip_layers.split(",") if args.skip_layers else []

    ternarizer = Ternarizer(
        weights,
        skip_layers=skip_layers,
        skip_threshold=args.threshold,
    )
    report = ternarizer.convert()

    # Print summary
    print(f"Ternarization Report")
    print(f"{'='*50}")
    print(f"Total parameters:    {report.total_params:>12,}")
    print(f"Ternary parameters:  {report.ternary_params:>12,}")
    print(f"INT8 parameters:     {report.int8_params:>12,}")
    print(f"FP16 parameters:     {report.fp16_params:>12,}")
    print(f"ROM bits:            {report.rom_bits:>12,}")
    print(f"Overall cosine sim:  {report.overall_cos_sim:>12.4f}")
    print(f"Overall MSE:         {report.overall_mse:>12.6f}")
    print(f"ROM area (est):      {report.estimated_rom_area_mm2:>12.4e} mm^2")
    print(f"ROM leakage (est):   {report.estimated_rom_leakage_uw:>12.4e} uW")
    print()

    # Per-layer details
    print(f"{'Layer':<30} {'Shape':<18} {'Cos Sim':>8} {'Sparsity':>9} {'Skip':>5}")
    print(f"{'-'*30} {'-'*18} {'-'*8} {'-'*9} {'-'*5}")
    for r in report.layers:
        shape = "x".join(str(d) for d in r.shape)
        print(
            f"{r.name:<30} {shape:<18} {r.cos_sim:>8.4f}"
            f" {r.sparsity:>8.4f} {'Y' if r.skip else 'N':>5}"
        )

    # Save ternary weights
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    save_dict = {}
    for r in report.layers:
        save_dict[r.name] = r.weight_ternary
    out_path = out / "ternary_weights.npz"
    np.savez_compressed(str(out_path), **save_dict)
    print(f"\nTernary weights saved to: {out_path}")


def cmd_netlist(args):
    """Generate structural Verilog from ternary weights."""
    from ternary_rom.netgen.generator import NetlistGenerator, NetlistConfig

    weights = _load_ternary_weights(args.weights_path)

    config = NetlistConfig(
        cell_lib=args.process,
        pipeline_depth=args.pipeline,
        time_mux_factor=args.time_mux,
    )

    gen = NetlistGenerator(weights, config=config)

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    # Write Verilog
    v_path = out / "design.v"
    gen.write_verilog(str(v_path))
    print(f"Verilog netlist:  {v_path}")

    # Write summary
    summary_path = out / "summary.txt"
    gen.write_summary(str(summary_path))
    print(f"Array summary:    {summary_path}")

    # Write weight map
    map_path = out / "weight_map.txt"
    gen.write_weight_map(str(map_path))
    print(f"Weight map:       {map_path}")

    print(f"\nProcess: {args.process}")
    print(f"Pipeline depth: {args.pipeline}")
    print(f"Time mux factor: {args.time_mux}")


def cmd_cells(args):
    """Generate cell library files."""
    from ternary_rom.cells.library import ROMCellLibrary

    lib = ROMCellLibrary.from_bundle(args.process)

    out = Path(args.output)
    lib.write_all(str(out))

    print(f"Cell library files generated: {out}")
    print()
    print(lib.summary())


def cmd_flow(args):
    """Run OpenROAD flow (generate Tcl scripts or execute)."""
    from ternary_rom.flow.openroad import OpenROADFlow, FlowConfig

    # Build config from args
    config = FlowConfig(
        process=args.process,
        clock_period_ns=args.clock_period,
        clock_port=args.clock_port,
        placement_density=args.density,
        routing_effort=args.effort,
        output_dir=args.output,
        structural_placement=not args.no_structural,
        route_peripheral_only=not args.route_all,
    )

    if args.pdk_root:
        config.pdk_root = args.pdk_root
    if args.openroad_bin:
        config.openroad_bin = args.openroad_bin

    flow = OpenROADFlow(config)

    if args.execute:
        # Check prerequisites first
        ok, issues = flow.check_prerequisites()
        if not ok:
            print("Prerequisites not met:", file=sys.stderr)
            for issue in issues:
                print(f"  - {issue}", file=sys.stderr)
            sys.exit(1)

        # Need lef and lib paths for execution
        if not args.lef or not args.lib:
            print(
                "Error: --lef and --lib required for execution.",
                file=sys.stderr,
            )
            sys.exit(1)

        result = flow.run(args.netlist_path, args.lef, args.lib)
        if result.success:
            print(f"Flow completed successfully!")
            print(f"  GDS:     {result.gds_path}")
            print(f"  Log:     {result.log_path}")
            print(f"  Reports: {result.reports_dir}")
        else:
            print("Flow FAILED:", file=sys.stderr)
            for err in result.errors:
                print(f"  {err}", file=sys.stderr)
            sys.exit(1)
    else:
        # Just generate Tcl scripts
        flow.write_tcl_scripts(args.output)

        # Also generate Makefile
        makefile_path = Path(args.output) / "Makefile"
        makefile_path.write_text(flow.generate_makefile(), encoding="utf-8")

        # Generate the combined flow script
        lef = args.lef or "cells.lef"
        lib = args.lib or "cells.lib"
        full_tcl = flow.generate_full_flow_tcl(args.netlist_path, lef, lib)
        full_path = Path(args.output) / "run_full.tcl"
        full_path.write_text(full_tcl, encoding="utf-8")

        print(f"OpenROAD Tcl scripts generated in: {args.output}")
        print(f"  00_setup.tcl      — PDK initialization")
        print(f"  01_floorplan.tcl — Die area and pin placement")
        print(f"  02_placement.tcl — Global + detailed placement")
        print(f"  03_routing.tcl   — Signal routing")
        print(f"  04_gds_export.tcl— GDSII export and reports")
        print(f"  run_all.tcl      — Sources all stages in order")
        print(f"  run_full.tcl     — Combined single-file flow")
        print(f"  Makefile         — Build targets")

        # Prerequisites check
        ok, issues = flow.check_prerequisites()
        if not ok:
            print(f"\nNote: {len(issues)} issue(s) for execution:")
            for issue in issues:
                print(f"  - {issue}")
            print(
                "\nTcl scripts can still be used on a machine with OpenROAD."
            )


def _get_all_process_names():
    """Get sorted list of all available process names."""
    from ternary_rom.cells.library import ROMCellLibrary
    return [p["name"] for p in ROMCellLibrary.list_processes()]


def cmd_info(args):
    """Show system info and supported processes."""
    from ternary_rom import __version__
    from ternary_rom.cells.library import ROMCellLibrary
    from ternary_rom.flow.openroad import OpenROADFlow

    print(f"ternary-rom v{__version__}")
    print(f"Python:       {sys.version.split()[0]}")
    print()

    # Group by category
    categories = ROMCellLibrary.list_categories()
    cat_labels = {
        "legacy": "Legacy / Educational",
        "open_source": "Open-Source PDKs",
        "mature": "Mature Nodes",
        "production": "Production (28nm family)",
        "advanced": "Advanced (14-22nm FinFET/FD-SOI)",
        "cutting_edge": "Cutting-Edge (5-12nm)",
        "frontier": "Frontier (3nm / Angstrom)",
    }

    procs = ROMCellLibrary.list_processes()
    print(f"Supported processes ({len(procs)} total):")
    print()

    for cat in ["legacy", "open_source", "mature", "production",
                "advanced", "cutting_edge", "frontier"]:
        names = categories.get(cat, [])
        if not names:
            continue
        label = cat_labels.get(cat, cat)
        print(f"  {label}:")
        for name in names:
            p = next(x for x in procs if x["name"] == name)
            print(f"    {name:<20} {p['voltage']:>4}V  {p['cell_size_um']:>6}um  {p['n_cells']:>3} cells  {p['description']}")
        print()

    or_bin = OpenROADFlow.find_openroad()
    if or_bin:
        print(f"OpenROAD:     {or_bin}")
    else:
        print(f"OpenROAD:     not found (Tcl generation still works)")
    print()

    pdk_root = os.environ.get("PDK_ROOT", "(not set)")
    print(f"PDK_ROOT:     {pdk_root}")
    print()

    print("Tape-out options:")
    print("  TinyTapeout (sky130, $300, 8 weeks) — recommended first proof-of-concept")
    print("  Metal-only masks (1-3 layers, $200K) — production ternary ROM")
    print("  Full ASIC ($2-4M) — only if non-ROM peripheral is complex")


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="ternary-rom",
        description="Model-to-GDS flow for mask-locked ternary inference chips.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ternary-rom info
  ternary-rom cells sky130 -o ./cells
  ternary-rom cells tsmc7 -o ./cells_tsmc7
  ternary-rom analyze weights.npy
  ternary-rom ternarize weights.npy -o ./build
  ternary-rom netlist ternary_weights.npz --process sky130
  ternary-rom netlist ternary_weights.npz --process tsmc7
  ternary-rom flow design.v --execute --lef cells.lef --lib cells.lib
  ternary-rom cells intel18a -o ./cells_18a --drive x4 --vt hvt
""",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {_get_version()}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- analyze ---
    p_analyze = subparsers.add_parser(
        "analyze",
        help="Analyze model weights for sensitivity to ternarization",
    )
    p_analyze.add_argument(
        "model_path",
        help="Path to .npy or .npz file containing model weights",
    )
    p_analyze.add_argument(
        "-o", "--output", default="./build",
        help="Output directory (default: ./build)",
    )
    p_analyze.set_defaults(func=cmd_analyze)

    # --- ternarize ---
    p_tern = subparsers.add_parser(
        "ternarize",
        help="Ternarize model weights to {-1, 0, +1}",
    )
    p_tern.add_argument(
        "model_path",
        help="Path to .npy or .npz file containing model weights",
    )
    p_tern.add_argument(
        "-o", "--output", default="./build",
        help="Output directory (default: ./build)",
    )
    p_tern.add_argument(
        "--skip-layers", default="",
        help="Comma-separated layer name patterns to skip (e.g. 'dt_proj,norm')",
    )
    p_tern.add_argument(
        "--threshold", type=float, default=0.95,
        help="Cosine similarity threshold for auto-skip (default: 0.95)",
    )
    p_tern.set_defaults(func=cmd_ternarize)

    # --- netlist ---
    p_net = subparsers.add_parser(
        "netlist",
        help="Generate structural Verilog from ternary weights",
    )
    p_net.add_argument(
        "weights_path",
        help="Path to .npz file with ternary weights",
    )
    p_net.add_argument(
        "-o", "--output", default="./build",
        help="Output directory (default: ./build)",
    )
    p_net.add_argument(
        "--process", default="sky130",
        help="Target process (default: sky130). Use 'ternary-rom info' for full list.",
    )
    p_net.add_argument(
        "--pipeline", type=int, default=0,
        help="Pipeline depth (0=combinational, default: 0)",
    )
    p_net.add_argument(
        "--time-mux", type=int, default=1,
        help="Time multiplexing factor (default: 1)",
    )
    p_net.set_defaults(func=cmd_netlist)

    # --- cells ---
    p_cells = subparsers.add_parser(
        "cells",
        help="Generate cell library files (LEF, LIB, Verilog)",
    )
    p_cells.add_argument(
        "process",
        help="Target process name (e.g. sky130, tsmc7, intel18a). Use 'ternary-rom info' for full list.",
    )
    p_cells.add_argument(
        "-o", "--output", default="./build",
        help="Output directory (default: ./build)",
    )
    p_cells.set_defaults(func=cmd_cells)

    # --- flow ---
    p_flow = subparsers.add_parser(
        "flow",
        help="Run OpenROAD flow (generate Tcl or execute)",
    )
    p_flow.add_argument(
        "netlist_path",
        help="Path to input Verilog netlist",
    )
    p_flow.add_argument(
        "-o", "--output", default="./build/flow",
        help="Output directory (default: ./build/flow)",
    )
    p_flow.add_argument(
        "--process", default="sky130",
        help="Target process (default: sky130). Use 'ternary-rom info' for full list.",
    )
    p_flow.add_argument(
        "--execute", action="store_true",
        help="Execute the flow with OpenROAD (requires openroad binary)",
    )
    p_flow.add_argument(
        "--lef", default=None,
        help="Path to ROM cell LEF file (required for --execute)",
    )
    p_flow.add_argument(
        "--lib", default=None,
        help="Path to ROM cell liberty file (required for --execute)",
    )
    p_flow.add_argument(
        "--pdk-root", default=None,
        help="Path to PDK installation (default: $PDK_ROOT)",
    )
    p_flow.add_argument(
        "--openroad-bin", default=None,
        help="Path to openroad binary (default: auto-detect)",
    )
    p_flow.add_argument(
        "--clock-period", type=float, default=10.0,
        help="Clock period in nanoseconds (default: 10.0)",
    )
    p_flow.add_argument(
        "--clock-port", default="clk",
        help="Clock port name (default: clk)",
    )
    p_flow.add_argument(
        "--density", type=float, default=0.5,
        help="Placement density 0.0-1.0 (default: 0.5)",
    )
    p_flow.add_argument(
        "--effort", type=int, default=10,
        help="Routing effort 1-20 (default: 10)",
    )
    p_flow.add_argument(
        "--no-structural", action="store_true",
        help="Disable structured ROM placement (use conventional P&R)",
    )
    p_flow.add_argument(
        "--route-all", action="store_true",
        help="Route all nets including ROM internals (not recommended)",
    )
    p_flow.set_defaults(func=cmd_flow)

    # --- info ---
    p_info = subparsers.add_parser(
        "info",
        help="Show system info and supported processes",
    )
    p_info.set_defaults(func=cmd_info)

    return parser


def _get_version() -> str:
    """Get version string, handling import issues gracefully."""
    try:
        from ternary_rom import __version__
        return __version__
    except Exception:
        return "0.1.0"


def cli_entry():
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    cli_entry()
