"""Coding-theoretic foundations for ternary ROM fault tolerance.

Covers error-correcting codes for ROM stuck-at faults, ternary
code constructions, fault-tolerant weight storage, Manhattan-distance
error detection, and yield modeling with defect tolerance.

Key theoretical results:
- For ternary ROM cells, stuck-at faults can be: +1->0, -1->0 (open),
  0->+1, 0->-1 (short), or +/-1 swap (threshold shift).
- Ternary BCH codes over GF(3) provide multi-error correction.
- The ternary Golay code [11, 6, 5]_3 can correct 2 trit errors.
- A ternary Hamming code over GF(3) has n = (3^m - 1)/2 for m >= 2.
- For ROM defect tolerance, the key metric is accuracy impact per defect,
  not functional failure: a single defective cell changes the weight
  by alpha, causing relative error ~1/sqrt(K) per output.

References:
  MacWilliams, F.J. & Sloane, N.J.A. (1977). The Theory of Error-Correcting Codes.
  Hamming, R.W. (1950). "Error Detecting and Error Correcting Codes." Bell Sys. Tech. J.
  Berlekamp, E.R. (1968). Algebraic Coding Theory. McGraw-Hill.
"""

import numpy as np
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class FaultModel:
    """Statistical model of ROM cell fault types and rates."""
    n_cells: int
    stuck_at_plus_rate: float    # P(cell stuck at +1)
    stuck_at_minus_rate: float   # P(cell stuck at -1)
    stuck_at_zero_rate: float    # P(cell stuck at 0)
    open_circuit_rate: float     # P(+/-1 cell becomes unconnected -> reads as 0)
    short_circuit_rate: float    # P(0 cell shorts to VDD or VSS)
    threshold_shift_rate: float  # P(cell threshold shifts, causing misread)
    overall_defect_rate: float   # P(any defect per cell)


@dataclass
class CodeCapability:
    """Capability of an error-correcting code."""
    name: str
    n: int                      # code length (trits)
    k: int                      # information trits
    d: int                      # minimum Hamming distance
    t: int                      # maximum correctable errors
    rate: float                 # k/n
    overhead_percent: float     # (n-k)/k * 100
    detection_capability: int   # maximum detectable errors


@dataclass
class DefectToleranceAnalysis:
    """Analysis of defect tolerance for a ternary ROM array."""
    bare_die_yield: float         # standard Poisson yield
    fault_tolerance_yield: float  # yield with <threshold accuracy loss
    yield_improvement: float      # relative improvement
    expected_accuracy_loss_per_defect: float  # avg accuracy loss per single defect
    critical_defect_fraction: float  # fraction of defects that are accuracy-critical
    optimal_code: Optional[str]  # recommended ECC if any
    redundancy_overhead: float   # area overhead for ECC


@dataclass
class TernaryCodeWord:
    """A ternary codeword over GF(3)."""
    symbols: np.ndarray  # array of values in {0, 1, 2} representing {-1, 0, +1}


# ============================================================================
# CodingTheory — main class
# ============================================================================

class CodingTheory:
    """Coding-theoretic tools for ternary ROM fault tolerance.

    Provides fault modeling, ternary ECC construction, defect
    tolerance analysis, and yield modeling for mask-programmed ROM.
    """

    # Ternary field GF(3) arithmetic
    GF3_MOD = 3

    # ------------------------------------------------------------------
    # GF(3) arithmetic
    # ------------------------------------------------------------------

    @staticmethod
    def gf3_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Addition in GF(3) (mod 3)."""
        return (np.asarray(a) + np.asarray(b)) % CodingTheory.GF3_MOD

    @staticmethod
    def gf3_mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Multiplication in GF(3) (mod 3)."""
        return (np.asarray(a) * np.asarray(b)) % CodingTheory.GF3_MOD

    @staticmethod
    def gf3_inv(a: int) -> int:
        """Multiplicative inverse in GF(3)."""
        a = a % 3
        if a == 0:
            raise ZeroDivisionError("0 has no inverse in GF(3)")
        return a  # 1^-1 = 1, 2^-1 = 2 in GF(3)

    @staticmethod
    def gf3_sub(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Subtraction in GF(3) (mod 3)."""
        return (np.asarray(a) - np.asarray(b)) % CodingTheory.GF3_MOD

    # ------------------------------------------------------------------
    # Ternary <-> GF(3) mapping
    # ------------------------------------------------------------------

    @staticmethod
    def ternary_to_gf3(ternary: np.ndarray) -> np.ndarray:
        """Map {-1, 0, +1} to GF(3) elements {2, 0, 1}."""
        w = np.asarray(ternary, dtype=np.int8)
        lookup = np.array([2, 0, 1], dtype=np.int8)  # index by (w + 1)
        return lookup[w + 1]

    @staticmethod
    def gf3_to_ternary(gf3: np.ndarray) -> np.ndarray:
        """Map GF(3) elements {0, 1, 2} back to {-1, 0, +1}."""
        g = np.asarray(gf3, dtype=np.int8) % 3
        lookup = np.array([0, 1, -1, 0], dtype=np.int8)  # index 0,1,2,3
        return lookup[g]

    # ------------------------------------------------------------------
    # Ternary Hamming distance
    # ------------------------------------------------------------------

    @staticmethod
    def ternary_hamming_distance(a: np.ndarray, b: np.ndarray) -> int:
        """Compute Hamming distance between two ternary vectors."""
        a = np.asarray(a).ravel()
        b = np.asarray(b).ravel()
        return int(np.sum(a != b))

    @staticmethod
    def ternary_hamming_weight(a: np.ndarray) -> int:
        """Compute Hamming weight (number of non-zero elements)."""
        return int(np.sum(np.asarray(a) != 0))

    # ------------------------------------------------------------------
    # Ternary Hamming code
    # ------------------------------------------------------------------

    @staticmethod
    def ternary_hamming_code(m: int = 3) -> CodeCapability:
        """Compute parameters of a ternary Hamming code.

        A ternary Hamming code over GF(3) has parameters:
            n = (3^m - 1) / 2
            k = n - m
            d = 3

        It can correct 1 trit error and detect 2.

        Args:
            m: Redundancy parameter (m >= 2).

        Returns:
            CodeCapability describing the code.
        """
        n = (3 ** m - 1) // 2
        k = n - m
        d = 3
        t = (d - 1) // 2  # = 1

        return CodeCapability(
            name=f"Ternary Hamming [{n}, {k}, {d}]_3",
            n=n, k=k, d=d, t=t,
            rate=k / n,
            overhead_percent=(n - k) / k * 100,
            detection_capability=d - 1,  # 2
        )

    @staticmethod
    def ternary_golay_code() -> CodeCapability:
        """Return parameters of the perfect ternary Golay code.

        The ternary Golay code [11, 6, 5]_3 is a perfect code
        that can correct 2 trit errors with 5 trits of redundancy.

        Returns:
            CodeCapability describing the Golay code.
        """
        return CodeCapability(
            name="Ternary Golay [11, 6, 5]_3",
            n=11, k=6, d=5, t=2,
            rate=6 / 11,
            overhead_percent=(11 - 6) / 6 * 100,
            detection_capability=4,
        )

    @staticmethod
    def ternary_repetition_code(k: int = 1, t: int = 1) -> CodeCapability:
        """Design a ternary repetition code for t-error correction.

        A repetition code repeats each trit (2t+1) times and takes
        majority vote. Parameters: [n = k*(2t+1), k, d = 2t+1]_3.

        Args:
            k: Information trits per codeword.
            t: Number of errors to correct.

        Returns:
            CodeCapability describing the repetition code.
        """
        n = k * (2 * t + 1)
        d = 2 * t + 1
        return CodeCapability(
            name=f"Ternary Repetition [{n}, {k}, {d}]_3",
            n=n, k=k, d=d, t=t,
            rate=k / n,
            overhead_percent=(n - k) / k * 100,
            detection_capability=2 * t,
        )

    # ------------------------------------------------------------------
    # Fault modeling
    # ------------------------------------------------------------------

    @staticmethod
    def rom_fault_model(
        defect_density_per_cm2: float = 0.1,
        cell_area_um2: float = 0.048,
        temperature_kelvin: float = 300.0,
    ) -> FaultModel:
        """Create a statistical fault model for ROM cells.

        Uses Poisson defect statistics calibrated to typical
        semiconductor manufacturing defect densities.

        Args:
            defect_density_per_cm2: Manufacturing defect density (D0).
            cell_area_um2: ROM cell area in square micrometers.
            temperature_kelvin: Operating temperature (affects threshold shift rate).

        Returns:
            FaultModel with per-cell fault probabilities.
        """
        cell_area_cm2 = cell_area_um2 * 1e-8  # um^2 to cm^2

        # Base defect probability (Poisson: P(defect) = 1 - exp(-D0 * A))
        p_defect = 1.0 - math.exp(-defect_density_per_cm2 * cell_area_cm2)

        # Temperature-dependent threshold shift
        # Threshold voltage decreases ~2mV/K from 25C
        temp_factor = max(0.1, 1.0 - (temperature_kelvin - 298.15) * 0.002)

        # Fault type distribution (based on ROM physics):
        # - Open circuit: ~40% (broken contact/via)
        # - Stuck-at fault: ~30% (contamination, particle)
        # - Short circuit: ~15% (bridging defect)
        # - Threshold shift: ~15% (dopant fluctuation, NBTI)
        open_rate = 0.40 * p_defect
        stuck_rate = 0.30 * p_defect
        short_rate = 0.15 * p_defect
        threshold_rate = 0.15 * p_defect * (2.0 - temp_factor)

        # For stuck-at faults, +1 and -1 are equally likely
        stuck_plus = stuck_rate / 2
        stuck_minus = stuck_rate / 2

        overall = open_rate + stuck_plus + stuck_minus + short_rate + threshold_rate

        return FaultModel(
            n_cells=0,  # filled by caller
            stuck_at_plus_rate=stuck_plus,
            stuck_at_minus_rate=stuck_minus,
            stuck_at_zero_rate=0.0,  # 0 cells can't be stuck at zero
            open_circuit_rate=open_rate,
            short_circuit_rate=short_rate,
            threshold_shift_rate=threshold_rate,
            overall_defect_rate=min(overall, 1.0),
        )

    # ------------------------------------------------------------------
    # Defect tolerance analysis
    # ------------------------------------------------------------------

    @staticmethod
    def defect_tolerance_analysis(
        rows: int,
        cols: int,
        defect_density_per_cm2: float = 0.1,
        cell_area_um2: float = 0.048,
        input_dimension: int = 0,
        accuracy_threshold: float = 0.01,
        temperature_kelvin: float = 300.0,
    ) -> DefectToleranceAnalysis:
        """Analyze the defect tolerance of a ternary ROM array.

        Key insight: a single defective cell changes one weight by at most
        alpha (the quantization scale). For a layer with K inputs,
        the relative output error is alpha / (alpha * sqrt(K)) = 1/sqrt(K).
        This means ternary ROM is *intrinsically* fault-tolerant for
        large input dimensions.

        Args:
            rows, cols: ROM array dimensions.
            defect_density_per_cm2: Manufacturing defect density.
            cell_area_um2: Cell area.
            input_dimension: If 0, uses rows (assumes square MAC).
            accuracy_threshold: Maximum tolerable accuracy loss (e.g., 0.01 = 1%).
            temperature_kelvin: Operating temperature.

        Returns:
            DefectToleranceAnalysis with yield and tolerance metrics.
        """
        if input_dimension == 0:
            input_dimension = rows

        K = input_dimension
        N = rows * cols
        die_area_cm2 = N * cell_area_um2 * 1e-8

        # Standard Poisson yield
        bare_yield = math.exp(-defect_density_per_cm2 * die_area_cm2)

        # Fault model
        fm = CodingTheory.rom_fault_model(defect_density_per_cm2, cell_area_um2, temperature_kelvin)
        fm = FaultModel(
            n_cells=N, stuck_at_plus_rate=fm.stuck_at_plus_rate,
            stuck_at_minus_rate=fm.stuck_at_minus_rate,
            stuck_at_zero_rate=fm.stuck_at_zero_rate,
            open_circuit_rate=fm.open_circuit_rate,
            short_circuit_rate=fm.short_circuit_rate,
            threshold_shift_rate=fm.threshold_shift_rate,
            overall_defect_rate=fm.overall_defect_rate,
        )

        # Expected number of defects
        n_defects_expected = N * fm.overall_defect_rate

        # Accuracy impact per defect
        # Single weight error of magnitude alpha in a K-input accumulation:
        # relative error ~ 1/sqrt(K) (by CLT, the output has std ~ sqrt(K))
        per_defect_accuracy_loss = 1.0 / math.sqrt(K) if K > 0 else 1.0

        # Expected total accuracy loss from all defects
        # For independent defects, variance adds: total_loss ~ sqrt(n_defects) * per_defect_loss
        expected_total_loss = math.sqrt(n_defects_expected) * per_defect_accuracy_loss

        # Fault-tolerant yield: fraction of dies where accuracy loss < threshold
        # Using Gaussian approximation for the sum of defects
        if per_defect_accuracy_loss > 0:
            # Number of defects that would cause threshold loss:
            n_critical = (accuracy_threshold / per_defect_accuracy_loss) ** 2
            # P(n_defects <= n_critical) = sum_{k=0}^{n_critical} Poisson(lambda, k)
            lam = n_defects_expected
            if lam > 0:
                n_crit_int = min(int(math.ceil(n_critical)), N)
                p_acceptable = sum(
                    (lam ** k) * math.exp(-lam) / math.factorial(k)
                    for k in range(n_crit_int + 1)
                )
                # Cap at Poisson sum for very large n
                if n_crit_int >= N:
                    p_acceptable = 1.0
            else:
                p_acceptable = 1.0
        else:
            p_acceptable = bare_yield

        # Yield improvement
        yield_improvement = p_acceptable / bare_yield if bare_yield > 0 else 1.0

        # Fraction of defects that are accuracy-critical
        # (defects that cause accuracy loss > threshold / n_defects_expected)
        if n_defects_expected > 0:
            critical_defect_fraction = min(1.0, n_critical / n_defects_expected)
        else:
            critical_defect_fraction = 0.0

        # Recommend ECC if needed
        optimal_code = None
        redundancy_overhead = 0.0
        if expected_total_loss > accuracy_threshold:
            # Need error correction
            # Choose based on how many errors we expect
            t_needed = int(math.ceil(math.sqrt(n_defects_expected)))
            if t_needed <= 2:
                code = CodingTheory.ternary_golay_code()
                optimal_code = code.name
                redundancy_overhead = code.overhead_percent
            elif t_needed <= 5:
                code = CodingTheory.ternary_repetition_code(k=1, t=t_needed)
                optimal_code = code.name
                redundancy_overhead = code.overhead_percent

        return DefectToleranceAnalysis(
            bare_die_yield=bare_yield,
            fault_tolerance_yield=p_acceptable,
            yield_improvement=yield_improvement,
            expected_accuracy_loss_per_defect=per_defect_accuracy_loss,
            critical_defect_fraction=critical_defect_fraction,
            optimal_code=optimal_code,
            redundancy_overhead=redundancy_overhead,
        )

    # ------------------------------------------------------------------
    # Manhattan distance error detection
    # ------------------------------------------------------------------

    @staticmethod
    def manhattan_error_detect(
        weights: np.ndarray,
        row_parities: Optional[np.ndarray] = None,
        col_parities: Optional[np.ndarray] = None,
    ) -> Dict[str, object]:
        """Detect errors using Manhattan-distance parity checks.

        For a ternary matrix, the Manhattan distance (L1 norm) of
        each row and column provides a lightweight error detection
        mechanism. A single-cell error changes exactly one row parity
        and one column parity, pinpointing the error location.

        Args:
            weights: 2-D ternary weight matrix.
            row_parities: Precomputed row parities (optional, for stored checksum).
            col_parities: Precomputed column parities (optional).

        Returns:
            Dict with detection results.
        """
        w = np.asarray(weights, dtype=np.int8)
        if w.ndim != 2:
            w = w.reshape(1, -1)

        # Compute current parities
        current_row_parity = np.sum(np.abs(w), axis=1)
        current_col_parity = np.sum(np.abs(w), axis=0)

        detected_errors = []

        if row_parities is not None:
            row_diff = current_row_parity - np.asarray(row_parities)
            error_rows = np.where(row_diff != 0)[0]
            detected_errors.extend([("row", int(r), int(row_diff[r])) for r in error_rows])

        if col_parities is not None:
            col_diff = current_col_parity - np.asarray(col_parities)
            error_cols = np.where(col_diff != 0)[0]
            detected_errors.extend([("col", int(c), int(col_diff[c])) for c in error_cols])

        # Cross-reference row and column errors to locate the defective cell
        error_locations = []
        row_errors = {r for loc, r, d in detected_errors if loc == "row"}
        col_errors = {c for loc, c, d in detected_errors if loc == "col"}
        for r in row_errors:
            for c in col_errors:
                error_locations.append((int(r), int(c)))

        return {
            "n_rows": w.shape[0],
            "n_cols": w.shape[1],
            "row_parities": current_row_parity.tolist(),
            "col_parities": current_col_parity.tolist(),
            "n_detected_errors": len(detected_errors),
            "error_details": detected_errors,
            "localized_cells": error_locations,
            "parity_overhead_bits": w.shape[0] + w.shape[1],  # row + col parities
            "parity_overhead_percent": (w.shape[0] + w.shape[1]) / (w.shape[0] * w.shape[1]) * 100,
        }

    # ------------------------------------------------------------------
    # Yield modeling
    # ------------------------------------------------------------------

    @staticmethod
    def fault_tolerant_yield(
        die_area_mm2: float,
        defect_density_per_cm2: float = 0.1,
        accuracy_threshold: float = 0.01,
        input_dimension: int = 1024,
        cell_area_um2: float = 0.048,
    ) -> Dict[str, float]:
        """Compute fault-tolerant yield for a ternary ROM die.

        Compares standard Poisson yield against fault-tolerant yield
        where "functional" means "accuracy loss < threshold."

        Args:
            die_area_mm2: Total die area.
            defect_density_per_cm2: Manufacturing defect density.
            accuracy_threshold: Maximum tolerable accuracy degradation.
            input_dimension: Typical layer input dimension.
            cell_area_um2: ROM cell area.

        Returns:
            Dict with yield comparison and economic impact.
        """
        die_area_cm2 = die_area_mm2 * 0.01  # mm^2 to cm^2

        # Standard Poisson yield
        poisson_yield = math.exp(-defect_density_per_cm2 * die_area_cm2)

        # Fault-tolerant yield (uses the key insight that a defect
        # in the ROM array causes ~1/sqrt(K) accuracy loss, not failure)
        n_cells_approx = die_area_mm2 * 1e6 / cell_area_um2  # rough estimate
        per_defect_loss = 1.0 / math.sqrt(input_dimension)

        # Expected defects
        lambda_defects = defect_density_per_cm2 * die_area_cm2

        # Maximum tolerable defects
        if per_defect_loss > 0:
            max_defects = (accuracy_threshold / per_defect_loss) ** 2
        else:
            max_defects = lambda_defects

        # Fault-tolerant yield = P(n_defects <= max_defects)
        # Using Poisson CDF
        ft_yield = sum(
            (lambda_defects ** k) * math.exp(-lambda_defects) / math.factorial(k)
            for k in range(int(max_defects) + 1)
        )
        ft_yield = min(ft_yield, 1.0)

        # Economic impact
        yield_improvement = ft_yield / poisson_yield if poisson_yield > 0 else 1.0
        cost_savings_percent = (1 - 1 / yield_improvement) * 100

        return {
            "die_area_mm2": die_area_mm2,
            "die_area_cm2": die_area_cm2,
            "poisson_yield": poisson_yield,
            "fault_tolerant_yield": ft_yield,
            "yield_improvement_factor": yield_improvement,
            "cost_savings_percent": max(0, cost_savings_percent),
            "expected_defects": lambda_defects,
            "max_tolerable_defects": max_defects,
            "per_defect_accuracy_loss": per_defect_loss,
        }
