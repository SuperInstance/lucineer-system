"""Stochastic process and random matrix theory for ternary ROM systems.

Covers spectral properties of ternary weight matrices, Marchenko-Pastur
distribution analysis, concentration inequalities for ternary sums,
random walk on ternary lattices, and noise propagation models.

Key theoretical results:
- The limiting spectral distribution of random ternary matrices
  W in {-1,0,+1}^{m x n} with i.i.d. entries follows a modified
  Marchenko-Pastur law scaled by the Bernoulli(2p/3) non-zero fraction.
- Hoeffding's inequality for ternary: P(|sum X_i - E[sum]| > t)
  <= 2*exp(-2*t^2 / (n * a^2)) where |X_i| <= a = 1.
- Bernstein's inequality for bounded variables accounts for variance.
- Berry-Esseen theorem gives convergence rate to CLT: O(1/sqrt(n)).
- For the column sum (MAC output), the CLT gives Gaussian approximation
  with sigma^2 = n * Var(X) where X ~ {(-1, p_-), (0, p_0), (+1, p_+)}.

References:
  Marchenko, V.A. & Pastur, L.A. (1967). "Distribution of eigenvalues
    for some sets of random matrices."
  Vershynin, R. (2018). High-Dimensional Probability. Cambridge UP.
  Tao, T. (2012). Topics in Random Matrix Theory. AMS.
  Wigner, E.P. (1958). "On the distribution of the roots of certain
    symmetric matrices."
"""

import numpy as np
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class SpectralProfile:
    """Spectral analysis of a ternary weight matrix."""
    rows: int
    cols: int
    eigenvalues: np.ndarray         # eigenvalues of W^T W / n or W W^T / m
    top_eigenvalue: float
    spectral_radius: float
    spectral_norm: float            # = max singular value
    trace: float
    determinant: float
    rank: int
    effective_rank: float           # (trace)^2 / trace(A^2) [effective degrees of freedom]
    condition_number: float
    singular_values: np.ndarray     # top-k singular values
    top_k_energy_fraction: float    # energy in top-k singular values
    marchenko_pastur_conformity: float  # 0-1, how well spectra match MP
    mp_ratio: float                 # m/n aspect ratio


@dataclass
class ConcentrationBounds:
    """Concentration inequality bounds for ternary accumulation."""
    n: int                          # number of summands
    expected_sum: float             # E[sum X_i]
    variance: float                 # Var(sum X_i)
    std_dev: float
    p_plus: float                   # P(X = +1)
    p_minus: float                  # P(X = -1)
    p_zero: float                   # P(X = 0)
    hoeffding_bound: float          # P(|S - E[S]| > t) <= this
    bernstein_bound: float          # P(|S - E[S]| > t) <= this
    chernoff_bound: float           # P(|S - E[S]| > t) <= this (Gaussian approx)
    berry_essen_rate: float         # rate of CLT convergence
    clt_quality: str                # "excellent" / "good" / "moderate" / "poor"
    dynamic_range_bits: int         # bits needed for full range
    gauss_approx_bits: int          # bits needed for 6-sigma coverage


@dataclass
class ErrorPropagationResult:
    """Error propagation analysis through a network of ternary layers."""
    per_layer_error_var: List[float]  # variance of quantization error per layer
    end_to_end_error_var: float
    end_to_end_error_std: float
    error_amplification_factor: float  # ratio of output to input error
    worst_case_error: float
    clt_bound_3sigma: float
    clt_bound_6sigma: float
    jacobian_spectral_norm: float   # max singular value of average Jacobian
    is_stable: bool                 # whether error propagation is stable


@dataclass
class RandomMatrixPrediction:
    """Predictions from random matrix theory for a ternary matrix ensemble."""
    mp_upper_edge: float           # Marchenko-Pastur upper edge lambda+
    mp_lower_edge: float           # Marchenko-Pastur lower edge lambda-
    mp_peak: float                 # Location of MP distribution peak
    bulk_eigenvalue_count: int     # Expected number of "bulk" eigenvalues
    outlier_threshold: float       # Baik-Ben Arous-Peche threshold
    expected_top_eigenvalue: float # Tracy-Widom expected top eigenvalue
    expected_spectral_radius: float
    expected_condition_number: float
    expected_rank_efficiency: float


# ============================================================================
# StochasticProcesses — main class
# ============================================================================

class StochasticProcesses:
    """Stochastic process and random matrix theory for ternary ROM.

    Provides spectral analysis, concentration bounds, error propagation
    modeling, and random matrix theory predictions for ternary weight
    matrices.
    """

    # ------------------------------------------------------------------
    # Spectral analysis
    # ------------------------------------------------------------------

    @staticmethod
    def spectral_profile(
        weights: np.ndarray,
        top_k: int = 10,
    ) -> SpectralProfile:
        """Compute the full spectral profile of a ternary weight matrix.

        Analyzes singular values, eigenvalues, effective rank, condition
        number, and conformity to the Marchenko-Pastur distribution.

        Args:
            weights: 2-D weight matrix (ternary or full-precision).
            top_k: Number of top singular values to track.

        Returns:
            SpectralProfile with complete spectral analysis.
        """
        W = np.asarray(weights, dtype=np.float64)
        m, n = W.shape

        # Singular value decomposition (thin SVD for efficiency)
        if m >= n:
            # W = U S V^T, S has min(m,n) values
            s = np.linalg.svd(W, compute_uv=False)
        else:
            # Compute via W^T for efficiency
            s = np.linalg.svd(W.T, compute_uv=False)

        # Eigenvalues of the covariance matrix W^T W / m (or W W^T / n)
        aspect = n / m
        if m >= n:
            eigenvalues = s ** 2 / m
        else:
            eigenvalues = s ** 2 / n

        top_sv = s[0] if len(s) > 0 else 0.0
        spectral_radius = float(top_sv)

        # Effective rank: (tr(W^T W))^2 / tr((W^T W)^2)
        s2 = s ** 2
        trace_wtw = float(np.sum(s2))
        trace_wtw2 = float(np.sum(s2 ** 2))
        eff_rank = (trace_wtw ** 2 / trace_wtw2) if trace_wtw2 > 0 else 0.0

        # Condition number
        s_positive = s[s > 1e-10]
        cond_number = float(s_positive[0] / s_positive[-1]) if len(s_positive) > 1 else float('inf')

        # Top-k energy fraction
        k = min(top_k, len(s))
        top_k_energy = float(np.sum(s2[:k])) if k > 0 else 0.0
        total_energy = trace_wtw
        top_k_frac = top_k_energy / total_energy if total_energy > 0 else 1.0

        # Marchenko-Pastur conformity
        # For a random matrix with i.i.d. entries, eigenvalues of W^T W/n
        # follow the Marchenko-Pastur law
        mp_conformity = StochasticProcesses._mp_conformity(eigenvalues, aspect)

        # Rank (numerical)
        rank = int(np.sum(s > 1e-10 * top_sv)) if top_sv > 0 else 0

        return SpectralProfile(
            rows=m, cols=n,
            eigenvalues=eigenvalues,
            top_eigenvalue=float(eigenvalues[0]) if len(eigenvalues) > 0 else 0.0,
            spectral_radius=spectral_radius,
            spectral_norm=spectral_radius,
            trace=trace_wtw,
            determinant=float(np.prod(s2)) if len(s2) > 0 and len(s2) <= 100 else 0.0,
            rank=rank,
            effective_rank=eff_rank,
            condition_number=cond_number,
            singular_values=s[:k],
            top_k_energy_fraction=top_k_frac,
            marchenko_pastur_conformity=mp_conformity,
            mp_ratio=aspect,
        )

    @staticmethod
    def _mp_conformity(eigenvalues: np.ndarray, aspect_ratio: float) -> float:
        """Measure how well the eigenvalue distribution matches Marchenko-Pastur.

        Uses the Kolmogorov-Smirnov statistic between the empirical CDF
        and the theoretical MP CDF.

        Args:
            eigenvalues: Observed eigenvalues.
            aspect_ratio: n/m (columns / rows).

        Returns:
            Conformity score in [0, 1], higher = better match.
        """
        if len(eigenvalues) < 5:
            return 0.0

        gamma = min(aspect_ratio, 1.0 / aspect_ratio)  # use the smaller
        gamma = min(gamma, 1.0)

        # MP distribution edges
        lambda_plus = (1 + math.sqrt(gamma)) ** 2
        lambda_minus = max(0, (1 - math.sqrt(gamma)) ** 2)

        # Empirical CDF
        ev_sorted = np.sort(eigenvalues)
        n = len(ev_sorted)
        emp_cdf = np.arange(1, n + 1) / n

        # Theoretical CDF (Marchenko-Pastur)
        def mp_cdf(x):
            if x <= lambda_minus:
                return 0.0
            if x >= lambda_plus:
                return 1.0
            # MP CDF: F(x) = integral of MP density from lambda- to x
            # MP density: f(x) = sqrt((lambda+ - x)(x - lambda-)) / (2*pi*gamma*x)
            # CDF has no closed form — approximate via numerical integration
            # Use the simple approximation
            return min(1.0, max(0.0,
                (x - lambda_minus) / (lambda_plus - lambda_minus)
            ))

        # KS statistic
        max_ks = 0.0
        for i, x in enumerate(ev_sorted):
            theoretical_cdf = mp_cdf(x)
            ks = abs(emp_cdf[i] - theoretical_cdf)
            max_ks = max(max_ks, ks)

        # Convert to conformity: 1 - KS
        return max(0.0, 1.0 - max_ks)

    # ------------------------------------------------------------------
    # Concentration inequalities
    # ------------------------------------------------------------------

    @staticmethod
    def concentration_bounds(
        ternary_weights: np.ndarray,
        confidence_t: float = 0.0,
    ) -> ConcentrationBounds:
        """Compute concentration inequality bounds for ternary accumulation.

        For a column of ternary weights X_i in {-1, 0, +1}, the sum
        S = sum(X_i) is a random variable. This computes multiple
        bounds on P(|S - E[S]| > t) using Hoeffding, Bernstein,
        and Berry-Esseen theorems.

        Args:
            ternary_weights: 1-D array of ternary weights.
            confidence_t: The deviation threshold t. If 0, uses 2*std.

        Returns:
            ConcentrationBounds with multiple bound estimates.
        """
        w = np.asarray(ternary_weights, dtype=np.int8).ravel()
        n = len(w)

        if n == 0:
            return ConcentrationBounds(
                n=0, expected_sum=0, variance=0, std_dev=0,
                p_plus=0, p_minus=0, p_zero=1,
                hoeffding_bound=0, bernstein_bound=0, chernoff_bound=0,
                berry_esssen_rate=0, clt_quality="unknown",
                dynamic_range_bits=0, gauss_approx_bits=0,
            )

        # Distribution parameters
        counts = np.bincount(w + 1, minlength=3).astype(float)
        p_plus = float(counts[2] / n)
        p_minus = float(counts[0] / n)
        p_zero = float(counts[1] / n)

        # Moments
        E_X = p_plus - p_minus
        E_X2 = p_plus + p_minus  # E[X^2] = P(|X|=1)
        var_X = E_X2 - E_X ** 2
        E_X3 = p_plus - p_minus  # E[X^3] = E[X] for ternary
        abs_m3 = p_plus + p_minus  # E[|X - E[X]|^3]

        E_S = n * E_X
        var_S = n * var_X
        std_S = math.sqrt(var_S) if var_S > 0 else 0.0

        if confidence_t <= 0:
            confidence_t = 2.0 * std_S

        t = confidence_t

        # Hoeffding's inequality: P(|S - E[S]| > t) <= 2*exp(-2*t^2 / (n * (b-a)^2))
        # For ternary in [-1, 1]: a=-1, b=1, (b-a)^2 = 4
        hoeffding = 2.0 * math.exp(-2.0 * t ** 2 / (n * 4.0))

        # Bernstein's inequality: P(|S - E[S]| > t) <= 2*exp(-t^2 / (2*n*var + 2*t/3))
        bernstein = 2.0 * math.exp(-t ** 2 / (2 * n * var_X + 2 * t / 3)) if (2 * n * var_X + 2 * t / 3) > 0 else 0.0

        # Chernoff (Gaussian approximation): P(|S - E[S]| > t) <= 2*exp(-t^2 / (2*var_S))
        if var_S > 0:
            chernoff = 2.0 * math.exp(-t ** 2 / (2 * var_S))
        else:
            chernoff = 0.0

        # Berry-Esseen rate: sup |F_n(x) - Phi(x)| <= C * E[|X|^3] / (sigma^3 * sqrt(n))
        if var_X > 0:
            be_rate = abs_m3 / (var_X ** 1.5 * math.sqrt(n))
            be_rate = min(be_rate, 0.4748)  # Berry-Esseen constant for independent
        else:
            be_rate = 1.0

        # CLT quality assessment
        if be_rate < 0.01:
            quality = "excellent"
        elif be_rate < 0.05:
            quality = "good"
        elif be_rate < 0.15:
            quality = "moderate"
        else:
            quality = "poor"

        # Dynamic range: max sum = n, min sum = -n
        max_abs_sum = int(np.sum(np.abs(w)))
        dynamic_range_bits = int(math.ceil(math.log2(max_abs_sum + 1))) + 1 if max_abs_sum > 0 else 1

        # Gaussian approximation: 6-sigma coverage
        gauss_bits = int(math.ceil(math.log2(6 * std_S + 1))) + 1 if std_S > 0 else dynamic_range_bits

        return ConcentrationBounds(
            n=n,
            expected_sum=E_S,
            variance=var_S,
            std_dev=std_S,
            p_plus=p_plus,
            p_minus=p_minus,
            p_zero=p_zero,
            hoeffding_bound=hoeffding,
            bernstein_bound=bernstein,
            chernoff_bound=chernoff,
            berry_essen_rate=be_rate,
            clt_quality=quality,
            dynamic_range_bits=dynamic_range_bits,
            gauss_approx_bits=gauss_bits,
        )

    # ------------------------------------------------------------------
    # Error propagation
    # ------------------------------------------------------------------

    @staticmethod
    def error_propagation(
        layer_jacobians: List[np.ndarray],
        per_layer_error_var: Optional[List[float]] = None,
    ) -> ErrorPropagationResult:
        """Model quantization error propagation through a network.

        Given a sequence of layer Jacobians J_1, J_2, ..., J_L and
        per-layer quantization error variances sigma_1^2, ..., sigma_L^2,
        computes the end-to-end output error variance using the
        linearized propagation model.

        The output error covariance is:
            Sigma_out = J_L * ... * J_1 * Sigma_1 * J_1^T * ... * J_L^T
                  + ... + J_L * Sigma_L * J_L^T

        Simplified: the total variance scales with the product of
        spectral norms of downstream Jacobians.

        Args:
            layer_jacobians: List of Jacobian matrices (one per layer).
            per_layer_error_var: Per-layer quantization error variance.
                If None, assumes uniform variance = 1.

        Returns:
            ErrorPropagationResult with propagation analysis.
        """
        L = len(layer_jacobians)
        if L == 0:
            return ErrorPropagationResult(
                per_layer_error_var=[], end_to_end_error_var=0,
                end_to_end_error_std=0, error_amplification_factor=1.0,
                worst_case_error=0, clt_bound_3sigma=0, clt_bound_6sigma=0,
                jacobian_spectral_norm=1.0, is_stable=True,
            )

        if per_layer_error_var is None:
            per_layer_error_var = [1.0] * L

        # Compute spectral norms of Jacobians
        j_spec_norms = []
        for J in layer_jacobians:
            J = np.asarray(J, dtype=np.float64)
            s = np.linalg.svd(J, compute_uv=False)
            j_spec_norms.append(float(s[0]) if len(s) > 0 else 1.0)

        # Error propagation: error from layer l is amplified by
        # the spectral norms of all downstream layers
        # Output error var = sum_l (sigma_l^2 * prod_{k>l} ||J_k||^2)
        end_to_end_var = 0.0
        layer_errors = []

        for l in range(L):
            downstream_product = 1.0
            for k in range(l + 1, L):
                downstream_product *= j_spec_norms[k] ** 2
            error_contrib = per_layer_error_var[l] * downstream_product
            layer_errors.append(error_contrib)
            end_to_end_var += error_contrib

        end_to_end_std = math.sqrt(end_to_end_var)

        # Amplification factor
        total_input_error = sum(per_layer_error_var)
        amp_factor = end_to_end_var / total_input_error if total_input_error > 0 else 1.0

        # Worst case (all errors add constructively)
        worst_case = sum(math.sqrt(v) * j_spec_norms[l]
                        for l, v in enumerate(per_layer_error_var))

        # CLT bounds (assuming errors are approximately independent)
        clt_3sigma = 3 * end_to_end_std
        clt_6sigma = 6 * end_to_end_std

        # Average Jacobian spectral norm
        avg_j_spec = float(np.mean(j_spec_norms)) if j_spec_norms else 1.0

        # Stability: error doesn't amplify unboundedly
        is_stable = amp_factor < 1e6  # practical stability

        return ErrorPropagationResult(
            per_layer_error_var=layer_errors,
            end_to_end_error_var=end_to_end_var,
            end_to_end_error_std=end_to_end_std,
            error_amplification_factor=amp_factor,
            worst_case_error=worst_case,
            clt_bound_3sigma=clt_3sigma,
            clt_bound_6sigma=clt_6sigma,
            jacobian_spectral_norm=avg_j_spec,
            is_stable=is_stable,
        )

    # ------------------------------------------------------------------
    # Random matrix theory predictions
    # ------------------------------------------------------------------

    @staticmethod
    def random_matrix_prediction(
        rows: int,
        cols: int,
        sparsity: float = 0.45,
    ) -> RandomMatrixPrediction:
        """Predict spectral properties of a random ternary matrix.

        For W in {-1, 0, +1}^{m x n} with i.i.d. entries where
        P(X=0) = sparsity, P(X=+1) = P(X=-1) = (1-sparsity)/2,
        predicts the limiting spectral distribution and key quantities.

        The singular values of W/sqrt(n) follow a modified
        Marchenko-Pastur distribution with variance parameter
        sigma^2 = (1 - sparsity) (non-zero fraction).

        Args:
            rows: Matrix rows (m).
            cols: Matrix columns (n).
            sparsity: Fraction of zero entries.

        Returns:
            RandomMatrixPrediction with theoretical predictions.
        """
        m, n = rows, cols
        gamma = min(m, n) / max(m, n)  # aspect ratio
        sigma2 = 1.0 - sparsity  # variance per entry

        # Marchenko-Pastur edges for variance sigma^2
        lambda_plus = sigma2 * (1 + math.sqrt(gamma)) ** 2
        lambda_minus = max(0, sigma2 * (1 - math.sqrt(gamma)) ** 2)

        # MP peak (mode of the distribution)
        # For gamma < 1: peak at lambda_minus * (1 - gamma) / (1 + gamma)^2 * something
        # Simplified: peak near sigma2 * (1 - sqrt(gamma))^2
        mp_peak = sigma2 * (1 - math.sqrt(gamma)) ** 2

        # Bulk eigenvalue count
        min_dim = min(m, n)
        bulk_count = min_dim

        # Tracy-Widom expected top eigenvalue
        # For MP with sigma^2: E[lambda_max] ~ lambda+ + sigma * TW_1
        # TW_1 mean ~ -1.21 (for beta=1, real matrices) or -1.77 (beta=2, complex)
        tw_shift = 1.77 * sigma2 * n ** (-2/3)  # Tracy-Widom fluctuation scale
        expected_top = lambda_plus + tw_shift

        # Expected spectral radius
        expected_spectral_radius = math.sqrt(lambda_plus)

        # Expected condition number
        if lambda_minus > 0:
            expected_cond = math.sqrt(lambda_plus / lambda_minus)
        else:
            # For gamma < 1, there are (m-n) zero eigenvalues
            expected_cond = float('inf') if gamma < 1 else 100.0

        # Outlier threshold (Baik-Ben Arous-Peche)
        # Phase transition at sqrt(sigma^2) + sqrt(sigma^2 * gamma)
        outlier_threshold = math.sqrt(sigma2) * (1 + math.sqrt(gamma))

        # Expected rank efficiency
        expected_rank_eff = min(1.0, gamma)  # effective rank / min(m,n)

        return RandomMatrixPrediction(
            mp_upper_edge=lambda_plus,
            mp_lower_edge=lambda_minus,
            mp_peak=mp_peak,
            bulk_eigenvalue_count=bulk_count,
            outlier_threshold=outlier_threshold,
            expected_top_eigenvalue=expected_top,
            expected_spectral_radius=expected_spectral_radius,
            expected_condition_number=expected_cond if expected_cond != float('inf') else 1e6,
            expected_rank_efficiency=expected_rank_eff,
        )

    # ------------------------------------------------------------------
    # Weight distribution statistics
    # ------------------------------------------------------------------

    @staticmethod
    def weight_distribution_stats(weights: np.ndarray) -> Dict[str, float]:
        """Compute comprehensive statistical properties of a weight matrix.

        Includes moments, kurtosis, skewness, Gini coefficient,
        and structural sensitivity predictors.

        Args:
            weights: Weight array (any shape).

        Returns:
            Dict with statistical properties.
        """
        w = np.asarray(weights, dtype=np.float64).ravel()
        n = len(w)
        if n == 0:
            return {}

        w_abs = np.abs(w)
        mean_abs = float(np.mean(w_abs))
        std = float(np.std(w))
        mean = float(np.mean(w))

        # Higher moments
        skewness = float(np.mean(((w - mean) / std) ** 3)) if std > 0 else 0.0
        kurtosis = float(np.mean(((w - mean) / std) ** 4)) - 3.0 if std > 0 else 0.0

        # Gini coefficient of |W| (inequality measure)
        w_sorted = np.sort(w_abs)
        gini = float(2 * np.sum((np.arange(n) + 1) * w_sorted) / (n * np.sum(w_sorted)) - (n + 1) / n) if np.sum(w_sorted) > 0 else 0.0

        # Effective rank
        if w.ndim >= 2:
            W_2d = np.asarray(weights, dtype=np.float64)
            if W_2d.ndim > 2:
                W_2d = W_2d.reshape(-1, W_2d.shape[-1])
            s = np.linalg.svd(W_2d, compute_uv=False)
            s2 = s ** 2
            eff_rank = float((np.sum(s2) ** 2) / np.sum(s2 ** 2))
        else:
            eff_rank = 1.0

        return {
            "n": n,
            "mean": mean,
            "std": std,
            "mean_abs": mean_abs,
            "max_abs": float(np.max(w_abs)),
            "min": float(np.min(w)),
            "max": float(np.max(w)),
            "skewness": skewness,
            "excess_kurtosis": kurtosis,
            "gini_coefficient": gini,
            "effective_rank": eff_rank,
            "sparsity_estimate": float(np.mean(np.abs(w) < 0.5 * mean_abs)) if mean_abs > 0 else 0.0,
            "cv": std / mean_abs if mean_abs > 0 else float('inf'),  # coefficient of variation
        }
