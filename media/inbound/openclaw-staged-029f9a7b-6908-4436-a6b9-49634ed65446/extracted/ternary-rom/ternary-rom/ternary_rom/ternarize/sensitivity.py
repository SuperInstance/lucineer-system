"""Per-layer sensitivity analysis for mixed-precision ternary quantization.

Identifies which layers can tolerate ternary quantization and which need
higher precision (INT8 / INT4 / FP16), based on cosine-similarity
degradation.  Critical for Mamba/SSM models where the dt (step size)
projection is highly sensitive (cos_sim ≈ 0.91 ternary vs 0.99 INT8)
while A/B/C projections tolerate ternary well (cos_sim > 0.95).
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class LayerSensitivity:
    """Per-layer quantization sensitivity profile."""

    name: str
    shape: Tuple[int, ...]
    cos_sim_ternary: float   # cos_sim after ternarization
    cos_sim_int8: float     # cos_sim after INT8 quantization
    cos_sim_int4: float     # cos_sim after INT4 quantization
    sensitivity_rank: int   # 1 = most sensitive (lowest cos_sim)
    recommendation: str     # "ternary", "int8", "int4", or "fp16"
    rationale: str


# Layer-name patterns that are known to be sensitive to aggressive
# quantization, independent of the measured cosine similarity.
_HARD_SENSITIVE_PATTERNS: List[str] = [
    "dt_proj",
    "dt",
    "norm",
    "layernorm",
    "final",
    "lm_head",
    "output",
    "router",
    "gate",
]


class SensitivityAnalyzer:
    """Per-layer sensitivity analysis for mixed-precision quantization.

    Identifies which layers can tolerate ternary quantization and which
    need higher precision, based on cosine similarity degradation.

    This is critical for Mamba/SSM models where the dt (step size)
    projection is highly sensitive (cos_sim=0.91 ternary vs 0.99 INT8)
    while A/B/C projections tolerate ternary well (cos_sim > 0.95).

    Args:
        ternary_threshold: cos_sim above this → ternary is OK (default 0.95)
        int8_threshold:    cos_sim above this → INT8 is OK (default 0.98)
        int4_threshold:    cos_sim above this → INT4 is OK (default 0.995)
    """

    def __init__(
        self,
        ternary_threshold: float = 0.95,
        int8_threshold: float = 0.98,
        int4_threshold: float = 0.995,
    ) -> None:
        self._ternary_threshold = ternary_threshold
        self._int8_threshold = int8_threshold
        self._int4_threshold = int4_threshold

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze(self, weights: Dict[str, np.ndarray]) -> List[LayerSensitivity]:
        """Analyze all layers and return sorted sensitivity list.

        Layers are sorted so that the most sensitive (lowest ternary
        cos_sim) comes first (rank 1).
        """
        sensitivities: List[LayerSensitivity] = []
        for name, w in weights.items():
            sensitivities.append(self.analyze_layer(name, w))

        # Sort by ternary cos_sim ascending (worst first)
        sensitivities.sort(key=lambda s: s.cos_sim_ternary)
        for rank, s in enumerate(sensitivities, start=1):
            s.sensitivity_rank = rank

        return sensitivities

    def analyze_layer(self, name: str, w: np.ndarray) -> LayerSensitivity:
        """Analyze a single layer at ternary, INT8, INT4 precisions."""
        w = np.asarray(w, dtype=np.float64)
        shape = w.shape
        flat = w.ravel()
        norm = np.linalg.norm(flat)

        # --- Ternary cos_sim ---
        from .engine import Ternarizer

        w_t, alpha = Ternarizer.ternarize_bitnet(w)
        w_t_f = w_t.astype(np.float64)
        if norm == 0.0:
            cos_ternary = 1.0
        else:
            cos_ternary = float(
                np.dot(flat, w_t_f.ravel()) / (norm * np.linalg.norm(w_t_f))
            )
            cos_ternary = min(cos_ternary, 1.0)

        # --- INT8 cos_sim ---
        w_int8, _scale8 = self.quantize_int8(w)
        if norm == 0.0:
            cos_int8 = 1.0
        else:
            cos_int8 = float(
                np.dot(flat, w_int8.ravel().astype(np.float64))
                / (norm * np.linalg.norm(w_int8))
            )
            cos_int8 = min(cos_int8, 1.0)  # numerical clamp

        # --- INT4 cos_sim ---
        w_int4, _scale4 = self.quantize_int4(w)
        if norm == 0.0:
            cos_int4 = 1.0
        else:
            cos_int4 = float(
                np.dot(flat, w_int4.ravel().astype(np.float64))
                / (norm * np.linalg.norm(w_int4))
            )
            cos_int4 = min(cos_int4, 1.0)

        # --- Recommendation ---
        precision, rationale = self.recommend_precision(cos_ternary, name)

        return LayerSensitivity(
            name=name,
            shape=shape,
            cos_sim_ternary=cos_ternary,
            cos_sim_int8=cos_int8,
            cos_sim_int4=cos_int4,
            sensitivity_rank=0,  # filled in by analyze()
            recommendation=precision,
            rationale=rationale,
        )

    # ------------------------------------------------------------------
    # Quantization primitives
    # ------------------------------------------------------------------

    @staticmethod
    def quantize_int8(w: np.ndarray) -> Tuple[np.ndarray, float]:
        """Symmetric per-tensor INT8 quantization.

        scale = max(|W|) / 127
        W_q = clamp(round(W / scale), -128, 127)

        Returns:
            (quantized int8 array, scale)
        """
        w = np.asarray(w, dtype=np.float64)
        abs_max = float(np.max(np.abs(w)))
        if abs_max == 0.0:
            return np.zeros_like(w, dtype=np.int8), 1.0
        scale = abs_max / 127.0
        w_q = np.round(w / scale)
        w_q = np.clip(w_q, -128, 127)
        return w_q.astype(np.int8), scale

    @staticmethod
    def quantize_int4(w: np.ndarray) -> Tuple[np.ndarray, float]:
        """Symmetric per-tensor INT4 quantization.

        scale = max(|W|) / 7
        W_q = clamp(round(W / scale), -8, 7)

        Returns:
            (quantized int8 array (values in [-8, 7]), scale)
        """
        w = np.asarray(w, dtype=np.float64)
        abs_max = float(np.max(np.abs(w)))
        if abs_max == 0.0:
            return np.zeros_like(w, dtype=np.int8), 1.0
        scale = abs_max / 7.0
        w_q = np.round(w / scale)
        w_q = np.clip(w_q, -8, 7)
        return w_q.astype(np.int8), scale

    # ------------------------------------------------------------------
    # Recommendation logic
    # ------------------------------------------------------------------

    def recommend_precision(
        self, cos_sim: float, layer_name: str
    ) -> Tuple[str, str]:
        """Recommend precision level based on cosine similarity.

        Also checks layer name patterns (e.g. ``dt_proj`` → always INT8).

        Returns:
            (precision, rationale)
        """
        name_lower = layer_name.lower()

        # Hard-override: certain layer types are known to be fragile
        for pattern in _HARD_SENSITIVE_PATTERNS:
            if pattern in name_lower:
                # Even with hard override, use the best precision that
                # makes sense — INT8 for most, FP16 for exceptionally
                # sensitive ones.
                if cos_sim < self._int8_threshold:
                    return (
                        "int8",
                        f"Layer name contains '{pattern}' (known sensitive pattern) "
                        f"and ternary cos_sim={cos_sim:.4f} < {self._int8_threshold}"
                    )
                # cos_sim is already good enough for INT8, but pattern
                # says be cautious
                return (
                    "int8",
                    f"Layer name contains '{pattern}' (known sensitive pattern); "
                    f"keeping at INT8 for safety (ternary cos_sim={cos_sim:.4f})",
                )

        # Normal decision path based on measured cosine similarity
        if cos_sim >= self._ternary_threshold:
            return (
                "ternary",
                f"cos_sim={cos_sim:.4f} >= {self._ternary_threshold} (ternary threshold); "
                f"layer tolerates ternary quantization well",
            )

        if cos_sim >= self._int8_threshold:
            return (
                "int8",
                f"cos_sim={cos_sim:.4f} in [{self._int8_threshold}, {self._ternary_threshold}); "
                f"INT8 provides sufficient fidelity",
            )

        if cos_sim >= self._int4_threshold:
            return (
                "int4",
                f"cos_sim={cos_sim:.4f} in [{self._int4_threshold}, {self._int8_threshold}); "
                f"INT4 required for acceptable fidelity",
            )

        return (
            "fp16",
            f"cos_sim={cos_sim:.4f} < {self._int4_threshold}; "
            f"even INT4 degrades quality — keep at FP16",
        )

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, sensitivities: List[LayerSensitivity]) -> str:
        """Generate a human-readable sensitivity report.

        Formatted as a markdown table with columns:
        Layer | Shape | Ternary cos_sim | INT8 cos_sim | Recommendation | Rationale
        Sorted by sensitivity_rank (most sensitive first).
        """
        lines: List[str] = []
        lines.append("# Layer Sensitivity Analysis Report")
        lines.append("")
        lines.append(
            "| Rank | Layer | Shape | Ternary cos_sim | INT8 cos_sim | "
            "INT4 cos_sim | Recommendation | Rationale |"
        )
        lines.append(
            "|------|-------|-------|-----------------|-------------| "
            "------------|----------------|----------|"
        )

        for s in sensitivities:
            shape_str = "x".join(str(d) for d in s.shape)
            lines.append(
                f"| {s.sensitivity_rank} | `{s.name}` | {shape_str} | "
                f"{s.cos_sim_ternary:.4f} | {s.cos_sim_int8:.4f} | "
                f"{s.cos_sim_int4:.4f} | {s.recommendation} | {s.rationale} |"
            )

        lines.append("")

        # Summary counts
        n_total = len(sensitivities)
        n_ternary = sum(1 for s in sensitivities if s.recommendation == "ternary")
        n_int8 = sum(1 for s in sensitivities if s.recommendation == "int8")
        n_int4 = sum(1 for s in sensitivities if s.recommendation == "int4")
        n_fp16 = sum(1 for s in sensitivities if s.recommendation == "fp16")
        lines.append(f"**Summary:** {n_total} layers total")
        lines.append(f"- Ternary: {n_ternary}")
        lines.append(f"- INT8:    {n_int8}")
        lines.append(f"- INT4:    {n_int4}")
        lines.append(f"- FP16:    {n_fp16}")

        return "\n".join(lines) + "\n"
