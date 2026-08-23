"""Tests for the ternary-rom CLI.

Uses subprocess to invoke the CLI entry point.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest


# ======================================================================
# Fixtures: create test weight files
# ======================================================================

@pytest.fixture
def test_weights_npy(tmp_path):
    """Create a small test weights .npy file."""
    np.random.seed(42)
    weights = {
        "fc1.weight": np.random.randn(16, 32).astype(np.float64),
        "dt_proj.weight": np.random.randn(8, 16).astype(np.float64),
    }
    # Save as a single stacked array (simplest .npy format)
    w_stacked = np.stack([weights["fc1.weight"], weights["dt_proj.weight"]])
    p = tmp_path / "test_weights.npy"
    np.save(str(p), w_stacked)
    return str(p)


@pytest.fixture
def test_weights_npz(tmp_path):
    """Create a small test weights .npz file."""
    np.random.seed(42)
    weights = {
        "fc1.weight": np.random.randn(16, 32).astype(np.float64),
        "dt_proj.weight": np.random.randn(8, 16).astype(np.float64),
    }
    p = tmp_path / "test_weights.npz"
    np.savez(str(p), **weights)
    return str(p)


@pytest.fixture
def test_ternary_weights_npz(tmp_path):
    """Create ternary weights .npz file for netlist generation."""
    np.random.seed(42)
    w1 = np.random.choice([-1, 0, 1], size=(8, 4)).astype(np.int8)
    w2 = np.random.choice([-1, 0, 1], size=(4, 8)).astype(np.int8)
    p = tmp_path / "ternary_weights.npz"
    np.savez(str(p), fc1=w1, fc2=w2)
    return str(p)


def _run_cli(*args, expect_fail=False):
    """Run the CLI as a subprocess and return (returncode, stdout, stderr)."""
    # Use python -m to invoke the module
    cmd = [sys.executable, "-m", "ternary_rom.cli.main"] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
        cwd="/home/z/my-project/ternary-rom",
    )
    return result.returncode, result.stdout, result.stderr


# ======================================================================
# 1. ternary-rom --help exits 0
# ======================================================================

class TestHelp:
    def test_help_exits_zero(self):
        rc, out, err = _run_cli("--help")
        assert rc == 0
        assert "ternary-rom" in out
        assert "analyze" in out

    def test_version_exits_zero(self):
        rc, out, err = _run_cli("-v")
        assert rc == 0


# ======================================================================
# 2. ternary-rom info exits 0 and prints version
# ======================================================================

class TestInfo:
    def test_info_exits_zero(self):
        rc, out, err = _run_cli("info")
        assert rc == 0

    def test_info_prints_version(self):
        rc, out, err = _run_cli("info")
        assert "0.1.0" in out or "ternary-rom" in out

    def test_info_prints_processes(self):
        rc, out, err = _run_cli("info")
        assert "sky130" in out
        assert "generic_28nm" in out

    def test_info_prints_openroad_status(self):
        rc, out, err = _run_cli("info")
        assert "OpenROAD" in out


# ======================================================================
# 3. ternary-rom cells sky130 creates cell files
# ======================================================================

class TestCells:
    def test_sky130_creates_files(self, tmp_path):
        out_dir = str(tmp_path / "test_cells")
        rc, out, err = _run_cli("cells", "sky130", "-o", out_dir)
        assert rc == 0
        out_p = Path(out_dir)
        assert (out_p / "cells.v").is_file()
        assert (out_p / "cells.lef").is_file()
        assert (out_p / "cells.lib").is_file()
        assert (out_p / "cells.vh").is_file()

    def test_28nm_creates_files(self, tmp_path):
        out_dir = str(tmp_path / "test_cells_28nm")
        rc, out, err = _run_cli("cells", "generic_28nm", "-o", out_dir)
        assert rc == 0
        out_p = Path(out_dir)
        assert (out_p / "cells.v").is_file()
        assert (out_p / "cells.lef").is_file()
        assert (out_p / "cells.lib").is_file()

    def test_cells_prints_summary(self):
        rc, out, err = _run_cli("cells", "sky130", "-o", "/tmp/test_cells_cli")
        assert rc == 0
        assert "ROM" in out


# ======================================================================
# 4. ternary-rom analyze prints sensitivity table
# ======================================================================

class TestAnalyze:
    def test_analyze_with_npz(self, test_weights_npz, tmp_path):
        out_dir = str(tmp_path / "analyze_out")
        rc, out, err = _run_cli("analyze", test_weights_npz, "-o", out_dir)
        assert rc == 0
        assert "Layer" in out  # markdown table header
        assert "fc1" in out

    def test_analyze_saves_report(self, test_weights_npz, tmp_path):
        out_dir = str(tmp_path / "analyze_out2")
        rc, out, err = _run_cli("analyze", test_weights_npz, "-o", out_dir)
        assert rc == 0
        assert (Path(out_dir) / "sensitivity_report.md").is_file()


# ======================================================================
# 5. ternary-rom ternarize creates output .npz
# ======================================================================

class TestTernarize:
    def test_ternarize_creates_npz(self, test_weights_npz, tmp_path):
        out_dir = str(tmp_path / "tern_out")
        rc, out, err = _run_cli("ternarize", test_weights_npz, "-o", out_dir)
        assert rc == 0
        assert (Path(out_dir) / "ternary_weights.npz").is_file()

    def test_ternarize_prints_report(self, test_weights_npz, tmp_path):
        out_dir = str(tmp_path / "tern_out2")
        rc, out, err = _run_cli("ternarize", test_weights_npz, "-o", out_dir)
        assert rc == 0
        assert "Ternarization Report" in out
        assert "cosine" in out.lower() or "Cos Sim" in out

    def test_ternarize_skip_layers(self, test_weights_npz, tmp_path):
        out_dir = str(tmp_path / "tern_out3")
        rc, out, err = _run_cli(
            "ternarize", test_weights_npz, "-o", out_dir,
            "--skip-layers", "dt_proj"
        )
        assert rc == 0


# ======================================================================
# 6. ternary-rom netlist creates .v file
# ======================================================================

class TestNetlist:
    def test_netlist_creates_verilog(self, test_ternary_weights_npz, tmp_path):
        out_dir = str(tmp_path / "netlist_out")
        rc, out, err = _run_cli(
            "netlist", test_ternary_weights_npz, "-o", out_dir
        )
        assert rc == 0
        # The netlist generator writes design.v or per-layer files
        out_p = Path(out_dir)
        v_files = list(out_p.glob("**/*.v"))
        assert len(v_files) > 0

    def test_netlist_summary(self, test_ternary_weights_npz, tmp_path):
        out_dir = str(tmp_path / "netlist_out2")
        rc, out, err = _run_cli(
            "netlist", test_ternary_weights_npz, "-o", out_dir
        )
        assert rc == 0
        assert (Path(out_dir) / "summary.txt").is_file()

    def test_netlist_process_option(self, test_ternary_weights_npz, tmp_path):
        out_dir = str(tmp_path / "netlist_out3")
        rc, out, err = _run_cli(
            "netlist", test_ternary_weights_npz, "-o", out_dir,
            "--process", "generic_28nm"
        )
        assert rc == 0
        assert "generic_28nm" in out


# ======================================================================
# 7. ternary-rom flow --help shows flow-specific options
# ======================================================================

class TestFlowHelp:
    def test_flow_help_exits_zero(self):
        rc, out, err = _run_cli("flow", "--help")
        assert rc == 0

    def test_flow_help_shows_execute(self):
        rc, out, err = _run_cli("flow", "--help")
        assert "--execute" in out

    def test_flow_help_shows_lef(self):
        rc, out, err = _run_cli("flow", "--help")
        assert "--lef" in out

    def test_flow_help_shows_process(self):
        rc, out, err = _run_cli("flow", "--help")
        assert "--process" in out

    def test_flow_generates_tcl(self, tmp_path):
        # Create a dummy netlist
        dummy_v = tmp_path / "dummy.v"
        dummy_v.write_text("module top(input clk, output reg [7:0] out); endmodule\n")

        out_dir = str(tmp_path / "flow_out")
        rc, out, err = _run_cli(
            "flow", str(dummy_v), "-o", out_dir
        )
        assert rc == 0
        assert "00_setup.tcl" in out
        assert "run_all.tcl" in out
        assert (Path(out_dir) / "00_setup.tcl").is_file()
        assert (Path(out_dir) / "Makefile").is_file()
