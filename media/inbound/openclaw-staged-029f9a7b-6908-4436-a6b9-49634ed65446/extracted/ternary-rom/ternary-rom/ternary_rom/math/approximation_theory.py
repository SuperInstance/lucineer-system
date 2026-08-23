"""Approximation theory for ternary neural network representations.

Covers Kolmogorov entropy, VC dimension, best approximation theory,
spectral analysis of ternary operators, and accuracy bounds.

Key theoretical results:
- Kolmogorov epsilon-entropy of a ternary weight class: H_eps(W)
  measures the minimum bits needed to approximate any weight matrix
  in the class to within epsilon.
- VC dimension of a ternary neural network with N ternary weights
  and L layers is O(N * L * log(N)). For binary networks, it's O(N);
  ternary adds a factor of log(N) due to the three-state alphabet.
- Best approximation by ternary functions: the minimax error
  E* = inf_{W_t in {-1,0,+1}} ||W - alpha*W_t||_inf is related
  to the Chebyshev alternation theorem for discrete approximation.
- Jackson-type theorems: for smooth weight matrices (rapidly
  decaying singular values), ternary approximation error is
  O(n^{-1} log n) where n is the number of non-zero weights.

References:
  Barron, A.R. (1993). "Universal approximation bounds for
    superpositions of a sigmoidal function." IEEE Trans. IT.
  Kolmogorov, A.N. & Tikhomirov, V.M. (1959). "epsilon-entropy
    and epsilon-capacity of sets in function spaces."
  Vapnik, V.N. & Chervonenkis, A.Y. (1971). "On the uniform
    convergence of relative frequencies of events to their
    probabilities." Theory Prob. Appl.
  DeVore, R.A. & Lorentz, G.G. (1993). Constructive Approximation.
"""

import numpy as np
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class KolmogorovEntropy:
    """Kolmogorov epsilon-entropy of a ternary weight set."""
    epsilon: float              # approximation tolerance
    log_covering_number: float  # log2 of minimum covering set size
    bits_per_weight: float      # H_eps / N
    effective_dimension: float  # rate of growth of H_eps
    is_compressible: bool       # True if H_eps grows sublinearly in N
    compression_ratio: float    # original bits / H_eps bits


@dataclass
class VCAnalysis:
    """VC dimension analysis of a ternary neural network."""
    n_ternary_params: int
    n_layers: int
    vc_dimension_upper: float
    vc_dimension_lower: float
    sample_complexity_bound: int    # samples needed for PAC learning
    generalization_gap_bound: float


@dataclass
class BestApproxResult:
    """Best approximation analysis."""
    mse_optimal: float          # best achievable MSE
    l_inf_error: float          # best achievable L-inf error
    l1_error: float             # best achievable L1 error
    current_mse: float          # current BitNet MSE
    gap_mse: float              # how far current is from optimal
    improvement_potential: float  # % improvement possible
    alternation_points: int     # number of Chebyshev alternation points


@dataclass
class SpectralAccuracy:
    """Spectral analysis of ternary approximation quality."""
    total_energy: float
    captured_energy: float
    energy_fraction: float
    top_k_captured: List[float]  # cumulative energy capture for k=1,2,...
    spectral_tail_error: float    # error from truncated tail
    approximation_order: str      # "algebraic" / "spectral" / "mixed"
    decay_rate: float             # singular value decay rate


# ============================================================================
# ApproximationTheory — main class
# ============================================================================

class ApproximationTheory:
    """Approximation-theoretic tools for ternary neural networks.

    Provides Kolmogorov entropy estimation, VC dimension bounds,
    best approximation analysis, and spectral accuracy measurement.
    """

    # ------------------------------------------------------------------
    # Kolmogorov entropy
    # ------------------------------------------------------------------

    @staticmethod
    def kolmogorov_entropy(
        weights: np.ndarray,
        epsilon: float = 0.01,
    ) -> KolmogorovEntropy:
        """Estimate the Kolmogorov epsilon-entropy of a weight matrix.

        The epsilon-entropy H_eps(W) is the log2 of the minimum number
        of ternary codewords needed to epsilon-cover the set of
        perturbations around the given weight matrix.

        For a weight matrix with effective rank r, the epsilon-entropy
        scales as H_eps ~ r * log2(1/epsilon).

        Args:
            weights: Weight matrix.
            epsilon: Approximation tolerance.

        Returns:
            KolmogorovEntropy with estimates.
        """
        W = np.asarray(weights, dtype=np.float64)
        w = W.ravel()
        n = len(w)
        frobenius = float(np.linalg.norm(W, 'fro'))

        if n == 0 or frobenius == 0:
            return KolmogorovEntropy(
                epsilon=epsilon, log_covering_number=0,
                bits_per_weight=0, effective_dimension=0,
                is_compressible=False, compression_ratio=0,
            )

        # Effective rank
        if W.ndim >= 2:
            W_2d = W.reshape(-1, W.shape[-1]) if W.ndim > 2 else W
            s = np.linalg.svd(W_2d, compute_uv=False)
            s2 = s ** 2
            eff_rank = float((np.sum(s2) ** 2) / np.sum(s2 ** 2))
        else:
            eff_rank = 1.0

        # Kolmogorov entropy estimate:
        # H_eps ~ eff_rank * log2(frobenius / (epsilon * sqrt(n)))
        scale = frobenius / (epsilon * math.sqrt(n)) if n > 0 else 1
        if scale > 1:
            h_eps = eff_rank * math.log2(scale)
        else:
            h_eps = 0.0

        bits_per_weight = h_eps / n if n > 0 else 0

        # Compressibility: H_eps < N * log2(3) means compressible
        max_bits = n * math.log2(3)
        is_compressible = h_eps < max_bits
        compression_ratio = max_bits / h_eps if h_eps > 0 else float('inf')

        return KolmogorovEntropy(
            epsilon=epsilon,
            log_covering_number=h_eps,
            bits_per_weight=bits_per_weight,
            effective_dimension=eff_rank,
            is_compressible=is_compressible,
            compression_ratio=compression_ratio,
        )

    # ------------------------------------------------------------------
    # VC dimension
    # ------------------------------------------------------------------

    @staticmethod
    def vc_dimension(
        n_ternary_params: int,
        n_layers: int = 1,
        input_dimension: int = 0,
    ) -> VCAnalysis:
        """Estimate VC dimension bounds for a ternary neural network.

        For a network with piecewise-linear activation functions
        and ternary weights, the VC dimension is bounded by:
            d_VC <= O(N * L * log(N))
        where N is the number of parameters and L is the number of layers.

        For comparison, a binary network has d_VC = O(N) and a
        real-valued network has d_VC = O(N * L).

        Args:
            n_ternary_params: Number of ternary weight parameters.
            n_layers: Number of layers.
            input_dimension: Input dimension (for bias terms).

        Returns:
            VCAnalysis with dimension bounds.
        """
        N = n_ternary_params
        L = n_layers

        if N == 0:
            return VCAnalysis(0, L, 0, 0, 0, 0)

        # Upper bound: O(N * L * log(N))
        if N > 1:
            log_N = math.log2(N)
            vc_upper = 8 * N * L * log_N  # constant 8 from Warren & Bartlett
        else:
            vc_upper = N * L

        # Lower bound: at least N (parameter counting)
        vc_lower = N

        # Sample complexity for PAC learning:
        # m >= (1/epsilon) * (vc * log(1/epsilon) + log(1/delta))
        # For epsilon=0.01, delta=0.01:
        epsilon_pac = 0.01
        delta_pac = 0.01
        sample_bound = int(
            (1 / epsilon_pac) * (vc_upper * math.log(1 / epsilon_pac) + math.log(1 / delta_pac))
        )

        # Generalization gap bound
        gen_gap = math.sqrt((vc_upper * math.log(2 * N / delta_pac) + math.log(2 / delta_pac)) / max(N, 1))

        return VCAnalysis(
            n_ternary_params=N,
            n_layers=L,
            vc_dimension_upper=vc_upper,
            vc_dimension_lower=vc_lower,
            sample_complexity_bound=sample_bound,
            generalization_gap_bound=gen_gap,
        )

    # ------------------------------------------------------------------
    # Best approximation
    # ------------------------------------------------------------------

    @staticmethod
    def best_approximation(
        weights: np.ndarray,
        alpha: Optional[float] = None,
    ) -> BestApproxResult:
        """Analyze the best possible ternary approximation.

        The best ternary approximation minimizes some norm of the
        reconstruction error. We analyze multiple norms:
        - L2 (MSE): ||W - alpha*W_t||_F
        - L-inf (Chebyshev): max |W_i - alpha*W_t_i|
        - L1: sum |W_i - alpha*W_t_i|

        The Chebyshev alternation theorem states that the best
        L-inf approximation has at least N+2 alternation points
        where the error alternates sign and achieves maximum magnitude.

        Args:
            weights: Original weight matrix.
            alpha: Scaling factor (if None, uses MSE-optimal).

        Returns:
            BestApproxResult with analysis.
        """
        W = np.asarray(weights, dtype=np.float64)
        w = W.ravel()
        n = len(w)

        if n == 0:
            return BestApproxResult(0, 0, 0, 0, 0, 0, 0)

        # Compute alpha if not provided
        if alpha is None:
            alpha = float(np.mean(np.abs(w)))

        # Current BitNet quantization
        w_t_bitnet = np.round(w / alpha).clip(-1, 1).astype(np.float64)
        reconstruction = alpha * w_t_bitnet

        # Current MSE
        current_mse = float(np.mean((w - reconstruction) ** 2))

        # MSE-optimal: try all three possible quantizations and pick the best per element
        # This is the elementwise-optimal (not global-optimal) ternary approximation
        # The true optimal requires considering the interaction between elements.
        # Lower bound: use per-element optimal
        w_t_opt = np.zeros_like(w)
        for i in range(n):
            # Try +1, 0, -1 and pick the one minimizing error
            errors = [
                (w[i] - alpha * 1) ** 2,   # +1
                (w[i] - alpha * 0) ** 2,   # 0
                (w[i] - alpha * (-1)) ** 2,  # -1
            ]
            w_t_opt[i] = [-1, 0, 1][np.argmin(errors)]

        mse_optimal = float(np.mean((w - alpha * w_t_opt) ** 2))

        # L-inf error (best possible)
        # For each element, the best possible error is min(|w - alpha*v| for v in {-1,0,1})
        l_inf_errors = np.minimum(
            np.minimum(np.abs(w - alpha), np.abs(w + alpha)),
            np.abs(w)
        )
        l_inf_error = float(np.max(l_inf_errors))

        # L1 error
        l1_error = float(np.sum(np.abs(w - alpha * w_t_opt)))

        # Gap and improvement potential
        gap = current_mse - mse_optimal
        improvement = (gap / current_mse * 100) if current_mse > 0 else 0

        # Chebyshev alternation points
        residual = w - alpha * w_t_opt
        # Count sign changes in the residual at maximum-error positions
        max_err = float(np.max(np.abs(residual)))
        if max_err > 0:
            near_max = np.abs(np.abs(residual) - max_err) < 0.1 * max_err
            signs_at_max = np.sign(residual[near_max])
            alternations = int(np.sum(np.diff(signs_at_max) != 0))
        else:
            alternations = 0

        return BestApproxResult(
            mse_optimal=mse_optimal,
            l_inf_error=l_inf_error,
            l1_error=l1_error,
            current_mse=current_mse,
            gap_mse=gap,
            improvement_potential=improvement,
            alternation_points=alternations,
        )

    # ------------------------------------------------------------------
    # Spectral accuracy
    # ------------------------------------------------------------------

    @staticmethod
    def spectral_accuracy(
        weights: np.ndarray,
        ternary_weights: np.ndarray,
        alpha: float = 1.0,
    ) -> SpectralAccuracy:
        """Analyze how well ternary quantization preserves spectral properties.

        Compares singular value spectra of the original and quantized
        matrices. The spectral accuracy determines how well the
        quantized matrix approximates the linear transformation.

        Args:
            weights: Original weight matrix.
            ternary_weights: Ternary quantized weights.
            alpha: Scaling factor.

        Returns:
            SpectralAccuracy with analysis.
        """
        W = np.asarray(weights, dtype=np.float64)
        W_t = np.asarray(ternary_weights, dtype=np.float64) * alpha

        if W.ndim == 1:
            W = W.reshape(1, -1)
            W_t = W_t.reshape(1, -1)

        # SVD
        s_orig = np.linalg.svd(W, compute_uv=False)
        s_tern = np.linalg.svd(W_t, compute_uv=False)

        # Energy
        total_energy = float(np.sum(s_orig ** 2))
        captured_energy = float(np.sum(s_tern ** 2))
        energy_frac = captured_energy / total_energy if total_energy > 0 else 1.0

        # Top-k cumulative capture
        k_max = min(len(s_orig), len(s_tern), 20)
        top_k = []
        cum_orig = 0.0
        cum_tern = 0.0
        for k in range(1, k_max + 1):
            cum_orig += float(s_orig[k - 1] ** 2)
            cum_tern += float(s_tern[k - 1] ** 2)
            top_k.append(cum_tern / cum_orig if cum_orig > 0 else 1.0)

        # Spectral tail error
        # Error from singular values beyond the effective rank
        s_match_len = min(len(s_orig), len(s_tern))
        spectral_tail = float(np.sum((s_orig[:s_match_len] - s_tern[:s_match_len]) ** 2))
        if s_match_len < len(s_orig):
            spectral_tail += float(np.sum(s_orig[s_match_len:] ** 2))

        # Decay rate (fit power law to singular values)
        s = s_orig[s_orig > 0]
        if len(s) > 2:
            log_s = np.log10(s)
            log_k = np.log10(np.arange(1, len(s) + 1))
            # Linear fit: log10(s_k) = a - b * log10(k)
            coeffs = np.polyfit(log_k, log_s, 1)
            decay_rate = abs(coeffs[0])
        else:
            decay_rate = 0.0

        # Determine approximation order
        if decay_rate > 1.5:
            order = "spectral"  # rapid decay, spectral methods work well
        elif decay_rate > 0.5:
            order = "mixed"
        else:
            order = "algebraic"  # slow decay, algebraic approximation

        return SpectralAccuracy(
            total_energy=total_energy,
            captured_energy=captured_energy,
            energy_fraction=energy_frac,
            top_k_captured=top_k,
            spectral_tail_error=spectral_tail,
            approximation_order=order,
            decay_rate=decay_rate,
        )

    # ------------------------------------------------------------------
    # Representation power analysis
    # ------------------------------------------------------------------

    @staticmethod
    def representation_power(
        rows: int,
        cols: int,
        sparsity: float = 0.45,
    ) -> Dict[str, float]:
        """Analyze the representation power of a ternary weight matrix.

        The number of distinct linear transformations representable
        by a ternary matrix of size (m x n) with sparsity s is:

            3^{m*n*(1-s)}

        But many of these are redundant (permutation equivalent).
        The number of *functionally distinct* transformations is much
        smaller and depends on the row/column sum distributions.

        Args:
            rows, cols: Matrix dimensions.
            sparsity: Expected sparsity fraction.

        Returns:
            Dict with representation power metrics.
        """
        n_total = rows * cols
        n_nonzero = int(n_total * (1 - sparsity))

        # Total distinct matrices
        total_matrices = 3 ** n_total
        total_nonzero_matrices = 2 ** n_nonzero * 3 ** (n_total - n_nonzero)

        # Log2 of these (bits of representational capacity)
        log2_total = n_total * math.log2(3)
        log2_nonzero = n_nonzero * 1.0 + (n_total - n_nonzero) * math.log2(3)

        # Functional distinctness (upper bound via row/column sum equivalence classes)
        # Row sums range from -cols to +cols, so (2*cols + 1) possibilities
        row_sum_classes = 2 * cols + 1
        col_sum_classes = 2 * rows + 1
        log2_functional = math.log2(row_sum_classes * col_sum_classes)

        # Representation density: how densely the ternary matrices
        # cover the space of all possible linear transformations
        # The space of all m x n matrices with frobenius norm <= R
        # has volume proportional to R^{mn}. The ternary matrices
        # are discrete points, so density ~ 3^{mn} / R^{mn}
        # For R = sqrt(m*n) (typical neural network weight scale):
        R = math.sqrt(n_total)
        log2_volume = n_total * math.log2(R) + n_total * 0.5 * math.log2(2 * math.pi * math.e)
        density = 2 ** (log2_total - log2_volume) if log2_volume > 0 else float('inf')

        return {
            "total_distinct_matrices": total_matrices,
            "log2_representational_capacity": log2_total,
            "nonzero_matrix_count": total_nonzero_matrices,
            "log2_nonzero_capacity": log2_nonzero,
            "row_sum_equivalence_classes": row_sum_classes,
            "col_sum_equivalence_classes": col_sum_classes,
            "log2_functional_capacity_upper_bound": log2_functional,
            "covering_density": min(density, 1e10),  # cap for display
            "n_nonzero_params": n_nonzero,
            "effective_bits_per_param": log2_total / n_total if n_total > 0 else 0,
        }
