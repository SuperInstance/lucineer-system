"""Tests for the structural Verilog netlist generator.

All tests use np.random.seed(42) for deterministic behaviour.
No external Verilog simulator is required; tests validate the
*structure* and *correctness* of the generated text.
"""

import tempfile
from pathlib import Path

import numpy as np
import pytest

from ternary_rom.netgen import NetlistGenerator
from ternary_rom.netgen.generator import NetlistConfig, ROMArraySpec


# ======================================================================
# Deterministic seed (applied per-test below where needed)
# ======================================================================

@pytest.fixture(autouse=True)
def _seed():
    np.random.seed(42)


# ======================================================================
# 1. Generated Verilog contains module, endmodule, wire declarations
# ======================================================================

class TestVerilogValidity:
    """Generated Verilog is valid structural Verilog-2001."""

    def test_module_and_endmodule(self):
        weights = {"fc1": np.array([[1, 0, -1], [0, 1, 0]], dtype=np.int8)}
        gen = NetlistGenerator(weights)
        v = gen.generate()
        assert "module ternary_rom_fc1" in v
        assert "endmodule" in v

    def test_wire_declarations(self):
        weights = {"fc1": np.array([[1, -1]], dtype=np.int8)}
        gen = NetlistGenerator(weights)
        v = gen.generate()
        assert "wire" in v

    def test_input_output_ports(self):
        weights = {"l": np.array([[1]], dtype=np.int8)}
        gen = NetlistGenerator(weights)
        v = gen.generate()
        assert "input" in v
        assert "output" in v
        assert "wl" in v
        assert "clk" in v
        assert "result" in v

    def test_proper_verilog_2001_syntax(self):
        """Port list uses Verilog-2001 ANSI style."""
        w = np.array([[1, 0, -1]], dtype=np.int8)
        gen = NetlistGenerator({"l": w})
        v = gen.generate()
        # ANSI port declarations are inside the module header parentheses
        assert "input  wire" in v or "input wire" in v
        assert "output wire" in v or "output reg" in v

    def test_pipelined_output_is_reg(self):
        """When pipelined, result is declared as reg."""
        config = NetlistConfig(pipeline_depth=1)
        gen = NetlistGenerator({"l": np.array([[1]], dtype=np.int8)}, config=config)
        v = gen.generate()
        assert "output reg" in v
        assert "always @(posedge clk)" in v


# ======================================================================
# 2. Correct number of ROM_PLUS and ROM_MINUS instantiations
# ======================================================================

class TestCellCounts:
    def test_correct_plus_minus_counts(self):
        """Instantiation count matches the number of +1 / -1 weights."""
        # Row 0: 1,  0, -1  → 1 PLUS, 1 MINUS
        # Row 1: -1, 1,  0  → 1 PLUS, 1 MINUS
        # Row 2: 0,  0,  1  → 1 PLUS, 0 MINUS
        w = np.array(
            [[1, 0, -1], [-1, 1, 0], [0, 0, 1]], dtype=np.int8
        )
        gen = NetlistGenerator({"l": w})
        v = gen.generate()

        plus_count = sum(
            1
            for line in v.split("\n")
            if "ROM_PLUS" in line and not line.strip().startswith("//")
        )
        minus_count = sum(
            1
            for line in v.split("\n")
            if "ROM_MINUS" in line and not line.strip().startswith("//")
        )
        assert plus_count == 3
        assert minus_count == 2

    def test_single_cell(self):
        """A 1×1 matrix with +1 produces exactly one ROM_PLUS."""
        gen = NetlistGenerator({"l": np.array([[1]], dtype=np.int8)})
        v = gen.generate()
        plus = sum(
            1
            for line in v.split("\n")
            if "ROM_PLUS" in line and not line.strip().startswith("//")
        )
        assert plus == 1


# ======================================================================
# 3. No ROM_ZERO instantiations (only comments)
# ======================================================================

class TestZeroCells:
    def test_zero_cells_are_comments_only(self):
        """ROM_ZERO positions produce comments, never instantiations."""
        w = np.array([[1, 0], [0, -1]], dtype=np.int8)
        gen = NetlistGenerator({"l": w})
        v = gen.generate()

        for line in v.split("\n"):
            stripped = line.strip()
            # Skip empty lines and comments
            if stripped and not stripped.startswith("//"):
                assert "ROM_ZERO" not in stripped, (
                    f"ROM_ZERO found in non-comment line: {line!r}"
                )

    def test_zero_weight_comment_present(self):
        """A comment is emitted for every zero-weight position."""
        w = np.array([[0, 1]], dtype=np.int8)
        gen = NetlistGenerator({"l": w})
        v = gen.generate()
        # Should have a comment about rom_0_0 being ZERO
        assert "rom_0_0" in v
        assert "ZERO" in v


# ======================================================================
# 4. Area estimation matches formula
# ======================================================================

class TestAreaEstimate:
    def test_area_formula_default(self):
        """Area = rows × cols × 0.048 um² × 1e-6 mm²/um²."""
        area = NetlistGenerator.rom_area_estimate(100, 100)
        expected = 100 * 100 * 0.048 * 1e-6
        assert area == pytest.approx(expected, abs=1e-15)

    def test_area_custom_cell_size(self):
        """Area formula works with custom cell_area_um2."""
        area = NetlistGenerator.rom_area_estimate(4096, 4096, cell_area_um2=0.1)
        expected = 4096 * 4096 * 0.1 * 1e-6
        assert area == pytest.approx(expected, abs=1e-12)

    def test_area_in_spec(self):
        """ROMArraySpec.estimated_area_mm2 uses the static method."""
        gen = NetlistGenerator({"l": np.array([[1, -1], [0, 1]], dtype=np.int8)})
        specs = gen.analyze_arrays()
        expected = 2 * 2 * 0.048 * 1e-6
        assert specs[0].estimated_area_mm2 == pytest.approx(expected, abs=1e-15)


# ======================================================================
# 5. Leakage estimation: only non-zero cells contribute
# ======================================================================

class TestLeakageEstimate:
    def test_zero_cells_no_leakage(self):
        """Zero cells (no transistor) have zero leakage."""
        leak = NetlistGenerator.rom_leakage_estimate(0, 0)
        assert leak == 0.0

    def test_only_nonzero_contributes(self):
        """Leakage = (plus + minus) × 2.37 pA × voltage × 1e-6."""
        leak = NetlistGenerator.rom_leakage_estimate(10, 5)
        expected = (10 + 5) * 2.37 * 1.0 * 1e-6
        assert leak == pytest.approx(expected, abs=1e-20)

    def test_custom_leakage_params(self):
        """Custom per-cell leakage and voltage are respected."""
        leak = NetlistGenerator.rom_leakage_estimate(
            5, 3, leakage_per_cell_pa=5.0, voltage=0.8
        )
        expected = 8 * 5.0 * 0.8 * 1e-6
        assert leak == pytest.approx(expected, abs=1e-20)

    def test_leakage_in_spec(self):
        """ROMArraySpec.estimated_leakage_uw matches formula."""
        w = np.array([[1, 0, -1], [0, 0, 0]], dtype=np.int8)
        gen = NetlistGenerator({"l": w})
        specs = gen.analyze_arrays()
        # plus=1, minus=1
        expected = 2 * 2.37 * 1.0 * 1e-6
        assert specs[0].estimated_leakage_uw == pytest.approx(expected, abs=1e-20)


# ======================================================================
# 6. Weight map produces correct + / - / . grid
# ======================================================================

class TestWeightMap:
    def test_weight_map_characters(self):
        """Each weight maps to the correct character."""
        # Row 0: +1,  0, -1 → "+.-"
        # Row 1:  0,  0, +1 → "..+"
        w = np.array([[1, 0, -1], [0, 0, 1]], dtype=np.int8)
        gen = NetlistGenerator({"l": w})

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            path = f.name
        try:
            gen.write_weight_map(path)
            content = Path(path).read_text()
            lines = [
                l
                for l in content.strip().split("\n")
                if not l.startswith("//")
            ]
            assert lines[0] == "+.-"
            assert lines[1] == "..+"
        finally:
            Path(path).unlink()

    def test_weight_map_all_zeros(self):
        """All-zero matrix produces a grid of '.' characters."""
        w = np.zeros((2, 3), dtype=np.int8)
        gen = NetlistGenerator({"l": w})

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            path = f.name
        try:
            gen.write_weight_map(path)
            content = Path(path).read_text()
            lines = [
                l
                for l in content.strip().split("\n")
                if not l.startswith("//")
            ]
            assert lines[0] == "..."
            assert lines[1] == "..."
        finally:
            Path(path).unlink()


# ======================================================================
# 7. Single-layer and multi-layer generation
# ======================================================================

class TestMultiLayer:
    def test_single_layer(self):
        """Single layer generates exactly one module."""
        gen = NetlistGenerator({"l1": np.array([[1]], dtype=np.int8)})
        v = gen.generate()
        assert "module ternary_rom_l1" in v
        assert v.count("module ternary_rom_") == 1

    def test_multi_layer(self):
        """Multiple layers generate multiple modules."""
        gen = NetlistGenerator(
            {
                "fc1": np.array([[1, 0]], dtype=np.int8),
                "fc2": np.array([[-1]], dtype=np.int8),
            }
        )
        v = gen.generate()
        assert "module ternary_rom_fc1" in v
        assert "module ternary_rom_fc2" in v
        assert v.count("endmodule") >= 2

    def test_multi_layer_write_verilog(self):
        """write_verilog with multiple layers creates one file per layer."""
        gen = NetlistGenerator(
            {
                "a": np.array([[1]], dtype=np.int8),
                "b": np.array([[-1]], dtype=np.int8),
            }
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir) / "model.v"
            gen.write_verilog(str(base))
            assert (Path(tmpdir) / "model_a.v").exists()
            assert (Path(tmpdir) / "model_b.v").exists()

    def test_single_layer_write_verilog(self):
        """write_verilog with a single layer writes exactly one file."""
        gen = NetlistGenerator({"only": np.array([[1]], dtype=np.int8)})
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir) / "model.v"
            gen.write_verilog(str(base))
            assert base.exists()
            # Should not create split files
            assert not (Path(tmpdir) / "model_only.v").exists()


# ======================================================================
# 8. Time-multiplexed configuration reduces cell count
# ======================================================================

class TestTimeMux:
    def test_reduced_cell_count(self):
        """time_mux_factor > 1 reduces the number of instantiated cells."""
        # 4 rows × 2 cols
        # Row 0: [ 1, -1] → 1 PLUS, 1 MINUS
        # Row 1: [ 0,  1] → 1 PLUS, 0 MINUS
        # Row 2: [-1,  0] → 0 PLUS, 1 MINUS
        # Row 3: [ 1,  1] → 2 PLUS, 0 MINUS
        # Full total: 4 PLUS, 2 MINUS = 6 cells
        # Mux=2 (first 2 rows): 2 PLUS, 1 MINUS = 3 cells
        w = np.array(
            [[1, -1], [0, 1], [-1, 0], [1, 1]], dtype=np.int8
        )

        def _count_cells(verilog: str) -> int:
            return sum(
                1
                for line in verilog.split("\n")
                if ("ROM_PLUS" in line or "ROM_MINUS" in line)
                and not line.strip().startswith("//")
            )

        gen_normal = NetlistGenerator({"l": w})
        v_normal = gen_normal.generate()
        n_normal = _count_cells(v_normal)

        config = NetlistConfig(time_mux_factor=2)
        gen_mux = NetlistGenerator({"l": w}, config=config)
        v_mux = gen_mux.generate()
        n_mux = _count_cells(v_mux)

        assert n_normal == 6
        assert n_mux == 3
        assert n_mux < n_normal

    def test_mux_factor_4_halves_again(self):
        """Larger mux factor further reduces cell count."""
        w = np.array(
            [[1, -1], [0, 1], [-1, 0], [1, 1]], dtype=np.int8
        )

        def _count_cells(verilog: str) -> int:
            return sum(
                1
                for line in verilog.split("\n")
                if ("ROM_PLUS" in line or "ROM_MINUS" in line)
                and not line.strip().startswith("//")
            )

        config2 = NetlistConfig(time_mux_factor=2)
        config4 = NetlistConfig(time_mux_factor=4)
        n2 = _count_cells(
            NetlistGenerator({"l": w}, config=config2).generate()
        )
        n4 = _count_cells(
            NetlistGenerator({"l": w}, config=config4).generate()
        )
        # With mux=4, effective_rows = 4//4 = 1; row 0 is [1, -1] → 2 cells
        assert n4 == 2
        assert n4 < n2


# ======================================================================
# 9. Testbench is generated when requested
# ======================================================================

class TestTestbench:
    def test_testbench_present_when_requested(self):
        """include_testbench=True appends a testbench module."""
        config = NetlistConfig(include_testbench=True)
        gen = NetlistGenerator(
            {"l": np.array([[1]], dtype=np.int8)}, config=config
        )
        v = gen.generate()
        assert "module tb_ternary_rom_l" in v
        assert "dut" in v  # device under test instantiation
        assert "$display" in v
        assert "$finish" in v

    def test_testbench_absent_by_default(self):
        """include_testbench=False (default) produces no testbench."""
        gen = NetlistGenerator({"l": np.array([[1]], dtype=np.int8)})
        v = gen.generate()
        assert "module tb_" not in v

    def test_testbench_checks_all_zero(self):
        """Testbench includes a test for all word lines inactive."""
        config = NetlistConfig(include_testbench=True)
        gen = NetlistGenerator(
            {"l": np.array([[1, -1]], dtype=np.int8)}, config=config
        )
        v = gen.generate()
        assert "wl = 0" in v or "wl = 0;" in v
        assert "expected 0" in v

    def test_testbench_checks_individual_rows(self):
        """Testbench activates each row and checks per-column outputs."""
        config = NetlistConfig(include_testbench=True)
        w = np.array([[1, -1], [0, 1]], dtype=np.int8)
        gen = NetlistGenerator({"l": w}, config=config)
        v = gen.generate()
        # Should check row 0: col 0 → 1, col 1 → -1
        assert "expected 1" in v
        assert "expected -1" in v
        # Should check row 1: col 0 → 0, col 1 → 1
        assert "expected 0" in v

    def test_testbench_clock_generation(self):
        """Testbench has a clock generator."""
        config = NetlistConfig(include_testbench=True)
        gen = NetlistGenerator(
            {"l": np.array([[1]], dtype=np.int8)}, config=config
        )
        v = gen.generate()
        assert "initial clk" in v
        assert "always #5 clk" in v


# ======================================================================
# 10. Summary file contains all expected fields
# ======================================================================

class TestSummary:
    def test_summary_fields(self):
        """Summary includes name, shape, cell counts, zero fraction, area, leakage."""
        w = np.array([[1, 0, -1], [0, 1, 0]], dtype=np.int8)
        gen = NetlistGenerator({"fc": w})

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            path = f.name
        try:
            gen.write_summary(path)
            content = Path(path).read_text()

            assert "Layer: fc" in content
            # Alignment pads spaces between label and value
            assert "Shape:" in content and "2 x 3" in content
            assert "ROM_PLUS" in content
            assert "ROM_MINUS" in content
            assert "ROM_ZERO" in content
            assert "Zero fraction" in content
            assert "area" in content.lower()
            assert "leakage" in content.lower()
        finally:
            Path(path).unlink()

    def test_summary_multi_layer(self):
        """Summary lists all layers."""
        gen = NetlistGenerator(
            {
                "a": np.array([[1]], dtype=np.int8),
                "b": np.array([[-1, 1]], dtype=np.int8),
            }
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            path = f.name
        try:
            gen.write_summary(path)
            content = Path(path).read_text()
            assert "Layer: a" in content
            assert "Layer: b" in content
        finally:
            Path(path).unlink()

    def test_summary_zero_fraction(self):
        """Zero fraction is computed correctly."""
        # 2×3 = 6 cells, 3 zeros → fraction = 0.5
        w = np.array([[1, 0, -1], [0, 1, 0]], dtype=np.int8)
        gen = NetlistGenerator({"l": w})
        specs = gen.analyze_arrays()
        assert specs[0].zero_fraction == pytest.approx(3 / 6)


# ======================================================================
# Bonus: edge cases and additional coverage
# ======================================================================

class TestEdgeCases:
    def test_empty_weights_raises(self):
        """Empty weights dict raises ValueError."""
        with pytest.raises(ValueError, match="must not be empty"):
            NetlistGenerator({})

    def test_invalid_value_raises(self):
        """Weights outside {-1, 0, +1} raise ValueError."""
        with pytest.raises(ValueError, match="invalid value"):
            NetlistGenerator({"l": np.array([[2]], dtype=np.int8)})

    def test_1d_raises(self):
        """1-D weight array raises ValueError."""
        with pytest.raises(ValueError, match="must be 2D"):
            NetlistGenerator({"l": np.array([1, 0, -1], dtype=np.int8)})

    def test_generic_28nm_templates(self):
        """generic_28nm library produces correct cell names and port casing."""
        config = NetlistConfig(cell_lib="generic_28nm")
        gen = NetlistGenerator(
            {"l": np.array([[1, -1]], dtype=np.int8)}, config=config
        )
        v = gen.generate()
        # 28nm uses lowercase port names and X1 cell names
        assert "ROM_PLUS_X1 rom_" in v
        assert "ROM_MINUS_X1 rom_" in v
        assert ".wl(" in v
        assert ".bl(" in v
        assert ".vdd(" in v
        assert ".vss(" in v
        # sky130-style port casing should NOT be present
        assert ".VDD(" not in v

    def test_tree_adder_style(self):
        """Tree adder style generates the tree structure."""
        config = NetlistConfig(adder_style="tree")
        # 4 terms in column 0 → needs at least one tree level
        w = np.array(
            [[1], [1], [-1], [1]], dtype=np.int8
        )
        gen = NetlistGenerator({"l": w}, config=config)
        v = gen.generate()
        # Tree adder creates intermediate wires named col0_s0_0, etc.
        assert "col0_s0_" in v

    def test_ripple_adder_style(self):
        """Ripple adder style generates sequential sums."""
        config = NetlistConfig(adder_style="ripple")
        w = np.array(
            [[1], [1], [-1], [1]], dtype=np.int8
        )
        gen = NetlistGenerator({"l": w}, config=config)
        v = gen.generate()
        # Ripple adder creates wires named col0_r0, col0_r1, etc.
        assert "col0_r0" in v
        assert "col0_r1" in v

    def test_column_all_zeros(self):
        """A column with all-zero weights gets assign to 0."""
        w = np.array([[0, 1]], dtype=np.int8)  # col 0 all zeros
        gen = NetlistGenerator({"l": w})
        v = gen.generate()
        assert "assign col_accum[0]" in v
        assert "0" in v

    def test_adder_tree_correct_structure(self):
        """The adder tree produces correct assign/accumulation for a known case.

        Weight matrix:
            [[ 1, -1],
             [ 0,  1]]

        Column 0: +wl[0]  →  expected = wl[0]
        Column 1: -wl[0] + wl[1]  →  expected = -wl[0] + wl[1]
        """
        w = np.array([[1, -1], [0, 1]], dtype=np.int8)
        gen = NetlistGenerator({"l": w})
        v = gen.generate()

        # Column 0: only one term (wl[0], positive)
        assert "col0_t0_r0" in v
        assert "assign col_accum[0]" in v

        # Column 1: two terms (+wl[1], -wl[0])
        # Terms are ordered: plus_rows first, then minus_rows
        # plus_rows=[1], minus_rows=[0] → t0=r1 (positive), t1=r0 (negative)
        assert "col1_t0_r1" in v  # +wl[1]
        assert "col1_t1_r0" in v  # -wl[0]
        # Should have an addition (ripple sum of the two terms)
        assert "col1_r0" in v

    def test_write_verilog_specific_layer(self):
        """write_verilog with layer_name writes only that layer."""
        gen = NetlistGenerator(
            {
                "a": np.array([[1]], dtype=np.int8),
                "b": np.array([[-1]], dtype=np.int8),
            }
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.v"
            gen.write_verilog(str(path), layer_name="b")
            content = path.read_text()
            assert "module ternary_rom_b" in content
            assert "module ternary_rom_a" not in content

    def test_write_verilog_invalid_layer_raises(self):
        """write_verilog with unknown layer_name raises ValueError."""
        gen = NetlistGenerator({"a": np.array([[1]], dtype=np.int8)})
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.v"
            with pytest.raises(ValueError, match="No layer named"):
                gen.write_verilog(str(path), layer_name="nonexistent")
