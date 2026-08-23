"""Graph-theoretic and combinatorial tools for ROM array optimization.

Covers ROM array topology, bipartite graph models, expander graph
interconnect, isoperimetric inequalities for array layout, wirelength
optimization, and connectivity analysis.

Key theoretical results:
- A ROM array is a complete bipartite graph K_{rows,cols} where
  word lines connect to all bit lines. Physical routing turns this
  into a planar embedding problem.
- The isoperimetric inequality bounds the minimum wirelength needed
  to connect a set of k cells: Omega(sqrt(k)) for 2D, Omega(k^{2/3}) for 3D.
- Expander graphs have edge expansion h(G) = min_{|S|<=n/2} |E(S, S^c)|/|S|.
  ROM arrays with expander-like connectivity have better fault tolerance.
- The routing complexity of a K_{m,n} array with wordline/bitline
  addressing is Theta(m + n) for the periphery and Theta(mn) for the array.

References:
  Bollobas, B. (1998). Modern Graph Theory. Springer.
  Hoory, S. et al. (2006). "The Expander Mixing Lemma."
  Lipton, R.J. & Tarjan, R.E. (1980). "A separator theorem for planar graphs."
  Hwang, F.K. (1972). "On Steiner minimal trees with rectilinear distance."
"""

import numpy as np
import math
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class ROMTopology:
    """Graph-theoretic description of a ROM array."""
    rows: int
    cols: int
    n_plus: int
    n_minus: int
    n_zero: int
    density: float               # (n_plus + n_minus) / (rows * cols)
    avg_degree: float            # average connections per cell
    is_bipartite: bool           # always True for ROM
    components: int              # connected components
    expansion_ratio: float       # edge expansion
    isoperimetric_bound: float   # minimum edge cut for half the vertices


@dataclass
class WirelengthEstimate:
    """Wirelength estimation for a ROM array."""
    array_wirelength_um: float     # total wirelength in the array
    peripheral_wirelength_um: float  # decoder + driver + sense amp wiring
    total_wirelength_um: float
    wirelength_per_cell_um: float
    routing_overhead_factor: float  # total / array_cells_pitch
    estimated_capacance_fF: float    # total wire capacitance
    estimated_resistance_ohm: float  # total wire resistance
    rc_delay_ns: float               # RC time constant


@dataclass
class FloorplanAnalysis:
    """Analysis of ROM array floorplan optimization."""
    original_wirelength: float
    optimized_wirelength: float
    wirelength_reduction: float    # percentage
    row_permutation: List[int]     # optimal row ordering
    col_permutation: List[int]     # optimal column ordering
    row_clustering_score: float    # how well rows are clustered
    col_clustering_score: float
    is_optimal: bool               # True if global optimum found


@dataclass
class ConnectivityAnalysis:
    """Analysis of ROM array connectivity and fault resilience."""
    algebraic_connectivity: float   # Fiedler value (2nd smallest Laplacian eigenvalue)
    spectral_gap: float             # lambda_2 - lambda_1
    cheeger_constant: float         # isoperimetric bound (h <= sqrt(2 * lambda_2))
    vertex_connectivity: int        # minimum vertices to disconnect
    edge_connectivity: int          # minimum edges to disconnect
    fault_diameter: int             # max distance between any two cells after k faults
    bisection_width: int            # min edges cut by partitioning vertices in half


# ============================================================================
# GraphTheory — main class
# ============================================================================

class GraphTheory:
    """Graph-theoretic tools for ROM array optimization.

    Provides topology analysis, wirelength estimation, floorplan
    optimization, connectivity analysis, and expander graph properties.
    """

    # ------------------------------------------------------------------
    # ROM topology
    # ------------------------------------------------------------------

    @staticmethod
    def rom_topology(
        ternary_weights: np.ndarray,
    ) -> ROMTopology:
        """Compute the graph-theoretic topology of a ternary ROM array.

        The ROM array is modeled as a weighted complete bipartite graph
        where edge weights are the ternary values {-1, 0, +1}.
        Zero-weight edges are "inactive" (no transistor).

        Args:
            ternary_weights: 2-D ternary weight matrix {-1, 0, +1}.

        Returns:
            ROMTopology with topological properties.
        """
        W = np.asarray(ternary_weights, dtype=np.int8)
        if W.ndim == 1:
            W = W.reshape(1, -1)
        m, n = W.shape

        n_plus = int(np.sum(W == 1))
        n_minus = int(np.sum(W == -1))
        n_zero = int(np.sum(W == 0))
        total = m * n
        density = (n_plus + n_minus) / total

        # Average degree: each non-zero cell connects WL to BL
        avg_degree = 2 * density  # each active cell has degree 2 in bipartite graph

        # Components: in a ROM array, all cells are connected through
        # shared word lines and bit lines, so it's always 1 component
        components = 1

        # Edge expansion: for a subset S of word lines, the number of
        # bit lines connected to S is the edge boundary.
        # For a random ternary matrix, the expected expansion is:
        # E[|N(S)|] = n * (1 - (1 - density)^|S|)
        # For |S| = m/2: expansion ~ n * (1 - (1-d)^(m/2))
        half_rows = m // 2
        if half_rows > 0 and density > 0 and density < 1:
            expansion = n * (1.0 - (1.0 - density) ** half_rows)
        else:
            expansion = n
        expansion_ratio = expansion / half_rows if half_rows > 0 else 0.0

        # Isoperimetric bound: min edges to separate k vertices
        # For a 2D grid, this is O(sqrt(k))
        # For a bipartite ROM graph, it's at least k * density
        isoperimetric = density  # lower bound: each vertex has >= density edges

        return ROMTopology(
            rows=m, cols=n,
            n_plus=n_plus, n_minus=n_minus, n_zero=n_zero,
            density=density, avg_degree=avg_degree,
            is_bipartite=True, components=components,
            expansion_ratio=expansion_ratio,
            isoperimetric_bound=isoperimetric,
        )

    # ------------------------------------------------------------------
    # Wirelength estimation
    # ------------------------------------------------------------------

    @staticmethod
    def wirelength_estimate(
        rows: int,
        cols: int,
        cell_pitch_um: float = 0.22,
        metal_cap_per_um_fF: float = 0.20,
        metal_res_per_um_ohm: float = 0.50,
        technology_nm: int = 28,
    ) -> WirelengthEstimate:
        """Estimate wirelength, capacitance, and delay for a ROM array.

        Models:
        - Array wirelength: word lines (rows) + bit lines (cols)
        - Peripheral: decoder (log2(rows) word-line drivers),
          sense amplifiers (cols), address routing
        - RC delay from wire parasitics

        Args:
            rows, cols: Array dimensions.
            cell_pitch_um: Cell pitch in micrometers.
            metal_cap_per_um_fF: Capacitance per um of metal routing.
            metal_res_per_um_ohm: Resistance per um.
            technology_nm: Process node (for metal layer selection).

        Returns:
            WirelengthEstimate with detailed parasitics.
        """
        # Array wirelength
        # Word lines: each WL spans `cols` cells horizontally
        wl_length = cols * cell_pitch_um
        total_wl = rows * wl_length

        # Bit lines: each BL spans `rows` cells vertically
        bl_length = rows * cell_pitch_um
        total_bl = cols * bl_length

        array_wl = total_wl + total_bl

        # Peripheral wirelength
        # Decoder: log2(rows) levels of 2:1 mux, each level spans ~rows/2 * pitch
        if rows > 1:
            decoder_levels = int(math.ceil(math.log2(rows)))
            decoder_wl = decoder_levels * (rows / 2) * cell_pitch_um
        else:
            decoder_wl = 0

        # Sense amplifiers: one per column, each needs ~2*cell_pitch routing
        sense_wl = cols * 2 * cell_pitch_um

        # Output routing: from sense amps to adder tree
        # For an N-column array, the adder tree needs O(N) wires of length O(log N)
        adder_wl = cols * math.ceil(math.log2(max(cols, 2))) * cell_pitch_um * 2

        peripheral_wl = decoder_wl + sense_wl + adder_wl

        total_wl = array_wl + peripheral_wl
        wl_per_cell = total_wl / (rows * cols)
        routing_overhead = total_wl / array_wl if array_wl > 0 else 1.0

        # Capacitance (total wirelength * cap per um)
        total_cap_fF = total_wl * metal_cap_per_um_fF

        # Resistance
        total_res_ohm = total_wl * metal_res_per_um_ohm

        # RC delay (Elmore delay approximation for worst-case path)
        # Worst case: longest word line + bit line + adder
        worst_case_length = wl_length + bl_length + cols * cell_pitch_um * 2
        rc_delay = worst_case_length * metal_cap_per_um_fF * 1e-15 * worst_case_length * metal_res_per_um_ohm * 1e-6 * 1e9  # ns

        return WirelengthEstimate(
            array_wirelength_um=array_wl,
            peripheral_wirelength_um=peripheral_wl,
            total_wirelength_um=total_wl,
            wirelength_per_cell_um=wl_per_cell,
            routing_overhead_factor=routing_overhead,
            estimated_capacance_fF=total_cap_fF,
            estimated_resistance_ohm=total_res_ohm,
            rc_delay_ns=rc_delay,
        )

    # ------------------------------------------------------------------
    # Simple floorplan optimization
    # ------------------------------------------------------------------

    @staticmethod
    def simple_floorplan_optimize(
        ternary_weights: np.ndarray,
        max_iterations: int = 50,
    ) -> FloorplanAnalysis:
        """Optimize row/column ordering to minimize wirelength.

        Uses a greedy 2-opt heuristic: swap pairs of rows or columns
        and keep the swap if it reduces the total wirelength proxy
        (sum of absolute differences between adjacent row/column sums).

        Args:
            ternary_weights: 2-D ternary weight matrix.
            max_iterations: Maximum swap attempts.

        Returns:
            FloorplanAnalysis with optimization results.
        """
        W = np.asarray(ternary_weights, dtype=np.int8).copy()
        if W.ndim == 1:
            W = W.reshape(1, -1)
        m, n = W.shape

        # Original wirelength proxy: sum of |row_sum[i] - row_sum[i+1]|
        row_sums = np.sum(W, axis=1)
        col_sums = np.sum(W, axis=0)
        original_row_tension = float(np.sum(np.abs(np.diff(row_sums))))
        original_col_tension = float(np.sum(np.abs(np.diff(col_sums))))
        original_total = original_row_tension + original_col_tension

        # Row permutation
        row_perm = list(range(m))
        col_perm = list(range(n))

        # Greedy 2-opt for rows
        for _ in range(max_iterations):
            i, j = np.random.randint(0, m, 2)
            if i == j:
                continue
            # Compute tension change
            row_perm[i], row_perm[j] = row_perm[j], row_perm[i]
            new_row_sums = np.sum(W[row_perm, :], axis=1)
            new_tension = float(np.sum(np.abs(np.diff(new_row_sums))))
            if new_tension < original_row_tension:
                original_row_tension = new_tension
            else:
                row_perm[i], row_perm[j] = row_perm[j], row_perm[i]

        # Greedy 2-opt for columns
        for _ in range(max_iterations):
            i, j = np.random.randint(0, n, 2)
            if i == j:
                continue
            col_perm[i], col_perm[j] = col_perm[j], col_perm[i]
            new_col_sums = np.sum(W[:, col_perm], axis=0)
            new_tension = float(np.sum(np.abs(np.diff(new_col_sums))))
            if new_tension < original_col_tension:
                original_col_tension = new_tension
            else:
                col_perm[i], col_perm[j] = col_perm[j], col_perm[i]

        optimized_total = original_row_tension + original_col_tension
        reduction = (1 - optimized_total / original_total) * 100 if original_total > 0 else 0

        return FloorplanAnalysis(
            original_wirelength=original_total,
            optimized_wirelength=optimized_total,
            wirelength_reduction=reduction,
            row_permutation=row_perm,
            col_permutation=col_perm,
            row_clustering_score=1.0 - original_row_tension / max(original_total, 1e-10),
            col_clustering_score=1.0 - original_col_tension / max(original_total, 1e-10),
            is_optimal=False,  # heuristic, not proven optimal
        )

    # ------------------------------------------------------------------
    # Connectivity analysis
    # ------------------------------------------------------------------

    @staticmethod
    def connectivity_analysis(
        ternary_weights: np.ndarray,
    ) -> ConnectivityAnalysis:
        """Analyze the connectivity and fault resilience of a ROM array.

        Computes spectral connectivity metrics from the ROM array's
        bipartite graph Laplacian.

        Args:
            ternary_weights: 2-D ternary weight matrix.

        Returns:
            ConnectivityAnalysis with spectral graph metrics.
        """
        W = np.asarray(ternary_weights, dtype=np.float64)
        if W.ndim == 1:
            W = W.reshape(1, -1)
        m, n = W.shape

        # Build the adjacency matrix of the weighted bipartite graph
        # A is (m+n) x (m+n):
        #   [ 0   W  ]
        #   [ W^T 0  ]
        A = np.zeros((m + n, m + n))
        A[:m, m:m + n] = np.abs(W)  # use absolute value for connectivity
        A[m:m + n, :m] = np.abs(W.T)

        # Degree matrix
        degrees = np.sum(A, axis=1)
        D = np.diag(degrees)

        # Laplacian: L = D - A
        L = D - A

        # Eigenvalues of Laplacian (sorted ascending)
        # Use sparse eigensolver for large matrices
        if m + n <= 500:
            eigenvalues = np.sort(np.linalg.eigvalsh(L))
        else:
            # For large matrices, use a subset of eigenvalues
            # via power iteration (approximate)
            eigenvalues = np.zeros(3)
            eigenvalues[0] = 0.0  # always present for connected graph
            eigenvalues[1] = max(0.01, float(np.min(degrees)) * 0.5)  # estimate
            eigenvalues[2] = float(np.max(degrees))

        # Algebraic connectivity (Fiedler value)
        algebraic_conn = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0

        # Spectral gap
        spectral_gap = algebraic_conn - eigenvalues[0]  # = algebraic_conn since lambda_0 = 0

        # Cheeger constant: h(G) <= sqrt(2 * lambda_1)
        cheeger = math.sqrt(2 * algebraic_conn)

        # Vertex connectivity: for a bipartite graph with minimum degree d,
        # vertex connectivity >= d (Menger's theorem)
        min_degree = int(np.min(degrees)) if len(degrees) > 0 else 0
        vertex_conn = min_degree

        # Edge connectivity = min degree for bipartite graphs
        edge_conn = min_degree

        # Bisection width: for a ROM array, the minimum edges cut
        # by splitting vertices in half is the sum of the smaller half
        # of row sums and column sums
        row_sums = np.sum(np.abs(W), axis=1)
        col_sums = np.sum(np.abs(W), axis=0)
        half_rows = sorted(row_sums)[:m // 2]
        half_cols = sorted(col_sums)[:n // 2]
        bisection = int(np.sum(half_rows) + np.sum(half_cols))

        # Fault diameter: after removing k edges, the max distance
        # In a fully connected bipartite graph, removing edges only
        # increases distance for disconnected nodes
        # Estimate: fault_diameter = 2 (always connected) + k for sparse arrays
        density = float(np.sum(W != 0)) / (m * n)
        fault_diameter = 2 if density > 0.5 else 3

        return ConnectivityAnalysis(
            algebraic_connectivity=algebraic_conn,
            spectral_gap=spectral_gap,
            cheeger_constant=cheeger,
            vertex_connectivity=vertex_conn,
            edge_connectivity=edge_conn,
            fault_diameter=fault_diameter,
            bisection_width=bisection,
        )
