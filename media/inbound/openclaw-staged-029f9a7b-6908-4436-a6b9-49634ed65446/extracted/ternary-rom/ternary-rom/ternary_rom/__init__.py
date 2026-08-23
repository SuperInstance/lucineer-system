"""ternary-rom: Model-to-GDS flow for mask-locked ternary inference chips.

Converts a trained neural network into a tape-out-ready GDSII file
where weights are permanently encoded in mask-programmed ROM cells.

Quick start:
    from ternary_rom import Ternarizer, NetlistGenerator, OpenROADFlow

    # 1. Ternarize a PyTorch model
    ternarizer = Ternarizer(model, layers_to_skip=["dt_proj"])
    ternary_weights = ternarizer.convert()
    sensitivity = ternarizer.sensitivity_report()

    # 2. Generate structural Verilog
    netgen = NetlistGenerator(ternary_weights, cell_lib="sky130")
    netgen.write_verilog("output/model_netlist.v")
    netgen.write_lef("output/model.lef")

    # 3. Run OpenROAD flow
    flow = OpenROADFlow("output/model_netlist.v", "sky130")
    flow.run_all(output_dir="output/gds")
"""

__version__ = "0.3.0"
__all__ = [
    "Ternarizer",
    "SensitivityAnalyzer",
    "NetlistGenerator",
    "ROMCellLibrary",
    "OpenROADFlow",
    "MathFoundation",
    "NumberTheory",
    "InformationTheory",
    "CodingTheory",
    "StochasticProcesses",
    "OptimizationTheory",
    "GraphTheory",
    "ThermodynamicModels",
    "ApproximationTheory",
]

try:
    from ternary_rom.ternarize.engine import Ternarizer
    from ternary_rom.ternarize.sensitivity import SensitivityAnalyzer
    from ternary_rom.netgen.generator import NetlistGenerator
    from ternary_rom.cells.library import ROMCellLibrary
    from ternary_rom.flow.openroad import OpenROADFlow
except ImportError as e:
    import warnings
    warnings.warn(f"Could not import all modules: {e}")

try:
    from ternary_rom.math.foundation import MathFoundation
    from ternary_rom.math.number_theory import NumberTheory
    from ternary_rom.math.information_theory import InformationTheory
    from ternary_rom.math.coding_theory import CodingTheory
    from ternary_rom.math.stochastic_processes import StochasticProcesses
    from ternary_rom.math.optimization_theory import OptimizationTheory
    from ternary_rom.math.graph_theory import GraphTheory
    from ternary_rom.math.thermodynamic_models import ThermodynamicModels
    from ternary_rom.math.approximation_theory import ApproximationTheory
except ImportError as e:
    import warnings
    warnings.warn(f"Could not import math modules: {e}")
