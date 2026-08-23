# TinyTapeout 8x8 Ternary MAC Tile

**Status:** Proof-of-concept | **Cost:** $300 | **Turnaround:** 8 weeks | **Process:** SkyWater 130nm

## What This Demonstrates

This is the smallest possible proof-of-concept for mask-locked ternary inference: an 8×8 matrix-vector multiply unit where weights are permanently encoded in ROM cells during fabrication.

- 64 ternary weights {-1, 0, +1} in mask-programmed ROM (no SRAM needed)
- Matrix-vector multiply via add/sub/skip (no multipliers)
- Time-multiplexed: 8 clock cycles per input vector
- Demonstrates the complete ternary-rom flow: model → ternarize → Verilog → GDS

## Architecture

```
         Input Vector (8 elements, one per cycle)
              │
    ┌─────────┼──────────────────────┐
    │  Row 0  │  ROM cells for weight[0][0..7]  │
    │  Row 1  │  ROM cells for weight[1][0..7]  │
    │  ...    │  ...                                  │
    │  Row 7  │  ROM cells for weight[7][0..7]  │
    └─────────┼──────────────────────┘
              │
         Accumulator (8-bit signed)
              │
         Output Result
```

Each ROM cell drives +input (PLUS), -input (MINUS), or nothing (ZERO) onto the bitline. An accumulator sums the bitline contributions over 8 clock cycles.

## Generate Design Files

```bash
# From the ternary-rom project root
cd examples/tinytapeout_8x8_mac

# Generate cell library, ternarize weights, produce Verilog
python generate.py

# Output in ./build/:
#   cells.v          ROM cell behavioral models
#   cells.lef         LEF macro definitions
#   ternary_mac.v     Structural Verilog netlist
#   weight_map.txt    Human-readable weight visualization
#   summary.txt       Area and leakage estimates
```

## Simulate

```bash
# Requires: iverilog
make sim
# Expected output: "TEST PASSED - All 8 columns match"
```

## Submit to TinyTapeout

1. Generate design files: `python generate.py`
2. Wrap the generated Verilog in the TinyTapeout project template
3. Ensure design fits the TinyTapeout area constraint
4. Submit via [tinytapeout.com](https://tinytapeout.com)
5. Wait 8 weeks for fabricated chips

## Expected Results (sky130)

| Metric | Value |
|--------|-------|
| Die area (active) | ~150 μm² (64 cells × 1.49 μm²/cell + peripheral) |
| Cell area (per ROM cell) | 1.49 μm² (1.22 × 1.22 μm) |
| Leakage (all non-zero cells) | ~0.3 nA at 3.3V |
| Clock frequency | ~100 MHz (conservative for sky130) |
| Throughput | 12.5 M MACs/sec (8 cycles per MAC) |
| Energy per MAC | ~75 pJ (estimated) |

## Modifying for Your Own Model

Edit `generate.py` to change the weight matrix:

```python
# Replace with your own trained ternary weights
my_weights = np.array([
    [ 1,  0, -1,  1,  0,  0, -1,  0],
    [ 0,  1,  0,  0, -1,  1,  0,  0],
    # ... your weights here
], dtype=np.int8)
```

Then re-run `python generate.py` to get new Verilog.

## Cost Analysis

| Item | Cost |
|------|------|
| TinyTapeout shuttle slot | $300 |
| 8-week turnaround | Included |
| SkyWater 130nm wafer | Shared (included) |
| Packaging | Included |
| **Total** | **$300** |

This is the cheapest possible way to validate the ternary ROM concept in silicon.
