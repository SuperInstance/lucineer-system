"""Optimization-theoretic foundations for ternary ROM precision allocation.

Covers Lloyd-Max quantization, ADMM-based mixed-precision optimization,
Markowitz portfolio-theoretic bit allocation, proximal operators for
ternary constraints, and precision schedule optimization.

Key theoretical results:
- The optimal ternary quantizer (Lloyd-Max) minimizes MSE by placing
  decision boundaries at midpoints of Voronoi regions.
- MSE-optimal alpha for ternary: alpha* = <W, W_t> / ||W_t||^2,
  which differs from BitNet's mean(|W|) for non-Gaussian distributions.
- Mixed-precision allocation is a quadratic program isomorphic to
  Markowitz portfolio optimization: maximize accuracy subject to
  area budget, where the "covariance matrix" is the loss Hessian.
- ADMM formulation: min ||W - alpha*W_t||^2 + lambda*||W_t||_0
  with the ternary constraint W_t in {-1,0,+1}.

References:
  Lloyd, S. (1982). "Least squares quantization in PCM."
  Max, J. (1960). "Quantizing for minimum distortion."
  Markowitz, H. (1952). "Portfolio Selection." Journal of Finance.
  Boyd, S. et al. (2011). "Distributed Optimization and Statistical
    Learning via the Alternating Direction Method of Multipliers."
  Dong, Z. et al. (2019). "HAWQ: Hessian Aware Quantization." NeurIPS.
"""

import numpy as np
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class OptimalAlphaResult:
    """Result of optimal alpha computation."""
    bitnet_alpha: float             # mean(|W|) — BitNet's choice
    mse_optimal_alpha: float        # <W, W_t> / ||W_t||^2 — MSE-optimal
    lloyd_max_alpha: float          # Lloyd-Max optimal threshold
    fisher_optimal_alpha: float     # Fisher-information-based threshold
    alpha_gap_bitnet_mse: float     # relative difference
    mse_bitnet: float               # MSE with BitNet alpha
    mse_optimal: float              # MSE with optimal alpha
    mse_improvement: float          # % improvement from using optimal alpha
    condition_number: float         # cond(W) — explains when gap is large


@dataclass
class PrecisionAllocation:
    """Bit-width allocation for each layer."""
    layer_names: List[str]
    bit_widths: List[int]           # bits per layer (2, 4, 8, or 16)
    area_per_layer: List[float]     # estimated area in mm^2
    accuracy_per_layer: List[float] # cos_sim per layer
    total_area_mm2: float
    total_accuracy: float           # weighted average cos_sim
    area_budget_used: float         # fraction of budget used


@dataclass
class MarkowitzResult:
    """Portfolio-theoretic precision allocation result."""
    efficient_frontier: List[Tuple[float, float]]  # (area, accuracy) points
    optimal_allocation: PrecisionAllocation
    information_sharpe: float       # accuracy_gain / sqrt(area)
    tangency_point: Tuple[float, float]  # (area, accuracy) at max Sharpe


@dataclass
class ADMMQuantizeResult:
    """Result of ADMM-based ternary quantization."""
    weights_ternary: np.ndarray
    alpha: float
    mse: float
    cos_sim: float
    iterations: int
    converged: bool
    sparsity: float
    objective_history: List[float]


# ============================================================================
# OptimizationTheory — main class
# ============================================================================

class OptimizationTheory:
    """Optimization-theoretic tools for ternary ROM precision allocation.

    Provides optimal alpha computation, Lloyd-Max quantization,
    Markowitz portfolio-style bit allocation, ADMM quantization,
    and precision schedule optimization.
    """

    # ------------------------------------------------------------------
    # Optimal alpha computation
    # ------------------------------------------------------------------

    @staticmethod
    def compute_optimal_alpha(weights: np.ndarray) -> OptimalAlphaResult:
        """Compute multiple optimal alpha candidates and compare.

        Compares three alpha choices:
        1. BitNet b1.58: alpha = mean(|W|)
        2. MSE-optimal: alpha* = <W, W_t> / ||W_t||^2
        3. Lloyd-Max: alpha at the midpoint of the largest Voronoi region

        Also computes the condition number of W, which predicts when
        the gap between BitNet and MSE-optimal is large.

        Args:
            weights: Full-precision weight matrix.

        Returns:
            OptimalAlphaResult with comparison.
        """
        W = np.asarray(weights, dtype=np.float64)
        w = W.ravel()
        n = len(w)

        if n == 0:
            return OptimalAlphaResult(0, 0, 0, 0, 0, 0, 0, 0, 1.0)

        # 1. BitNet alpha
        alpha_bitnet = float(np.mean(np.abs(w)))

        # Ternarize with BitNet alpha
        if alpha_bitnet > 0:
            wt_bitnet = np.round(w / alpha_bitnet).clip(-1, 1).astype(np.float64)
        else:
            wt_bitnet = np.zeros_like(w)
        mse_bitnet = float(np.mean((w - alpha_bitnet * wt_bitnet) ** 2))

        # 2. MSE-optimal alpha: alpha* = <W, W_t> / ||W_t||^2
        wt_norm_sq = float(np.dot(wt_bitnet, wt_bitnet))
        if wt_norm_sq > 0:
            alpha_mse = float(np.dot(w, wt_bitnet)) / wt_norm_sq
            alpha_mse = max(0, alpha_mse)
        else:
            alpha_mse = 0.0

        # Compute MSE with optimal alpha
        if alpha_mse > 0:
            # Re-ternarize might not change, but the scaling does
            mse_optimal = float(np.mean((w - alpha_mse * wt_bitnet) ** 2))
        else:
            mse_optimal = mse_bitnet

        # 3. Lloyd-Max alpha: place threshold at the midpoint that
        # minimizes total distortion for a 3-level quantizer
        # For symmetric distributions, this is close to mean(|W|)
        # For asymmetric, we compute the two boundaries separately
        w_pos = w[w > 0]
        w_neg = w[w < 0]
        w_zero = w[w == 0]

        if len(w_pos) > 0 and len(w_neg) > 0:
            # Boundaries between neg/zero and zero/pos
            boundary_nz = 0.5 * (np.max(w_neg) + np.min(w_zero)) if len(w_zero) > 0 else 0.5 * np.max(w_neg)
            boundary_zp = 0.5 * (np.max(w_zero) + np.min(w_pos)) if len(w_zero) > 0 else 0.5 * np.min(w_pos)
            alpha_lloyd = 0.5 * (boundary_zp - boundary_nz)
        elif len(w_pos) > 0:
            alpha_lloyd = 0.5 * np.min(w_pos)
        elif len(w_neg) > 0:
            alpha_lloyd = 0.5 * abs(np.max(w_neg))
        else:
            alpha_lloyd = 0.0

        # 4. Fisher-optimal alpha (simplified): based on Fisher info at boundary
        # I_F ~ 1/alpha^2, optimal alpha maximizes I_F * (1 - P(|W| < alpha))
        if alpha_bitnet > 0:
            sparsity = float(np.mean(np.abs(w) < alpha_bitnet))
            # Optimize: max alpha * (1 - sparsity) subject to structure
            alpha_fisher = alpha_bitnet * (1.0 + 0.1 * (1.0 - sparsity))
        else:
            alpha_fisher = 0.0

        # Condition number
        W_2d = W.reshape(-1, W.shape[-1]) if W.ndim > 2 else W
        if W_2d.ndim == 2:
            s = np.linalg.svd(W_2d, compute_uv=False)
            s_pos = s[s > 1e-10]
            cond = float(s_pos[0] / s_pos[-1]) if len(s_pos) > 1 else 1.0
        else:
            cond = 1.0

        # Alpha gap
        alpha_gap = (abs(alpha_bitnet - alpha_mse) / alpha_bitnet) if alpha_bitnet > 0 else 0.0
        mse_improvement = ((mse_bitnet - mse_optimal) / mse_bitnet * 100) if mse_bitnet > 0 else 0.0

        return OptimalAlphaResult(
            bitnet_alpha=alpha_bitnet,
            mse_optimal_alpha=alpha_mse,
            lloyd_max_alpha=alpha_lloyd,
            fisher_optimal_alpha=alpha_fisher,
            alpha_gap_bitnet_mse=alpha_gap,
            mse_bitnet=mse_bitnet,
            mse_optimal=mse_optimal,
            mse_improvement=mse_improvement,
            condition_number=cond,
        )

    # ------------------------------------------------------------------
    # ADMM ternary quantization
    # ------------------------------------------------------------------

    @staticmethod
    def admm_ternarize(
        weights: np.ndarray,
        rho: float = 0.1,
        max_iter: int = 100,
        tol: float = 1e-6,
        sparsity_weight: float = 0.0,
    ) -> ADMMQuantizeResult:
        """Ternarize using ADMM (Alternating Direction Method of Multipliers).

        Formulation:
            minimize  ||W - alpha * W_t||^2_F + lambda * ||W_t||_0
            subject to  W_t in {-1, 0, +1}

        ADMM splits into:
            W-update: W = (W_orig + rho * (W_t - u)) / (1 + rho)
            W_t-update: project onto {-1, 0, +1} with sparsity penalty
            u-update: u = u + W_t - W

        Args:
            weights: Original weight matrix.
            rho: ADMM penalty parameter.
            max_iter: Maximum iterations.
            tol: Convergence tolerance.
            sparsity_weight: L0 penalty encouraging zeros.

        Returns:
            ADMMQuantizeResult with quantized weights and convergence info.
        """
        W_orig = np.asarray(weights, dtype=np.float64)
        W = W_orig.copy()
        w = W.ravel()
        n = len(w)

        # Initialize
        alpha = float(np.mean(np.abs(w))) if np.mean(np.abs(w)) > 0 else 1.0
        W_t = np.round(W / alpha).clip(-1, 1)
        U = np.zeros_like(W)

        objective_history = []

        for iteration in range(max_iter):
            # W-update (soft thresholding)
            W_new = (W_orig + rho * (alpha * W_t - U)) / (1.0 + rho)

            # W_t-update: project onto ternary set
            if alpha > 0:
                W_t_new = np.round(W_new / alpha + U / alpha).clip(-1, 1)

                # Sparsity promotion: push small magnitudes to zero
                if sparsity_weight > 0:
                    residual = np.abs(W_new / alpha + U / alpha)
                    threshold = sparsity_weight * rho / (2.0 * alpha)
                    W_t_new[np.abs(residual) < threshold] = 0
            else:
                W_t_new = np.zeros_like(W)

            # U-update (dual variable)
            U_new = U + alpha * W_t_new - W_new

            # Compute objective
            reconstruction = alpha * W_t_new
            data_fit = float(np.sum((W_orig - reconstruction) ** 2))
            sparsity_term = sparsity_weight * float(np.sum(W_t_new != 0))
            objective = data_fit + sparsity_term
            objective_history.append(objective)

            # Check convergence
            primal_res = float(np.linalg.norm(alpha * W_t_new - alpha * W_t))
            dual_res = float(np.linalg.norm(W_t_new - W_t))
            W_t = W_t_new
            W = W_new
            U = U_new

            if primal_res < tol and dual_res < tol:
                break

        # Final metrics
        w_final = (alpha * W_t).ravel()
        w_orig = W_orig.ravel()
        mse = float(np.mean((w_orig - w_final) ** 2))

        norm_orig = np.linalg.norm(w_orig)
        norm_quant = np.linalg.norm(w_final)
        cos_sim = float(np.dot(w_orig, w_final) / (norm_orig * norm_quant)) if norm_orig > 0 and norm_quant > 0 else 1.0

        sparsity = float(np.mean(W_t == 0))

        return ADMMQuantizeResult(
            weights_ternary=W_t.astype(np.int8),
            alpha=alpha,
            mse=mse,
            cos_sim=cos_sim,
            iterations=iteration + 1,
            converged=primal_res < tol,
            sparsity=sparsity,
            objective_history=objective_history,
        )

    # ------------------------------------------------------------------
    # Markowitz portfolio-theoretic bit allocation
    # ------------------------------------------------------------------

    @staticmethod
    def markowitz_precision_allocation(
        layer_names: List[str],
        layer_shapes: List[Tuple[int, ...]],
        layer_cos_sims: List[float],
        layer_hessians: Optional[List[np.ndarray]] = None,
        area_budget_mm2: float = 10.0,
        cell_area_mm2: float = 4.8e-14,
        available_bits: List[int] = None,
    ) -> MarkowitzResult:
        """Allocate bit-widths across layers using portfolio optimization.

        The precision allocation problem is isomorphic to Markowitz
        portfolio optimization:
        - "Assets" = layers
        - "Returns" = accuracy contribution (proportional to cos_sim)
        - "Risk" = quantization error variance
        - "Budget" = total ROM/SRAM area

        The efficient frontier traces the Pareto-optimal tradeoff
        between area and accuracy.

        Args:
            layer_names: Names of layers.
            layer_shapes: Shapes of weight matrices.
            layer_cos_sims: Per-layer cosine similarities.
            layer_hessians: Optional per-layer Hessian traces (for risk weighting).
            area_budget_mm2: Maximum total area.
            cell_area_mm2: Area per cell at target process.
            available_bits: Available bit-widths. Default [2, 4, 8, 16].

        Returns:
            MarkowitzResult with efficient frontier and optimal allocation.
        """
        if available_bits is None:
            available_bits = [2, 4, 8, 16]

        L = len(layer_names)
        if L == 0:
            return MarkowitzResult([], [], [], [], [], 0, 0, 0.0, (0.0, 0.0))

        # Compute per-layer properties
        n_params = [int(np.prod(s)) for s in layer_shapes]
        total_params = sum(n_params)

        # Area per layer at each bit-width
        # ternary: cell_area per param; INT8: 4x cell_area; FP16: 8x cell_area
        area_multipliers = {2: 1.0, 4: 2.0, 8: 4.0, 16: 8.0}

        # Risk per layer (quantization error variance)
        # Higher cos_sim = lower risk. Use (1 - cos_sim)^2 as risk proxy.
        # If Hessian traces are provided, weight by Hessian magnitude.
        risks = [(1.0 - cs) ** 2 for cs in layer_cos_sims]
        if layer_hessians is not None:
            for i, H in enumerate(layer_hessians):
                if H is not None and i < len(risks):
                    h_trace = float(np.trace(np.asarray(H, dtype=np.float64)))
                    if h_trace > 0:
                        risks[i] *= (1.0 + math.log1p(h_trace))

        total_risk = sum(risks)
        risk_weights = [r / total_risk if total_risk > 0 else 1/L for r in risks]

        # Build efficient frontier by sweeping area budget
        frontier = []
        n_points = 20

        for i in range(n_points):
            budget_frac = (i + 1) / n_points
            budget = area_budget_mm2 * budget_frac

            # Greedy allocation: give more bits to riskier layers
            allocations = [2] * L  # start with all ternary
            remaining_budget = budget

            for bit in [4, 8, 16]:
                if remaining_budget <= 0:
                    break
                for l_idx in sorted(range(L), key=lambda l: risk_weights[l], reverse=True):
                    if allocations[l_idx] >= bit:
                        continue
                    # Cost of upgrading from current to this bit-width
                    current_area = n_params[l_idx] * area_multipliers[allocations[l_idx]] * cell_area_mm2
                    new_area = n_params[l_idx] * area_multipliers[bit] * cell_area_mm2
                    cost = new_area - current_area
                    if cost <= remaining_budget:
                        allocations[l_idx] = bit
                        remaining_budget -= cost

            # Compute accuracy for this allocation
            # Higher bits = higher cos_sim (capped at 1.0)
            accuracy = 0.0
            total_w = 0.0
            for l_idx in range(L):
                # Accuracy scales with bits: cos_sim approx 1 - (1 - cs) * (2/bits)
                bits = allocations[l_idx]
                layer_acc = 1.0 - (1.0 - layer_cos_sims[l_idx]) * (2.0 / bits)
                layer_acc = min(1.0, layer_acc)
                w = n_params[l_idx]
                accuracy += layer_acc * w
                total_w += w
            accuracy /= total_w if total_w > 0 else 1.0

            # Total area
            total_area = sum(
                n_params[l] * area_multipliers[allocations[l]] * cell_area_mm2
                for l in range(L)
            )

            frontier.append((total_area, accuracy))

        # Find optimal (max Sharpe ratio)
        best_sharpe = -1
        best_point = (0.0, 0.0)
        for area, acc in frontier:
            sharpe = acc / math.sqrt(area) if area > 0 else 0
            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_point = (area, acc)

        # Build the optimal allocation at the tangency point
        # Use the budget that achieves the tangency point
        tangency_budget = best_point[0] * 1.1  # slight over-allocation for safety
        allocations = [2] * L
        remaining = tangency_budget
        for bit in [4, 8, 16]:
            if remaining <= 0:
                break
            for l_idx in sorted(range(L), key=lambda l: risk_weights[l], reverse=True):
                if allocations[l_idx] >= bit:
                    continue
                cost = n_params[l_idx] * (area_multipliers[bit] - area_multipliers[allocations[l_idx]]) * cell_area_mm2
                if cost <= remaining:
                    allocations[l_idx] = bit
                    remaining -= cost

        areas = [n_params[l] * area_multipliers[allocations[l]] * cell_area_mm2 for l in range(L)]
        accs = [min(1.0, 1.0 - (1.0 - layer_cos_sims[l]) * (2.0 / allocations[l])) for l in range(L)]

        optimal = PrecisionAllocation(
            layer_names=layer_names,
            bit_widths=allocations,
            area_per_layer=areas,
            accuracy_per_layer=accs,
            total_area_mm2=sum(areas),
            total_accuracy=float(np.mean(accs)),
            area_budget_used=sum(areas) / tangency_budget if tangency_budget > 0 else 1.0,
        )

        return MarkowitzResult(
            efficient_frontier=frontier,
            optimal_allocation=optimal,
            information_sharpe=best_sharpe,
            tangency_point=best_point,
        )

    # ------------------------------------------------------------------
    # Precision schedule optimization
    # ------------------------------------------------------------------

    @staticmethod
    def precision_schedule(
        n_layers: int,
        layer_cos_sims: List[float],
        available_bits: List[int] = None,
    ) -> List[int]:
        """Compute an optimal precision schedule across network layers.

        Based on the theoretical result that early layers benefit more
        from higher precision (they process raw, high-variance input)
        while later layers can tolerate lower precision (representations
        have been progressively compressed).

        The schedule is: [high_bits, ..., high_bits, 2, 2, ..., 2]
        where the transition point depends on the cumulative
        cos_sim degradation.

        Args:
            n_layers: Number of layers.
            layer_cos_sims: Per-layer cosine similarities.
            available_bits: Available bit-widths.

        Returns:
            List of bit-widths, one per layer.
        """
        if available_bits is None:
            available_bits = [2, 4, 8, 16]

        schedule = []
        cumulative_error = 0.0
        error_threshold = 0.5  # total error budget

        for i in range(n_layers):
            cs = layer_cos_sims[i] if i < len(layer_cos_sims) else 0.95
            layer_error = 1.0 - cs
            cumulative_error += layer_error

            # Assign bits based on position and error contribution
            if cumulative_error < 0.1 * error_threshold:
                # Early layers: use highest precision available
                schedule.append(available_bits[-1])
            elif cumulative_error < 0.3 * error_threshold:
                schedule.append(available_bits[-2] if len(available_bits) >= 3 else available_bits[-1])
            elif cumulative_error < 0.6 * error_threshold:
                schedule.append(available_bits[-3] if len(available_bits) >= 4 else available_bits[-2])
            else:
                schedule.append(available_bits[0])

        return schedule
