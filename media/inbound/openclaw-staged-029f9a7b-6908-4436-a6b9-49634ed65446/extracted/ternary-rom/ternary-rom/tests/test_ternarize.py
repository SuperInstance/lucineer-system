"""Comprehensive tests for the ternarization engine.

All tests use numpy only (no torch dependency).
Deterministic via np.random.seed(42).
"""

import math
import numpy as np
import pytest

from ternary_rom.ternarize.engine import Ternarizer, TernarizeResult, TernarizeReport
from ternary_rom.ternarize.sensitivity import SensitivityAnalyzer, LayerSensitivity


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture(autouse=True)
def _seed():
    np.random.seed(42)


def _gaussian_matrix(shape=(128, 256)) -> np.ndarray:
    """Well-behaved Gaussian weights (should ternarize well)."""
    return np.random.randn(*shape).astype(np.float64)


def _high_dynamic_range_matrix(shape=(64, 128)) -> np.ndarray:
    """Weights with high dynamic range (sensitive to ternarization).

    Mix of very large and very small values — the kind of distribution
    you see in Mamba dt_proj layers.
    """
    w = np.random.randn(*shape).astype(np.float64)
    # Inject a few very large outliers
    n = w.size
    w.flat[np.random.choice(n, size=n // 10, replace=False)] *= 10.0
    # And some very small values
    w.flat[np.random.choice(n, size=n // 10, replace=False)] *= 0.01
    return w


# ======================================================================
# 1. ternarize_bitnet produces only {-1, 0, +1} values
# ======================================================================

class TestTernarizeBitnet:
    def test_output_values(self):
        """Ternarized weights contain only -1, 0, +1."""
        w = _gaussian_matrix()
        w_t, alpha = Ternarizer.ternarize_bitnet(w)
        unique = np.unique(w_t)
        assert set(unique.tolist()).issubset({-1, 0, 1})

    def test_alpha_equals_mean_abs(self):
        """alpha = mean(|W|) is computed correctly."""
        w = _gaussian_matrix()
        expected_alpha = float(np.mean(np.abs(w)))
        w_t, alpha = Ternarizer.ternarize_bitnet(w)
        assert abs(alpha - expected_alpha) < 1e-12

    def test_custom_alpha(self):
        """Providing a custom alpha is respected."""
        w = _gaussian_matrix()
        custom_alpha = 0.5
        w_t, alpha = Ternarizer.ternarize_bitnet(w, alpha=custom_alpha)
        assert alpha == custom_alpha
        unique = np.unique(w_t)
        assert set(unique.tolist()).issubset({-1, 0, 1})

    def test_all_zeros(self):
        """All-zero weights return all zeros, alpha=0."""
        w = np.zeros((4, 4), dtype=np.float64)
        w_t, alpha = Ternarizer.ternarize_bitnet(w)
        assert alpha == 0.0
        assert np.all(w_t == 0)

    def test_single_element(self):
        """Single-element array."""
        w = np.array([0.3])
        w_t, alpha = Ternarizer.ternarize_bitnet(w)
        assert set(w_t.tolist()).issubset({-1, 0, 1})

    def test_int8_dtype(self):
        """Output dtype is int8."""
        w = _gaussian_matrix()
        w_t, _ = Ternarizer.ternarize_bitnet(w)
        assert w_t.dtype == np.int8


# ======================================================================
# 2. cosine_similarity is positive for non-trivial weights
# ======================================================================

class TestCosineSimilarity:
    def test_positive_cos_sim(self):
        """cos_sim between original and ternary is > 0 for non-trivial weights."""
        w = _gaussian_matrix()
        w_t, alpha = Ternarizer.ternarize_bitnet(w)
        cos_sim = Ternarizer.cosine_similarity(w.ravel(), w_t.astype(np.float64).ravel())
        assert cos_sim > 0.0

    def test_identical_vectors(self):
        """cos_sim of a vector with itself is 1.0."""
        v = np.array([1.0, 2.0, 3.0])
        assert Ternarizer.cosine_similarity(v, v) == pytest.approx(1.0)

    def test_orthogonal_vectors(self):
        """cos_sim of orthogonal vectors is 0.0."""
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        assert Ternarizer.cosine_similarity(a, b) == pytest.approx(0.0)

    def test_zero_vectors(self):
        """cos_sim of two zero vectors is defined as 1.0."""
        z = np.zeros(5)
        assert Ternarizer.cosine_similarity(z, z) == 1.0

    def test_one_zero_vector(self):
        """cos_sim of zero with non-zero is 0.0."""
        z = np.zeros(5)
        v = np.ones(5)
        assert Ternarizer.cosine_similarity(z, v) == 0.0


# ======================================================================
# 3. pack_ternary / unpack_ternary round-trip is lossless
# ======================================================================

class TestPackUnpack:
    def test_roundtrip_exact(self):
        """pack → unpack is lossless for any ternary array."""
        w = _gaussian_matrix()
        w_t, _ = Ternarizer.ternarize_bitnet(w)
        packed = Ternarizer.pack_ternary(w_t)
        restored = Ternarizer.unpack_ternary(packed, w_t.shape)
        np.testing.assert_array_equal(w_t, restored)

    def test_roundtrip_all_values(self):
        """Round-trip works when all three values are present."""
        w = np.array([-1, 0, 1, -1, 0, 1, -1, 0, 1, 1, 1, -1], dtype=np.int8)
        packed = Ternarizer.pack_ternary(w)
        restored = Ternarizer.unpack_ternary(packed, w.shape)
        np.testing.assert_array_equal(w, restored)

    def test_pack_output_uint8(self):
        """Packed output is uint8."""
        w = np.array([1, 0, -1, 1], dtype=np.int8)
        packed = Ternarizer.pack_ternary(w)
        assert packed.dtype == np.uint8

    def test_pack_compression_ratio(self):
        """4 ternary weights → 1 byte."""
        w = np.ones(400, dtype=np.int8)
        packed = Ternarizer.pack_ternary(w)
        assert packed.shape == (100,)  # 400 / 4

    def test_pack_padding(self):
        """Non-multiple-of-4 lengths are padded correctly."""
        w = np.array([1, -1, 0], dtype=np.int8)  # 3 elements → 1 byte
        packed = Ternarizer.pack_ternary(w)
        assert packed.shape == (1,)
        restored = Ternarizer.unpack_ternary(packed, w.shape)
        np.testing.assert_array_equal(w, restored)

    def test_pack_encoding(self):
        """Verify exact bit encoding: 00=+1, 01=0, 10=-1."""
        # [+1, +1, +1, +1] → all 00 → byte 0x00
        w = np.array([1, 1, 1, 1], dtype=np.int8)
        packed = Ternarizer.pack_ternary(w)
        assert packed[0] == 0x00

        # [-1, -1, -1, -1] → all 10 → byte 0b10101010 = 0xAA
        w = np.array([-1, -1, -1, -1], dtype=np.int8)
        packed = Ternarizer.pack_ternary(w)
        assert packed[0] == 0xAA

        # [0, 0, 0, 0] → all 01 → byte 0b01010101 = 0x55
        w = np.array([0, 0, 0, 0], dtype=np.int8)
        packed = Ternarizer.pack_ternary(w)
        assert packed[0] == 0x55

    def test_roundtrip_2d(self):
        """Round-trip works for 2-D weight matrices."""
        w = np.random.choice([-1, 0, 1], size=(16, 32)).astype(np.int8)
        packed = Ternarizer.pack_ternary(w)
        restored = Ternarizer.unpack_ternary(packed, w.shape)
        np.testing.assert_array_equal(w, restored)


# ======================================================================
# 4. export_rom_bitmap produces correct mapping
# ======================================================================

class TestRomBitmap:
    def test_plus_one_mapping(self):
        """+1 → 0x00 (ROM_PLUS)."""
        w = np.array([1], dtype=np.int8)
        bmp = Ternarizer.export_rom_bitmap(w)
        assert bmp[0] == 0x00

    def test_zero_mapping(self):
        """0 → 0x01 (ROM_ZERO)."""
        w = np.array([0], dtype=np.int8)
        bmp = Ternarizer.export_rom_bitmap(w)
        assert bmp[0] == 0x01

    def test_minus_one_mapping(self):
        """-1 → 0x02 (ROM_MINUS)."""
        w = np.array([-1], dtype=np.int8)
        bmp = Ternarizer.export_rom_bitmap(w)
        assert bmp[0] == 0x02

    def test_mixed_values(self):
        """Mixed array produces correct byte sequence."""
        w = np.array([1, 0, -1, 1, -1, 0], dtype=np.int8)
        bmp = Ternarizer.export_rom_bitmap(w)
        expected = np.array([0x00, 0x01, 0x02, 0x00, 0x02, 0x01], dtype=np.uint8)
        np.testing.assert_array_equal(bmp, expected)

    def test_bitmap_preserves_shape(self):
        """Output shape matches input shape."""
        w = np.random.choice([-1, 0, 1], size=(8, 16)).astype(np.int8)
        bmp = Ternarizer.export_rom_bitmap(w)
        assert bmp.shape == w.shape

    def test_bitmap_dtype(self):
        """Output dtype is uint8."""
        w = np.array([1], dtype=np.int8)
        bmp = Ternarizer.export_rom_bitmap(w)
        assert bmp.dtype == np.uint8


# ======================================================================
# 5. SensitivityAnalyzer — sensitive layer detection
# ======================================================================

class TestSensitivityAnalyzer:
    def test_identifies_sensitive_layer(self):
        """High dynamic range layer gets non-ternary recommendation."""
        w = _high_dynamic_range_matrix()
        analyzer = SensitivityAnalyzer()
        result = analyzer.analyze_layer("dt_proj.weight", w)
        # dt_proj should always get int8 or higher due to name pattern
        assert result.recommendation in ("int8", "int4", "fp16")
        assert "dt_proj" in result.rationale or "sensitive" in result.rationale.lower()

    def test_recommends_ternary_for_gaussian(self):
        """Weights with narrow magnitude range ternarize with high cos_sim."""
        # Values clustered near ±1 preserve direction after ternarization
        w = np.random.choice([-1.0, -0.9, 0.9, 1.0], size=(128, 256))
        analyzer = SensitivityAnalyzer(ternary_threshold=0.99)
        result = analyzer.analyze_layer("fc1.weight", w)
        assert result.recommendation == "ternary"
        assert result.cos_sim_ternary >= 0.99

    def test_int8_better_than_ternary_for_sensitive(self):
        """For a sensitive layer, INT8 cos_sim > ternary cos_sim."""
        w = _high_dynamic_range_matrix()
        analyzer = SensitivityAnalyzer()
        result = analyzer.analyze_layer("some_layer", w)
        assert result.cos_sim_int8 >= result.cos_sim_ternary

    def test_int8_at_least_as_good_as_int4(self):
        """INT8 (256 levels) has cos_sim >= INT4 (16 levels)."""
        w = _gaussian_matrix()
        analyzer = SensitivityAnalyzer()
        result = analyzer.analyze_layer("fc1.weight", w)
        assert result.cos_sim_int8 >= result.cos_sim_int4 - 1e-6

    def test_ranking_order(self):
        """Most sensitive layer (lowest cos_sim) gets rank 1."""
        weights = {
            "good_layer": _gaussian_matrix(),
            "dt_proj": _high_dynamic_range_matrix(),
            "another_good": _gaussian_matrix(),
        }
        analyzer = SensitivityAnalyzer()
        results = analyzer.analyze(weights)
        # Rank 1 should have the lowest ternary cos_sim
        ranks_cos = [(r.sensitivity_rank, r.cos_sim_ternary) for r in results]
        ranks_cos.sort(key=lambda x: x[0])
        for i in range(len(ranks_cos) - 1):
            assert ranks_cos[i][1] <= ranks_cos[i + 1][1]

    def test_norm_layer_skipped(self):
        """LayerNorm-like layers should be recommended INT8 or higher."""
        # LayerNorm weights are often gamma (all near 1.0) — ternary
        # destroys the fine-grained scale information.
        w = np.ones((512,), dtype=np.float64) + np.random.randn(512) * 0.01
        analyzer = SensitivityAnalyzer()
        result = analyzer.analyze_layer("norm.weight", w)
        assert result.recommendation in ("int8", "int4", "fp16")

    def test_generate_report(self):
        """Report is a non-empty string with markdown table."""
        weights = {"fc1.weight": _gaussian_matrix()}
        analyzer = SensitivityAnalyzer()
        results = analyzer.analyze(weights)
        report = analyzer.generate_report(results)
        assert isinstance(report, str)
        assert len(report) > 0
        assert "Layer" in report
        assert "fc1.weight" in report


# ======================================================================
# 6. TernarizeReport area and leakage calculations
# ======================================================================

class TestTernarizeReport:
    def _make_weights(self) -> dict:
        """Create a small model dict for testing."""
        np.random.seed(42)
        return {
            "fc1.weight": np.random.randn(64, 128).astype(np.float64),
            "fc2.weight": np.random.randn(128, 64).astype(np.float64),
        }

    def test_area_calculation(self):
        """ROM area = ternary_params * 0.048e-12 mm²."""
        weights = self._make_weights()
        t = Ternarizer(weights)
        report = t.convert()

        expected_area = report.ternary_params * 0.048e-12
        assert report.estimated_rom_area_mm2 == pytest.approx(
            expected_area, rel=1e-9
        )

    def test_leakage_only_nonzero(self):
        """Leakage power only counts non-zero ternary cells."""
        weights = self._make_weights()
        t = Ternarizer(weights)
        report = t.convert()

        # Manually count non-zero ternary cells
        nonzero = sum(
            int(np.count_nonzero(r.weight_ternary))
            for r in report.layers
            if not r.skip
        )
        # leakage = nonzero * 2.37e-12 A * 1.0 V * 1e6 uW/W
        expected_uw = nonzero * 2.37e-12 * 1.0 * 1e6
        assert report.estimated_rom_leakage_uw == pytest.approx(
            expected_uw, rel=1e-9
        )

    def test_rom_bits(self):
        """ROM bits = 2 * ternary_params."""
        weights = self._make_weights()
        t = Ternarizer(weights)
        report = t.convert()
        assert report.rom_bits == 2 * report.ternary_params

    def test_sram_bits_all_ternary(self):
        """When no layers are skipped, SRAM bits = 0."""
        weights = self._make_weights()
        t = Ternarizer(weights)
        report = t.convert()
        skipped = [r for r in report.layers if r.skip]
        if not skipped:
            assert report.sram_bits == 0

    def test_sram_bits_with_skipped(self):
        """Skipped layers contribute to SRAM bits at their keep_bits."""
        weights = self._make_weights()
        # Force-skip fc1
        t = Ternarizer(weights, skip_layers=["fc1"])
        report = t.convert()

        expected_sram = 0
        for r in report.layers:
            if r.skip:
                expected_sram += int(np.prod(r.shape)) * r.keep_bits
        assert report.sram_bits == expected_sram

    def test_total_params(self):
        """total_params matches sum of all layer sizes."""
        weights = self._make_weights()
        t = Ternarizer(weights)
        report = t.convert()
        expected = sum(int(np.prod(w.shape)) for w in weights.values())
        assert report.total_params == expected

    def test_sparsity_reasonable(self):
        """Ternarized layers should have ~30-60% sparsity for Gaussian weights."""
        weights = self._make_weights()
        t = Ternarizer(weights)
        report = t.convert()
        for r in report.layers:
            if not r.skip:
                # Gaussian ternarization ≈ 45% zeros
                assert 0.15 < r.sparsity < 0.80, (
                    f"Layer {r.name} has unexpected sparsity {r.sparsity:.3f}"
                )

    def test_overall_cos_sim_range(self):
        """Overall cos_sim should be in [0, 1]."""
        weights = self._make_weights()
        t = Ternarizer(weights)
        report = t.convert()
        assert 0.0 <= report.overall_cos_sim <= 1.0

    def test_leakage_zero_cells_dont_leak(self):
        """A layer that's all zeros after ternarization contributes 0 leakage."""
        # Very small weights → all become 0 after rounding
        w = np.random.randn(32, 32) * 1e-10
        weights = {"tiny.weight": w}
        t = Ternarizer(weights)
        report = t.convert()
        assert report.estimated_rom_leakage_uw == pytest.approx(0.0, abs=1e-20)


# ======================================================================
# 7. Full Ternarizer.convert() integration
# ======================================================================

class TestTernarizerIntegration:
    def test_convert_returns_report(self):
        """convert() returns a TernarizeReport with all fields populated."""
        weights = {
            "a": np.random.randn(8, 16),
            "b": np.random.randn(16, 8),
        }
        report = Ternarizer(weights).convert()
        assert isinstance(report, TernarizeReport)
        assert len(report.layers) == 2
        assert report.total_params == 8 * 16 + 16 * 8

    def test_skip_layers_honored(self):
        """Layers in skip_layers are marked skip=True."""
        weights = {"fc1.weight": np.random.randn(32, 64)}
        t = Ternarizer(weights, skip_layers=["fc1"])
        report = t.convert()
        assert report.layers[0].skip is True
        assert report.layers[0].keep_bits in (8, 16)

    def test_auto_skip_low_cos_sim(self):
        """Layers with cos_sim < skip_threshold are auto-skipped."""
        # Monotonic ascending values cause many small entries to round to
        # zero while larger entries round to +1, shifting the direction
        # enough to drop cos_sim below 0.95.
        row = np.linspace(0.1, 1.0, 32)
        w = np.tile(row, (64, 1))
        weights = {"pathological.weight": w}
        t = Ternarizer(weights, skip_threshold=0.95)
        report = t.convert()
        assert report.layers[0].skip is True

    def test_no_torch_needed(self):
        """Engine works with pure numpy — no torch import."""
        import sys

        # If torch is installed, temporarily hide it
        torch_hidden = "torch" in sys.modules
        torch_mod = sys.modules.pop("torch", None)
        try:
            # Force reimport of engine
            import importlib

            from ternary_rom.ternarize import engine

            importlib.reload(engine)
            w = np.random.randn(4, 4)
            w_t, alpha = engine.Ternarizer.ternarize_bitnet(w)
            assert set(np.unique(w_t).tolist()).issubset({-1, 0, 1})
        finally:
            if torch_mod is not None:
                sys.modules["torch"] = torch_mod
            elif torch_hidden:
                pass  # torch wasn't there anyway
            importlib.reload(engine)
