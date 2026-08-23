"""Number-theoretic foundations for ternary ROM systems.

Covers balanced ternary arithmetic, Cantor set connections,
redundant number representations, ternary error-correcting codes,
and modular arithmetic structures relevant to ternary weight encoding.

Mathematical grounding:
- Balanced ternary is the most efficient integer base (Hayes 2001, extending Euler's conjecture):
  base-3 minimizes radix * digits for a given precision range.
- The Cantor set is the canonical ternary fractal, encoding which ternary
  representations are "forbidden" and providing a natural measure of ternary
  quantization information loss.
- Redundant representations (signed-digit arithmetic) enable carry-free addition,
  directly applicable to ternary ROM adder tree optimization.

References:
  Hayes, B. (2001). "Third Base." American Scientist, 89(6), 490-494.
  Knuth, D.E. (1997). TAOCP Vol 2, Section 4.1: Positional Number Systems.
  Avizienis, A. (1961). "Signed-digit number representations for fast parallel
    arithmetic." IRE Trans. Electronic Computers, 10(3), 389-400.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class TernaryDigit:
    """A single balanced ternary digit (trit) with its position weight."""
    value: int          # -1, 0, or +1
    position: int       # 0 = least significant trit

    @property
    def weighted_value(self) -> float:
        return self.value * (3.0 ** self.position)


@dataclass
class BalancedTernaryRep:
    """Full balanced ternary representation of a number."""
    trits: List[int]    # trits[i] is position i (LSB = index 0)

    @property
    def n_trits(self) -> int:
        return len(self.trits)

    @property
    def decimal_value(self) -> float:
        return sum(t * (3.0 ** i) for i, t in enumerate(self.trits))

    @property
    def trit_entropy(self) -> float:
        """Entropy of the trit distribution in bits."""
        vals = np.array(self.trits, dtype=np.int8)
        counts = np.bincount(vals + 1, minlength=3).astype(float)
        probs = counts / counts.sum()
        probs = probs[probs > 0]
        return float(-np.sum(probs * np.log2(probs)))


@dataclass
class CantorAnalysis:
    """Analysis of a ternary weight matrix through the lens of the Cantor set."""
    total_weights: int
    zero_fraction: float           # fraction of weights = 0
    cantor_measure: float          # Hausdorff measure of the quantization set
    information_preserved: float   # fraction of representable real values
    forbidden_intervals: int       # count of Cantor-set-level forbidden ranges
    effective_bits_per_weight: float


@dataclass
class RedundantNumberAnalysis:
    """Analysis of carry-free addition potential for ternary ROM adder trees."""
    max_carry_propagation: int      # worst-case carry chain length
    average_carry_propagation: float
    cancellation_pairs: int         # count of +1/-1 adjacent pairs
    cancellation_fraction: float
    dynamic_range_reduction: float  # factor by which sum range reduces after cancellation
    carry_free_achievable: bool


# ============================================================================
# NumberTheory — main class
# ============================================================================

class NumberTheory:
    """Number-theoretic tools for ternary ROM analysis.

    Provides balanced ternary arithmetic, Cantor set analysis,
    redundant (signed-digit) representation analysis, and modular
    arithmetic structures relevant to weight encoding and adder design.
    """

    # ------------------------------------------------------------------
    # Balanced ternary conversion
    # ------------------------------------------------------------------

    @staticmethod
    def to_balanced_ternary(n: int, n_trits: Optional[int] = None) -> BalancedTernaryRep:
        """Convert an integer to balanced ternary representation.

        Balanced ternary uses digits {-1, 0, +1} (written as T, 0, 1).
        This is the unique signed-digit representation without redundancy.

        Args:
            n: Integer to convert (can be negative).
            n_trits: If specified, pad/truncate to exactly this many trits.

        Returns:
            BalancedTernaryRep with trits in LSB-first order.

        Example:
            >>> NumberTheory.to_balanced_ternary(5)
            BalancedTernaryRep(trits=[-1, -1, 1])  # 1*9 + (-1)*3 + (-1)*1 = 5
        """
        if n == 0:
            trits = [0]
        else:
            trits = []
            n_remaining = n
            while n_remaining != 0:
                remainder = n_remaining % 3
                n_remaining = n_remaining // 3
                if remainder == 2:
                    remainder = -1
                    n_remaining += 1
                trits.append(remainder)

        if n_trits is not None:
            if len(trits) < n_trits:
                trits.extend([0] * (n_trits - len(trits)))
            else:
                trits = trits[:n_trits]

        return BalancedTernaryRep(trits=trits)

    @staticmethod
    def from_balanced_ternary(trits: List[int]) -> int:
        """Convert balanced ternary trits back to integer.

        Args:
            trits: List of trits in {-1, 0, +1}, LSB first.

        Returns:
            Integer value.
        """
        value = 0
        for i, t in enumerate(trits):
            value += t * (3 ** i)
        return value

    @staticmethod
    def balanced_ternary_addition(a: List[int], b: List[int]) -> List[int]:
        """Add two balanced ternary numbers (LSB-first trit lists).

        Uses standard ternary addition with carry propagation.
        Carry rules for balanced ternary:
            1 + 1 = -1 carry +1
            -1 + (-1) = 1 carry -1
            1 + (-1) = 0 carry 0

        Args:
            a, b: Trit lists in {-1, 0, +1}, LSB first.

        Returns:
            Sum as trit list, LSB first.
        """
        max_len = max(len(a), len(b))
        a = a + [0] * (max_len - len(a))
        b = b + [0] * (max_len - len(b))

        result = []
        carry = 0
        for i in range(max_len):
            s = a[i] + b[i] + carry
            if s == 2:
                result.append(-1)
                carry = 1
            elif s == -2:
                result.append(1)
                carry = -1
            elif s == 3:
                result.append(0)
                carry = 1
            elif s == -3:
                result.append(0)
                carry = -1
            else:
                result.append(s)
                carry = 0

        if carry != 0:
            result.append(carry)

        return result

    @staticmethod
    def carry_free_addition(a: List[int], b: List[int]) -> Tuple[List[int], bool]:
        """Attempt carry-free addition using Avizienis signed-digit arithmetic.

        In the Avizienis redundant representation with digit set {-1, 0, 1, 2}
        or {-2, -1, 0, 1}, addition can be done in O(1) time per digit
        (no carry chain) at the cost of redundancy.

        For ternary ROM, this is relevant because the adder tree
        accumulation can use redundant intermediates to avoid carry
        propagation delays.

        Args:
            a, b: Trit lists in {-1, 0, +1}, LSB first.

        Returns:
            (result_trits, is_carry_free) where result may use extended
            digit set {-2, -1, 0, 1, 2}.
        """
        max_len = max(len(a), len(b))
        a = a + [0] * (max_len - len(a))
        b = b + [0] * (max_len - len(b))

        result = []
        is_carry_free = True
        for i in range(max_len):
            s = a[i] + b[i]
            if s in (-1, 0, 1):
                result.append(s)
            else:
                # Need carry — not fully carry-free for this digit
                # But we store the redundant result
                result.append(s)
                is_carry_free = False

        return result, is_carry_free

    # ------------------------------------------------------------------
    # Cantor set analysis
    # ------------------------------------------------------------------

    @staticmethod
    def cantor_set_analysis(weights: np.ndarray) -> CantorAnalysis:
        """Analyze a ternary weight matrix through the Cantor set lens.

        The middle-third Cantor set is constructed by repeatedly removing
        the open middle third of intervals. In the context of ternary
        quantization, the "removed" intervals represent weight values
        that are mapped to zero — information that is destroyed.

        The Hausdorff dimension of the Cantor set is ln(2)/ln(3) ~ 0.6309,
        meaning the quantized weight space has fractal dimension 0.6309
        of the original.

        Args:
            weights: Original weight array before quantization.

        Returns:
            CantorAnalysis with fractal and information-theoretic metrics.
        """
        w = np.asarray(weights, dtype=np.float64).ravel()
        n = len(w)
        w_abs_max = np.max(np.abs(w)) if n > 0 else 1.0

        if w_abs_max == 0:
            return CantorAnalysis(
                total_weights=n,
                zero_fraction=1.0,
                cantor_measure=0.0,
                information_preserved=0.0,
                forbidden_intervals=0,
                effective_bits_per_weight=0.0,
            )

        # Normalize weights to [-1, 1]
        w_norm = w / w_abs_max

        # Apply BitNet b1.58 quantization to find the alpha
        alpha = float(np.mean(np.abs(w_norm)))
        if alpha == 0:
            zero_frac = 1.0
        else:
            w_t = np.round(w_norm / alpha).clip(-1, 1).astype(np.int8)
            zero_frac = float(np.mean(w_t == 0))

        # Hausdorff measure of the Cantor set:
        # The ternary quantization with threshold alpha creates a set
        # of representable values. The "Cantor-like" measure is:
        #   mu = (fraction of non-zero weights) * (alpha / w_abs_max)
        # This captures how much of the original value range is preserved.
        nonzero_frac = 1.0 - zero_frac
        cantor_measure = nonzero_frac * (alpha / w_abs_max) if w_abs_max > 0 else 0.0

        # Information preserved: ratio of ternary entropy to original entropy
        # Original: continuous distribution, approximate as uniform for the measure
        # Ternary: 3 states with empirical probabilities
        if alpha > 0:
            w_t_full = np.round(w_norm / alpha).clip(-1, 1).astype(np.int8)
            counts = np.bincount(w_t_full + 1, minlength=3).astype(float)
            probs = counts / counts.sum()
            probs_pos = probs[probs > 0]
            ternary_entropy = float(-np.sum(probs_pos * np.log2(probs_pos)))
            # Maximum entropy for ternary = log2(3)
            info_preserved = ternary_entropy / np.log2(3)
        else:
            info_preserved = 0.0

        # Count forbidden intervals (Cantor set iterations where
        # the middle third was "removed")
        # Each zero-weight represents a point in a "removed" interval
        # The number of distinct forbidden ranges depends on the alpha value
        if alpha > 0:
            # The ternary quantization creates floor(1/alpha) forbidden bands
            # in the normalized [-1, 1] range
            forbidden = max(0, int(np.floor(1.0 / alpha)) - 1)
        else:
            forbidden = 0

        # Effective bits per weight: log2(3) * (1 - zero_fraction) for non-zero,
        # plus 0 for zero weights. Weighted average.
        effective_bpw = np.log2(3) * nonzero_frac

        return CantorAnalysis(
            total_weights=n,
            zero_fraction=zero_frac,
            cantor_measure=cantor_measure,
            information_preserved=info_preserved,
            forbidden_intervals=forbidden,
            effective_bits_per_weight=effective_bpw,
        )

    # ------------------------------------------------------------------
    # Redundant number analysis for adder optimization
    # ------------------------------------------------------------------

    @staticmethod
    def redundant_adder_analysis(ternary_weights: np.ndarray) -> RedundantNumberAnalysis:
        """Analyze the carry-free addition potential of a ternary weight column.

        For a column of ternary weights being accumulated (the MAC operation
        in a ROM array), this computes how many +1/-1 cancellation pairs
        exist and whether carry-free addition is achievable.

        The key insight: in balanced ternary, +1 + (-1) = 0 with NO carry.
        If weights are arranged so that +1 and -1 alternate or are
        adjacent, carry propagation is minimized.

        Args:
            ternary_weights: 1-D array of ternary weights {-1, 0, +1}.

        Returns:
            RedundantNumberAnalysis with carry propagation statistics.
        """
        w = np.asarray(ternary_weights, dtype=np.int8).ravel()
        n = len(w)

        if n == 0:
            return RedundantNumberAnalysis(
                max_carry_propagation=0,
                average_carry_propagation=0.0,
                cancellation_pairs=0,
                cancellation_fraction=0.0,
                dynamic_range_reduction=1.0,
                carry_free_achievable=True,
            )

        # Count +1 and -1
        n_plus = int(np.sum(w == 1))
        n_minus = int(np.sum(w == -1))
        n_zero = int(np.sum(w == 0))

        # Cancellation pairs: min(+1, -1) weights cancel
        cancellation_pairs = min(n_plus, n_minus)
        cancellation_fraction = cancellation_pairs / max(n_plus + n_minus, 1)

        # Net sum after cancellation
        net_sum = n_plus - n_minus

        # Dynamic range: original max is n (all +1), after cancellation it's |net_sum|
        original_range = n_plus + n_minus
        reduced_range = abs(net_sum)
        dynamic_range_reduction = (original_range / reduced_range) if reduced_range > 0 else float('inf')

        # Carry propagation analysis
        # For the remaining net weights, carry can propagate at most
        # ceil(log3(|net_sum| + 1)) positions in balanced ternary
        if net_sum != 0:
            max_carry = int(np.ceil(np.log(abs(net_sum) + 1) / np.log(3)))
        else:
            max_carry = 0

        # Average carry propagation: for random ternary sequences,
        # the expected carry chain length is O(1) due to cancellation
        # For structured sequences, it can be O(log n) or O(n)
        if n > 0 and (n_plus + n_minus) > 0:
            # Estimate: carry chains form where consecutive non-cancelled
            # weights have the same sign
            signs = w[w != 0]
            if len(signs) > 1:
                same_sign_runs = np.sum(signs[1:] == signs[:-1])
                avg_carry = 1.0 + same_sign_runs / len(signs)
            else:
                avg_carry = 0.0
        else:
            avg_carry = 0.0

        # Carry-free achievable if all +1/-1 pairs cancel completely
        carry_free = (net_sum == 0) or (n_plus == 0) or (n_minus == 0)

        return RedundantNumberAnalysis(
            max_carry_propagation=max_carry,
            average_carry_propagation=avg_carry,
            cancellation_pairs=cancellation_pairs,
            cancellation_fraction=cancellation_fraction,
            dynamic_range_reduction=dynamic_range_reduction,
            carry_free_achievable=carry_free,
        )

    # ------------------------------------------------------------------
    # Ternary divisibility and modular arithmetic
    # ------------------------------------------------------------------

    @staticmethod
    def ternary_weight_parity(weights: np.ndarray) -> Dict[str, int]:
        """Compute parity and modular properties of a ternary weight matrix.

        In balanced ternary, a number is divisible by 2 if the sum of
        its trits is divisible by 2, and divisible by 4 if the sum
        in base 9 is divisible by 4. These properties affect the
        distribution of possible outputs from a ternary MAC.

        Args:
            weights: 2-D ternary weight matrix {-1, 0, +1}.

        Returns:
            Dict with parity statistics.
        """
        w = np.asarray(weights, dtype=np.int8)
        row_sums = np.sum(w, axis=1)
        col_sums = np.sum(w, axis=0)

        return {
            "rows": w.shape[0],
            "cols": w.shape[1],
            "row_sum_even": int(np.sum(np.abs(row_sums) % 2 == 0)),
            "row_sum_odd": int(np.sum(np.abs(row_sums) % 2 == 1)),
            "col_sum_even": int(np.sum(np.abs(col_sums) % 2 == 0)),
            "col_sum_odd": int(np.sum(np.abs(col_sums) % 2 == 1)),
            "total_sum": int(np.sum(w)),
            "row_sum_mean": float(np.mean(np.abs(row_sums))),
            "row_sum_std": float(np.std(row_sums)),
            "col_sum_mean": float(np.mean(np.abs(col_sums))),
            "col_sum_std": float(np.std(col_sums)),
        }

    @staticmethod
    def trit_wise_complexity(weights: np.ndarray) -> float:
        """Compute the algorithmic complexity of a ternary weight matrix.

        Uses a normalized Lempel-Ziv-like measure on the ternary
        sequence to estimate how "compressible" the weight pattern is.
        A weight matrix with simple structure (all +1, checkerboard, etc.)
        has low complexity; a random-looking matrix has high complexity.

        This matters for ROM design because structured patterns can
        be exploited for layout optimization (e.g., word-line sharing,
        bit-line compression).

        Args:
            weights: 2-D ternary weight matrix {-1, 0, +1}.

        Returns:
            Complexity score in [0, 1] where 0 = maximally structured,
            1 = random.
        """
        w = np.asarray(weights, dtype=np.int8).ravel()
        n = len(w)
        if n <= 1:
            return 0.0

        # Convert to a string of characters for LZ-like analysis
        # Map: -1 -> 'T', 0 -> '0', +1 -> '1'
        char_map = {1: '1', 0: '0', -1: 'T'}
        sequence = ''.join(char_map.get(int(v), '0') for v in w)

        # Simple LZ complexity: count distinct substrings of increasing length
        # Normalize by the maximum possible (random sequence)
        vocab_sizes = []
        for length in range(1, min(8, n // 2 + 1)):
            substrings = set()
            for i in range(n - length + 1):
                substrings.add(sequence[i:i + length])
            vocab_sizes.append(len(substrings))

        if not vocab_sizes:
            return 0.0

        # Maximum distinct substrings of length L from alphabet of size 3
        max_vocab = [min(3 ** L, n - L + 1) for L in range(1, len(vocab_sizes) + 1)]

        # Normalize and average
        ratios = [v / m if m > 0 else 0 for v, m in zip(vocab_sizes, max_vocab)]
        return float(np.mean(ratios))

    # ------------------------------------------------------------------
    # Balanced ternary efficiency theorems
    # ------------------------------------------------------------------

    @staticmethod
    def radix_efficiency(base: int = 3) -> Dict[str, float]:
        """Compute the radix efficiency of a number base for weight representation.

        Hayes (2001) showed that base-3 is optimal for minimizing
        the product (radix) * (digits needed). The efficiency measure is:

            eta(b) = b^{1/log2(b)} = e^{ln(b)/log2(b)} = e^{ln(2)} = 2  [constant!]

        But the *area* efficiency for ROM is:
            eta_area(b) = log2(b) / (cell_area(b) / cell_area(2))

        For ternary ROM, log2(3) = 1.585 bits per cell, and the cell
        area is essentially the same as binary (same transistor, different
        read threshold), giving 58.5% information density advantage.

        Args:
            base: Number base to analyze.

        Returns:
            Dict with efficiency metrics.
        """
        import math

        bits_per_digit = math.log2(base)
        digits_for_range = math.log(base)  # digits needed per decade
        radix_product = base * digits_for_range  # Hayes' measure

        # Ternary vs binary comparison
        ternary_advantage = math.log2(3) / math.log2(2)  # 1.585 bits vs 1 bit

        return {
            "base": base,
            "bits_per_digit": bits_per_digit,
            "digits_per_decade": digits_for_range,
            "radix_product": radix_product,
            "hayes_efficiency": math.log(2),  # constant for all bases
            "info_vs_binary": bits_per_digit,  # relative to binary's 1.0
            "ternary_density_advantage": ternary_advantage if base == 3 else 0.0,
            "optimal_base": 3,
        }

    @staticmethod
    def weight_range_trits(max_abs_value: float) -> int:
        """Compute minimum trits needed to represent a weight range.

        For balanced ternary, N trits represent [- (3^N - 1)/2, (3^N - 1)/2].

        Args:
            max_abs_value: Maximum absolute weight value.

        Returns:
            Minimum number of trits needed.
        """
        if max_abs_value <= 0:
            return 1
        # N trits: range = (3^N - 1) / 2
        n = 1
        while (3 ** n - 1) / 2 < max_abs_value:
            n += 1
        return n
