"""Tests for the ROM cell library.

Covers: bundle loading, Verilog/LEF/Liberty generation,
pre-generated file consistency, cell property invariants,
multi-drive-strength cells, Vt flavors, reference cells,
all 31 process nodes, custom process creation, and filtering.
"""

import json
import re
from pathlib import Path

import pytest

from ternary_rom.cells.library import (
    CellDef,
    ROMCellLibrary,
    PROCESS_DB,
    DRIVE_SCALING,
    VT_MODIFIERS,
)


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def sky130_lib():
    return ROMCellLibrary.from_bundle("sky130")


@pytest.fixture
def nm28_lib():
    return ROMCellLibrary.from_bundle("generic_28nm")


@pytest.fixture
def tsmc7_lib():
    return ROMCellLibrary.from_bundle("tsmc7")


@pytest.fixture
def intel18a_lib():
    return ROMCellLibrary.from_bundle("intel18a")


# ------------------------------------------------------------------
# 1. from_bundle basic loading
# ------------------------------------------------------------------


class TestFromBundle:
    def test_sky130_has_cells(self, sky130_lib):
        assert len(sky130_lib.cells) >= 5

    def test_sky130_has_plus_minus_zero_x1(self, sky130_lib):
        for prefix in ["ROM_PLUS_X1", "ROM_MINUS_X1", "ROM_ZERO_X1"]:
            assert prefix in sky130_lib.cells

    def test_sky130_has_ref_cells(self, sky130_lib):
        assert "ROM_REF_HI" in sky130_lib.cells
        assert "ROM_REF_LO" in sky130_lib.cells

    def test_unknown_bundle_raises(self):
        with pytest.raises(ValueError, match="Unknown bundle"):
            ROMCellLibrary.from_bundle("nonexistent")

    def test_all_processes_loadable(self):
        procs = ROMCellLibrary.list_processes()
        for p in procs:
            lib = ROMCellLibrary.from_bundle(p["name"])
            assert len(lib.cells) >= 5
            assert lib.voltage > 0
            assert lib.process == p["name"]


# ------------------------------------------------------------------
# 2. 28nm bundle with multi-drive and Vt flavors
# ------------------------------------------------------------------


class Test28nm:
    def test_has_x1_x2_x4(self, nm28_lib):
        for ds in [1, 2, 4]:
            assert f"ROM_PLUS_X{ds}" in nm28_lib.cells
            assert f"ROM_MINUS_X{ds}" in nm28_lib.cells
            assert f"ROM_ZERO_X{ds}" in nm28_lib.cells

    def test_has_vt_flavors(self, nm28_lib):
        for vt in ["std", "lvt", "hvt"]:
            assert f"ROM_PLUS_X1_{vt}" in nm28_lib.cells or (vt == "std" and "ROM_PLUS_X1" in nm28_lib.cells)

    def test_voltage(self, nm28_lib):
        assert nm28_lib.voltage == 1.0

    def test_process_name(self, nm28_lib):
        assert nm28_lib.process == "generic_28nm"

    def test_cell_count(self, nm28_lib):
        # 3 types x 3 drives x 3 Vt + 2 ref = 29
        assert len(nm28_lib.cells) == 29


# ------------------------------------------------------------------
# 3. generate_verilog() produces valid Verilog
# ------------------------------------------------------------------


class TestVerilog:
    def test_module_endmodule_for_x1(self, sky130_lib):
        v = sky130_lib.generate_verilog()
        for prefix in ["ROM_PLUS_X1", "ROM_MINUS_X1", "ROM_ZERO_X1"]:
            assert f"module {prefix} (WL, BL);" in v
        assert v.count("endmodule") >= 3

    def test_has_input_output(self, sky130_lib):
        v = sky130_lib.generate_verilog()
        assert "input WL;" in v
        assert "output BL;" in v

    def test_plus_drives_high(self, sky130_lib):
        v = sky130_lib.generate_verilog()
        assert "assign BL = WL ? 1'b1 : 1'bz;" in v

    def test_minus_drives_low(self, sky130_lib):
        v = sky130_lib.generate_verilog()
        assert "assign BL = WL ? 1'b0 : 1'bz;" in v

    def test_zero_always_floating(self, sky130_lib):
        v = sky130_lib.generate_verilog()
        assert "assign BL = 1'bz;" in v

    def test_ref_hi_always_high(self, sky130_lib):
        v = sky130_lib.generate_verilog()
        assert "assign BL = 1'b1;" in v

    def test_ref_lo_always_low(self, sky130_lib):
        v = sky130_lib.generate_verilog()
        assert "assign BL = 1'b0;" in v

    def test_has_drive_and_vt_comments(self, nm28_lib):
        v = nm28_lib.generate_verilog()
        assert "Drive: X2" in v
        assert "Drive: X4" in v
        assert "Vt: lvt" in v
        assert "Vt: hvt" in v

    def test_x2_cells_wider(self, nm28_lib):
        x1 = nm28_lib.cells["ROM_PLUS_X1"]
        x2 = nm28_lib.cells["ROM_PLUS_X2"]
        assert x2.width_um > x1.width_um
        assert x2.height_um == x1.height_um  # height stays same

    def test_x4_cells_widest(self, nm28_lib):
        x2 = nm28_lib.cells["ROM_PLUS_X2"]
        x4 = nm28_lib.cells["ROM_PLUS_X4"]
        assert x4.width_um > x2.width_um


# ------------------------------------------------------------------
# 4. generate_lef() produces valid LEF
# ------------------------------------------------------------------


class TestLEF:
    def test_macro_end_for_each_cell(self, sky130_lib):
        lef = sky130_lib.generate_lef()
        for prefix in ["ROM_PLUS_X1", "ROM_MINUS_X1", "ROM_ZERO_X1"]:
            assert f"MACRO {prefix}" in lef

    def test_has_version(self, sky130_lib):
        lef = sky130_lib.generate_lef()
        assert "VERSION 5.8 ;" in lef

    def test_has_end_library(self, sky130_lib):
        lef = sky130_lib.generate_lef()
        assert "END LIBRARY" in lef

    def test_pin_wl_and_bl(self, sky130_lib):
        lef = sky130_lib.generate_lef()
        assert "PIN WL" in lef
        assert "PIN BL" in lef

    def test_wl_metal1(self, sky130_lib):
        lef = sky130_lib.generate_lef()
        wl_section = re.search(
            r"PIN WL.*?END WL", lef, re.DOTALL
        ).group(0)
        assert "LAYER Metal1" in wl_section

    def test_bl_metal2(self, sky130_lib):
        lef = sky130_lib.generate_lef()
        bl_section = re.search(
            r"PIN BL.*?END BL", lef, re.DOTALL
        ).group(0)
        assert "LAYER Metal2" in bl_section

    def test_has_obs(self, sky130_lib):
        lef = sky130_lib.generate_lef()
        assert "OBS" in lef

    def test_x2_has_larger_size(self, nm28_lib):
        lef = nm28_lib.generate_lef()
        x1_size_match = re.search(r"MACRO ROM_PLUS_X1.*?SIZE ([\d.]+) BY ([\d.]+)", lef, re.DOTALL)
        x2_size_match = re.search(r"MACRO ROM_PLUS_X2.*?SIZE ([\d.]+) BY ([\d.]+)", lef, re.DOTALL)
        assert x1_size_match
        assert x2_size_match
        x1_w = float(x1_size_match.group(1))
        x2_w = float(x2_size_match.group(1))
        assert x2_w > x1_w

    def test_has_vt_comment(self, nm28_lib):
        lef = nm28_lib.generate_lef()
        assert "Vt: lvt" in lef
        assert "Vt: hvt" in lef


# ------------------------------------------------------------------
# 5. generate_lib() produces valid Liberty
# ------------------------------------------------------------------


class TestLiberty:
    def test_cell_for_plus(self, sky130_lib):
        lib = sky130_lib.generate_lib()
        assert "cell (ROM_PLUS_X1)" in lib

    def test_has_library_header(self, sky130_lib):
        lib = sky130_lib.generate_lib()
        assert "library(ternary_rom_sky130)" in lib
        assert "technology (cmos)" in lib

    def test_has_timing_for_plus(self, sky130_lib):
        lib = sky130_lib.generate_lib()
        assert 'related_pin : "WL"' in lib
        assert "cell_rise" in lib
        assert "delay_template_1x1" in lib

    def test_has_timing_for_minus(self, sky130_lib):
        lib = sky130_lib.generate_lib()
        assert "negative_unate" in lib
        assert "cell_fall" in lib

    def test_zero_no_timing_arc(self, sky130_lib):
        lib = sky130_lib.generate_lib()
        zero_section = re.search(
            r"cell \(ROM_ZERO_X1\).*?^  \}", lib, re.DOTALL | re.MULTILINE
        ).group(0)
        assert "timing" not in zero_section

    def test_28nm_lib_header(self, nm28_lib):
        lib = nm28_lib.generate_lib()
        assert "library(ternary_rom_generic_28nm)" in lib
        assert "voltage : 1.0" in lib

    def test_x2_has_higher_capacitance(self, nm28_lib):
        lib = nm28_lib.generate_lib()
        # X2 should have 2x input cap
        x1_cap = re.search(r"cell \(ROM_PLUS_X1\).*?pin \(WL\).*?capacitance : ([\d.]+)", lib, re.DOTALL)
        x2_cap = re.search(r"cell \(ROM_PLUS_X2\).*?pin \(WL\).*?capacitance : ([\d.]+)", lib, re.DOTALL)
        assert x1_cap and x2_cap
        assert float(x2_cap.group(1)) > float(x1_cap.group(1))

    def test_lvt_has_higher_leakage(self, nm28_lib):
        lib = nm28_lib.generate_lib()
        std_leak = re.search(r"cell \(ROM_PLUS_X1\).*?cell_leakage_power : ([\d.]+)", lib, re.DOTALL)
        lvt_leak = re.search(r"cell \(ROM_PLUS_X1_lvt\).*?cell_leakage_power : ([\d.]+)", lib, re.DOTALL)
        if std_leak and lvt_leak:
            assert float(lvt_leak.group(1)) > float(std_leak.group(1))

    def test_hvt_has_lower_leakage(self, nm28_lib):
        lib = nm28_lib.generate_lib()
        std_leak = re.search(r"cell \(ROM_PLUS_X1\).*?cell_leakage_power : ([\d.]+)", lib, re.DOTALL)
        hvt_leak = re.search(r"cell \(ROM_PLUS_X1_hvt\).*?cell_leakage_power : ([\d.]+)", lib, re.DOTALL)
        if std_leak and hvt_leak:
            assert float(hvt_leak.group(1)) < float(std_leak.group(1))


# ------------------------------------------------------------------
# 6. ROM_ZERO has 0 transistors and 0 leakage
# ------------------------------------------------------------------


class TestZeroCell:
    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_zero_transistors(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        cell = lib.get_default_cell("zero")
        assert cell.transistors == 0

    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_zero_leakage(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        cell = lib.get_default_cell("zero")
        assert cell.leakage_pa == 0.0

    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_zero_delay(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        cell = lib.get_default_cell("zero")
        assert cell.delay_ns == 0.0


# ------------------------------------------------------------------
# 7. ROM_PLUS and ROM_MINUS symmetry
# ------------------------------------------------------------------


class TestPlusMinusSymmetry:
    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_same_dimensions(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        plus = lib.get_default_cell("plus")
        minus = lib.get_default_cell("minus")
        assert plus.width_um == minus.width_um
        assert plus.height_um == minus.height_um
        assert plus.area_um2 == minus.area_um2

    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_same_transistors(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        plus = lib.get_default_cell("plus")
        minus = lib.get_default_cell("minus")
        assert plus.transistors == minus.transistors == 2

    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_same_leakage(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        plus = lib.get_default_cell("plus")
        minus = lib.get_default_cell("minus")
        assert plus.leakage_pa == minus.leakage_pa

    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_same_delay(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        plus = lib.get_default_cell("plus")
        minus = lib.get_default_cell("minus")
        assert plus.delay_ns == minus.delay_ns


# ------------------------------------------------------------------
# 8. write_all creates all expected files
# ------------------------------------------------------------------


class TestWriteAll:
    def test_creates_all_files(self, sky130_lib, tmp_path):
        sky130_lib.write_all(str(tmp_path))
        expected = ["cells.v", "cells.lef", "cells.lib", "cells.vh", "cells.json"]
        for fname in expected:
            assert (tmp_path / fname).exists(), f"Missing {fname}"

    def test_verilog_content_matches(self, sky130_lib, tmp_path):
        sky130_lib.write_all(str(tmp_path))
        written = (tmp_path / "cells.v").read_text()
        assert written == sky130_lib.generate_verilog()

    def test_lef_content_matches(self, sky130_lib, tmp_path):
        sky130_lib.write_all(str(tmp_path))
        written = (tmp_path / "cells.lef").read_text()
        assert written == sky130_lib.generate_lef()

    def test_lib_content_matches(self, sky130_lib, tmp_path):
        sky130_lib.write_all(str(tmp_path))
        written = (tmp_path / "cells.lib").read_text()
        assert written == sky130_lib.generate_lib()

    def test_vh_has_defines(self, sky130_lib, tmp_path):
        sky130_lib.write_all(str(tmp_path))
        vh = (tmp_path / "cells.vh").read_text()
        assert "`define ROM_CELL_WIDTH_UM" in vh
        assert "`define ROM_VOLTAGE" in vh
        assert "`define ROM_NUM_CELLS" in vh

    def test_json_is_valid(self, sky130_lib, tmp_path):
        sky130_lib.write_all(str(tmp_path))
        data = json.loads((tmp_path / "cells.json").read_text())
        assert data["process"] == "sky130"
        assert data["num_cells"] == len(sky130_lib.cells)
        assert "cells" in data


# ------------------------------------------------------------------
# 9. Pre-generated sky130 files
# ------------------------------------------------------------------


class TestPreGenSky130:
    SKY130_DIR = Path(__file__).resolve().parent.parent / "cells" / "sky130"

    def test_files_exist(self):
        for ext in [".v", ".lef", ".lib", ".vh", ".json"]:
            fpath = self.SKY130_DIR / f"cells{ext}"
            assert fpath.exists(), f"Missing {fpath}"

    def test_verilog_matches(self, sky130_lib):
        pregen = (self.SKY130_DIR / "cells.v").read_text()
        generated = sky130_lib.generate_verilog()
        assert pregen == generated

    def test_lef_matches(self, sky130_lib):
        pregen = (self.SKY130_DIR / "cells.lef").read_text()
        generated = sky130_lib.generate_lef()
        assert pregen == generated

    def test_lib_matches(self, sky130_lib):
        pregen = (self.SKY130_DIR / "cells.lib").read_text()
        generated = sky130_lib.generate_lib()
        assert pregen == generated


# ------------------------------------------------------------------
# 10. Pre-generated 28nm files
# ------------------------------------------------------------------


class TestPreGen28nm:
    NM28_DIR = (
        Path(__file__).resolve().parent.parent
        / "cells"
        / "generic_28nm"
    )

    def test_files_exist(self):
        for ext in [".v", ".lef", ".lib", ".vh", ".json"]:
            fpath = self.NM28_DIR / f"cells{ext}"
            assert fpath.exists(), f"Missing {fpath}"

    def test_verilog_matches(self, nm28_lib):
        pregen = (self.NM28_DIR / "cells.v").read_text()
        generated = nm28_lib.generate_verilog()
        assert pregen == generated

    def test_lef_matches(self, nm28_lib):
        pregen = (self.NM28_DIR / "cells.lef").read_text()
        generated = nm28_lib.generate_lef()
        assert pregen == generated

    def test_lib_matches(self, nm28_lib):
        pregen = (self.NM28_DIR / "cells.lib").read_text()
        generated = nm28_lib.generate_lib()
        assert pregen == generated


# ------------------------------------------------------------------
# 11. All pre-generated process directories have files
# ------------------------------------------------------------------


class TestAllPreGenerated:
    CELLS_DIR = Path(__file__).resolve().parent.parent / "cells"

    @pytest.mark.parametrize("proc_name", list(PROCESS_DB.keys()))
    def test_directory_has_all_files(self, proc_name):
        d = self.CELLS_DIR / proc_name
        assert d.is_dir(), f"Missing directory: {d}"
        for ext in [".v", ".lef", ".lib", ".vh", ".json"]:
            fpath = d / f"cells{ext}"
            assert fpath.exists(), f"Missing {fpath}"

    @pytest.mark.parametrize("proc_name", list(PROCESS_DB.keys()))
    def test_json_is_parseable(self, proc_name):
        fpath = self.CELLS_DIR / proc_name / "cells.json"
        data = json.loads(fpath.read_text())
        assert data["process"] == proc_name
        assert data["num_cells"] >= 5
        assert len(data["cells"]) == data["num_cells"]


# ------------------------------------------------------------------
# 12. Drive strength scaling
# ------------------------------------------------------------------


class TestDriveStrength:
    def test_x2_is_twice_as_wide(self, nm28_lib):
        x1 = nm28_lib.cells["ROM_PLUS_X1"]
        x2 = nm28_lib.cells["ROM_PLUS_X2"]
        assert x2.width_um == pytest.approx(2 * x1.width_um)

    def test_x4_is_four_times_as_wide(self, nm28_lib):
        x1 = nm28_lib.cells["ROM_PLUS_X1"]
        x4 = nm28_lib.cells["ROM_PLUS_X4"]
        assert x4.width_um == pytest.approx(4 * x1.width_um)

    def test_x2_has_double_leakage(self, nm28_lib):
        x1 = nm28_lib.cells["ROM_PLUS_X1"]
        x2 = nm28_lib.cells["ROM_PLUS_X2"]
        assert x2.leakage_pa == pytest.approx(2 * x1.leakage_pa)

    def test_x4_has_quadruple_leakage(self, nm28_lib):
        x1 = nm28_lib.cells["ROM_PLUS_X1"]
        x4 = nm28_lib.cells["ROM_PLUS_X4"]
        assert x4.leakage_pa == pytest.approx(4 * x1.leakage_pa)

    def test_x2_is_faster(self, nm28_lib):
        x1 = nm28_lib.cells["ROM_PLUS_X1"]
        x2 = nm28_lib.cells["ROM_PLUS_X2"]
        assert x2.delay_ns < x1.delay_ns

    def test_x4_is_fastest(self, nm28_lib):
        x2 = nm28_lib.cells["ROM_PLUS_X2"]
        x4 = nm28_lib.cells["ROM_PLUS_X4"]
        assert x4.delay_ns < x2.delay_ns

    def test_drive_strength_field(self, nm28_lib):
        assert nm28_lib.cells["ROM_PLUS_X1"].drive_strength == 1
        assert nm28_lib.cells["ROM_PLUS_X2"].drive_strength == 2
        assert nm28_lib.cells["ROM_PLUS_X4"].drive_strength == 4


# ------------------------------------------------------------------
# 13. Vt flavor modifiers
# ------------------------------------------------------------------


class TestVtFlavor:
    def test_lvt_higher_leakage_than_std(self, nm28_lib):
        std = nm28_lib.cells["ROM_PLUS_X1"]
        lvt = nm28_lib.cells["ROM_PLUS_X1_lvt"]
        assert lvt.leakage_pa > std.leakage_pa

    def test_hvt_lower_leakage_than_std(self, nm28_lib):
        std = nm28_lib.cells["ROM_PLUS_X1"]
        hvt = nm28_lib.cells["ROM_PLUS_X1_hvt"]
        assert hvt.leakage_pa < std.leakage_pa

    def test_lvt_faster_than_std(self, nm28_lib):
        std = nm28_lib.cells["ROM_PLUS_X1"]
        lvt = nm28_lib.cells["ROM_PLUS_X1_lvt"]
        assert lvt.delay_ns < std.delay_ns

    def test_hvt_slower_than_std(self, nm28_lib):
        std = nm28_lib.cells["ROM_PLUS_X1"]
        hvt = nm28_lib.cells["ROM_PLUS_X1_hvt"]
        assert hvt.delay_ns > std.delay_ns

    def test_vt_flavor_field(self, nm28_lib):
        assert nm28_lib.cells["ROM_PLUS_X1"].vt_flavor == "std"
        assert nm28_lib.cells["ROM_PLUS_X1_lvt"].vt_flavor == "lvt"
        assert nm28_lib.cells["ROM_PLUS_X1_hvt"].vt_flavor == "hvt"

    def test_leakage_ratio_lvt(self, nm28_lib):
        std = nm28_lib.cells["ROM_PLUS_X1"]
        lvt = nm28_lib.cells["ROM_PLUS_X1_lvt"]
        ratio = lvt.leakage_pa / std.leakage_pa
        assert ratio == pytest.approx(3.0, rel=0.01)

    def test_leakage_ratio_hvt(self, nm28_lib):
        std = nm28_lib.cells["ROM_PLUS_X1"]
        hvt = nm28_lib.cells["ROM_PLUS_X1_hvt"]
        ratio = hvt.leakage_pa / std.leakage_pa
        assert ratio == pytest.approx(0.15, rel=0.01)


# ------------------------------------------------------------------
# 14. Reference cells
# ------------------------------------------------------------------


class TestRefCells:
    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_ref_hi_exists(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        assert "ROM_REF_HI" in lib.cells

    @pytest.mark.parametrize("proc", ["sky130", "generic_28nm", "tsmc7", "intel18a"])
    def test_ref_lo_exists(self, proc):
        lib = ROMCellLibrary.from_bundle(proc)
        assert "ROM_REF_LO" in lib.cells

    def test_ref_hi_type(self, sky130_lib):
        cell = sky130_lib.cells["ROM_REF_HI"]
        assert cell.cell_type == "ref_hi"
        assert cell.transistors == 2

    def test_ref_lo_type(self, sky130_lib):
        cell = sky130_lib.cells["ROM_REF_LO"]
        assert cell.cell_type == "ref_lo"
        assert cell.transistors == 2

    def test_ref_verilog(self, sky130_lib):
        v = sky130_lib.generate_verilog()
        assert "module ROM_REF_HI (WL, BL);" in v
        assert "assign BL = 1'b1;" in v  # ref_hi
        assert "module ROM_REF_LO (WL, BL);" in v
        assert "assign BL = 1'b0;" in v  # ref_lo


# ------------------------------------------------------------------
# 15. Process scaling trends
# ------------------------------------------------------------------


class TestProcessScaling:
    def test_smaller_nodes_have_smaller_cells(self):
        old = ROMCellLibrary.from_bundle("generic_180nm")
        new = ROMCellLibrary.from_bundle("tsmc7")
        old_cell = old.get_default_cell("plus")
        new_cell = new.get_default_cell("plus")
        assert new_cell.width_um < old_cell.width_um
        assert new_cell.area_um2 < old_cell.area_um2

    def test_smaller_nodes_have_less_leakage(self):
        old = ROMCellLibrary.from_bundle("generic_180nm")
        new = ROMCellLibrary.from_bundle("generic_28nm")
        old_cell = old.get_default_cell("plus")
        new_cell = new.get_default_cell("plus")
        assert new_cell.leakage_pa < old_cell.leakage_pa

    def test_smaller_nodes_are_faster(self):
        old = ROMCellLibrary.from_bundle("generic_180nm")
        new = ROMCellLibrary.from_bundle("generic_28nm")
        old_cell = old.get_default_cell("plus")
        new_cell = new.get_default_cell("plus")
        assert new_cell.delay_ns < old_cell.delay_ns

    def test_density_scales_with_node(self):
        old = ROMCellLibrary.from_bundle("sky130")
        new = ROMCellLibrary.from_bundle("tsmc7")
        old_density = 1e6 / old.get_default_cell("plus").area_um2
        new_density = 1e6 / new.get_default_cell("plus").area_um2
        assert new_density > old_density * 10  # 7nm should be >10x denser


# ------------------------------------------------------------------
# 16. Filtering APIs
# ------------------------------------------------------------------


class TestFiltering:
    def test_get_cells_by_type_plus(self, nm28_lib):
        plus = nm28_lib.get_cells_by_type("plus")
        assert all(c.cell_type == "plus" for c in plus.values())
        assert len(plus) > 1  # X1, X2, X4 at minimum

    def test_get_cells_by_drive_x2(self, nm28_lib):
        x2 = nm28_lib.get_cells_by_drive(2)
        assert all(c.drive_strength == 2 for c in x2.values())
        assert len(x2) > 0

    def test_get_cells_by_vt_lvt(self, nm28_lib):
        lvt = nm28_lib.get_cells_by_vt("lvt")
        assert all(c.vt_flavor == "lvt" for c in lvt.values())
        assert len(lvt) > 0

    def test_get_default_cell(self, nm28_lib):
        cell = nm28_lib.get_default_cell("plus")
        assert cell.name == "ROM_PLUS_X1"
        assert cell.drive_strength == 1
        assert cell.vt_flavor == "std"

    def test_get_default_cell_missing_raises(self, nm28_lib):
        with pytest.raises(KeyError):
            nm28_lib.get_default_cell("nonexistent")


# ------------------------------------------------------------------
# 17. Custom process creation
# ------------------------------------------------------------------


class TestCustomProcess:
    def test_custom_process_basic(self):
        lib = ROMCellLibrary.from_custom(
            "my_22nm", cell_size_um=0.10, voltage=0.8,
            leakage_per_transistor_pa=0.3, delay_ns=0.15,
            description="My custom 22nm",
        )
        assert lib.process == "my_22nm"
        assert lib.category == "custom"
        assert "ROM_PLUS_X1" in lib.cells
        assert len(lib.cells) >= 5

    def test_custom_process_only_x1(self):
        lib = ROMCellLibrary.from_custom(
            "minimal", cell_size_um=1.0, voltage=3.3,
            leakage_per_transistor_pa=10.0, delay_ns=2.0,
            drive_strengths=(1,),
            vt_flavors=("std",),
        )
        assert len(lib.cells) == 5  # 3 + 2 ref

    def test_custom_generates_valid_verilog(self):
        lib = ROMCellLibrary.from_custom(
            "test_proc", cell_size_um=0.5, voltage=1.2,
            leakage_per_transistor_pa=5.0, delay_ns=1.0,
        )
        v = lib.generate_verilog()
        assert "module ROM_PLUS_X1 (WL, BL);" in v
        assert "endmodule" in v


# ------------------------------------------------------------------
# 18. list_processes and list_categories
# ------------------------------------------------------------------


class TestProcessList:
    def test_list_returns_all(self):
        procs = ROMCellLibrary.list_processes()
        assert len(procs) == len(PROCESS_DB)

    def test_list_has_required_keys(self):
        procs = ROMCellLibrary.list_processes()
        for p in procs:
            assert "name" in p
            assert "category" in p
            assert "description" in p
            assert "voltage" in p
            assert "cell_size_um" in p
            assert "n_cells" in p

    def test_list_sorted_by_size(self):
        procs = ROMCellLibrary.list_processes()
        sizes = [p["cell_size_um"] for p in procs]
        assert sizes == sorted(sizes, reverse=True)

    def test_categories_cover_all(self):
        cats = ROMCellLibrary.list_categories()
        all_names = {p["name"] for p in ROMCellLibrary.list_processes()}
        cat_names = set()
        for names in cats.values():
            cat_names.update(names)
        assert cat_names == all_names

    def test_known_categories(self):
        cats = ROMCellLibrary.list_categories()
        expected = {"legacy", "open_source", "mature", "production",
                    "advanced", "cutting_edge", "frontier"}
        assert set(cats.keys()) == expected


# ------------------------------------------------------------------
# 19. summary() smoke test
# ------------------------------------------------------------------


class TestSummary:
    def test_summary_runs(self, sky130_lib):
        s = sky130_lib.summary()
        assert "sky130" in s
        assert "ROM_PLUS_X1" in s
        assert "cells/mm2" in s

    def test_summary_shows_drive_groups(self, nm28_lib):
        s = nm28_lib.summary()
        assert "Drive X1" in s
        assert "Drive X2" in s
        assert "Drive X4" in s

    def test_summary_shows_category(self, tsmc7_lib):
        s = tsmc7_lib.summary()
        assert "cutting_edge" in s

    def test_intel18a_summary(self, intel18a_lib):
        s = intel18a_lib.summary()
        assert "intel18a" in s
        assert "frontier" in s


# ------------------------------------------------------------------
# 20. CellDef dataclass
# ------------------------------------------------------------------


class TestCellDef:
    def test_fields(self):
        c = CellDef(
            name="TEST", cell_type="plus",
            width_um=1.0, height_um=1.0, area_um2=1.0,
            transistors=2, leakage_pa=5.0, delay_ns=1.0,
            drive_strength=1, vt_flavor="std",
        )
        assert c.name == "TEST"
        assert c.drive_strength == 1
        assert c.vt_flavor == "std"

    def test_all_bundled_cells_have_required_fields(self):
        procs = ROMCellLibrary.list_processes()
        for p in procs:
            lib = ROMCellLibrary.from_bundle(p["name"])
            for name, cell in lib.cells.items():
                assert cell.name == name
                assert cell.cell_type in ("plus", "minus", "zero", "ref_hi", "ref_lo")
                assert cell.width_um > 0
                assert cell.height_um > 0
                assert cell.area_um2 > 0
                assert cell.drive_strength in (1, 2, 4)
                assert cell.vt_flavor in ("std", "lvt", "hvt")
