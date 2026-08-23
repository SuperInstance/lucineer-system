#!/usr/bin/env python3
"""Generate TinyTapeout 8x8 ternary MAC tile design files.

Demonstrates the complete ternary-rom flow:
1. Define example weights
2. Ternarize using BitNet b1.58 method
3. Generate structural Verilog netlist
4. Generate ROM cell library files
5. Estimate area and leakage
"""

import sys
import os
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from ternary_rom.ternarize.engine import Ternarizer
from ternary_rom.netgen.generator import NetlistGenerator, NetlistConfig
from ternary_rom.cells.library import ROMCellLibrary


def main():
    np.random.seed(42)
    build_dir = os.path.join(os.path.dirname(__file__), "build")
    os.makedirs(build_dir, exist_ok=True)

    print("=" * 60)
    print("ternary-rom: TinyTapeout 8x8 MAC Tile Generator")
    print("=" * 60)

    # ── Step 1: Define example weights ──
    print("\n[1/5] Creating example weight matrix (8x8)...")

    # Simulate a small trained weight matrix with natural sparsity
    W_raw = np.random.randn(8, 8).astype(np.float32)
    weights_dict = {"mac_layer": W_raw}

    print(f"  Raw weight range: [{W_raw.min():.3f}, {W_raw.max():.3f}]")
    print(f"  Raw weight mean abs: {np.abs(W_raw).mean():.3f}")

    # ── Step 2: Ternarize ──
    print("\n[2/5] Ternarizing weights (BitNet b1.58 method)...")
    ternarizer = Ternarizer(weights_dict, skip_layers=[], skip_threshold=0.0)
    report = ternarizer.convert()

    result = report.layers[0]
    W_t = result.weight_ternary

    print(f"  Alpha (scaling): {result.alpha:.4f}")
    print(f"  Cosine similarity: {result.cos_sim:.4f}")
    print(f"  MSE: {result.mse:.6f}")
    print(f"  Sparsity: {result.sparsity*100:.1f}% zeros")
    print(f"  Cell counts: +1={np.sum(W_t==1)}, -1={np.sum(W_t==-1)}, 0={np.sum(W_t==0)}")
    print(f"  ROM area (sky130): {report.estimated_rom_area_mm2*1e6:.1f} um2")
    print(f"  ROM leakage (sky130): {report.estimated_rom_leakage_uw*1000:.2f} nW")

    # Save ternary weights
    np.savez(os.path.join(build_dir, "ternary_weights.npz"), mac_layer=W_t)
    print(f"  Saved: {build_dir}/ternary_weights.npz")

    # ── Step 3: Generate Verilog netlist ──
    print("\n[3/5] Generating structural Verilog netlist...")
    config = NetlistConfig(
        cell_lib="sky130",
        word_width=8,
        pipeline_depth=1,
        adder_style="ripple",
        include_testbench=True,
    )
    netgen = NetlistGenerator({"mac_layer": W_t}, config=config)
    netgen.write_verilog(os.path.join(build_dir, "ternary_mac.v"))
    netgen.write_summary(os.path.join(build_dir, "summary.txt"))
    netgen.write_weight_map(os.path.join(build_dir, "weight_map.txt"))

    specs = netgen.analyze_arrays()
    for s in specs:
        print(f"  Array: {s.name} ({s.rows}x{s.cols})")
        print(f"    Plus: {s.plus_count}, Minus: {s.minus_count}, Zero: {s.zero_count}")
        print(f"    Zero fraction: {s.zero_fraction*100:.1f}%")
        print(f"    Area (sky130): {s.estimated_area_mm2*1e6:.1f} um2")
    print(f"  Saved: {build_dir}/ternary_mac.v")

    # ── Step 4: Generate cell library ──
    print("\n[4/5] Generating ROM cell library (sky130)...")
    lib = ROMCellLibrary.from_bundle("sky130")
    lib.write_all(build_dir)
    print(f"  Saved to {build_dir}:")
    print(f"    cells.v   (Verilog behavioral models)")
    print(f"    cells.lef (LEF macro definitions)")
    print(f"    cells.lib (Liberty timing)")
    print(f"    cells.vh  (Verilog includes)")
    print(lib.summary())

    # ── Step 5: Summary ──
    print("\n[5/5] Design summary")
    print("-" * 40)
    print(f"  Process:           SkyWater 130nm")
    print(f"  Weight matrix:     8 x 8 ternary")
    print(f"  ROM cells:         {s.plus_count + s.minus_count} active, {s.zero_count} zero")
    print(f"  Estimated area:    {s.estimated_area_mm2*1e6:.1f} um2")
    print(f"  Estimated leakage: {report.estimated_rom_leakage_uw*1000:.2f} nW")
    print(f"  TinyTapeout cost:  $300")
    print(f"  Turnaround:        8 weeks")
    print("=" * 60)
    print("DESIGN FILES GENERATED SUCCESSFULLY")
    print(f"Output directory: {build_dir}")
    print("=" * 60)

    # Print the weight map
    print("\nWeight map (+ = +1, - = -1, . = 0):")
    for row in W_t:
        print("  " + " ".join("+" if w == 1 else "-" if w == -1 else "." for w in row))


if __name__ == "__main__":
    main()
