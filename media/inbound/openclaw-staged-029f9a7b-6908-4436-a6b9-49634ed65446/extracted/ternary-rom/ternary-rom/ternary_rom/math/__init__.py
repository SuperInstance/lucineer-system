"""Mathematical foundations for ternary ROM inference chips.

Deep mathematical toolkit covering:
- Number theory (balanced ternary, Cantor set, modular arithmetic)
- Information theory (entropy, channel capacity, rate-distortion, mutual information)
- Coding theory (error-correcting codes, stuck-at fault tolerance)
- Stochastic processes (random matrix theory, concentration inequalities)
- Optimization theory (Lloyd-Max, ADMM, proximal operators, Markowitz precision allocation)
- Graph theory (ROM topology, expander graphs, isoperimetric bounds)
- Thermodynamic & physical models (Landauer, Boltzmann, subthreshold conduction)
- Approximation theory (Kolmogorov entropy, VC dimension, spectral analysis)
"""

__all__ = [
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
