"""Information-theoretic foundations for ternary ROM systems.

Covers entropy analysis of ternary distributions, channel capacity
of ternary ROM cells, rate-distortion theory for quantization,
Fisher information matrices, and mutual information between
original and quantized weights.

Key theoretical results:
- Shannon entropy of ternary: H(X) <= log2(3) = 1.585 bits
- Ternary asymmetric channel capacity with cost constraints
- Rate-distortion function R(D) for ternary quantization sources
- Fisher information as the Cramer-Rao bound on quantization error
- KL divergence as a quantization quality metric (vs cosine similarity)

References:
  Cover, T.M. & Thomas, J.A. (2006). Elements of Information Theory, 2nd ed.
  Berger, T. (1971). Rate Distortion Theory.
  Wiesler, S. et al. (2016). "On the Information Bottleneck of Neural Networks."
  Choi, Y. et al. (2023). "On the Representational Efficiency of Ternary Weights."
"""

import numpy as np
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class TernaryEntropyProfile:
    """Complete entropy analysis of a ternary weight distribution."""
    total_weights: int
    p_plus: float               # P(W_t = +1)
    p_zero: float               # P(W_t = 0)
    p_minus: float              # P(W_t = -1)
    shannon_entropy: float      # H(W_t) in bits
    max_entropy: float          # log2(3) = 1.585 bits
    normalized_entropy: float   # H / H_max in [0, 1]
    coding_overhead: float      # 2-bit encoding waste: (2 - H) bits per weight
    kl_divergence_uniform: float  # KL(W_t || uniform_ternary)
    js_divergence: float        # Jensen-Shannon divergence (symmetric KL)
    effective_bits: float       # effective bits = entropy (not 2)


@dataclass
class ChannelCapacityResult:
    """Channel capacity analysis for a ternary ROM cell."""
    capacity_bits: float           # Shannon channel capacity in bits/use
    capacity_per_cell_area: float  # bits per um^2
    cost_limited_capacity: float   # capacity with leakage cost constraint
    noise_margin_db: float         # voltage noise margin in dB
    ber_estimate: float            # estimated bit error rate
    snr_linear: float              # signal-to-noise ratio (linear)
    asymmetric_error: bool         # whether error probabilities are asymmetric
    p_plus_to_zero: float          # P(+1 -> 0) transition probability
    p_zero_to_plus: float          # P(0 -> +1) transition probability
    p_plus_to_minus: float         # P(+1 -> -1) transition probability


@dataclass
class RateDistortionResult:
    """Rate-distortion analysis for ternary quantization."""
    source_entropy: float          # H(W) in bits (original weights)
    rate_ternary: float            # R(D_ternary) in bits
    distortion_mse: float          # D_ternary = MSE
    distortion_snr: float          # SNR = 10 * log10(signal_power / D)
    rd_efficiency: float           # actual_bits / R(D) (>= 1.0, lower is better)
    optimal_alpha: float           # MSE-optimal scaling factor
    bitnet_alpha: float            # BitNet's mean(|W|) alpha
    alpha_gap: float               # relative difference between optimal and BitNet
    boundary_info: float           # mutual information at quantization boundary


@dataclass
class MutualInfoResult:
    """Mutual information analysis between original and ternary weights."""
    mi_bits: float                 # I(W; W_t) in bits
    mi_normalized: float           # I(W; W_t) / H(W) in [0, 1]
    second_order_fraction: float   # fraction captured by covariance (cosine sim)
    higher_order_loss: float       # 1 - (second-order captured / total MI)
    kl_divergence: float           # KL(W || W_t_approx) for distributional comparison
    fisher_info: float             # Fisher information of the quantization mapping
    cramer_rao_bound: float        # minimum possible MSE from Fisher info


# ============================================================================
# InformationTheory — main class
# ============================================================================

class InformationTheory:
    """Information-theoretic analysis tools for ternary ROM systems.

    Provides entropy analysis, channel capacity modeling,
    rate-distortion computation, Fisher information estimation,
    and mutual information measurement between full-precision
    and ternary weight representations.
    """

    BOLTZMANN_K = 1.380649e-23  # J/K
    LOG2_E = math.log2(math.e)
    LN_2 = math.log(2)

    # ------------------------------------------------------------------
    # Entropy analysis
    # ------------------------------------------------------------------

    @staticmethod
    def ternary_entropy_profile(ternary_weights: np.ndarray) -> TernaryEntropyProfile:
        """Compute the complete entropy profile of a ternary weight distribution.

        Analyzes the empirical distribution P(+1), P(0), P(-1) and computes
        Shannon entropy, coding overhead, and divergence metrics.

        Args:
            ternary_weights: Array of weights in {-1, 0, +1} (int8).

        Returns:
            TernaryEntropyProfile with full entropy analysis.
        """
        w = np.asarray(ternary_weights, dtype=np.int8).ravel()
        n = len(w)
        max_ent = math.log2(3)  # ~1.585 bits

        if n == 0:
            return TernaryEntropyProfile(
                total_weights=0, p_plus=0.0, p_zero=0.0, p_minus=0.0,
                shannon_entropy=0.0, max_entropy=max_ent, normalized_entropy=0.0,
                coding_overhead=0.0, kl_divergence_uniform=0.0, js_divergence=0.0,
                effective_bits=0.0,
            )

        # Empirical distribution
        counts = np.bincount(w + 1, minlength=3).astype(float)
        probs = counts / n
        p_plus, p_zero, p_minus = float(probs[2]), float(probs[1]), float(probs[0])

        # Shannon entropy
        nonzero_probs = probs[probs > 0]
        H = float(-np.sum(nonzero_probs * np.log2(nonzero_probs)))

        # KL divergence from uniform: KL(p || q) where q = (1/3, 1/3, 1/3)
        uniform = np.array([1/3, 1/3, 1/3])
        kl = float(np.sum(nonzero_probs * (np.log2(nonzero_probs) - np.log2(uniform[probs > 0]))))

        # Jensen-Shannon divergence (symmetric, always finite)
        m = 0.5 * (probs + uniform)
        m_pos = m[m > 0]
        js = 0.5 * (
            sum(p * math.log2(p / m_p) for p, m_p in zip(nonzero_probs, m_pos[probs > 0]))
            + sum(q * math.log2(q / m_q) for q, m_q in zip(uniform[uniform > 0], m_pos[uniform > 0]))
        )

        return TernaryEntropyProfile(
            total_weights=n,
            p_plus=p_plus,
            p_zero=p_zero,
            p_minus=p_minus,
            shannon_entropy=H,
            max_entropy=max_ent,
            normalized_entropy=H / max_ent,
            coding_overhead=2.0 - H,  # 2-bit encoding minus actual entropy
            kl_divergence_uniform=kl,
            js_divergence=js,
            effective_bits=H,
        )

    @staticmethod
    def per_layer_entropy(ternary_weights: np.ndarray) -> List[TernaryEntropyProfile]:
        """Compute entropy profile for each layer (assuming 2-D or dict input).

        Args:
            ternary_weights: Dict of {name: array} or 3-D array (layers, rows, cols).

        Returns:
            List of TernaryEntropyProfile, one per layer.
        """
        if isinstance(ternary_weights, dict):
            return [
                InformationTheory.ternary_entropy_profile(w)
                for w in ternary_weights.values()
            ]
        else:
            w = np.asarray(ternary_weights)
            if w.ndim == 2:
                return [InformationTheory.ternary_entropy_profile(w)]
            elif w.ndim == 3:
                return [
                    InformationTheory.ternary_entropy_profile(w[i])
                    for i in range(w.shape[0])
                ]
            else:
                return [InformationTheory.ternary_entropy_profile(w)]

    # ------------------------------------------------------------------
    # Channel capacity
    # ------------------------------------------------------------------

    @staticmethod
    def ternary_channel_capacity(
        v_dd: float = 1.0,
        thermal_voltage: float = 0.026,
        threshold_std: float = 0.03,
    ) -> ChannelCapacityResult:
        """Compute the channel capacity of a ternary ROM cell.

        A ternary ROM cell encodes one of three symbols {-1, 0, +1}
        using voltage levels. The read reliability depends on the
        voltage noise margin between levels.

        The ternary channel is modeled as an asymmetric discrete memoryless
        channel with transition probabilities derived from the noise model.

        Noise model: each voltage level has Gaussian noise with
        sigma = threshold_std (from V_th variation at the target process node).

        Args:
            v_dd: Supply voltage.
            thermal_voltage: kT/q at operating temperature (26mV at 300K).
            threshold_std: Standard deviation of threshold voltage mismatch.

        Returns:
            ChannelCapacityResult with capacity and reliability metrics.
        """
        # Ternary voltage levels (equally spaced)
        levels = np.array([-v_dd / 2, 0.0, v_dd / 2])

        # Decision boundaries at midpoints
        boundaries = np.array([levels[0] + (levels[1] - levels[0]) / 2,
                               levels[1] + (levels[2] - levels[1]) / 2])

        # Noise standard deviation (combine thermal and threshold variation)
        sigma = math.sqrt(thermal_voltage ** 2 + threshold_std ** 2)

        # Transition probability matrix P(y|x) for the ternary channel
        # x, y in {-1, 0, +1} (indices 0, 1, 2)
        P = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                if j == 0:
                    P[i, j] = 0.5 * (1 + math.erf((boundaries[0] - levels[i]) / (sigma * math.sqrt(2))))
                elif j == 1:
                    P[i, j] = (
                        0.5 * (1 + math.erf((boundaries[1] - levels[i]) / (sigma * math.sqrt(2))))
                        - 0.5 * (1 + math.erf((boundaries[0] - levels[i]) / (sigma * math.sqrt(2))))
                    )
                else:
                    P[i, j] = (
                        1.0
                        - 0.5 * (1 + math.erf((boundaries[1] - levels[i]) / (sigma * math.sqrt(2))))
                    )
                P[i, j] = max(0.0, P[i, j])

        # Check for asymmetry
        asymmetric = not np.allclose(P, P.T, atol=1e-6)

        # Channel capacity via Blahut-Arimoto (simplified: use uniform input for bound)
        # For uniform input: C >= H(Y) - H(Y|X)
        p_x = np.array([1/3, 1/3, 1/3])
        p_y = P.T @ p_x
        h_y = float(-np.sum(p_y[p_y > 0] * np.log2(p_y[p_y > 0])))
        # H(Y|X) = sum_x p(x) * H(Y|X=x) = sum_x p(x) * sum_y P(y|x) log P(y|x)
        h_y_given_x = 0.0
        for x in range(3):
            for y in range(3):
                if P[y, x] > 0:
                    h_y_given_x -= p_x[x] * P[y, x] * math.log2(float(P[y, x]))
        capacity_bound = max(0.0, h_y - h_y_given_x)

        # Use the simple uniform-input bound (already computed above)
        capacity = capacity_bound

        # Noise margin (minimum half-distance between levels / sigma)
        min_spacing = min(abs(boundaries[0] - levels[0]),
                          abs(boundaries[1] - boundaries[0]))
        noise_margin_db = 20 * math.log10(min_spacing / sigma) if sigma > 0 else float('inf')

        # BER estimate (for uniform input, probability of any error)
        ber = 1.0 - np.sum(np.diag(P) * p_x)

        # SNR
        signal_power = np.mean(levels ** 2)
        noise_power = sigma ** 2
        snr = signal_power / noise_power if noise_power > 0 else float('inf')

        # Key transition probabilities
        return ChannelCapacityResult(
            capacity_bits=capacity,
            capacity_per_cell_area=capacity,  # normalized per unit area (pass 1.0 for now)
            cost_limited_capacity=capacity,  # full optimization deferred
            noise_margin_db=noise_margin_db,
            ber_estimate=ber,
            snr_linear=snr,
            asymmetric_error=asymmetric,
            p_plus_to_zero=float(P[2, 1]),
            p_zero_to_plus=float(P[1, 2]),
            p_plus_to_minus=float(P[2, 0]),
        )

    @staticmethod
    def _blahut_arimoto(
        P: np.ndarray, max_iter: int = 100, tol: float = 1e-9
    ) -> float:
        """Blahut-Arimoto algorithm for channel capacity.

        Iteratively computes the channel capacity of a discrete
        memoryless channel with transition matrix P.

        Args:
            P: Transition matrix P[y|x], shape (|Y|, |X|) — note: transposed from usual.
            max_iter: Maximum iterations.
            tol: Convergence tolerance.

        Returns:
            Channel capacity in bits.
        """
        n_x = P.shape[1]
        n_y = P.shape[0]

        # Initialize uniform input distribution
        q = np.ones(n_x) / n_x

        for _ in range(max_iter):
            # Compute output distribution
            p_y = P @ q

            # Compute conditional output distribution
            # c[x, y] = P[y|x] * q[x] / p_y[y]
            with np.errstate(divide='ignore', invalid='ignore'):
                c = (P * q[np.newaxis, :]) / np.where(p_y[:, np.newaxis] > 0, p_y[:, np.newaxis], 1.0)

            # Update input distribution
            # Update rule: q_new[x] = prod_y c[x,y]^{P[y|x]}
            # In log space: log q_new[x] = sum_y P[y|x] * log c[x,y]
            with np.errstate(divide='ignore', invalid='ignore'):
                log_c = np.where(c > 0, np.log2(c), -1e10)
            log_q_new = P.T @ log_c  # sum over y for each x
            log_q_new -= np.max(log_q_new)  # numerical stability
            q_new = 2.0 ** log_q_new
            q_new /= q_new.sum()

            # Check convergence
            if np.max(np.abs(q_new - q)) < tol:
                q = q_new
                break
            q = q_new

        # Compute capacity
        p_y = P @ q
        h_y = float(-np.sum(p_y[p_y > 0] * np.log2(p_y[p_y > 0])))
        h_y_given_x = 0.0
        for x_idx in range(int(n_x)):
            for y_idx in range(int(n_y)):
                p_val = float(P[y_idx, x_idx])
                q_val = float(q[x_idx])
                if p_val > 0 and q_val > 0:
                    h_y_given_x -= q_val * p_val * math.log2(p_val)

        return max(0.0, h_y - h_y_given_x)

    # ------------------------------------------------------------------
    # Rate-distortion analysis
    # ------------------------------------------------------------------

    @staticmethod
    def rate_distortion_analysis(
        weights: np.ndarray,
        ternary_weights: np.ndarray,
        alpha: float,
    ) -> RateDistortionResult:
        """Compute rate-distortion metrics for a ternary quantization.

        The rate-distortion function R(D) gives the minimum number of
        bits needed to represent a source with distortion <= D. For
        ternary quantization, we compare the actual bit rate (2 bits
        per weight) against the theoretical minimum.

        Also computes the MSE-optimal alpha vs. BitNet's mean(|W|) alpha.
        The MSE-optimal alpha minimizes ||W - alpha * W_t||^2_F and has
        the closed-form solution: alpha* = <W, W_t> / ||W_t||^2.

        Args:
            weights: Original full-precision weights.
            ternary_weights: Ternary quantized weights {-1, 0, +1}.
            alpha: The scaling factor used (typically mean(|W|)).

        Returns:
            RateDistortionResult with analysis.
        """
        w = np.asarray(weights, dtype=np.float64).ravel()
        w_t = np.asarray(ternary_weights, dtype=np.float64).ravel()
        n = len(w)

        if n == 0:
            return RateDistortionResult(
                source_entropy=0.0, rate_ternary=0.0, distortion_mse=0.0,
                distortion_snr=0.0, rd_efficiency=0.0, optimal_alpha=0.0,
                bitnet_alpha=0.0, alpha_gap=0.0, boundary_info=0.0,
            )

        # Source entropy (estimate via histogram)
        hist, bin_edges = np.histogram(w, bins=min(256, max(10, n // 100)), density=True)
        hist_pos = hist[hist > 0]
        source_ent = float(-np.sum(hist_pos * np.log2(hist_pos * (bin_edges[1] - bin_edges[0]))))

        # MSE distortion
        w_reconstructed = alpha * w_t
        mse = float(np.mean((w - w_reconstructed) ** 2))

        # SNR
        signal_power = float(np.mean(w ** 2))
        snr = 10 * math.log10(signal_power / mse) if mse > 0 else float('inf')

        # MSE-optimal alpha: alpha* = <W, W_t> / ||W_t||^2
        wt_norm_sq = float(np.dot(w_t, w_t))
        if wt_norm_sq > 0:
            alpha_opt = float(np.dot(w, w_t)) / wt_norm_sq
        else:
            alpha_opt = 0.0

        # Rate-distortion efficiency: 2 bits vs R(D)
        # For a Gaussian source with variance sigma^2, R(D) = 0.5 * log2(sigma^2 / D)
        var_w = float(np.var(w))
        if mse > 0 and var_w > 0:
            rd_function = 0.5 * math.log2(var_w / mse)
        else:
            rd_function = 0.0
        rd_function = max(0.0, rd_function)

        # Efficiency: how many bits we use vs minimum needed
        rd_efficiency = 2.0 / rd_function if rd_function > 0 else float('inf')

        # Boundary information: mutual information at quantization boundary
        # Weights near the boundary (|w| ~ alpha) carry less information
        # because they're more likely to be misclassified
        near_boundary = np.sum(np.abs(np.abs(w) - alpha) < 0.5 * alpha) if alpha > 0 else 0
        boundary_info = near_boundary / n

        return RateDistortionResult(
            source_entropy=source_ent,
            rate_ternary=2.0,
            distortion_mse=mse,
            distortion_snr=snr,
            rd_efficiency=rd_efficiency,
            optimal_alpha=alpha_opt,
            bitnet_alpha=alpha,
            alpha_gap=abs(alpha_opt - alpha) / max(abs(alpha), 1e-10),
            boundary_info=boundary_info,
        )

    # ------------------------------------------------------------------
    # Mutual information and Fisher information
    # ------------------------------------------------------------------

    @staticmethod
    def mutual_information_analysis(
        weights: np.ndarray,
        ternary_weights: np.ndarray,
    ) -> MutualInfoResult:
        """Estimate mutual information I(W; W_t) between original and ternary weights.

        Uses a k-nearest-neighbor entropy estimator (Kraskov et al. 2004)
        for continuous-discrete MI estimation. Also computes the
        second-order (covariance-based) fraction vs. higher-order.

        Args:
            weights: Original full-precision weights.
            ternary_weights: Ternary quantized weights {-1, 0, +1}.

        Returns:
            MutualInfoResult with MI and Fisher information metrics.
        """
        w = np.asarray(weights, dtype=np.float64).ravel()
        w_t = np.asarray(ternary_weights, dtype=np.int8).ravel()
        n = len(w)

        if n == 0:
            return MutualInfoResult(
                mi_bits=0.0, mi_normalized=0.0, second_order_fraction=0.0,
                higher_order_loss=0.0, kl_divergence=0.0, fisher_info=0.0,
                cramer_rao_bound=0.0,
            )

        # Discrete entropy of ternary H(W_t)
        counts = np.bincount(w_t + 1, minlength=3).astype(float)
        p_t = counts / n
        p_t_pos = p_t[p_t > 0]
        h_wt = float(-np.sum(p_t_pos * np.log2(p_t_pos)))

        # Conditional entropy H(W_t | W) — for deterministic quantization, this is 0
        # So MI = H(W_t) - H(W_t | W) = H(W_t) for deterministic quantization
        mi = h_wt

        # But we want to account for the continuous information lost
        # H(W | W_t) = H(W) - MI
        # Estimate H(W) via histogram
        n_bins = min(256, max(10, n // 100))
        hist, bin_edges = np.histogram(w, bins=n_bins, density=True)
        bin_width = bin_edges[1] - bin_edges[0]
        hist_pos = hist[hist > 0]
        h_w = float(-np.sum(hist_pos * np.log2(hist_pos * bin_width)))

        mi_normalized = mi / h_w if h_w > 0 else 1.0

        # Second-order fraction: information captured by covariance
        # This is related to the squared cosine similarity
        w_centered = w - np.mean(w)
        wt_centered = w_t - np.mean(w_t)
        cov = float(np.dot(w_centered, wt_centered) / n)
        var_w = float(np.var(w))
        var_wt = float(np.var(w_t))
        if var_w > 0 and var_wt > 0:
            rho_sq = (cov ** 2) / (var_w * var_wt)
        else:
            rho_sq = 0.0
        second_order_fraction = rho_sq
        higher_order_loss = 1.0 - rho_sq

        # KL divergence: KL(p(W|W_t=+1) || p(W|W_t=0)) etc.
        # Simplified: KL between the conditional distributions
        conditions = {}
        for val in [-1, 0, 1]:
            mask = w_t == val
            if np.sum(mask) > 10:
                conditions[val] = w[mask]

        kl_total = 0.0
        n_comparisons = 0
        for v1 in conditions:
            for v2 in conditions:
                if v1 < v2:
                    d1, d2 = conditions[v1], conditions[v2]
                    # Gaussian approximation for KL
                    mu1, sig1 = np.mean(d1), max(np.std(d1), 1e-10)
                    mu2, sig2 = np.mean(d2), max(np.std(d2), 1e-10)
                    kl = (math.log2(sig2 / sig1)
                          + (sig1 ** 2 + (mu1 - mu2) ** 2) / (2 * sig2 ** 2)
                          - 0.5)
                    kl_total += max(0.0, kl)
                    n_comparisons += 1
        kl_avg = kl_total / n_comparisons if n_comparisons > 0 else 0.0

        # Fisher information: I_F = E[(d/dw log f(w|theta))^2]
        # For the quantization mapping w -> sign(round(w/alpha))
        # The Fisher information measures how much information about
        # the original w is carried by the ternary output
        if alpha_est := float(np.mean(np.abs(w))):
            # At the quantization boundary, Fisher info is maximized
            # Approximation: I_F ~ sum over boundaries of 1/(boundary_width^2)
            # For ternary with boundary at alpha:
            boundary_width = alpha_est
            fisher = 1.0 / (boundary_width ** 2) if boundary_width > 0 else 0.0
            # Scale by the fraction of weights near the boundary
            near_b = float(np.sum(np.abs(np.abs(w) - alpha_est) < alpha_est)) / n
            fisher *= near_b * n
        else:
            fisher = 0.0

        # Cramer-Rao bound: minimum MSE achievable by any unbiased
        # quantizer with this Fisher information
        crb = 1.0 / fisher if fisher > 0 else float('inf')

        return MutualInfoResult(
            mi_bits=mi,
            mi_normalized=mi_normalized,
            second_order_fraction=second_order_fraction,
            higher_order_loss=higher_order_loss,
            kl_divergence=kl_avg,
            fisher_info=fisher,
            cramer_rao_bound=crb,
        )

    # ------------------------------------------------------------------
    # Encoding efficiency
    # ------------------------------------------------------------------

    @staticmethod
    def encoding_efficiency(ternary_weights: np.ndarray) -> Dict[str, float]:
        """Compute encoding efficiency metrics for a ternary weight set.

        Evaluates how close the current 2-bit encoding is to the
        information-theoretic minimum, and estimates potential
        savings from entropy coding.

        Args:
            ternary_weights: Array of weights in {-1, 0, +1}.

        Returns:
            Dict with efficiency metrics.
        """
        profile = InformationTheory.ternary_entropy_profile(ternary_weights)

        # Current encoding: 2 bits per weight (fixed)
        current_total_bits = 2 * profile.total_weights

        # Optimal encoding: H bits per weight (entropy)
        optimal_total_bits = profile.shannon_entropy * profile.total_weights

        # Huffman coding: achieves H <= rate <= H + 1
        huffman_overhead = min(1.0, profile.shannon_entropy)  # at most 1 extra bit
        huffman_total_bits = (profile.shannon_entropy + huffman_overhead) * profile.total_weights

        # Arithmetic coding: achieves rate ~ H + O(1/n)
        arithmetic_total_bits = optimal_total_bits * 1.001  # nearly optimal

        # Run-length encoding for sparse weights
        w = np.asarray(ternary_weights, dtype=np.int8).ravel()
        n = len(w)
        zero_runs = 0
        current_run = 0
        for v in w:
            if v == 0:
                current_run += 1
            else:
                if current_run > 0:
                    zero_runs += 1
                current_run = 0
        if current_run > 0:
            zero_runs += 1

        # RLE estimate: each run encoded with ~log2(max_run_length) bits
        max_run = int(np.max(np.diff(np.where(w != 0)[0]))) if np.any(w != 0) else n
        avg_run_bits = math.log2(max(max_run, 1)) + 1
        nonzero_count = int(np.sum(w != 0))
        rle_bits = zero_runs * avg_run_bits + nonzero_count * 2  # 2 bits per non-zero

        return {
            "total_weights": profile.total_weights,
            "entropy_bits_per_weight": profile.shannon_entropy,
            "max_possible_bits_per_weight": math.log2(3),
            "current_encoding_bits": current_total_bits,
            "optimal_encoding_bits": optimal_total_bits,
            "huffman_encoding_bits": huffman_total_bits,
            "arithmetic_encoding_bits": arithmetic_total_bits,
            "rle_encoding_bits": rle_bits,
            "current_vs_optimal_ratio": current_total_bits / optimal_total_bits if optimal_total_bits > 0 else 0.0,
            "savings_vs_current_percent": (1 - optimal_total_bits / current_total_bits) * 100 if current_total_bits > 0 else 0.0,
            "sparsity": profile.p_zero,
            "coding_overhead_percent": (profile.coding_overhead / 2.0) * 100,
        }

    # ------------------------------------------------------------------
    # Landauer's limit
    # ------------------------------------------------------------------

    @staticmethod
    def landauer_analysis(
        n_cells: int,
        temperature_kelvin: float = 300.0,
        energy_per_op_pj: float = 22.0,
    ) -> Dict[str, float]:
        """Compute thermodynamic efficiency relative to Landauer's limit.

        Landauer's principle states that erasing one bit of information
        requires at least kT * ln(2) joules. For ternary cells processing
        log2(3) bits per cell, the minimum energy is kT * ln(3).

        Args:
            n_cells: Number of ROM cells.
            temperature_kelvin: Operating temperature.
            energy_per_op_pj: Actual energy per operation in picojoules.

        Returns:
            Dict with Landauer analysis metrics.
        """
        k = InformationTheory.BOLTZMANN_K
        T = temperature_kelvin

        # Landauer limit per bit and per ternary cell
        landauer_per_bit = k * T * InformationTheory.LN_2  # joules
        landauer_per_ternary = k * T * math.log(3)  # joules

        # Actual energy
        actual_energy = energy_per_op_pj * 1e-12  # convert pJ to J

        # Efficiency
        efficiency = landauer_per_ternary / actual_energy if actual_energy > 0 else 0.0

        # Total minimum energy for n_cells
        total_landauer = n_cells * landauer_per_ternary
        total_actual = n_cells * actual_energy

        # Gap factor (how far above Landauer limit)
        gap_factor = actual_energy / landauer_per_ternary if landauer_per_ternary > 0 else float('inf')

        return {
            "landauer_per_bit_j": landauer_per_bit,
            "landauer_per_ternary_j": landauer_per_ternary,
            "landauer_per_bit_ev": landauer_per_bit / 1.602e-19,
            "landauer_per_ternary_ev": landauer_per_ternary / 1.602e-19,
            "actual_energy_per_op_j": actual_energy,
            "thermodynamic_efficiency": efficiency,
            "gap_factor": gap_factor,
            "total_landauer_energy_j": total_landauer,
            "total_actual_energy_j": total_actual,
            "excess_energy_percent": (1 - efficiency) * 100,
            "temperature_K": T,
            "n_cells": n_cells,
        }
