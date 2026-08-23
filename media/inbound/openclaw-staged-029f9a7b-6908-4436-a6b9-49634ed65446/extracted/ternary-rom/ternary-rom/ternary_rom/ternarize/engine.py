"""Ternary weight quantization engine for mask-locked ROM inference chips.

Implements BitNet b1.58 ternarization: round(W / alpha) clamped to {-1, 0, +1},
where alpha = mean(|W|).  Supports mixed-precision by selectively skipping
sensitive layers and keeping them at INT8 or FP16.

All core math is numpy-only; torch is never required.
"""

import math
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class TernarizeResult:
    """Result of ternarizing a single layer."""

    name: str
    shape: Tuple[int, ...]
    weight_ternary: np.ndarray       # int8 values in {-1, 0, +1}
    weight_original: np.ndarray       # original FP32/FP16 weights
    alpha: float                      # scaling factor used
    cos_sim: float                    # cosine similarity original vs ternary
    mse: float                        # mean squared error
    sparsity: float                   # fraction of zeros
    skip: bool                        # True if kept at full precision
    keep_bits: int                    # 2 for ternary, 8 for INT8, 16 for FP16


@dataclass
class TernarizeReport:
    """Full report for a model."""

    layers: List[TernarizeResult]
    total_params: int
    ternary_params: int
    int8_params: int                  # skipped layers kept at INT8
    fp16_params: int                  # skipped layers kept at FP16
    overall_cos_sim: float
    overall_mse: float
    rom_bits: int                     # 2 * ternary_params
    sram_bits: int                    # bits for skipped (INT8/FP16) layers
    estimated_rom_area_mm2: float     # at 28 nm, 0.048 um²/cell
    estimated_rom_leakage_uw: float   # at 28 nm, 2.37 pA/cell for ±1, 0 for 0


# ---------------------------------------------------------------------------
# Helper – fnv-1a style name-pattern matching
# ---------------------------------------------------------------------------

_SENSITIVE_PATTERNS: List[str] = [
    "dt_proj", "dt", "norm", "layernorm", "final", "lm_head", "output",
]


def _name_matches_any(name: str, patterns: List[str]) -> bool:
    """Return True if *name* contains any of *patterns* (case-insensitive)."""
    name_lower = name.lower()
    return any(p in name_lower for p in patterns)


# ---------------------------------------------------------------------------
# Ternarizer
# ---------------------------------------------------------------------------

class Ternarizer:
    """Convert neural network weights to ternary {-1, 0, +1} quantization.

    Supports per-layer sensitivity analysis to identify which layers
    should be skipped (kept at INT8) for mixed-precision models.

    Args:
        weights: Dict of {layer_name: np.ndarray} weights.
        skip_layers: List of layer name patterns to skip (kept at full precision).
        skip_threshold: Cosine similarity threshold below which a layer is
                        flagged for skipping (default 0.95).
    """

    # 28 nm ROM constants
    _CELL_AREA_UM2: float = 0.048          # um² per ternary ROM cell
    _CELL_AREA_MM2: float = 0.048e-12     # mm² per cell
    _CELL_LEAKAGE_PA: float = 2.37         # pA per non-zero ROM cell
    _NOMINAL_VOLTAGE: float = 1.0          # V (for leakage power)

    def __init__(
        self,
        weights: Dict[str, np.ndarray],
        skip_layers: Optional[List[str]] = None,
        skip_threshold: float = 0.95,
    ) -> None:
        self._weights = weights
        self._skip_patterns: List[str] = list(skip_layers or [])
        self._skip_threshold = skip_threshold

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def convert(self) -> TernarizeReport:
        """Ternarize all layers, returning full report."""
        results: List[TernarizeResult] = []
        all_cos_sims: List[float] = []
        all_mses: List[float] = []

        for name, w in self._weights.items():
            result = self.analyze_layer(name, w)
            results.append(result)
            if not result.skip:
                all_cos_sims.append(result.cos_sim)
                all_mses.append(result.mse)

        # Aggregate counts
        total_params = sum(int(np.prod(w.shape)) for w in self._weights.values())
        ternary_params = sum(
            int(np.prod(r.shape)) for r in results if not r.skip
        )
        int8_params = sum(
            int(np.prod(r.shape)) for r in results if r.skip and r.keep_bits == 8
        )
        fp16_params = sum(
            int(np.prod(r.shape)) for r in results if r.skip and r.keep_bits == 16
        )

        # Weighted-average cos_sim / MSE across ternarized layers only
        if all_cos_sims:
            overall_cos_sim = float(np.mean(all_cos_sims))
            overall_mse = float(np.mean(all_mses))
        else:
            overall_cos_sim = 1.0
            overall_mse = 0.0

        rom_bits = 2 * ternary_params
        sram_bits = 8 * int8_params + 16 * fp16_params

        # Area estimate
        rom_area_mm2 = ternary_params * self._CELL_AREA_MM2

        # Leakage estimate: only non-zero ternary cells consume power
        nonzero_ternary = sum(
            int(np.count_nonzero(r.weight_ternary))
            for r in results
            if not r.skip
        )
        rom_leakage_uw = (
            nonzero_ternary * self._CELL_LEAKAGE_PA * 1e-12  # pA → A
            * self._NOMINAL_VOLTAGE                     # P = I·V
            * 1e6                                       # W → uW
        )

        return TernarizeReport(
            layers=results,
            total_params=total_params,
            ternary_params=ternary_params,
            int8_params=int8_params,
            fp16_params=fp16_params,
            overall_cos_sim=overall_cos_sim,
            overall_mse=overall_mse,
            rom_bits=rom_bits,
            sram_bits=sram_bits,
            estimated_rom_area_mm2=rom_area_mm2,
            estimated_rom_leakage_uw=rom_leakage_uw,
        )

    def ternarize_weight(
        self, w: np.ndarray,
    ) -> Tuple[np.ndarray, float, float, float]:
        """Ternarize a single weight matrix.

        Returns: (ternary_weights, alpha, cos_sim, mse)
        Uses BitNet b1.58 method: round(w / alpha) clamped to {-1, 0, +1}.
        """
        w_t, alpha = self.ternarize_bitnet(w)
        w_float = w_t.astype(np.float64)
        cos_sim = self.cosine_similarity(w.ravel(), w_float.ravel())
        mse = float(np.mean((w.astype(np.float64) - w_float) ** 2))
        return w_t, alpha, cos_sim, mse

    def analyze_layer(self, name: str, w: np.ndarray) -> TernarizeResult:
        """Analyze a single layer's sensitivity to ternarization."""
        w = np.asarray(w, dtype=np.float64)
        shape = w.shape

        # Decide whether to skip this layer
        should_skip = _name_matches_any(name, self._skip_patterns)

        # Always compute ternary metrics (even for skipped layers, for the report)
        w_t, alpha, cos_sim, mse = self.ternarize_weight(w)
        sparsity = float(np.mean(w_t == 0))

        # If not explicitly skipped by pattern, auto-skip if cos_sim is too low
        if not should_skip and cos_sim < self._skip_threshold:
            should_skip = True

        if should_skip:
            keep_bits = 16  # default: keep at FP16
            # If the user explicitly listed this layer, they might want INT8;
            # but conservatively we keep FP16 unless cos_sim >= int8 range.
            # Layers with cos_sim >= 0.98 can survive INT8.
            if cos_sim >= 0.98:
                keep_bits = 8
            return TernarizeResult(
                name=name,
                shape=shape,
                weight_ternary=w_t,
                weight_original=w,
                alpha=alpha,
                cos_sim=cos_sim,
                mse=mse,
                sparsity=sparsity,
                skip=True,
                keep_bits=keep_bits,
            )

        return TernarizeResult(
            name=name,
            shape=shape,
            weight_ternary=w_t,
            weight_original=w,
            alpha=alpha,
            cos_sim=cos_sim,
            mse=mse,
            sparsity=sparsity,
            skip=False,
            keep_bits=2,
        )

    # ------------------------------------------------------------------
    # Static / class-level utilities
    # ------------------------------------------------------------------

    @staticmethod
    def ternarize_bitnet(
        w: np.ndarray, alpha: Optional[float] = None
    ) -> Tuple[np.ndarray, float]:
        """BitNet b1.58 ternarization.

        W_t = round(W / alpha).clamp(-1, 1)
        where alpha = mean(|W|)

        Args:
            w: Weight array (any shape, float).
            alpha: Optional pre-computed scaling factor.

        Returns:
            (ternary_weights as int8, alpha)
        """
        w = np.asarray(w, dtype=np.float64)
        if alpha is None:
            alpha = float(np.mean(np.abs(w)))
        if alpha == 0.0:
            # All-zero weight → return all zeros
            return np.zeros_like(w, dtype=np.int8), 0.0

        w_scaled = w / alpha
        w_rounded = np.round(w_scaled)
        w_clamped = np.clip(w_rounded, -1, 1)
        return w_clamped.astype(np.int8), alpha

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Cosine similarity between two flat arrays.

        Returns 1.0 if both vectors are zero-norm.
        """
        a = np.asarray(a, dtype=np.float64).ravel()
        b = np.asarray(b, dtype=np.float64).ravel()
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0.0 and norm_b == 0.0:
            return 1.0
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    @staticmethod
    def pack_ternary(weights: np.ndarray) -> np.ndarray:
        """Pack ternary weights {-1, 0, +1} into 2-bit representation.

        Encoding: 00 = +1, 01 = 0, 10 = -1.
        Packs 4 weights per byte (MSB first).
        Returns uint8 array of shape (..., ceil(N / 4)).

        For a 1-D array of length L, the output has length ceil(L / 4).
        For N-D arrays the last axis is packed.
        """
        w = np.asarray(weights, dtype=np.int8)
        original_shape = w.shape
        # Flatten to 1-D for packing, remember the leading dims
        flat = w.ravel()
        n = len(flat)

        # Pad to multiple of 4
        pad_len = (4 - n % 4) % 4
        if pad_len > 0:
            flat = np.concatenate([flat, np.zeros(pad_len, dtype=np.int8)])

        # Map: +1 → 0b00, 0 → 0b01, -1 → 0b10
        # Build lookup: index = w + 1 → {0: -1, 1: 0, 2: +1}
        # We want: +1 → 0, 0 → 1, -1 → 2
        lookup = np.array([2, 1, 0], dtype=np.uint8)  # index by (w + 1)
        codes = lookup[flat + 1]  # shape (padded_n,)

        # Reshape to groups of 4
        codes = codes.reshape(-1, 4)  # (groups, 4)

        # Pack MSB first: first weight in bits [7:6], second in [5:4], etc.
        packed = (
            (codes[:, 0].astype(np.uint32) << 6)
            | (codes[:, 1].astype(np.uint32) << 4)
            | (codes[:, 2].astype(np.uint32) << 2)
            | codes[:, 3].astype(np.uint32)
        ).astype(np.uint8)

        return packed

    @staticmethod
    def unpack_ternary(
        packed: np.ndarray, original_shape: Tuple[int, ...]
    ) -> np.ndarray:
        """Unpack 2-bit ternary representation back to {-1, 0, +1} int8 array.

        Inverse of :meth:`pack_ternary`.
        """
        packed = np.asarray(packed, dtype=np.uint8).ravel()
        n_groups = len(packed)
        total_elements = n_groups * 4

        # Extract 2-bit fields, MSB first
        codes = np.empty(total_elements, dtype=np.uint8)
        codes[0::4] = (packed >> 6) & 0x3
        codes[1::4] = (packed >> 4) & 0x3
        codes[2::4] = (packed >> 2) & 0x3
        codes[3::4] = packed & 0x3

        # Decode: 00→+1, 01→0, 10→-1, 11→invalid (treat as 0)
        lookup = np.array([1, 0, -1, 0], dtype=np.int8)
        flat = lookup[codes]

        # Trim to original size and reshape
        n_original = int(np.prod(original_shape))
        flat = flat[:n_original]
        return flat.reshape(original_shape)

    @staticmethod
    def export_rom_bitmap(weights: np.ndarray) -> np.ndarray:
        """Export ternary weights as a ROM programming bitmap.

        Returns a uint8 array where each byte represents one weight:
            0x00 = +1 (ROM_PLUS cell)
            0x01 =  0 (ROM_ZERO cell)
            0x02 = -1 (ROM_MINUS cell)

        This is the direct input to netlist generation.
        """
        w = np.asarray(weights, dtype=np.int8).ravel()
        # Map: +1 → 0x00, 0 → 0x01, -1 → 0x02
        lookup = np.array(
            [0x02, 0x01, 0x00], dtype=np.uint8
        )  # index by (w + 1): {-1→0, 0→1, +1→2}
        return lookup[w + 1].reshape(weights.shape)
