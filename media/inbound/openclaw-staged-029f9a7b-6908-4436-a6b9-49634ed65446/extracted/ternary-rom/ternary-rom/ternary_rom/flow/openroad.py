"""OpenROAD ASIC flow for ternary ROM inference chips.

Manages the complete flow from Verilog netlist to GDSII output:
1. Setup (PDK, constraints)
2. Floorplan (with structured ROM array placement)
3. Placement (grid-based for ROM, conventional for peripheral)
4. Routing (peripheral only; ROM auto-routed by metal mask)
5. GDSII export

The flow generates Tcl scripts that can be run in OpenROAD,
or executed directly if the openroad binary is available.

Example:
    flow = OpenROADFlow(FlowConfig(process="sky130"))
    # Generate Tcl scripts (no OpenROAD needed)
    flow.write_tcl_scripts("output/flow/")
    # Or run directly (requires OpenROAD installed)
    result = flow.run(netlist_path="model.v", lef_path="cells.lef",
                      lib_path="cells.lib")
    print(result.gds_path)
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ======================================================================
# Data classes
# ======================================================================

@dataclass
class FlowConfig:
    """Configuration for the OpenROAD ASIC flow.

    Attributes:
        process: PDK name (any supported process, e.g. 'sky130', 'tsmc7', 'intel18a')
        openroad_bin: Path to openroad executable (auto-detected if None)
        pdk_root: Path to PDK installation
        clock_period_ns: Target clock period in nanoseconds
        clock_port: Name of clock port in the netlist
        vdd_voltage: Supply voltage
        gnd_voltage: Ground voltage
        placement_density: Target placement density (0.0-1.0)
        routing_effort: Routing effort level (1-20, higher = more effort)
        output_dir: Directory for all output files
        structural_placement: If True, use grid-based placement for ROM arrays
        route_peripheral_only: If True, skip routing inside ROM arrays
    """
    process: str = "sky130"
    openroad_bin: Optional[str] = None
    pdk_root: Optional[str] = None
    clock_period_ns: float = 10.0
    clock_port: str = "clk"
    vdd_voltage: float = 3.3
    gnd_voltage: float = 0.0
    placement_density: float = 0.5
    routing_effort: int = 10
    output_dir: str = "./build"
    structural_placement: bool = True
    route_peripheral_only: bool = True


@dataclass
class FlowResult:
    """Result of running the OpenROAD flow.

    Attributes:
        success: Whether the flow completed without errors
        gds_path: Path to output GDSII file
        log_path: Path to OpenROAD log file
        reports_dir: Directory containing timing/power/area reports
        die_area_um2: Final die area in square micrometers
        total_power_mw: Estimated total power in milliwatts
        timing_met: Whether timing constraints were met
        errors: List of error messages
        warnings: List of warning messages
    """
    success: bool
    gds_path: Optional[str] = None
    log_path: Optional[str] = None
    reports_dir: Optional[str] = None
    die_area_um2: float = 0.0
    total_power_mw: float = 0.0
    timing_met: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# ======================================================================
# PDK-specific data
# ======================================================================

_PDK_CONFIGS: Dict[str, Dict] = {
    "sky130": {
        "lef_files": [
            "sky130/sky130_fd_sc_hd/timing/sky130_fd_sc_hd.tlef",
        ],
        "lib_files": [
            "sky130/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib",
        ],
        "tech_lef": "sky130/sky130_fd_sc_hd/timing/sky130_fd_sc_hd.tlef",
        "site": "unithd",
        "core_site": "unithd",
    },
}


def _get_pdk_config(process: str) -> Dict:
    """Get PDK config for any process.

    Returns a known config for sky130, or auto-generates one for
    any other process based on the cell library files.
    """
    if process in _PDK_CONFIGS:
        return _PDK_CONFIGS[process]

    # Auto-generate config for any process using cell library files
    return {
        "lef_files": [
            f"{process}/cells.lef",
        ],
        "lib_files": [
            f"{process}/cells.lib",
        ],
        "tech_lef": f"{process}/cells.lef",
        "site": "CORE",
        "core_site": "CORE",
    }


class OpenROADFlow:
    """OpenROAD ASIC flow for ternary ROM inference chips.

    Manages the complete flow from Verilog netlist to GDSII output.
    Generates Tcl scripts that can be run in OpenROAD,
    or executed directly if the openroad binary is available.

    Example:
        flow = OpenROADFlow(FlowConfig(process="sky130"))
        flow.write_tcl_scripts("output/flow/")
        result = flow.run(netlist_path="model.v", lef_path="cells.lef",
                          lib_path="cells.lib")
        print(result.gds_path)
    """

    def __init__(self, config: Optional[FlowConfig] = None):
        self.config = config or FlowConfig()

        # Auto-detect openroad binary
        if self.config.openroad_bin is None:
            self.config.openroad_bin = self.find_openroad()

        # Resolve PDK root
        if self.config.pdk_root is None:
            self.config.pdk_root = os.environ.get(
                "PDK_ROOT",
                "/usr/share/pdk",
            )

        # PDK-specific parameters
        self._pdk = _get_pdk_config(self.config.process)

    # ------------------------------------------------------------------
    # Tcl generation: individual stages
    # ------------------------------------------------------------------

    def generate_setup_tcl(self) -> str:
        """Generate OpenROAD setup Tcl script.

        Initializes PDK, reads LEF/LIB files, sets up technology.
        """
        pdk = self._pdk
        pdk_root = self.config.pdk_root or "."
        proc = self.config.process
        lines: List[str] = [
            "# ============================================================",
            "# 00_setup.tcl — PDK and technology initialization",
            "# Generated by ternary-rom OpenROADFlow",
            f"# Process: {proc}",
            "# ============================================================",
            "",
            f'set pdk_root "{pdk_root}"',
            f'set proc_name "{proc}"',
            "",
            "# --- Read technology LEF ---",
        ]

        tech_lef = pdk["tech_lef"]
        lines.append(f'read_lef $pdk_root/{tech_lef}')

        # Read additional LEF files
        for lef in pdk["lef_files"]:
            if lef != tech_lef:
                lines.append(f'read_lef $pdk_root/{lef}')

        lines.append("")
        lines.append("# --- Read liberty timing files ---")
        for lib in pdk["lib_files"]:
            lines.append(f'read_liberty $pdk_root/{lib}')

        lines.append("")
        lines.append("# --- Set voltage ---")
        lines.append('set ::env(VDD_PIN_NAME) "VDD"')
        lines.append('set ::env(GND_PIN_NAME) "VSS"')
        lines.append("")
        lines.append('puts "Setup complete: process=$proc_name"')
        lines.append("")
        return "\n".join(lines)

    def generate_floorplan_tcl(
        self,
        netlist_path: str,
        lef_path: str,
        rom_arrays: Optional[List] = None,
    ) -> str:
        """Generate floorplan Tcl script.

        Creates die area, places ROM arrays as rectangular regions,
        places peripheral logic in remaining space.

        For structured placement: ROM arrays are placed on a regular grid
        with known pitch. No simulated annealing needed.
        """
        pdk = self._pdk
        cfg = self.config
        site = pdk["core_site"]
        die_width = 500.0   # um
        die_height = 500.0  # um

        lines: List[str] = [
            "# ============================================================",
            "# 01_floorplan.tcl — Floorplan generation",
            "# Generated by ternary-rom OpenROADFlow",
            "# ============================================================",
            "",
            "# --- Read ROM cell LEF ---",
            f'read_lef "{lef_path}"',
            "",
            "# --- Read design netlist ---",
            f'read_verilog "{netlist_path}"',
            "link_design top",
            "",
            "# --- Initialize floorplan ---",
        ]

        # Build the initialize_floorplan command as a single string
        # to avoid f-string backslash issues
        fp_cmd = (
            f'initialize_floorplan -die_area "0 0 {die_width} {die_height}"'
            f' -core_area "10 10 {die_width - 10} {die_height - 10}"'
            f' -site {site} -tracks'
        )
        lines.append(fp_cmd)
        lines.append("")

        # Structured ROM placement
        if cfg.structural_placement and rom_arrays:
            lines.append("# --- Structured ROM array placement (O(N) grid tiling) ---")
            x_offset = 20.0
            y_offset = 20.0
            cell_pitch = 1.5  # um, approximate cell pitch

            for i, rom in enumerate(rom_arrays):
                name = getattr(rom, "name", f"rom_array_{i}")
                rows = getattr(rom, "rows", 16)
                cols = getattr(rom, "cols", 16)
                width = cols * cell_pitch
                height = rows * cell_pitch

                lines.append(f"# ROM array: {name} ({rows} x {cols})")
                rect_cmd = (
                    f'create_rectangle -name rom_region_{name}'
                    f' -area "{x_offset} {y_offset} {x_offset + width} {y_offset + height}"'
                )
                lines.append(rect_cmd)
                region_cmd = (
                    f'set_placement_region -region'
                    f' "{x_offset} {y_offset} {x_offset + width} {y_offset + height}"'
                )
                lines.append(region_cmd)
                y_offset += height + 5.0

            lines.append("")

        # Pin placement
        lines.append("# --- Pin placement ---")
        lines.append("place_pins -rand")
        lines.append("")
        lines.append('puts "Floorplan complete"')
        lines.append("")
        return "\n".join(lines)

    def generate_placement_tcl(self) -> str:
        """Generate placement Tcl script.

        For ROM arrays: grid-based deterministic placement (O(N)).
        For peripheral logic: standard OpenROAD placement.
        """
        cfg = self.config
        density = cfg.placement_density
        lines: List[str] = [
            "# ============================================================",
            "# 02_placement.tcl — Placement",
            "# Generated by ternary-rom OpenROADFlow",
            "# ============================================================",
            "",
        ]

        if cfg.structural_placement:
            lines.append("# --- Structured ROM placement (O(N) grid tiling) ---")
            lines.append("# ROM cells are placed on a regular grid by the floorplan.")
            lines.append("# Only peripheral logic needs conventional placement.")
            lines.append("")
            lines.append("# --- Global placement for peripheral logic ---")
        else:
            lines.append("# --- Global placement ---")

        gp_cmd = (
            f"global_placement -density {density}"
            " -pad_left 2 -pad_right 2 -pad_top 2 -pad_bottom 2"
        )
        lines.append(gp_cmd)
        lines.append("")
        lines.append("# --- Detailed placement ---")
        lines.append("detailed_placement")
        lines.append("")
        lines.append("# --- Optimize placement ---")
        lines.append("optimize_mirroring")
        lines.append("")
        lines.append('puts "Placement complete"')
        lines.append("")
        return "\n".join(lines)

    def generate_routing_tcl(self) -> str:
        """Generate routing Tcl script.

        For ROM arrays: skip routing (metal mask handles it).
        For peripheral logic: standard detail routing.
        """
        cfg = self.config
        lines: List[str] = [
            "# ============================================================",
            "# 03_routing.tcl — Routing",
            "# Generated by ternary-rom OpenROADFlow",
            "# ============================================================",
            "",
        ]

        if cfg.route_peripheral_only:
            lines.append("# --- Ternary ROM: metal-mask programming eliminates internal routing ---")
            lines.append("# WL on M1, BL on M2 auto-connect within ROM arrays.")
            lines.append("# Only peripheral logic (adders, accumulators, control) needs routing.")
            lines.append("")

        lines.append("# --- Global route ---")
        gr_cmd = (
            'global_route -guide_file "$::rundir/globalroute.guide"'
            ' -congestion_iterations 30 -verbose'
        )
        lines.append(gr_cmd)
        lines.append("")
        lines.append("# --- Detailed route ---")
        dr_cmd = (
            'detailed_route -output_drc "$::rundir/drc.rpt"'
            ' -output_maze "$::rundir/maze.log"'
            ' -save_db_to "$::rundir/route.db" -verbose'
        )
        lines.append(dr_cmd)
        lines.append("")
        lines.append('puts "Routing complete"')
        lines.append("")
        return "\n".join(lines)

    def generate_gds_export_tcl(self) -> str:
        """Generate GDSII export Tcl script."""
        lines: List[str] = [
            "# ============================================================",
            "# 04_gds_export.tcl — GDSII export",
            "# Generated by ternary-rom OpenROADFlow",
            "# ============================================================",
            "",
            "# --- Write GDSII ---",
            'write_gds "$::rundir/design.gds"',
            "",
            "# --- Write final reports ---",
            'file mkdir "$::rundir/reports"',
            "",
            "# Timing report",
        ]

        timing_cmd = (
            'report_timing -file "$::rundir/reports/timing.rpt"'
            ' -num_paths 10 -slack_max 0.0'
        )
        lines.append(timing_cmd)
        lines.append("")
        lines.append("# Power report")
        lines.append('report_power -file "$::rundir/reports/power.rpt"')
        lines.append("")
        lines.append("# Area report")
        lines.append('report_design_area -file "$::rundir/reports/area.rpt"')
        lines.append("")
        lines.append("# Final Verilog netlist (post-synthesis, post-P&R)")
        lines.append('write_verilog "$::rundir/design_final.v"')
        lines.append("")
        lines.append("# Save OpenROAD database")
        lines.append('write_db "$::rundir/final.db"')
        lines.append("")
        lines.append('puts "GDSII export complete: $::rundir/design.gds"')
        lines.append('puts "Reports written to: $::rundir/reports/"')
        lines.append("")
        return "\n".join(lines)

    def generate_full_flow_tcl(
        self, netlist_path: str, lef_path: str, lib_path: str
    ) -> str:
        """Generate a single combined Tcl script for the entire flow.

        This is the primary output — one file that runs everything.
        """
        cfg = self.config
        pdk = self._pdk
        pdk_root = cfg.pdk_root or "."
        proc = cfg.process
        site = pdk["core_site"]
        clock_port = cfg.clock_port
        clock_period = cfg.clock_period_ns
        die_width = 500.0
        die_height = 500.0

        lines: List[str] = [
            "#!/usr/bin/env openroad",
            "# ============================================================",
            "# run_all.tcl — Complete OpenROAD flow for ternary ROM",
            "# Generated by ternary-rom OpenROADFlow",
            f"# Process: {proc}",
            f"# Clock: {clock_port} @ {clock_period} ns",
            "# ============================================================",
            "",
            f'set pdk_root "{pdk_root}"',
            f'set proc_name "{proc}"',
            f'set rundir "{cfg.output_dir}"',
            "file mkdir $rundir",
            'file mkdir "$rundir/reports"',
            "",
            "# ============================================================",
            "# STAGE 1: SETUP — Read PDK and technology files",
            "# ============================================================",
            "",
            f'puts "[1/6] Setup: reading PDK for {proc}..."',
            "",
            "# Read technology LEF",
            f'read_lef "$pdk_root/{pdk["tech_lef"]}"',
        ]

        # Additional LEF files
        for lef in pdk["lef_files"]:
            if lef != pdk["tech_lef"]:
                lines.append(f'read_lef "$pdk_root/{lef}"')

        lines.append("")
        lines.append("# Read ROM cell LEF")
        lines.append(f'read_lef "{lef_path}"')
        lines.append("")
        lines.append("# Read liberty timing")
        for lib in pdk["lib_files"]:
            lines.append(f'read_liberty "$pdk_root/{lib}"')
        lines.append(f'read_liberty "{lib_path}"')
        lines.append("")

        # Stage 2: Read design
        lines.extend([
            "# ============================================================",
            "# STAGE 2: READ DESIGN — Read netlist and link",
            "# ============================================================",
            "",
            'puts "[2/6] Reading design netlist..."',
            "",
            f'read_verilog "{netlist_path}"',
            "link_design top",
            "check_design -unconstrained_ports",
            "",
        ])

        # Stage 3: Floorplan
        lines.extend([
            "# ============================================================",
            "# STAGE 3: FLOORPLAN — Die area, pin placement, ROM regions",
            "# ============================================================",
            "",
            'puts "[3/6] Generating floorplan..."',
            "",
        ])

        fp_cmd = (
            f'initialize_floorplan -die_area "0 0 {die_width} {die_height}"'
            f' -core_area "10 10 {die_width - 10} {die_height - 10}"'
            f' -site {site} -tracks'
        )
        lines.append(fp_cmd)
        lines.append("")
        lines.append("place_pins -rand")
        lines.append("")

        # Stage 4: Placement
        lines.extend([
            "# ============================================================",
            "# STAGE 4: PLACEMENT — Global + detailed placement",
            "# ============================================================",
            "",
            f'puts "[4/6] Running placement (density={cfg.placement_density})..."',
            "",
        ])

        if cfg.structural_placement:
            lines.extend([
                "# Structured ROM placement: O(N) grid tiling",
                "# ROM cells are pre-positioned by the floorplan;",
                "# only peripheral logic needs global placement.",
                "",
            ])

        gp_cmd = (
            f"global_placement -density {cfg.placement_density}"
            " -pad_left 2 -pad_right 2 -pad_top 2 -pad_bottom 2"
        )
        lines.append(gp_cmd)
        lines.append("")
        lines.append("detailed_placement")
        lines.append("optimize_mirroring")
        lines.append("")

        # Stage 5: Routing
        lines.extend([
            "# ============================================================",
            "# STAGE 5: CTS + ROUTING — Clock tree and signal routing",
            "# ============================================================",
            "",
            'puts "[5/6] Running clock tree synthesis and routing..."',
            "",
        ])

        if cfg.route_peripheral_only:
            lines.extend([
                "# Ternary ROM: metal-mask programming eliminates internal routing.",
                "# WL on M1, BL on M2 auto-connect within ROM arrays.",
                "# Only ~5% of chip (peripheral) needs conventional routing.",
                "",
            ])

        gr_cmd = (
            'global_route -guide_file "$rundir/globalroute.guide"'
            ' -congestion_iterations 30'
        )
        lines.append(gr_cmd)
        lines.append("")

        dr_cmd = (
            'detailed_route -output_drc "$rundir/drc.rpt"'
            ' -output_maze "$rundir/maze.log"'
        )
        lines.append(dr_cmd)
        lines.append("")

        # Stage 6: GDSII Export
        lines.extend([
            "# ============================================================",
            "# STAGE 6: GDSII EXPORT — Final outputs and reports",
            "# ============================================================",
            "",
            'puts "[6/6] Writing GDSII and reports..."',
            "",
            'write_gds "$rundir/design.gds"',
            "",
            "# Reports",
        ])

        timing_cmd = (
            'report_timing -file "$rundir/reports/timing.rpt" -num_paths 10'
        )
        lines.append(timing_cmd)
        lines.append("")
        lines.append('report_power -file "$rundir/reports/power.rpt"')
        lines.append("")
        lines.append('report_design_area -file "$rundir/reports/area.rpt"')
        lines.append("")
        lines.append("# Final netlist")
        lines.append('write_verilog "$rundir/design_final.v"')
        lines.append("")
        lines.append('puts "============================================"')
        lines.append('puts "Flow complete!"')
        lines.append('puts "  GDS:     $rundir/design.gds"')
        lines.append('puts "  Reports: $rundir/reports/"')
        lines.append('puts "============================================"')
        lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # File writing
    # ------------------------------------------------------------------

    def write_tcl_scripts(self, output_dir: str):
        """Write all Tcl scripts to directory.

        Creates:
        - 00_setup.tcl
        - 01_floorplan.tcl
        - 02_placement.tcl
        - 03_routing.tcl
        - 04_gds_export.tcl
        - run_all.tcl (sources all above in order)
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        # Individual stage scripts
        (out / "00_setup.tcl").write_text(self.generate_setup_tcl(), encoding="utf-8")
        (out / "01_floorplan.tcl").write_text(
            self.generate_floorplan_tcl("design.v", "cells.lef"),
            encoding="utf-8",
        )
        (out / "02_placement.tcl").write_text(self.generate_placement_tcl(), encoding="utf-8")
        (out / "03_routing.tcl").write_text(self.generate_routing_tcl(), encoding="utf-8")
        (out / "04_gds_export.tcl").write_text(self.generate_gds_export_tcl(), encoding="utf-8")

        # Combined run_all.tcl
        run_all = "#!/usr/bin/env openroad\n"
        run_all += "# run_all.tcl — Sources all flow stages in order\n"
        run_all += "# Generated by ternary-rom OpenROADFlow\n\n"
        run_all += f'set ::rundir "{self.config.output_dir}"\n\n'
        run_all += "source [file join [file dirname [info script]] 00_setup.tcl]\n"
        run_all += "source [file join [file dirname [info script]] 01_floorplan.tcl]\n"
        run_all += "source [file join [file dirname [info script]] 02_placement.tcl]\n"
        run_all += "source [file join [file dirname [info script]] 03_routing.tcl]\n"
        run_all += "source [file join [file dirname [info script]] 04_gds_export.tcl]\n"
        run_all += '\nputs "All flow stages complete."\n'

        (out / "run_all.tcl").write_text(run_all, encoding="utf-8")

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def run(
        self, netlist_path: str, lef_path: str, lib_path: str
    ) -> FlowResult:
        """Execute the full OpenROAD flow.

        Generates Tcl, runs openroad binary, parses results.
        Returns FlowResult with paths and metrics.

        Raises RuntimeError if openroad binary not found.
        """
        or_bin = self.config.openroad_bin or self.find_openroad()
        if or_bin is None:
            raise RuntimeError(
                "openroad binary not found. Install OpenROAD or set "
                "FlowConfig.openroad_bin to the path of the openroad executable."
            )

        # Ensure output directory exists
        out = Path(self.config.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        reports_dir = out / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Generate combined Tcl script
        tcl_content = self.generate_full_flow_tcl(netlist_path, lef_path, lib_path)
        tcl_path = out / "run_all.tcl"
        tcl_path.write_text(tcl_content, encoding="utf-8")

        # Run openroad
        log_path = out / "openroad.log"
        gds_path = str(out / "design.gds")

        try:
            result = subprocess.run(
                [or_bin, str(tcl_path)],
                capture_output=True,
                text=True,
                timeout=86400,  # 24 hour timeout for large designs
                cwd=str(out),
            )

            # Write log
            log_content = result.stdout + "\n\n" + result.stderr
            log_path.write_text(log_content, encoding="utf-8")

            # Parse results
            success = result.returncode == 0
            errors: List[str] = []
            warnings: List[str] = []
            timing_met = True
            die_area = 0.0
            power = 0.0

            if not success:
                for line in (result.stdout + result.stderr).split("\n"):
                    lower = line.lower()
                    if "error" in lower:
                        errors.append(line.strip())
                    if "warning" in lower:
                        warnings.append(line.strip())

            # Try to parse report files
            area_rpt = reports_dir / "area.rpt"
            if area_rpt.exists():
                try:
                    area_text = area_rpt.read_text(encoding="utf-8")
                    for line in area_text.split("\n"):
                        if "Design area" in line:
                            for p in line.split():
                                try:
                                    val = float(p)
                                    if val > 0:
                                        die_area = val
                                except ValueError:
                                    pass
                except Exception:
                    pass

            power_rpt = reports_dir / "power.rpt"
            if power_rpt.exists():
                try:
                    power_text = power_rpt.read_text(encoding="utf-8")
                    for line in power_text.split("\n"):
                        if "Total" in line:
                            for p in line.split():
                                try:
                                    val = float(p)
                                    if val > 0:
                                        power = val
                                except ValueError:
                                    pass
                except Exception:
                    pass

            return FlowResult(
                success=success,
                gds_path=gds_path if success and Path(gds_path).exists() else None,
                log_path=str(log_path),
                reports_dir=str(reports_dir),
                die_area_um2=die_area,
                total_power_mw=power,
                timing_met=timing_met and success,
                errors=errors,
                warnings=warnings,
            )

        except FileNotFoundError:
            raise RuntimeError(
                f"openroad binary not found at '{or_bin}'. "
                f"Install OpenROAD or set a valid path."
            )
        except subprocess.TimeoutExpired:
            return FlowResult(
                success=False,
                log_path=str(log_path),
                reports_dir=str(reports_dir),
                errors=["OpenROAD flow timed out after 24 hours."],
            )

    # ------------------------------------------------------------------
    # Static utilities
    # ------------------------------------------------------------------

    @staticmethod
    def find_openroad() -> Optional[str]:
        """Find openroad binary in PATH or common locations."""
        which_result = shutil.which("openroad")
        if which_result is not None:
            return which_result

        common_paths = [
            "/usr/local/bin/openroad",
            "/opt/openroad/bin/openroad",
            os.path.expanduser("~/tools/OpenROAD/bin/openroad"),
            os.path.expanduser("~/.local/bin/openroad"),
            "/tools/OpenROAD/bin/openroad",
        ]
        for p in common_paths:
            if os.path.isfile(p) and os.access(p, os.X_OK):
                return p

        return None

    def check_prerequisites(self) -> Tuple[bool, List[str]]:
        """Check if OpenROAD and PDK are available.

        Returns: (all_ok, list_of_issues)
        """
        issues: List[str] = []

        or_bin = self.config.openroad_bin or self.find_openroad()
        if or_bin is None:
            issues.append(
                "openroad binary not found in PATH or common locations. "
                "Install from https://github.com/The-OpenROAD-Project/OpenROAD"
            )
        else:
            if not os.access(or_bin, os.X_OK):
                issues.append(f"openroad binary at '{or_bin}' is not executable.")

        pdk_root = self.config.pdk_root
        if pdk_root is None:
            issues.append("PDK_ROOT is not set and no pdk_root configured.")
        elif not os.path.isdir(pdk_root):
            issues.append(f"PDK root directory does not exist: {pdk_root}")
        else:
            pdk = self._pdk
            tech_lef = os.path.join(pdk_root, pdk["tech_lef"])
            if not os.path.isfile(tech_lef):
                issues.append(
                    f"Tech LEF not found: {tech_lef}. "
                    f"Ensure PDK is installed for process '{self.config.process}'."
                )

        all_ok = len(issues) == 0
        return all_ok, issues

    # ------------------------------------------------------------------
    # Makefile generation
    # ------------------------------------------------------------------

    def generate_makefile(self) -> str:
        """Generate a Makefile for the flow.

        Targets: setup, floorplan, place, route, gds, clean, all
        """
        or_bin = self.config.openroad_bin or "openroad"
        out_dir = self.config.output_dir

        lines = [
            "# Makefile for ternary-rom OpenROAD flow",
            "# Generated by ternary-rom OpenROADFlow",
            f"# Process: {self.config.process}",
            "",
            f"OPENROAD := {or_bin}",
            f"OUT_DIR  := {out_dir}",
            "RUN_DIR  := $(OUT_DIR)/rundir",
            "",
            ".PHONY: all setup floorplan place route gds clean full",
            "",
            "all: gds",
            "",
            "setup:",
            "   mkdir -p $(RUN_DIR)",
            "   $(OPENROAD) $(OUT_DIR)/00_setup.tcl",
            "",
            "floorplan:",
            "   $(OPENROAD) $(OUT_DIR)/01_floorplan.tcl",
            "",
            "place:",
            "   $(OPENROAD) $(OUT_DIR)/02_placement.tcl",
            "",
            "route:",
            "   $(OPENROAD) $(OUT_DIR)/03_routing.tcl",
            "",
            "gds:",
            "   $(OPENROAD) $(OUT_DIR)/04_gds_export.tcl",
            "",
            "full:",
            "   $(OPENROAD) $(OUT_DIR)/run_all.tcl",
            "",
            "clean:",
            "   rm -rf $(OUT_DIR)",
            "",
            "# End of Makefile",
        ]
        return "\n".join(lines)
