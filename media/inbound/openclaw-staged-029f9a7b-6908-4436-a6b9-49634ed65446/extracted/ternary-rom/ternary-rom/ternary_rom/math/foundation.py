"""Unified mathematical foundation facade for ternary ROM.

Aggregates all eight mathematical domains into a single analysis
pipeline that can be run on any weight matrix to produce a
comprehensive mathematical profile.

Domains:
    1. NumberTheory — balanced ternary, Cantor set, carry-free arithmetic
    2. InformationTheory — entropy, channel capacity, rate-distortion, MI
    3. CodingTheory — ECC, fault tolerance, yield modeling
    4. StochasticProcesses — random matrix theory, concentration bounds
    5. OptimizationTheory — optimal alpha, ADMM, Markowitz allocation
    6. GraphTheory — ROM topology, wirelength, connectivity
    7. ThermodynamicModels — Landauer, subthreshold, thermal noise
    8. ApproximationTheory — Kolmogorov entropy, VC dimension, spectral accuracy

Usage:
    from ternary_rom.math import MathFoundation

    mf = MathFoundation(weights_dict)
    profile = mf.full_analysis(process="generic_28nm")
    print(profile.summary())
"""

import numpy as np
import math
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from ternary_rom.math.number_theory import NumberTheory
from ternary_rom.math.information_theory import InformationTheory
from ternary_rom.math.coding_theory import CodingTheory
from ternary_rom.math.stochastic_processes import StochasticProcesses
from ternary_rom.math.optimization_theory import OptimizationTheory
from ternary_rom.math.graph_theory import GraphTheory
from ternary_rom.math.thermodynamic_models import ThermodynamicModels
from ternary_rom.math.approximation_theory import ApproximationTheory


@dataclass
class MathProfile:
    """Complete mathematical profile of a ternary ROM design.

    Aggregates results from all eight mathematical domains
    into a single structured report.
    """
    layer_name: str
    # Number theory
    cantor_measure: float
    effective_bits_per_weight: float
    trit_complexity: float
    # Information theory
    shannon_entropy: float
    normalized_entropy: float
    coding_overhead_pct: float
    channel_capacity_bits: float
    rate_distortion_efficiency: float
    mutual_info_normalized: float
    higher_order_loss: float
    landauer_factor: float
    # Coding theory
    fault_tolerance_yield: float
    bare_die_yield: float
    yield_improvement: float
    per_defect_accuracy_loss: float
    # Stochastic processes
    condition_number: float
    effective_rank: float
    clt_quality: str
    dynamic_range_bits: int
    gauss_approx_bits: int
    berry_essen_rate: float
    # Optimization theory
    alpha_gap_pct: float
    mse_improvement_pct: float
    optimal_alpha: float
    bitnet_alpha: float
    # Graph theory
    density: float
    expansion_ratio: float
    routing_overhead_factor: float
    cheeger_constant: float
    # Thermodynamic
    noise_margin_db: float
    per_cell_ber: float
    is_thermally_reliable: bool
    energy_per_mac_fJ: float
    thermodynamic_efficiency: float
    subthreshold_swing: float
    # Approximation theory
    spectral_energy_fraction: float
    vc_dimension_upper: float
    kolmogorov_bits_per_weight: float
    approximation_order: str
    decay_rate: float

    def summary(self, width: int = 72) -> str:
        """Generate a human-readable summary of the math profile.

        Args:
            width: Line width for formatting.

        Returns:
            Multi-line summary string.
        """
        lines = [
            f"{'=' * width}",
            f" MATH PROFILE: {self.layer_name}",
            f"{'=' * width}",
            "",
            f" NUMBER THEORY",
            f"   Cantor measure:        {self.cantor_measure:.4f}",
            f"   Effective bits/weight:  {self.effective_bits_per_weight:.3f}",
            f"   Trit complexity:        {self.trit_complexity:.4f}",
            "",
            f" INFORMATION THEORY",
            f"   Shannon entropy:       {self.shannon_entropy:.4f} bits (of {math.log2(3):.3f} max)",
            f"   Normalized entropy:     {self.normalized_entropy:.4f}",
            f"   Coding overhead:        {self.coding_overhead_pct:.2f}%",
            f"   Channel capacity:      {self.channel_capacity_bits:.4f} bits/cell",
            f"   R-D efficiency:         {self.rate_distortion_efficiency:.2f}x",
            f"   Mutual info (norm):     {self.mutual_info_normalized:.4f}",
            f"   Higher-order info loss: {self.higher_order_loss:.4f}",
            f"   Landauer factor:        {self.landauer_factor:.2e}x above min",
            "",
            f" CODING THEORY (fault tolerance)",
            f"   Bare die yield:         {self.bare_die_yield:.4f}",
            f"   Fault-tol yield:        {self.fault_tolerance_yield:.4f}",
            f"   Yield improvement:      {self.yield_improvement:.2f}x",
            f"   Per-defect accuracy:    {self.per_defect_accuracy_loss:.6f}",
            "",
            f" STOCHASTIC PROCESSES",
            f"   Condition number:       {self.condition_number:.2f}",
            f"   Effective rank:         {self.effective_rank:.2f}",
            f"   CLT quality:            {self.clt_quality}",
            f"   Dynamic range:          {self.dynamic_range_bits} bits (exact)",
            f"   Gaussian approx:        {self.gauss_approx_bits} bits (6-sigma)",
            f"   Berry-Esseen rate:      {self.berry_essen_rate:.4f}",
            "",
            f" OPTIMIZATION THEORY",
            f"   BitNet alpha:           {self.bitnet_alpha:.6f}",
            f"   Optimal alpha:          {self.optimal_alpha:.6f}",
            f"   Alpha gap:              {self.alpha_gap_pct:.2f}%",
            f"   MSE improvement:        {self.mse_improvement_pct:.2f}%",
            "",
            f" GRAPH THEORY",
            f"   Density:                {self.density:.4f}",
            f"   Expansion ratio:        {self.expansion_ratio:.2f}",
            f"   Routing overhead:       {self.routing_overhead_factor:.2f}x",
            f"   Cheeger constant:       {self.cheeger_constant:.4f}",
            "",
            f" THERMODYNAMIC MODELS",
            f"   Noise margin:           {self.noise_margin_db:.2f} dB",
            f"   Per-cell BER:           {self.per_cell_ber:.2e}",
            f"   Thermally reliable:     {'YES' if self.is_thermally_reliable else 'NO'}",
            f"   Energy/MAC:             {self.energy_per_mac_fJ:.2f} fJ",
            f"   Thermodynamic eff:      {self.thermodynamic_efficiency:.2e}",
            f"   Subthreshold swing:     {self.subthreshold_swing:.1f} mV/dec",
            "",
            f" APPROXIMATION THEORY",
            f"   Spectral energy:        {self.spectral_energy_fraction:.4f}",
            f"   VC dimension (upper):   {self.vc_dimension_upper:.0f}",
            f"   Kolmogorov bits/weight:  {self.kolmogorov_bits_per_weight:.4f}",
            f"   Approximation order:    {self.approximation_order}",
            f"   Singular value decay:   {self.decay_rate:.4f}",
            f"{'=' * width}",
        ]
        return '\n'.join(lines)


# ============================================================================
# MathFoundation — unified facade
# ============================================================================

class MathFoundation:
    """Unified mathematical foundation analysis for ternary ROM.

    Combines all eight mathematical domains into a single
    analysis pipeline that produces a comprehensive MathProfile
    for any set of weight matrices.

    Args:
        weights: Dict of {layer_name: np.ndarray} weights.
        process: Target process node name (default: "generic_28nm").
        temperature_K: Operating temperature (default: 300K).
        defect_density: Manufacturing defect density (default: 0.1/cm^2).
    """

    def __init__(
        self,
        weights: Dict[str, np.ndarray],
        process: str = "generic_28nm",
        temperature_K: float = 300.0,
        defect_density: float = 0.1,
    ) -> None:
        self._weights = weights
        self._process = process
        self._temperature = temperature_K
        self._defect_density = defect_density

    def analyze_layer(self, name: str, w: np.ndarray) -> MathProfile:
        """Run all 8 mathematical analyses on a single layer.

        Args:
            name: Layer name.
            w: Weight array (full precision).

        Returns:
            MathProfile with complete analysis.
        """
        W = np.asarray(w, dtype=np.float64)
        if W.ndim == 1:
            W = W.reshape(1, -1)
        m, n = W.shape
        w_flat = W.ravel()
        total = m * n

        # Ternarize
        alpha = float(np.mean(np.abs(w_flat)))
        if alpha > 0:
            w_t = np.round(w_flat / alpha).clip(-1, 1).astype(np.int8)
        else:
            w_t = np.zeros_like(w_flat, dtype=np.int8)
        W_t = w_t.reshape(m, n)

        # 1. Number theory
        cantor = NumberTheory.cantor_set_analysis(w_flat)
        complexity = NumberTheory.trit_wise_complexity(W_t)

        # 2. Information theory
        ent = InformationTheory.ternary_entropy_profile(w_t)
        ch_cap = InformationTheory.ternary_channel_capacity(
            v_dd=1.0, thermal_voltage=1.380649e-23 * self._temperature / 1.602e-19,
            threshold_std=0.03,
        )
        rd = InformationTheory.rate_distortion_analysis(w_flat, w_t, alpha)
        mi = InformationTheory.mutual_information_analysis(w_flat, w_t)
        land = InformationTheory.landauer_analysis(total, self._temperature, 22.0)

        # 3. Coding theory
        cell_area = 0.048  # 28nm default
        ft = CodingTheory.defect_tolerance_analysis(
            m, n, self._defect_density, cell_area,
            input_dimension=n, temperature_kelvin=self._temperature,
        )

        # 4. Stochastic processes
        conc = StochasticProcesses.concentration_bounds(w_t)
        spec = StochasticProcesses.spectral_profile(W_t, top_k=10)

        # 5. Optimization theory
        opt = OptimizationTheory.compute_optimal_alpha(W)

        # 6. Graph theory
        topo = GraphTheory.rom_topology(W_t)
        wl = GraphTheory.wirelength_estimate(m, n, cell_pitch_um=0.22)
        conn = GraphTheory.connectivity_analysis(W_t)

        # 7. Thermodynamic models
        noise = ThermodynamicModels.thermal_noise_analysis(
            v_dd=1.0, temperature_K=self._temperature,
            input_dimension=m,
        )
        energy = ThermodynamicModels.rom_energy_model(
            m, n, v_dd=1.0, sparsity=float(np.mean(w_t == 0)),
        )
        sub_m = ThermodynamicModels.subthreshold_model(temperature_K=self._temperature)

        # 8. Approximation theory
        spectral_acc = ApproximationTheory.spectral_accuracy(W, W_t, alpha)
        vc = ApproximationTheory.vc_dimension(int(np.sum(w_t != 0)), n_layers=1)
        kolm = ApproximationTheory.kolmogorov_entropy(W)
        best = ApproximationTheory.best_approximation(W, alpha)

        return MathProfile(
            layer_name=name,
            # Number theory
            cantor_measure=cantor.cantor_measure,
            effective_bits_per_weight=cantor.effective_bits_per_weight,
            trit_complexity=complexity,
            # Information theory
            shannon_entropy=ent.shannon_entropy,
            normalized_entropy=ent.normalized_entropy,
            coding_overhead_pct=ent.coding_overhead / 2.0 * 100,
            channel_capacity_bits=ch_cap.capacity_bits,
            rate_distortion_efficiency=rd.rd_efficiency,
            mutual_info_normalized=mi.mi_normalized,
            higher_order_loss=mi.higher_order_loss,
            landauer_factor=land["gap_factor"],
            # Coding theory
            fault_tolerance_yield=ft.fault_tolerance_yield,
            bare_die_yield=ft.bare_die_yield,
            yield_improvement=ft.yield_improvement,
            per_defect_accuracy_loss=ft.expected_accuracy_loss_per_defect,
            # Stochastic processes
            condition_number=spec.condition_number,
            effective_rank=spec.effective_rank,
            clt_quality=conc.clt_quality,
            dynamic_range_bits=conc.dynamic_range_bits,
            gauss_approx_bits=conc.gauss_approx_bits,
            berry_essen_rate=conc.berry_essen_rate,
            # Optimization theory
            alpha_gap_pct=opt.alpha_gap_bitnet_mse * 100,
            mse_improvement_pct=opt.mse_improvement,
            optimal_alpha=opt.mse_optimal_alpha,
            bitnet_alpha=opt.bitnet_alpha,
            # Graph theory
            density=topo.density,
            expansion_ratio=topo.expansion_ratio,
            routing_overhead_factor=wl.routing_overhead_factor,
            cheeger_constant=conn.cheeger_constant,
            # Thermodynamic
            noise_margin_db=noise.noise_margin_v,
            per_cell_ber=noise.per_cell_error_prob,
            is_thermally_reliable=noise.is_reliable,
            energy_per_mac_fJ=energy.energy_per_mac_fJ,
            thermodynamic_efficiency=energy.thermodynamic_efficiency,
            subthreshold_swing=sub_m.s_slope_mv_per_decade,
            # Approximation theory
            spectral_energy_fraction=spectral_acc.energy_fraction,
            vc_dimension_upper=vc.vc_dimension_upper,
            kolmogorov_bits_per_weight=kolm.bits_per_weight,
            approximation_order=spectral_acc.approximation_order,
            decay_rate=spectral_acc.decay_rate,
        )

    def full_analysis(self) -> List[MathProfile]:
        """Run full mathematical analysis on all layers.

        Returns:
            List of MathProfile, one per layer.
        """
        return [
            self.analyze_layer(name, w)
            for name, w in self._weights.items()
        ]

    def cross_layer_analysis(self) -> Dict[str, Any]:
        """Analyze cross-layer mathematical properties.

        Computes properties that require looking at all layers together:
        error propagation, precision allocation, and global statistics.

        Returns:
            Dict with cross-layer analysis results.
        """
        profiles = self.full_analysis()

        if not profiles:
            return {}

        # Global statistics
        avg_entropy = float(np.mean([p.shannon_entropy for p in profiles]))
        min_entropy = float(np.min([p.shannon_entropy for p in profiles]))
        max_entropy = float(np.max([p.shannon_entropy for p in profiles]))

        avg_cond = float(np.mean([p.condition_number for p in profiles if p.condition_number != float('inf')]))
        max_cond = float(np.max([p.condition_number for p in profiles if p.condition_number != float('inf')]))

        avg_rd_eff = float(np.mean([p.rate_distortion_efficiency for p in profiles if p.rate_distortion_efficiency < 100]))

        avg_yield_imp = float(np.mean([p.yield_improvement for p in profiles]))

        total_landauer = float(np.mean([p.landauer_factor for p in profiles]))

        n_reliable = sum(1 for p in profiles if p.is_thermally_reliable)

        avg_clt = [p.clt_quality for p in profiles]
        clt_breakdown = {
            "excellent": avg_clt.count("excellent"),
            "good": avg_clt.count("good"),
            "moderate": avg_clt.count("moderate"),
            "poor": avg_clt.count("poor"),
        }

        return {
            "n_layers": len(profiles),
            "avg_entropy": avg_entropy,
            "min_entropy": min_entropy,
            "max_entropy": max_entropy,
            "entropy_spread": max_entropy - min_entropy,
            "avg_condition_number": avg_cond,
            "max_condition_number": max_cond,
            "avg_rd_efficiency": avg_rd_eff,
            "avg_yield_improvement": avg_yield_imp,
            "avg_landauer_factor": total_landauer,
            "thermally_reliable_layers": n_reliable,
            "thermally_reliable_fraction": n_reliable / len(profiles),
            "clt_quality_breakdown": clt_breakdown,
            "layers_needing_attention": [
                p.layer_name for p in profiles
                if (p.condition_number > 100
                    or p.rate_distortion_efficiency > 3
                    or not p.is_thermally_reliable
                    or p.clt_quality in ("moderate", "poor"))
            ],
        }
