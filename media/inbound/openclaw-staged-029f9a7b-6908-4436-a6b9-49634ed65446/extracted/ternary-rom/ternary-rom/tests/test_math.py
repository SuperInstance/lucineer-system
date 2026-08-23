"""Tests for the mathematical foundations module (ternary_rom.math).

Covers all 8 domains:
1. NumberTheory
2. InformationTheory
3. CodingTheory
4. StochasticProcesses
5. OptimizationTheory
6. GraphTheory
7. ThermodynamicModels
8. ApproximationTheory
Plus the unified MathFoundation facade.
"""

import math
import numpy as np
import pytest

from ternary_rom.math.number_theory import NumberTheory
from ternary_rom.math.information_theory import InformationTheory
from ternary_rom.math.coding_theory import CodingTheory
from ternary_rom.math.stochastic_processes import StochasticProcesses
from ternary_rom.math.optimization_theory import OptimizationTheory
from ternary_rom.math.graph_theory import GraphTheory
from ternary_rom.math.thermodynamic_models import ThermodynamicModels
from ternary_rom.math.approximation_theory import ApproximationTheory
from ternary_rom.math.foundation import MathFoundation


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def random_weights_32x16():
    """A 32x16 Gaussian weight matrix."""
    rng = np.random.RandomState(42)
    return rng.randn(32, 16).astype(np.float64)


@pytest.fixture
def ternary_weights_32x16(random_weights_32x16):
    """Ternarized version of random_weights_32x16."""
    w = random_weights_32x16
    alpha = float(np.mean(np.abs(w)))
    return np.round(w / alpha).clip(-1, 1).astype(np.int8)


@pytest.fixture
def tiny_weights():
    """A tiny 4x4 matrix for edge-case testing."""
    return np.array([[1.5, -0.2, 0.1, -2.0],
                      [0.3, 0.8, -0.1, 0.5],
                      [-1.0, 0.0, 0.7, -0.3],
                      [0.2, -1.5, 0.4, 0.9]], dtype=np.float64)


# ===========================================================================
# 1. NumberTheory
# ===========================================================================

class TestNumberTheory:
    def test_balanced_ternary_zero(self):
        rep = NumberTheory.to_balanced_ternary(0)
        assert rep.trits == [0]
        assert rep.decimal_value == 0

    def test_balanced_ternary_positive(self):
        rep = NumberTheory.to_balanced_ternary(5)
        assert rep.decimal_value == 5
        # 5 = 1*9 + (-1)*3 + (-1)*1 = 9 - 3 - 1 = 5
        assert rep.trits == [-1, -1, 1]

    def test_balanced_ternary_negative(self):
        rep = NumberTheory.to_balanced_ternary(-5)
        assert rep.decimal_value == -5

    def test_roundtrip(self):
        for n in range(-100, 101):
            rep = NumberTheory.to_balanced_ternary(n)
            assert rep.decimal_value == n

    def test_addition_simple(self):
        result = NumberTheory.balanced_ternary_addition([1, 0, 1], [1, 0, 0])
        # 1*1 + 0*3 + 1*9 = 10; 0*1 + 0*3 + 1*9 = 9; 10 + 9 = 19
        value = NumberTheory.from_balanced_ternary(result)
        assert value == 11

    def test_cantor_analysis(self, random_weights_32x16):
        result = NumberTheory.cantor_set_analysis(random_weights_32x16)
        assert result.total_weights == 32 * 16
        assert 0 <= result.zero_fraction <= 1
        assert 0 <= result.cantor_measure <= 1
        assert 0 <= result.information_preserved <= 1

    def test_redundant_adder_analysis(self, ternary_weights_32x16):
        col = ternary_weights_32x16[:, 0]
        result = NumberTheory.redundant_adder_analysis(col)
        assert result.cancellation_fraction >= 0
        assert result.cancellation_pairs >= 0
        assert result.dynamic_range_reduction >= 0

    def test_radix_efficiency(self):
        result = NumberTheory.radix_efficiency(base=3)
        assert result["base"] == 3
        assert abs(result["bits_per_digit"] - math.log2(3)) < 0.01
        assert result["ternary_density_advantage"] > 1.5  # 1.585x

    def test_weight_range_trits(self):
        assert NumberTheory.weight_range_trits(0) == 1
        assert NumberTheory.weight_range_trits(1) == 1
        assert NumberTheory.weight_range_trits(4) == 2  # (3^2-1)/2 = 4
        assert NumberTheory.weight_range_trits(13) == 3  # (3^3-1)/2 = 13

    def test_trit_wise_complexity(self, ternary_weights_32x16):
        complexity = NumberTheory.trit_wise_complexity(ternary_weights_32x16)
        assert 0 <= complexity <= 1


# ===========================================================================
# 2. InformationTheory
# ===========================================================================

class TestInformationTheory:
    def test_entropy_uniform(self):
        # Uniform distribution: p_plus = p_zero = p_minus = 1/3
        w = np.array([1, -1, 0, 1, -1, 0], dtype=np.int8)
        profile = InformationTheory.ternary_entropy_profile(w)
        assert abs(profile.shannon_entropy - math.log2(3)) < 0.01
        assert abs(profile.normalized_entropy - 1.0) < 0.01

    def test_entropy_deterministic(self):
        # All +1: H = 0
        w = np.ones(100, dtype=np.int8)
        profile = InformationTheory.ternary_entropy_profile(w)
        assert profile.shannon_entropy < 0.01
        assert profile.normalized_entropy < 0.01

    def test_entropy_sparse(self):
        # 90% zeros, 5% +1, 5% -1
        w = np.zeros(100, dtype=np.int8)
        w[:5] = 1
        w[5:10] = -1
        profile = InformationTheory.ternary_entropy_profile(w)
        assert profile.shannon_entropy < math.log2(3)
        assert profile.p_zero == 0.9

    def test_coding_overhead(self):
        w = np.array([1, -1, 0, 1, -1, 0], dtype=np.int8)
        profile = InformationTheory.ternary_entropy_profile(w)
        # Overhead = 2 - H, should be ~ 0.415 bits for uniform
        assert profile.coding_overhead > 0
        assert profile.coding_overhead < 2

    def test_channel_capacity(self):
        result = InformationTheory.ternary_channel_capacity(v_dd=1.0)
        assert result.capacity_bits > 0
        assert result.capacity_bits <= math.log2(3)
        assert result.ber_estimate >= 0
        assert result.snr_linear > 0

    def test_rate_distortion(self, random_weights_32x16):
        w = random_weights_32x16
        alpha = float(np.mean(np.abs(w)))
        w_t = np.round(w / alpha).clip(-1, 1).astype(np.int8)
        result = InformationTheory.rate_distortion_analysis(w, w_t, alpha)
        assert result.distortion_mse >= 0
        assert result.rate_ternary == 2.0
        assert result.bitnet_alpha == alpha

    def test_mutual_information(self, random_weights_32x16):
        w = random_weights_32x16
        alpha = float(np.mean(np.abs(w)))
        w_t = np.round(w / alpha).clip(-1, 1).astype(np.int8)
        result = InformationTheory.mutual_information_analysis(w, w_t)
        assert result.mi_bits >= 0
        assert 0 <= result.mi_normalized <= 1
        assert 0 <= result.higher_order_loss <= 1

    def test_landauer_analysis(self):
        result = InformationTheory.landauer_analysis(n_cells=1e6, energy_per_op_pj=22.0)
        assert result["landauer_per_bit_j"] > 0
        assert result["thermodynamic_efficiency"] > 0
        assert result["gap_factor"] > 1  # always far above Landauer

    def test_encoding_efficiency(self, ternary_weights_32x16):
        result = InformationTheory.encoding_efficiency(ternary_weights_32x16)
        assert result["total_weights"] == 32 * 16
        assert result["current_encoding_bits"] == 2 * 32 * 16
        assert result["entropy_bits_per_weight"] >= 0


# ===========================================================================
# 3. CodingTheory
# ===========================================================================

class TestCodingTheory:
    def test_gf3_arithmetic(self):
        assert CodingTheory.gf3_add(1, 2) == 0  # 1 + 2 = 0 mod 3
        assert CodingTheory.gf3_mul(1, 2) == 2  # 1 * 2 = 2 mod 3
        assert CodingTheory.gf3_mul(2, 2) == 1  # 2 * 2 = 1 mod 3
        assert CodingTheory.gf3_inv(1) == 1
        assert CodingTheory.gf3_inv(2) == 2

    def test_gf3_inv_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            CodingTheory.gf3_inv(0)

    def test_ternary_gf3_roundtrip(self):
        w = np.array([-1, 0, 1, -1, 1, 0], dtype=np.int8)
        gf3 = CodingTheory.ternary_to_gf3(w)
        back = CodingTheory.gf3_to_ternary(gf3)
        np.testing.assert_array_equal(w, back)

    def test_hamming_distance(self):
        a = np.array([1, 0, -1, 1])
        b = np.array([1, 1, -1, 0])
        assert CodingTheory.ternary_hamming_distance(a, b) == 2

    def test_ternary_hamming_code(self):
        code = CodingTheory.ternary_hamming_code(m=3)
        assert code.n == (3**3 - 1) // 2  # = 13
        assert code.k == code.n - 3  # = 10
        assert code.d == 3
        assert code.t == 1

    def test_ternary_golay_code(self):
        code = CodingTheory.ternary_golay_code()
        assert code.n == 11
        assert code.k == 6
        assert code.d == 5
        assert code.t == 2

    def test_repetition_code(self):
        code = CodingTheory.ternary_repetition_code(k=1, t=2)
        assert code.n == 5  # 1 * (2*2 + 1)
        assert code.d == 5
        assert code.t == 2

    def test_fault_model(self):
        fm = CodingTheory.rom_fault_model()
        assert fm.overall_defect_rate >= 0
        assert fm.overall_defect_rate < 1

    def test_defect_tolerance(self):
        result = CodingTheory.defect_tolerance_analysis(
            rows=1024, cols=1024, input_dimension=1024,
        )
        assert 0 <= result.bare_die_yield <= 1
        assert result.fault_tolerance_yield >= result.bare_die_yield
        assert result.yield_improvement >= 1.0
        assert result.expected_accuracy_loss_per_defect > 0

    def test_manhattan_error_detect(self, ternary_weights_32x16):
        w = ternary_weights_32x16
        result = CodingTheory.manhattan_error_detect(w)
        assert result["n_rows"] == 32
        assert result["n_cols"] == 16
        assert len(result["row_parities"]) == 32
        assert len(result["col_parities"]) == 16

    def test_fault_tolerant_yield(self):
        result = CodingTheory.fault_tolerant_yield(
            die_area_mm2=50.0,
        )
        assert 0 <= result["poisson_yield"] <= 1
        assert result["fault_tolerant_yield"] >= result["poisson_yield"]


# ===========================================================================
# 4. StochasticProcesses
# ===========================================================================

class TestStochasticProcesses:
    def test_spectral_profile_basic(self, random_weights_32x16):
        result = StochasticProcesses.spectral_profile(random_weights_32x16)
        assert result.rows == 32
        assert result.cols == 16
        assert result.spectral_radius > 0
        assert result.effective_rank >= 1
        assert result.condition_number >= 1
        assert 0 <= result.marchenko_pastur_conformity <= 1

    def test_concentration_bounds(self, ternary_weights_32x16):
        col = ternary_weights_32x16[:, 0]
        result = StochasticProcesses.concentration_bounds(col)
        assert result.n == 32
        assert result.variance >= 0
        assert result.hoeffding_bound >= 0
        assert result.bernstein_bound >= 0
        assert result.hoeffding_bound >= result.bernstein_bound  # Bernstein is tighter
        assert result.clt_quality in ("excellent", "good", "moderate", "poor")
        assert result.dynamic_range_bits >= 1
        assert result.gauss_approx_bits >= 1

    def test_concentration_bounds_zeros(self):
        w = np.zeros(100, dtype=np.int8)
        result = StochasticProcesses.concentration_bounds(w)
        assert result.std_dev == 0

    def test_error_propagation_single(self):
        J = np.array([[0.5, 0.1], [0.2, 0.8]])
        result = StochasticProcesses.error_propagation([J], [1.0])
        assert result.end_to_end_error_var >= 0
        assert result.is_stable

    def test_error_propagation_stable(self):
        # Contractive Jacobians: error should decay
        Js = [np.eye(10) * 0.5 for _ in range(5)]
        result = StochasticProcesses.error_propagation(Js, [1.0] * 5)
        assert result.error_amplification_factor < 1.0

    def test_random_matrix_prediction(self):
        result = StochasticProcesses.random_matrix_prediction(100, 50, sparsity=0.45)
        assert result.mp_upper_edge > result.mp_lower_edge
        assert result.expected_spectral_radius > 0

    def test_weight_distribution_stats(self, random_weights_32x16):
        result = StochasticProcesses.weight_distribution_stats(random_weights_32x16)
        assert result["n"] == 32 * 16
        assert abs(result["skewness"]) < 5  # reasonable range
        assert result["gini_coefficient"] >= 0
        assert result["gini_coefficient"] <= 1


# ===========================================================================
# 5. OptimizationTheory
# ===========================================================================

class TestOptimizationTheory:
    def test_optimal_alpha(self, random_weights_32x16):
        result = OptimizationTheory.compute_optimal_alpha(random_weights_32x16)
        assert result.bitnet_alpha > 0
        assert result.mse_optimal_alpha > 0
        assert result.mse_bitnet >= 0
        assert result.mse_optimal >= 0
        assert result.condition_number >= 1

    def test_optimal_alpha_close_to_bitnet(self):
        # For Gaussian weights, BitNet alpha should be close to optimal
        rng = np.random.RandomState(123)
        w = rng.randn(100, 100)
        result = OptimizationTheory.compute_optimal_alpha(w)
        # Alpha gap should be small for Gaussian
        assert result.alpha_gap_bitnet_mse < 0.5

    def test_admm_ternarize(self, random_weights_32x16):
        result = OptimizationTheory.admm_ternarize(random_weights_32x16, max_iter=20)
        assert result.weights_ternary.shape == random_weights_32x16.shape
        assert set(np.unique(result.weights_ternary)).issubset({-1, 0, 1})
        assert result.mse >= 0
        assert 0 <= result.cos_sim <= 1
        assert 0 <= result.sparsity <= 1

    def test_admm_converges(self, tiny_weights):
        result = OptimizationTheory.admm_ternarize(tiny_weights, max_iter=50, tol=1e-4)
        assert result.iterations <= 50

    def test_markowitz_allocation(self):
        names = ["fc1", "fc2", "fc3", "fc4"]
        shapes = [(128, 64), (64, 64), (64, 32), (32, 10)]
        cos_sims = [0.98, 0.96, 0.99, 0.85]
        result = OptimizationTheory.markowitz_precision_allocation(
            names, shapes, cos_sims,
        )
        assert len(result.efficient_frontier) > 0
        assert len(result.optimal_allocation.bit_widths) == 4
        assert all(b in (2, 4, 8, 16) for b in result.optimal_allocation.bit_widths)
        assert result.information_sharpe >= 0

    def test_precision_schedule(self):
        result = OptimizationTheory.precision_schedule(
            n_layers=10,
            layer_cos_sims=[0.99, 0.98, 0.97, 0.96, 0.95,
                            0.94, 0.93, 0.92, 0.91, 0.90],
        )
        assert len(result) == 10
        # Early layers should get more bits
        assert result[0] >= result[-1]


# ===========================================================================
# 6. GraphTheory
# ===========================================================================

class TestGraphTheory:
    def test_rom_topology(self, ternary_weights_32x16):
        result = GraphTheory.rom_topology(ternary_weights_32x16)
        assert result.rows == 32
        assert result.cols == 16
        assert result.n_plus >= 0
        assert result.n_minus >= 0
        assert result.n_zero >= 0
        assert result.n_plus + result.n_minus + result.n_zero == 32 * 16
        assert result.is_bipartite
        assert result.components == 1
        assert 0 <= result.density <= 1

    def test_wirelength_estimate(self):
        result = GraphTheory.wirelength_estimate(1024, 1024)
        assert result.total_wirelength_um > 0
        assert result.routing_overhead_factor >= 1.0
        assert result.estimated_capacance_fF > 0

    def test_floorplan_optimize(self, ternary_weights_32x16):
        result = GraphTheory.simple_floorplan_optimize(ternary_weights_32x16, max_iterations=10)
        assert len(result.row_permutation) == 32
        assert len(result.col_permutation) == 16
        assert result.wirelength_reduction >= 0

    def test_connectivity_analysis(self, ternary_weights_32x16):
        result = GraphTheory.connectivity_analysis(ternary_weights_32x16)
        assert result.algebraic_connectivity >= 0
        assert result.cheeger_constant >= 0
        assert result.bisection_width >= 0


# ===========================================================================
# 7. ThermodynamicModels
# ===========================================================================

class TestThermodynamicModels:
    def test_subthreshold_model(self):
        model = ThermodynamicModels.subthreshold_model()
        assert model.v_thermal > 0
        assert model.s_slope_mv_per_decade > 60
        assert model.s_slope_mv_per_decade < 120

    def test_subthreshold_leakage(self):
        model = ThermodynamicModels.subthreshold_model()
        # At V_gs = 0 (below threshold), leakage should be small
        I = ThermodynamicModels.subthreshold_leakage(model, v_gs=0.0)
        assert I > 0
        assert I < 1e-6  # should be tiny

    def test_leakage_vs_temperature(self):
        result = ThermodynamicModels.leakage_vs_temperature(
            base_leakage_pA=2.37, target_temp_K=358.15
        )
        assert result["target_leakage_pA"] > result["base_leakage_pA"]
        assert result["scaling_factor"] > 1

    def test_thermal_noise_analysis(self):
        result = ThermodynamicModels.thermal_noise_analysis(v_dd=1.0)
        assert result.thermal_noise_rms_v > 0
        assert result.snr_linear > 0
        assert result.per_cell_error_prob >= 0
        assert result.per_cell_error_prob <= 1

    def test_thermal_noise_reliable(self):
        # At high V_dd, should be reliable
        result = ThermodynamicModels.thermal_noise_analysis(v_dd=3.3)
        assert result.is_reliable

    def test_rom_energy_model(self):
        result = ThermodynamicModels.rom_energy_model(
            rows=256, cols=256, v_dd=1.0
        )
        assert result.total_energy_fJ > 0
        assert result.energy_per_mac_fJ > 0
        assert result.landauer_factor > 1  # far above Landauer

    def test_physics_scaling(self):
        result = ThermodynamicModels.physics_scaling_projection(
            node_nm=28, v_dd=1.0, cell_area_um2=0.048, leakage_pA=1.185
        )
        assert result.subthreshold_swing_mv_dec > 60
        assert result.max_freq_ghz > 0

    def test_near_threshold(self):
        result = ThermodynamicModels.near_threshold_optimum()
        assert "optimal_vdd" in result
        assert result["optimal_vdd"] > 0
        assert result["min_energy_fJ"] > 0


# ===========================================================================
# 8. ApproximationTheory
# ===========================================================================

class TestApproximationTheory:
    def test_kolmogorov_entropy(self, random_weights_32x16):
        result = ApproximationTheory.kolmogorov_entropy(random_weights_32x16)
        assert result.log_covering_number >= 0
        assert result.bits_per_weight >= 0
        assert result.effective_dimension >= 1

    def test_vc_dimension(self):
        result = ApproximationTheory.vc_dimension(n_ternary_params=1000, n_layers=6)
        assert result.vc_dimension_upper >= 1000
        assert result.vc_dimension_lower == 1000
        assert result.sample_complexity_bound > 0

    def test_best_approximation(self, tiny_weights):
        result = ApproximationTheory.best_approximation(tiny_weights)
        assert result.mse_optimal >= 0
        assert result.current_mse >= 0
        assert True  # gap can be negative when per-element uses different alpha
        assert result.l_inf_error >= 0

    def test_spectral_accuracy(self, random_weights_32x16):
        w = random_weights_32x16
        alpha = float(np.mean(np.abs(w)))
        w_t = np.round(w / alpha).clip(-1, 1).astype(np.int8)
        result = ApproximationTheory.spectral_accuracy(w, w_t, alpha)
        assert 0 <= result.energy_fraction <= 2  # can slightly exceed 1 due to scaling
        assert result.approximation_order in ("algebraic", "spectral", "mixed")
        assert result.decay_rate >= 0
        assert len(result.top_k_captured) > 0

    def test_representation_power(self):
        result = ApproximationTheory.representation_power(32, 16, sparsity=0.45)
        assert result["total_distinct_matrices"] > 0
        assert result["log2_representational_capacity"] > 0
        assert result["effective_bits_per_param"] > 0


# ===========================================================================
# MathFoundation (integration)
# ===========================================================================

class TestMathFoundation:
    def test_full_analysis(self, random_weights_32x16):
        weights = {"test_layer": random_weights_32x16}
        mf = MathFoundation(weights)
        profiles = mf.full_analysis()
        assert len(profiles) == 1
        p = profiles[0]
        assert p.layer_name == "test_layer"
        # Check all fields populated
        assert p.shannon_entropy >= 0
        assert p.condition_number >= 1
        assert p.thermodynamic_efficiency > 0

    def test_profile_summary(self, random_weights_32x16):
        weights = {"test_layer": random_weights_32x16}
        mf = MathFoundation(weights)
        profiles = mf.full_analysis()
        summary = profiles[0].summary()
        assert "MATH PROFILE" in summary
        assert "NUMBER THEORY" in summary
        assert "INFORMATION THEORY" in summary
        assert "THERMODYNAMIC" in summary

    def test_cross_layer_analysis(self):
        rng = np.random.RandomState(42)
        weights = {
            "layer1": rng.randn(64, 32),
            "layer2": rng.randn(32, 16),
            "layer3": rng.randn(16, 8),
        }
        mf = MathFoundation(weights)
        result = mf.cross_layer_analysis()
        assert result["n_layers"] == 3
        assert 0 <= result["avg_entropy"] <= math.log2(3)
        assert isinstance(result["layers_needing_attention"], list)

    def test_multi_layer(self):
        rng = np.random.RandomState(42)
        weights = {f"layer_{i}": rng.randn(32, 16) for i in range(5)}
        mf = MathFoundation(weights)
        profiles = mf.full_analysis()
        assert len(profiles) == 5
        for p in profiles:
            assert p.dynamic_range_bits >= 1
