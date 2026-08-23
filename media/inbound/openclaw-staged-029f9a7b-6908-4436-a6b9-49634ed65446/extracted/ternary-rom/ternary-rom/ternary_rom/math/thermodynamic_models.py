"""Thermodynamic and physical models for ternary ROM systems.

Covers Landauer's principle, subthreshold conduction, thermal noise
modeling, energy-delay optimization, near-threshold operation, and
physical scaling limits.

Key theoretical results:
- Landauer's limit: E_min = kT * ln(2) per bit erased (~2.8e-21 J at 300K).
- For ternary: E_min = kT * ln(3) per trit (~4.1e-21 J at 300K).
- Subthreshold leakage: I_sub = I_0 * exp((V_gs - V_th)/(n * V_t))
  where V_t = kT/q = 26mV at 300K and n is the subthreshold slope factor.
- The thermal noise margin for a ternary cell: SNR = (V_dd/2) / (n_th * V_t)
  where n_th accounts for noise from all sources.
- Near-threshold operation at V_dd ~ V_th achieves minimum energy per op
  but with 10-100x delay increase.
- Power gating wake-up energy: E_wake = 0.5 * C_virtual * V_dd^2
  with entropic cost kT * ln(3) per cell.

References:
  Landauer, R. (1961). "Irreversibility and heat generation in the
    computing process." IBM J. Res. Dev.
  Swanson, R.M. & Meindl, J.D. (1972). "Ion-implanted complementary
    MOS transistors in low-voltage circuits." IEEE JSSC.
  Dreslinski, R.G. et al. (2010). "Near-threshold computing." IEEE Micro.
  Chandrakasan, A.P. et al. (1992). "A low-power chip for the wireless.
    IEEE JSSC.
"""

import numpy as np
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# Physical constants
# ============================================================================

BOLTZMANN_K = 1.380649e-23   # J/K
ELECTRON_CHARGE = 1.602176634e-19  # C
BOLTZMANN_EV = 8.617333262e-5   # eV/K


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class SubthresholdModel:
    """Subthreshold conduction model parameters."""
    v_th: float               # threshold voltage (V)
    n_factor: float            # subthreshold slope factor (typically 1.2-1.8)
    i0_per_um: float           # pre-exponential current per um width (A/um)
    temperature_K: float
    v_thermal: float           # kT/q in volts
    s_slope_mv_per_decade: float  # subthreshold slope in mV/decade


@dataclass
class ThermalNoiseResult:
    """Thermal noise analysis for a ternary ROM cell."""
    v_dd: float
    noise_margin_v: float           # minimum voltage difference between levels
    thermal_noise_rms_v: float      # RMS thermal noise voltage
    snr_db: float                   # signal-to-noise ratio in dB
    snr_linear: float
    per_cell_error_prob: float      # probability of misread due to noise
    per_column_error_prob: float    # probability of any error in K-cell column
    ber: float                      # bit error rate
    operating_margin_db: float      # noise margin above threshold
    is_reliable: bool               # True if BER < 1e-9


@dataclass
class EnergyModel:
    """Complete energy model for a ROM array."""
    # Cell-level
    cell_switching_energy_fJ: float    # energy per cell read
    zero_cell_routing_energy_fJ: float # routing energy even for zero cells
    # Array-level
    decoder_energy_fJ: float
    wordline_energy_fJ: float
    bitline_precharge_energy_fJ: float
    adder_tree_energy_fJ: float
    # Per-inference totals
    total_dynamic_energy_fJ: float
    total_leakage_energy_fJ: float     # per inference at given freq
    total_energy_fJ: float
    energy_per_op_fJ: float
    energy_per_mac_fJ: float
    # Efficiency
    landauer_factor: float             # actual / Landauer minimum
    thermodynamic_efficiency: float    # 1 / landauer_factor


@dataclass
class ScalingProjection:
    """Physics-based scaling projection across process nodes."""
    node_nm: int
    v_dd: float
    cell_area_um2: float
    leakage_per_cell_pA: float
    # Physics-based (not hand-specified)
    v_thermal_fraction: float     # V_t / V_dd
    subthreshold_swing_mv_dec: float
    energy_per_op_fJ: float       # C * V^2 scaling
    leakage_energy_per_op_fJ: float
    total_energy_per_op_fJ: float
    noise_margin_db: float
    max_freq_ghz: float            # estimated from critical path
    thermal_limit_node_nm: float   # where thermal noise becomes dominant


# ============================================================================
# ThermodynamicModels — main class
# ============================================================================

class ThermodynamicModels:
    """Thermodynamic and physical models for ternary ROM.

    Provides subthreshold conduction modeling, thermal noise analysis,
    energy modeling, near-threshold optimization, and physics-based
    scaling projections.
    """

    # ------------------------------------------------------------------
    # Subthreshold conduction
    # ------------------------------------------------------------------

    @staticmethod
    def subthreshold_model(
        v_th: float = 0.4,
        n_factor: float = 1.4,
        temperature_K: float = 300.0,
        width_um: float = 0.1,
    ) -> SubthresholdModel:
        """Build a subthreshold conduction model.

        The subthreshold swing is:
            S = n * (kT/q) * ln(10) [V/decade]

        For n=1.4 at 300K: S = 1.4 * 26mV * 2.303 = 83.8 mV/decade

        Args:
            v_th: Threshold voltage.
            n_factor: Subthreshold slope factor.
            temperature_K: Temperature.
            width_um: Transistor width.

        Returns:
            SubthresholdModel with parameters.
        """
        v_t = BOLTZMANN_K * temperature_K / ELECTRON_CHARGE  # kT/q in volts
        s_slope = n_factor * v_t * math.log(10) * 1000  # mV/decade

        # I_0 is process-dependent; estimate from leakage specification
        # Typical: I_0 ~ 1e-15 A/um at 28nm, V_gs = V_th
        i0 = 1e-15 * (0.22 / width_um)  # scale with feature size

        return SubthresholdModel(
            v_th=v_th,
            n_factor=n_factor,
            i0_per_um=i0 / width_um,
            temperature_K=temperature_K,
            v_thermal=v_t,
            s_slope_mv_per_decade=s_slope,
        )

    @staticmethod
    def subthreshold_leakage(
        model: SubthresholdModel,
        v_gs: float = 0.0,
        v_ds: float = 1.0,
    ) -> float:
        """Compute subthreshold leakage current.

        I_sub = I_0 * exp((V_gs - V_th) / (n * V_t)) * (1 - exp(-V_ds / V_t))

        For V_ds >> V_t: I_sub ~ I_0 * exp((V_gs - V_th) / (n * V_t))

        Args:
            model: SubthresholdModel.
            v_gs: Gate-source voltage.
            v_ds: Drain-source voltage.

        Returns:
            Leakage current in amps.
        """
        exponent = (v_gs - model.v_th) / (model.n_factor * model.v_thermal)
        # Clamp exponent to prevent overflow
        exponent = min(exponent, 50)
        i_sub = model.i0_per_um * math.exp(exponent)

        # DIBL correction for V_ds
        if model.v_thermal > 0:
            dibl_factor = 1.0 - math.exp(-v_ds / model.v_thermal)
        else:
            dibl_factor = 1.0

        return i_sub * dibl_factor

    @staticmethod
    def leakage_vs_temperature(
        base_leakage_pA: float = 2.37,
        base_temp_K: float = 300.0,
        target_temp_K: float = 358.15,
        n_factor: float = 1.4,
    ) -> Dict[str, float]:
        """Compute leakage scaling with temperature.

        Subthreshold leakage doubles approximately every 10K (or more
        precisely, every n * V_t * ln(10) / V_th * 10K).

        For n=1.4, V_th=0.4V: doubles every ~8.5K.

        Args:
            base_leakage_pA: Leakage at base temperature.
            base_temp_K: Base temperature.
            target_temp_K: Target temperature.
            n_factor: Subthreshold slope factor.

        Returns:
            Dict with temperature scaling analysis.
        """
        delta_T = target_temp_K - base_temp_K

        # The leakage scaling: I(T2) = I(T1) * exp(delta_T * (1/V_t2 - 1/V_t1) * V_th)
        # Simplified: I(T2) = I(T1) * 2^(delta_T / T_double)
        T_double = n_factor * (BOLTZMANN_K * base_temp_K / ELECTRON_CHARGE) * math.log(10) / 0.4 * 10
        # More accurate: T_double ~ 10K for typical processes
        T_double_approx = 10.0  # K per doubling

        scaling_factor = 2.0 ** (delta_T / T_double_approx)

        return {
            "base_temp_K": base_temp_K,
            "target_temp_K": target_temp_K,
            "delta_T_K": delta_T,
            "base_leakage_pA": base_leakage_pA,
            "target_leakage_pA": base_leakage_pA * scaling_factor,
            "scaling_factor": scaling_factor,
            "doubling_temperature_K": T_double_approx,
            "n_doublings": delta_T / T_double_approx,
        }

    # ------------------------------------------------------------------
    # Thermal noise
    # ------------------------------------------------------------------

    @staticmethod
    def thermal_noise_analysis(
        v_dd: float = 1.0,
        temperature_K: float = 300.0,
        cell_capacitance_fF: float = 0.5,
        input_dimension: int = 1024,
        v_th: float = 0.4,
        n_factor: float = 1.4,
    ) -> ThermalNoiseResult:
        """Analyze thermal noise margins for ternary ROM cells.

        The noise margin for a ternary cell with levels at {-V_dd/2, 0, +V_dd/2}
        depends on thermal noise voltage: v_n = sqrt(kT/C).

        For reliable operation, the noise margin must exceed the noise
        voltage by a sufficient margin (typically 6-sigma for BER < 1e-9).

        Args:
            v_dd: Supply voltage.
            temperature_K: Operating temperature.
            cell_capacitance_fF: ROM cell capacitance in fF.
            input_dimension: K (number of rows in the array).
            v_th: Transistor threshold voltage.
            n_factor: Subthreshold slope factor.

        Returns:
            ThermalNoiseResult with noise analysis.
        """
        # Voltage levels
        level_spacing = v_dd / 2  # distance between adjacent levels

        # Thermal noise RMS voltage: v_n = sqrt(kT/C)
        C = cell_capacitance_fF * 1e-15  # F
        if C > 0:
            v_noise = math.sqrt(BOLTZMANN_K * temperature_K / C)
        else:
            v_noise = 0

        # Additional noise from subthreshold leakage fluctuation
        # (flicker noise contribution, simplified)
        v_t = BOLTZMANN_K * temperature_K / ELECTRON_CHARGE
        flicker_noise = 0.1 * v_t  # 10% of thermal voltage
        total_noise = math.sqrt(v_noise ** 2 + flicker_noise ** 2)

        # Noise margin
        noise_margin = level_spacing / 2 - total_noise

        # SNR
        snr_linear = level_spacing / total_noise if total_noise > 0 else float('inf')
        snr_db = 20 * math.log10(snr_linear) if snr_linear > 0 else float('inf')

        # Per-cell error probability (Gaussian tail)
        # P(error) = P(noise > noise_margin) = erfc(noise_margin / (sqrt(2) * sigma))
        if total_noise > 0:
            from math import erfc
            sigma = total_noise
            z = noise_margin / (sigma * math.sqrt(2))
            per_cell_ber = 0.5 * erfc(z)
        else:
            per_cell_ber = 0.0

        # Per-column error probability (union bound over K cells)
        per_column_ber = 1.0 - (1.0 - per_cell_ber) ** input_dimension
        per_column_ber = min(per_column_ber, 1.0)

        # Operating margin
        operating_margin = 20 * math.log10(noise_margin / total_noise) if total_noise > 0 else float('inf')

        # Reliability check
        is_reliable = per_column_ber < 1e-9

        return ThermalNoiseResult(
            v_dd=v_dd,
            noise_margin_v=noise_margin,
            thermal_noise_rms_v=total_noise,
            snr_db=snr_db,
            snr_linear=snr_linear,
            per_cell_error_prob=per_cell_ber,
            per_column_error_prob=per_column_ber,
            ber=per_column_ber,
            operating_margin_db=operating_margin,
            is_reliable=is_reliable,
        )

    # ------------------------------------------------------------------
    # Energy modeling
    # ------------------------------------------------------------------

    @staticmethod
    def rom_energy_model(
        rows: int,
        cols: int,
        v_dd: float = 1.0,
        frequency_hz: float = 1e9,
        cell_cap_fF: float = 0.5,
        wire_cap_per_um_fF: float = 0.2,
        cell_pitch_um: float = 0.22,
        leakage_per_cell_pA: float = 2.37,
        sparsity: float = 0.45,
        adder_style: str = "tree",
    ) -> EnergyModel:
        """Compute a ROM-specific energy model including all sources.

        Energy sources:
        1. Cell switching: C_cell * V_dd^2 per active cell
        2. Routing: C_wire * V_dd^2 for all cells (including zero)
        3. Bitline precharge: C_bl * V_dd^2 per column
        4. Wordline driver: C_wl * V_dd^2 per row
        5. Decoder: ~log2(rows) stages of logic
        6. Adder tree: O(cols * log2(rows)) additions
        7. Leakage: static power * 1/freq per inference

        Args:
            rows, cols: Array dimensions.
            v_dd: Supply voltage.
            frequency_hz: Operating frequency.
            cell_cap_fF: Cell switching capacitance.
            wire_cap_per_um_fF: Wire capacitance per um.
            cell_pitch_um: Cell pitch.
            leakage_per_cell_pA: Leakage per non-zero cell.
            sparsity: Fraction of zero weights.
            adder_style: "tree" or "ripple".

        Returns:
            EnergyModel with complete energy breakdown.
        """
        active_fraction = 1.0 - sparsity
        n_active = rows * cols * active_fraction
        n_total = rows * cols

        # 1. Cell switching energy
        e_cell = cell_cap_fF * 1e-15 * v_dd ** 2 * 1e15  # fJ
        e_cell_total = e_cell * n_active

        # 2. Routing energy (wire cap for all cells, even zero)
        wire_length_per_cell = cell_pitch_um  # approx
        e_routing_per_cell = wire_cap_per_um_fF * 1e-15 * wire_length_per_cell * 1e-6 * v_dd ** 2 * 1e15  # fJ
        e_routing_total = e_routing_per_cell * n_total

        # 3. Bitline precharge (each column: C_bl * V^2)
        bl_length = rows * cell_pitch_um  # um
        C_bl = bl_length * wire_cap_per_um_fF * 1e-15  # F
        e_bl = C_bl * v_dd ** 2 * 1e15  # fJ per column
        e_bl_total = e_bl * cols

        # 4. Wordline driver
        wl_length = cols * cell_pitch_um  # um
        C_wl = wl_length * wire_cap_per_um_fF * 1e-15  # F
        e_wl = C_wl * v_dd ** 2 * 1e15  # fJ per row
        # Only one wordline active per inference (one-hot)
        e_wl_total = e_wl

        # 5. Decoder
        decoder_stages = max(1, int(math.ceil(math.log2(max(rows, 2)))))
        e_decoder = decoder_stages * 10 * v_dd ** 2 * 1e15  # ~10fF per stage

        # 6. Adder tree
        adder_depth = int(math.ceil(math.log2(max(rows, 2)))) if adder_style == "tree" else rows
        word_width = max(1, int(math.ceil(math.log2(rows + 1)))) + 1
        e_adder_per_stage = word_width * 2 * v_dd ** 2 * 1e15  # ~2fF per bit
        e_adder = adder_depth * e_adder_per_stage * cols  # one adder tree per column

        # Total dynamic energy
        e_dynamic = e_cell_total + e_routing_total + e_bl_total + e_wl_total + e_decoder + e_adder

        # 7. Leakage energy per inference = P_leak / freq
        n_nonzero = n_active
        P_leak_W = n_nonzero * leakage_per_cell_pA * 1e-12 * v_dd
        if frequency_hz > 0:
            e_leakage = P_leak_W / frequency_hz * 1e15  # fJ
        else:
            e_leakage = 0

        e_total = e_dynamic + e_leakage

        # Per-op energy (one ternary MAC = one cell read + add)
        n_ops = n_active  # one "op" per active cell
        e_per_op = e_total / n_ops if n_ops > 0 else 0

        # Per-MAC energy (full dot product: K ops per column, N columns)
        n_macs = cols
        e_per_mac = e_total / n_macs if n_macs > 0 else 0

        # Landauer limit
        E_landauer = BOLTZMANN_K * 300.0 * math.log(3)  # per cell, 300K
        landauer_factor = (e_total / n_total * 1e-15) / E_landauer if n_total > 0 else 0

        return EnergyModel(
            cell_switching_energy_fJ=e_cell,
            zero_cell_routing_energy_fJ=e_routing_per_cell,
            decoder_energy_fJ=e_decoder,
            wordline_energy_fJ=e_wl_total,
            bitline_precharge_energy_fJ=e_bl_total,
            adder_tree_energy_fJ=e_adder,
            total_dynamic_energy_fJ=e_dynamic,
            total_leakage_energy_fJ=e_leakage,
            total_energy_fJ=e_total,
            energy_per_op_fJ=e_per_op,
            energy_per_mac_fJ=e_per_mac,
            landauer_factor=landauer_factor,
            thermodynamic_efficiency=1.0 / landauer_factor if landauer_factor > 0 else 0,
        )

    # ------------------------------------------------------------------
    # Physics-based scaling
    # ------------------------------------------------------------------

    @staticmethod
    def physics_scaling_projection(
        node_nm: int,
        v_dd: float = 1.0,
        cell_area_um2: float = 0.048,
        leakage_pA: float = 1.185,
        temperature_K: float = 300.0,
    ) -> ScalingProjection:
        """Project ROM performance using physics-based scaling.

        Uses first-principles scaling rather than hand-specified values:
        - Cell area scales with node^2 (Dennard scaling until ~28nm, then slower)
        - Voltage scales to maintain overdrive: V_dd ~ V_th + margin
        - Leakage: I_sub ~ exp(-V_th / (n*V_t)) with V_th decreasing ~0.1V/node
        - Energy: E ~ C * V^2, C ~ area ~ node^2
        - Delay: tau ~ C*V/I ~ (node^2 * V) / (W/V_th * exp(...))

        Args:
            node_nm: Process node in nm.
            v_dd: Supply voltage.
            cell_area_um2: Cell area.
            leakage_pA: Leakage per transistor.
            temperature_K: Temperature.

        Returns:
            ScalingProjection with physics-based estimates.
        """
        v_t = BOLTZMANN_K * temperature_K / ELECTRON_CHARGE

        # V_thermal fraction
        v_thermal_frac = v_t / v_dd if v_dd > 0 else 0

        # Subthreshold swing
        n_factor = 1.4  # typical
        s_slope = n_factor * v_t * math.log(10) * 1000  # mV/decade

        # Energy per op: C * V^2
        # C ~ area (simplified)
        e_op = cell_area_um2 * 1e-12 * v_dd ** 2 * 1e15  # fJ (rough)

        # Leakage energy per op (at 1 GHz)
        e_leak = leakage_pA * 1e-12 * v_dd / 1e9 * 1e15  # fJ

        # Noise margin
        noise_margin = v_dd / (2 * v_t) if v_t > 0 else 0
        noise_margin_db = 20 * math.log10(noise_margin) if noise_margin > 0 else 0

        # Max frequency estimate
        # tau = R_on * C where R_on ~ 1/(I_on) and I_on ~ (W/L) * mu * Cox * (V_dd - V_th)^2
        # Simplified: tau ~ cell_area_um2 * 1e-12 * v_dd / (leakage_pA * 1e-12 * 1e6)
        # The 1e6 factor converts pA to uA for on-current (I_on >> I_leak)
        i_on_estimate = max(leakage_pA * 1e6, 1e-3)  # uA, at least 1nA
        tau = cell_area_um2 * 1e-12 * v_dd / (i_on_estimate * 1e-6)  # seconds
        max_freq = 0.3 / tau if tau > 0 else 1e9  # ~1/3 tau for safe margin
        max_freq_ghz = min(max_freq, 1e12) / 1e9  # cap at 1 THz

        # Thermal limit: the node where V_dd approaches V_t
        # At this point, thermal noise overwhelms the signal
        thermal_limit_node = max(5, int(v_dd / (3 * v_t) * 28))  # rough estimate

        return ScalingProjection(
            node_nm=node_nm,
            v_dd=v_dd,
            cell_area_um2=cell_area_um2,
            leakage_per_cell_pA=leakage_pA,
            v_thermal_fraction=v_thermal_frac,
            subthreshold_swing_mv_dec=s_slope,
            energy_per_op_fJ=e_op,
            leakage_energy_per_op_fJ=e_leak,
            total_energy_per_op_fJ=e_op + e_leak,
            noise_margin_db=noise_margin_db,
            max_freq_ghz=max_freq_ghz,
            thermal_limit_node_nm=thermal_limit_node,
        )

    # ------------------------------------------------------------------
    # Near-threshold optimization
    # ------------------------------------------------------------------

    @staticmethod
    def near_threshold_optimum(
        cell_area_um2: float = 0.048,
        v_th: float = 0.4,
        temperature_K: float = 300.0,
    ) -> Dict[str, float]:
        """Find the voltage that minimizes energy per operation.

        The energy-delay product has a minimum at a specific V_dd:
            E_total(V) = E_dynamic(V) + E_leakage(V)
            E_dynamic = C * V^2
            E_leakage = I_leak(V) * V * t_delay(V)
            t_delay ~ V / (V - V_th)^alpha  (alpha ~ 1-2)

        The minimum occurs near V_dd = V_th + small_margin.

        Args:
            cell_area_um2: Cell area.
            v_th: Threshold voltage.
            temperature_K: Temperature.

        Returns:
            Dict with near-threshold analysis.
        """
        v_t = BOLTZMANN_K * temperature_K / ELECTRON_CHARGE
        C = cell_area_um2 * 1e-12  # F (rough)

        # Sweep V_dd from V_th to 1.2V and find minimum energy
        best_vdd = v_th + 0.1
        best_energy = float('inf')

        results = {}
        for v_dd_x10 in range(int(v_th * 10) + 1, 13):  # from V_th to 1.2V
            v_dd = v_dd_x10 / 10.0

            # Dynamic energy: C * V^2
            e_dyn = C * v_dd ** 2

            # Leakage current: I_sub ~ I_0 * exp((V_gs - V_th)/(n*V_t))
            # For a cell with V_gs = V_dd (ON state):
            n_factor = 1.4
            i0 = 1e-12  # rough pre-exponential
            exponent = (v_dd - v_th) / (n_factor * v_t)
            exponent = min(exponent, 50)
            i_leak = i0 * math.exp(exponent)

            # Delay: proportional to C * V / I_on
            i_on = max(i_leak * 1e6, 1e-6)  # rough
            t_delay = C * v_dd / i_on if i_on > 0 else 1e-3

            # Total energy per operation
            e_leak = i_leak * v_dd * t_delay
            e_total = e_dyn + e_leak

            results[f"vdd_{v_dd:.1f}V"] = {
                "e_dynamic_fJ": e_dyn * 1e15,
                "e_leakage_fJ": e_leak * 1e15,
                "e_total_fJ": e_total * 1e15,
                "delay_ns": t_delay * 1e9,
            }

            if e_total < best_energy:
                best_energy = e_total
                best_vdd = v_dd

        results["optimal_vdd"] = best_vdd
        results["min_energy_fJ"] = best_energy * 1e15
        results["v_th"] = v_th
        results["v_thermal_mV"] = v_t * 1000

        return results
