"""Ternarization engine for mask-locked ternary inference ROM chips.

This sub-package provides:

- :class:`Ternarizer` — core BitNet b1.58 ternary weight conversion
- :class:`SensitivityAnalyzer` — per-layer sensitivity analysis for
  mixed-precision quantization decisions
"""

from .engine import Ternarizer
from .sensitivity import SensitivityAnalyzer

__all__ = ["Ternarizer", "SensitivityAnalyzer"]
