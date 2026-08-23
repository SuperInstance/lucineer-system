# ternary-rom

**Model-to-GDS flow for mask-locked ternary inference chips.**

Convert a trained neural network into a tape-out-ready chip where weights are permanently encoded in mask-programmed ROM. No multipliers. No SRAM for weights. Just add/sub/skip.

```
pip install ternary-rom
```

## What It Does

`ternary-rom` takes ternary-quantized neural network weights ({-1, 0, +1}) and generates the complete set of files needed to manufacture an inference chip:

1. **Ternarize** a model's weights using BitNet b1.58 quantization
2. **Analyze** per-layer sensitivity to identify which layers need mixed precision
3. **Generate** structural Verilog netlists with ROM_PLUS/MINUS/ZERO cells
4. **Provide** ROM cell libraries (LEF/LIB/Verilog) for sky130 and 28nm
5. **Produce** OpenROAD flow scripts (Tcl) for placement, routing, and GDS export

## Why Ternary ROM?

| Property | Ternary ROM | Conventional (SRAM + FP16) |
|----------|------------|---------------------------|
| Weight storage | Mask-programmed ROM | SRAM |
| Bits per weight | 2 | 16 |
| Memory reduction | 8x | 1x (baseline) |
| Multiply operation | Eliminated (add/sub/skip) | Required |
| Gate count (MAC) | 103 | 360 |
| Energy per op | 22 pJ | 194 pJ |
| Weight update | New mask ($200K) | Rewrite SRAM (free) |
| Idle leakage | Zero for ~60% of cells (weight=0) | Full SRAM leakage |

Ternary ROM is not for every application. It's for **stable models that don't change often** — edge inference, embedded agents, dedicated accelerators. The tradeoff is permanence for radical simplicity and efficiency.

## Architecture

```
Trained Model (PyTorch/NumPy)
         │
         ▼
  ┌──────────────┐
  │  Ternarizer   │  BitNet b1.58: W_t = round(W/α).clamp(-1,1)
  │  + Sensitivity│  Identifies layers that need INT8 instead
  └──────┬───────┘
         │ ternary weights {-1, 0, +1}
         ▼
  ┌──────────────┐
  │  Netlist Gen  │  Structural Verilog with ROM cells
  │  + Cell Lib   │  LEF/LIB for OpenROAD
  └──────┬───────┘
         │ Verilog + LEF + LIB
         ▼
  ┌──────────────┐
  │  OpenROAD     │  Floorplan → Place → Route → GDSII
  │  Flow         │  Structured placement for ROM arrays
  └──────┬───────┘
         │ GDSII
         ▼
     Tape-out
```

### ROM Cell Design

Three cells form the entire weight storage:

| Cell | Transistors | Function | Leakage |
|------|------------|----------|----------|
| `ROM_PLUS` | 2T | WL=1 → BL=VDD (+1) | ~2.37 pA (28nm) |
| `ROM_MINUS` | 2T | WL=1 → BL=VSS (-1) | ~2.37 pA (28nm) |
| `ROM_ZERO` | **0T** | No cell (empty space) | **0 pA** |

The `ROM_ZERO` cell is just empty space — no transistors, no leakage. Since ~45% of ternary weights are zero (BitNet b1.58), this provides free leakage reduction.

## Quick Start

### Install

```bash
pip install ternary-rom
# or from source:
git clone https://github.com/yourname/ternary-rom.git
cd ternary-rom && pip install -e .
```

### CLI Usage

```bash
# Analyze a model's sensitivity to ternary quantization
ternary-rom analyze weights.npz

# Ternarize model weights
ternary-rom ternarize weights.npz -o build/

# Generate structural Verilog from ternary weights
ternary-rom netlist build/ternary_weights.npz --process sky130 -o build/

# Generate ROM cell library files
ternary-rom cells sky130 -o build/cells/

# Generate OpenROAD flow scripts
ternary-rom flow build/model.v --process sky130 -o build/flow/

# System info
ternary-rom info
```

### Python API

```python
import numpy as np
from ternary_rom import Ternarizer, SensitivityAnalyzer, NetlistGenerator, ROMCellLibrary, OpenROADFlow

# 1. Load weights (dict of {layer_name: weight_array})
weights = {
    "layer1": np.random.randn(256, 256).astype(np.float32),
    "layer2": np.random.randn(256, 128).astype(np.float32),
}

# 2. Analyze sensitivity (which layers tolerate ternary?)
analyzer = SensitivityAnalyzer()
sensitivities = analyzer.analyze(weights)
print(analyzer.generate_report(sensitivities))

# 3. Ternarize (with mixed precision for sensitive layers)
ternarizer = Ternarizer(weights, skip_layers=["dt_proj"])
report = ternarizer.convert()
print(f"ROM area: {report.estimated_rom_area_mm2:.2f} mm2")
print(f"ROM leakage: {report.estimated_rom_leakage_uw:.2f} uW")

# 4. Generate Verilog netlist
netgen = NetlistGenerator(
    {r.name: r.weight_ternary for r in report.layers if not r.skip},
    config=NetlistConfig(cell_lib="sky130", pipeline_depth=1)
)
netgen.write_verilog("build/model.v")

# 5. Generate cell library
lib = ROMCellLibrary.from_bundle("sky130")
lib.write_all("build/cells/")

# 6. Generate OpenROAD flow
flow = OpenROADFlow()
flow.write_tcl_scripts("build/flow/")
```

## Tape-Out Options

| Option | Cost | Turnaround | When to Use |
|--------|------|-----------|-------------|
| **TinyTapeout** (sky130) | **$300** | 8 weeks | First proof-of-concept. Submit the 8x8 MAC example. |
| Metal-only masks (1-3 layers) | $200K | 3-6 months | Production chip with ROM-only customization. |
| Full ASIC | $2-4M | 12-18 months | Complex peripheral logic beyond ROM arrays. |

## Supported Processes

### SkyWater 130nm (sky130)
- Open-source PDK, used by TinyTapeout
- Cell area: 1.49 um2 per ROM cell
- Voltage: 3.3V
- Density: ~672K cells/mm2
- **Recommended for prototyping**

### Generic 28nm CMOS
- Production-quality estimates
- Cell area: 0.048 um2 per ROM cell
- Voltage: 1.0V
- Density: ~20.8M cells/mm2
- **Recommended for production**

## Project Structure

``
ternary-rom/
├── ternary_rom/                  # Python package
│   ├── ternarize/               # Weight ternarization
│   │   ├── engine.py            # Ternarizer class (BitNet b1.58)
│   │   └── sensitivity.py       # Per-layer sensitivity analysis
│   ├── netgen/                  # Netlist generation
│   │   └── generator.py         # Verilog structural netlist from weights
│   ├── cells/                   # ROM cell libraries
│   │   └── library.py           # LEF/LIB/Verilog generation
│   ├── flow/                    # OpenROAD ASIC flow
│   │   └── openroad.py          # Tcl script generation
│   └── cli/                     # Command-line interface
│       └── main.py              # ternary-rom CLI entry point
├── cells/                        # Pre-generated cell library files
│   ├── sky130/                   # SkyWater 130nm
│   └── generic_28nm/            # Generic 28nm
├── examples/
│   └── tinytapeout_8x8_mac/     # $300 proof-of-concept
├── tests/                        # 220 tests
└── pyproject.toml
```

## Technical Background

This tool encodes the findings from extensive research on mask-locked ternary inference:

- **BitNet b1.58** (Wang et al., 2024): Ternary quantization achieves near-FP16 accuracy at 7B scale
- **ROM weight encoding**: Weights become physical structure — metal interconnect defines {+1, 0, -1}
- **Energy**: 22 pJ/op ternary vs 194 pJ/op FP16 (8.8x improvement)
- **Area**: 103 gates per ternary MAC vs 360 for FP16 (2.86x reduction)
- **Leakage**: Zero-weight cells eliminate leakage by construction (~60% of cells)
- **Process scaling**: 14nm recommended for production (best $/TOPS, accessible foundries)

## Limitations

- **Weights are permanent**: Changing weights requires a new mask ($200K+). This is for stable, deployed models.
- **QAT required**: Post-training quantization to ternary fails catastrophically. Models must be trained with ternary quantization aware training (QAT) from scratch.
- **Mixed precision needed**: Some layers (dt projections in Mamba/SSM, layer norms) don't tolerate ternary and need INT8 SRAM. The sensitivity analyzer identifies these.
- **No GPU support**: Ternary inference on GPUs is slower than FP8 (no native ternary operations). This is an ASIC-only advantage.

## License

MIT

## Contributing

Contributions welcome. Priority areas:
1. Additional process nodes (14nm, 22nm GF/Samsung)
2. PyTorch model export integration (direct `model.state_dict()` support)
3. OpenROAD flow validation with actual tape-out results
4. Power estimation improvements (activity factor modeling)
5. Larger TinyTapeout examples (16x16, 32x32)
