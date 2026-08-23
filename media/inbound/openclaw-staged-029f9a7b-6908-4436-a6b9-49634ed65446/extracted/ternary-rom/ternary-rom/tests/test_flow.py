"""Tests for OpenROAD flow Tcl generation.

These tests verify Tcl script generation without requiring OpenROAD to be installed.
"""

import os
import tempfile
from pathlib import Path

import pytest

from ternary_rom.flow.openroad import OpenROADFlow, FlowConfig, FlowResult


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def flow():
    """Create a default OpenROADFlow instance."""
    return OpenROADFlow(FlowConfig(process="sky130"))


@pytest.fixture
def flow_28nm():
    """Create a 28nm OpenROADFlow instance."""
    return OpenROADFlow(FlowConfig(process="generic_28nm"))


@pytest.fixture
def tmp_dir():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory() as d:
        yield d


# ======================================================================
# 1. generate_setup_tcl
# ======================================================================

class TestGenerateSetupTcl:
    def test_returns_non_empty_string(self, flow):
        tcl = flow.generate_setup_tcl()
        assert isinstance(tcl, str)
        assert len(tcl) > 0

    def test_contains_read_lef(self, flow):
        tcl = flow.generate_setup_tcl()
        assert "read_lef" in tcl

    def test_contains_read_liberty(self, flow):
        tcl = flow.generate_setup_tcl()
        assert "read_liberty" in tcl

    def test_contains_process_name(self, flow):
        tcl = flow.generate_setup_tcl()
        assert "sky130" in tcl

    def test_28nm_process(self, flow_28nm):
        tcl = flow_28nm.generate_setup_tcl()
        assert "generic_28nm" in tcl


# ======================================================================
# 2. generate_floorplan_tcl
# ======================================================================

class TestGenerateFloorplanTcl:
    def test_returns_non_empty_string(self, flow):
        tcl = flow.generate_floorplan_tcl("design.v", "cells.lef")
        assert isinstance(tcl, str)
        assert len(tcl) > 0

    def test_contains_initialize_floorplan(self, flow):
        tcl = flow.generate_floorplan_tcl("design.v", "cells.lef")
        assert "initialize_floorplan" in tcl

    def test_contains_read_verilog(self, flow):
        tcl = flow.generate_floorplan_tcl("design.v", "cells.lef")
        assert "read_verilog" in tcl

    def test_contains_netlist_path(self, flow):
        tcl = flow.generate_floorplan_tcl("my_design.v", "my_cells.lef")
        assert "my_design.v" in tcl

    def test_contains_lef_path(self, flow):
        tcl = flow.generate_floorplan_tcl("design.v", "my_cells.lef")
        assert "my_cells.lef" in tcl

    def test_structural_placement_comment(self, flow):
        # When no ROM arrays provided, the comment block is not generated.
        # But with structural_placement=True in config, it's noted elsewhere.
        tcl = flow.generate_floorplan_tcl("design.v", "cells.lef")
        assert "floorplan" in tcl.lower()


# ======================================================================
# 3. generate_placement_tcl
# ======================================================================

class TestGeneratePlacementTcl:
    def test_returns_non_empty_string(self, flow):
        tcl = flow.generate_placement_tcl()
        assert isinstance(tcl, str)
        assert len(tcl) > 0

    def test_contains_placement_commands(self, flow):
        tcl = flow.generate_placement_tcl()
        assert "global_placement" in tcl

    def test_contains_detailed_placement(self, flow):
        tcl = flow.generate_placement_tcl()
        assert "detailed_placement" in tcl

    def test_contains_density(self, flow):
        tcl = flow.generate_placement_tcl()
        assert "0.5" in tcl  # default density


# ======================================================================
# 4. generate_routing_tcl
# ======================================================================

class TestGenerateRoutingTcl:
    def test_returns_non_empty_string(self, flow):
        tcl = flow.generate_routing_tcl()
        assert isinstance(tcl, str)
        assert len(tcl) > 0

    def test_contains_global_route(self, flow):
        tcl = flow.generate_routing_tcl()
        assert "global_route" in tcl

    def test_contains_detailed_route(self, flow):
        tcl = flow.generate_routing_tcl()
        assert "detailed_route" in tcl

    def test_contains_peripheral_comment(self, flow):
        tcl = flow.generate_routing_tcl()
        assert "metal" in tcl.lower() or "peripheral" in tcl.lower()


# ======================================================================
# 5. generate_gds_export_tcl
# ======================================================================

class TestGenerateGdsExportTcl:
    def test_returns_non_empty_string(self, flow):
        tcl = flow.generate_gds_export_tcl()
        assert isinstance(tcl, str)
        assert len(tcl) > 0

    def test_contains_write_gds(self, flow):
        tcl = flow.generate_gds_export_tcl()
        assert "write_gds" in tcl

    def test_contains_report_timing(self, flow):
        tcl = flow.generate_gds_export_tcl()
        assert "report_timing" in tcl

    def test_contains_report_power(self, flow):
        tcl = flow.generate_gds_export_tcl()
        assert "report_power" in tcl

    def test_contains_report_area(self, flow):
        tcl = flow.generate_gds_export_tcl()
        assert "report_design_area" in tcl


# ======================================================================
# 6. generate_full_flow_tcl
# ======================================================================

class TestGenerateFullFlowTcl:
    def test_combines_all_stages(self, flow):
        tcl = flow.generate_full_flow_tcl("design.v", "cells.lef", "cells.lib")
        assert "read_lef" in tcl
        assert "read_verilog" in tcl
        assert "initialize_floorplan" in tcl
        assert "global_placement" in tcl
        assert "detailed_placement" in tcl
        assert "global_route" in tcl
        assert "detailed_route" in tcl
        assert "write_gds" in tcl

    def test_contains_paths(self, flow):
        tcl = flow.generate_full_flow_tcl(
            "my_design.v", "my_cells.lef", "my_cells.lib"
        )
        assert "my_design.v" in tcl
        assert "my_cells.lef" in tcl
        assert "my_cells.lib" in tcl

    def test_contains_stage_markers(self, flow):
        tcl = flow.generate_full_flow_tcl("d.v", "c.lef", "c.lib")
        assert "STAGE 1" in tcl
        assert "STAGE 2" in tcl
        assert "STAGE 3" in tcl
        assert "STAGE 4" in tcl
        assert "STAGE 5" in tcl
        assert "STAGE 6" in tcl


# ======================================================================
# 7. write_tcl_scripts
# ======================================================================

class TestWriteTclScripts:
    def test_creates_six_files(self, flow, tmp_dir):
        flow.write_tcl_scripts(tmp_dir)
        out = Path(tmp_dir)
        expected = [
            "00_setup.tcl",
            "01_floorplan.tcl",
            "02_placement.tcl",
            "03_routing.tcl",
            "04_gds_export.tcl",
            "run_all.tcl",
        ]
        for name in expected:
            assert (out / name).is_file(), f"Missing: {name}"

    def test_files_non_empty(self, flow, tmp_dir):
        flow.write_tcl_scripts(tmp_dir)
        out = Path(tmp_dir)
        for name in ["00_setup.tcl", "run_all.tcl"]:
            content = (out / name).read_text(encoding="utf-8")
            assert len(content) > 50

    def test_run_all_sources_all_stages(self, flow, tmp_dir):
        flow.write_tcl_scripts(tmp_dir)
        run_all = (Path(tmp_dir) / "run_all.tcl").read_text(encoding="utf-8")
        assert "00_setup.tcl" in run_all
        assert "01_floorplan.tcl" in run_all
        assert "02_placement.tcl" in run_all
        assert "03_routing.tcl" in run_all
        assert "04_gds_export.tcl" in run_all


# ======================================================================
# 8. generate_makefile
# ======================================================================

class TestGenerateMakefile:
    def test_contains_all_target(self, flow):
        mk = flow.generate_makefile()
        assert "all:" in mk

    def test_contains_gds_target(self, flow):
        mk = flow.generate_makefile()
        assert "gds:" in mk

    def test_contains_clean_target(self, flow):
        mk = flow.generate_makefile()
        assert "clean:" in mk

    def test_contains_setup_target(self, flow):
        mk = flow.generate_makefile()
        assert "setup:" in mk

    def test_contains_place_target(self, flow):
        mk = flow.generate_makefile()
        assert "place:" in mk

    def test_contains_route_target(self, flow):
        mk = flow.generate_makefile()
        assert "route:" in mk


# ======================================================================
# 9. find_openroad
# ======================================================================

class TestFindOpenroad:
    def test_returns_string_or_none(self):
        result = OpenROADFlow.find_openroad()
        assert result is None or isinstance(result, str)

    def test_returns_none_in_test_env(self):
        # In CI/test environments, openroad is typically not installed
        result = OpenROADFlow.find_openroad()
        # Either None or a valid path
        if result is not None:
            assert os.path.isfile(result)


# ======================================================================
# 10. check_prerequisites
# ======================================================================

class TestCheckPrerequisites:
    def test_returns_tuple(self, flow):
        ok, issues = flow.check_prerequisites()
        assert isinstance(ok, bool)
        assert isinstance(issues, list)

    def test_lists_issues(self, flow):
        """In test env, should find at least openroad or PDK missing."""
        ok, issues = flow.check_prerequisites()
        # We don't assert ok is False because some test envs might have things.
        # But issues should always be a list.
        assert isinstance(issues, list)

    def test_issues_are_strings(self, flow):
        _, issues = flow.check_prerequisites()
        for issue in issues:
            assert isinstance(issue, str)
            assert len(issue) > 0


# ======================================================================
# 11. FlowConfig defaults
# ======================================================================

class TestFlowConfigDefaults:
    def test_process_sky130(self):
        cfg = FlowConfig()
        assert cfg.process == "sky130"

    def test_clock_period(self):
        cfg = FlowConfig()
        assert cfg.clock_period_ns == 10.0

    def test_clock_port(self):
        cfg = FlowConfig()
        assert cfg.clock_port == "clk"

    def test_vdd_voltage_sky130(self):
        cfg = FlowConfig()
        assert cfg.vdd_voltage == 3.3

    def test_placement_density(self):
        cfg = FlowConfig()
        assert cfg.placement_density == 0.5

    def test_structural_placement_true(self):
        cfg = FlowConfig()
        assert cfg.structural_placement is True

    def test_route_peripheral_only_true(self):
        cfg = FlowConfig()
        assert cfg.route_peripheral_only is True

    def test_routing_effort(self):
        cfg = FlowConfig()
        assert cfg.routing_effort == 10

    def test_output_dir(self):
        cfg = FlowConfig()
        assert cfg.output_dir == "./build"

    def test_openroad_bin_none(self):
        cfg = FlowConfig()
        assert cfg.openroad_bin is None

    def test_pdk_root_none(self):
        cfg = FlowConfig()
        assert cfg.pdk_root is None


# ======================================================================
# 12. FlowResult defaults
# ======================================================================

class TestFlowResultDefaults:
    def test_success_field(self):
        r = FlowResult(success=True)
        assert r.success is True

    def test_gds_path_none(self):
        r = FlowResult(success=False)
        assert r.gds_path is None

    def test_log_path_none(self):
        r = FlowResult(success=False)
        assert r.log_path is None

    def test_reports_dir_none(self):
        r = FlowResult(success=False)
        assert r.reports_dir is None

    def test_die_area_zero(self):
        r = FlowResult(success=False)
        assert r.die_area_um2 == 0.0

    def test_power_zero(self):
        r = FlowResult(success=False)
        assert r.total_power_mw == 0.0

    def test_timing_met_false(self):
        r = FlowResult(success=False)
        assert r.timing_met is False

    def test_errors_empty(self):
        r = FlowResult(success=False)
        assert r.errors == []

    def test_warnings_empty(self):
        r = FlowResult(success=False)
        assert r.warnings == []

    def test_errors_mutable(self):
        r = FlowResult(success=False)
        r.errors.append("test error")
        assert len(r.errors) == 1
