from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CellDef:
    """Definition of a single ROM cell type."""
    name: str            # e.g. "ROM_PLUS_X1"
    cell_type: str       # "plus", "minus", "zero", "pair_p", "pair_n", "ref_hi", "ref_lo"
    width_um: float      # cell width in micrometers
    height_um: float     # cell height in micrometers
    area_um2: float      # width * height
    transistors: int     # number of transistors
    leakage_pa: float    # leakage current in picoamps at nominal voltage
    delay_ns: float      # typical access delay in nanoseconds
    drive_strength: int  # 1, 2, or 4 (relative to X1)
    vt_flavor: str       # "std" (standard Vt), "lvt" (low Vt), "hvt" (high Vt)


# ======================================================================
# Process node database
# Each entry defines: cell_size_um, voltage, leakage_per_transistor_pa,
#   delay_ns, description, category
# ======================================================================

PROCESS_DB: Dict[str, dict] = {
    # --- Mature / open-source / educational ---
    "generic_180nm": {
        "cell_size": 2.00, "voltage": 5.0, "leakage_per_t": 800.0,
        "delay": 8.0, "description": "Generic 180nm bulk CMOS (educational/legacy)",
        "category": "legacy",
    },
    "generic_90nm": {
        "cell_size": 1.00, "voltage": 1.2, "leakage_per_t": 200.0,
        "delay": 3.5, "description": "Generic 90nm CMOS",
        "category": "mature",
    },
    "generic_65nm": {
        "cell_size": 0.70, "voltage": 1.2, "leakage_per_t": 80.0,
        "delay": 2.0, "description": "Generic 65nm CMOS",
        "category": "mature",
    },
    "generic_40nm": {
        "cell_size": 0.45, "voltage": 1.1, "leakage_per_t": 30.0,
        "delay": 1.2, "description": "Generic 40nm LP CMOS",
        "category": "mature",
    },
    "sky130": {
        "cell_size": 1.22, "voltage": 3.3, "leakage_per_t": 7.5,
        "delay": 2.5, "description": "SkyWater 130nm open-source process (TinyTapeout compatible)",
        "category": "open_source",
    },
    "ihp130_sige": {
        "cell_size": 1.10, "voltage": 3.3, "leakage_per_t": 5.0,
        "delay": 2.0, "description": "IHP 130nm SiGe BiCMOS (open-source, RF-capable)",
        "category": "open_source",
    },
    "gf45_rfsoc": {
        "cell_size": 0.80, "voltage": 1.8, "leakage_per_t": 15.0,
        "delay": 1.8, "description": "GlobalFoundries 45nm RFSOI",
        "category": "mature",
    },

    # --- 28nm family ---
    "generic_28nm": {
        "cell_size": 0.22, "voltage": 1.0, "leakage_per_t": 1.185,
        "delay": 0.5, "description": "Generic 28nm CMOS (production estimate)",
        "category": "production",
    },
    "tsmc28": {
        "cell_size": 0.20, "voltage": 0.9, "leakage_per_t": 1.0,
        "delay": 0.4, "description": "TSMC 28nm HPM",
        "category": "production",
    },
    "samsung28": {
        "cell_size": 0.21, "voltage": 1.0, "leakage_per_t": 1.2,
        "delay": 0.45, "description": "Samsung 28nm LPP",
        "category": "production",
    },
    "gf28_slp": {
        "cell_size": 0.23, "voltage": 1.0, "leakage_per_t": 1.5,
        "delay": 0.5, "description": "GlobalFoundries 28nm SLP",
        "category": "production",
    },
    "smic28": {
        "cell_size": 0.22, "voltage": 1.0, "leakage_per_t": 1.3,
        "delay": 0.48, "description": "SMIC 28nm LP",
        "category": "production",
    },
    "st28_fdsoi": {
        "cell_size": 0.20, "voltage": 1.0, "leakage_per_t": 0.3,
        "delay": 0.35, "description": "STMicroelectronics 28nm FDSOI (ultra-low leakage)",
        "category": "production",
    },

    # --- 22nm / FD-SOI ---
    "gf22_fdx": {
        "cell_size": 0.16, "voltage": 0.8, "leakage_per_t": 0.5,
        "delay": 0.25, "description": "GlobalFoundries 22nm FD-SOI (back-bias capable)",
        "category": "advanced",
    },
    "generic_22fdsoi": {
        "cell_size": 0.17, "voltage": 0.8, "leakage_per_t": 0.6,
        "delay": 0.27, "description": "Generic 22nm FD-SOI",
        "category": "advanced",
    },

    # --- 14-16nm FinFET ---
    "gf14_lpp": {
        "cell_size": 0.10, "voltage": 0.8, "leakage_per_t": 0.4,
        "delay": 0.15, "description": "GlobalFoundries 14nm LPP FinFET",
        "category": "advanced",
    },
    "samsung14_lpp": {
        "cell_size": 0.09, "voltage": 0.8, "leakage_per_t": 0.35,
        "delay": 0.14, "description": "Samsung 14nm LPP FinFET",
        "category": "advanced",
    },
    "intel22_ffl": {
        "cell_size": 0.12, "voltage": 0.9, "leakage_per_t": 0.6,
        "delay": 0.20, "description": "Intel 22nm FinFET (first production FinFET)",
        "category": "advanced",
    },
    "tsmc16": {
        "cell_size": 0.09, "voltage": 0.8, "leakage_per_t": 0.3,
        "delay": 0.12, "description": "TSMC 16nm FinFET (N16)",
        "category": "advanced",
    },
    "smic14": {
        "cell_size": 0.10, "voltage": 0.8, "leakage_per_t": 0.5,
        "delay": 0.16, "description": "SMIC 14nm FinFET",
        "category": "advanced",
    },

    # --- 12nm ---
    "tsmc12": {
        "cell_size": 0.08, "voltage": 0.8, "leakage_per_t": 0.25,
        "delay": 0.10, "description": "TSMC 12nm FinFET (N12)",
        "category": "cutting_edge",
    },
    "gf12_lp": {
        "cell_size": 0.08, "voltage": 0.8, "leakage_per_t": 0.28,
        "delay": 0.11, "description": "GlobalFoundries 12LP FinFET",
        "category": "cutting_edge",
    },
    "intel16": {
        "cell_size": 0.08, "voltage": 0.75, "leakage_per_t": 0.22,
        "delay": 0.09, "description": "Intel 16nm (14nm+ process)",
        "category": "cutting_edge",
    },
    "samsung11_lpp": {
        "cell_size": 0.07, "voltage": 0.75, "leakage_per_t": 0.20,
        "delay": 0.08, "description": "Samsung 11nm LPP (10nm-class)",
        "category": "cutting_edge",
    },

    # --- 7nm and below ---
    "tsmc7": {
        "cell_size": 0.05, "voltage": 0.7, "leakage_per_t": 0.15,
        "delay": 0.06, "description": "TSMC 7nm (N7) EUV",
        "category": "cutting_edge",
    },
    "samsung5_lpe": {
        "cell_size": 0.04, "voltage": 0.7, "leakage_per_t": 0.10,
        "delay": 0.05, "description": "Samsung 5LPE EUV",
        "category": "cutting_edge",
    },
    "intel7": {
        "cell_size": 0.05, "voltage": 0.7, "leakage_per_t": 0.12,
        "delay": 0.055, "description": "Intel 7 (formerly 10nm ESF)",
        "category": "cutting_edge",
    },
    "tsmc5": {
        "cell_size": 0.03, "voltage": 0.7, "leakage_per_t": 0.08,
        "delay": 0.04, "description": "TSMC 5nm (N5) EUV",
        "category": "cutting_edge",
    },
    "tsmc3": {
        "cell_size": 0.02, "voltage": 0.65, "leakage_per_t": 0.05,
        "delay": 0.03, "description": "TSMC 3nm (N3E) EUV (estimate)",
        "category": "frontier",
    },
    "intel4": {
        "cell_size": 0.02, "voltage": 0.7, "leakage_per_t": 0.06,
        "delay": 0.035, "description": "Intel 4 EUV (first Intel EUV node)",
        "category": "frontier",
    },
    "intel18a": {
        "cell_size": 0.015, "voltage": 0.65, "leakage_per_t": 0.04,
        "delay": 0.025, "description": "Intel 18A (Angstrom era, ribbonFET)",
        "category": "frontier",
    },
}


# Drive-strength scaling factors
DRIVE_SCALING = {
    1: {"width_mult": 1.0, "leakage_mult": 1.0, "delay_mult": 1.0},
    2: {"width_mult": 2.0, "leakage_mult": 2.0, "delay_mult": 0.65},
    4: {"width_mult": 4.0, "leakage_mult": 4.0, "delay_mult": 0.45},
}

# Vt-flavor leakage/delay modifiers
VT_MODIFIERS = {
    "std":  {"leakage_mult": 1.0, "delay_mult": 1.0},
    "lvt":  {"leakage_mult": 3.0, "delay_mult": 0.80},
    "hvt":  {"leakage_mult": 0.15, "delay_mult": 1.30},
}


def _build_cells_for_process(
    proc_name: str,
    proc: dict,
    drive_strengths: Tuple[int, ...] = (1, 2, 4),
    vt_flavors: Tuple[str, ...] = ("std",),
) -> Tuple[Dict[str, CellDef], str, str]:
    """Build all cell definitions for a single process node.

    For each (drive_strength, vt_flavor) combination, generates:
      ROM_PLUS_X{ds}[_{vt}], ROM_MINUS_X{ds}[_{vt}], ROM_ZERO_X{ds}[_{vt}]
    Plus reference cells: ROM_REF_HI, ROM_REF_LO (always X1 std)

    Returns (cells_dict, voltage_str, description_str).
    """
    sz = proc["cell_size"]
    vdd = proc["voltage"]
    lk_base = proc["leakage_per_t"]
    dl_base = proc["delay"]
    desc = proc["description"]

    cells: Dict[str, CellDef] = {}

    for ds in drive_strengths:
        ds_info = DRIVE_SCALING[ds]
        w = sz * ds_info["width_mult"]
        for vt in vt_flavors:
            vt_info = VT_MODIFIERS[vt]

            suffix = f"_X{ds}"
            if vt != "std":
                suffix += f"_{vt}"

            # Plus cell: 2 transistors
            lk = lk_base * 2 * ds_info["leakage_mult"] * vt_info["leakage_mult"]
            dl = dl_base * ds_info["delay_mult"] * vt_info["delay_mult"]
            cells[f"ROM_PLUS{suffix}"] = CellDef(
                name=f"ROM_PLUS{suffix}",
                cell_type="plus",
                width_um=round(w, 6),
                height_um=round(sz, 6),
                area_um2=round(w * sz, 8),
                transistors=2,
                leakage_pa=round(lk, 6),
                delay_ns=round(dl, 6),
                drive_strength=ds,
                vt_flavor=vt,
            )

            # Minus cell: 2 transistors (same params as plus)
            cells[f"ROM_MINUS{suffix}"] = CellDef(
                name=f"ROM_MINUS{suffix}",
                cell_type="minus",
                width_um=round(w, 6),
                height_um=round(sz, 6),
                area_um2=round(w * sz, 8),
                transistors=2,
                leakage_pa=round(lk, 6),
                delay_ns=round(dl, 6),
                drive_strength=ds,
                vt_flavor=vt,
            )

            # Zero cell: 0 transistors, but same physical footprint
            cells[f"ROM_ZERO{suffix}"] = CellDef(
                name=f"ROM_ZERO{suffix}",
                cell_type="zero",
                width_um=round(w, 6),
                height_um=round(sz, 6),
                area_um2=round(w * sz, 8),
                transistors=0,
                leakage_pa=0.0,
                delay_ns=0.0,
                drive_strength=ds,
                vt_flavor=vt,
            )

    # Reference cells (always X1 std) — used for differential sensing
    cells["ROM_REF_HI"] = CellDef(
        name="ROM_REF_HI", cell_type="ref_hi",
        width_um=round(sz, 6), height_um=round(sz, 6),
        area_um2=round(sz * sz, 8),
        transistors=2, leakage_pa=round(lk_base * 2, 6),
        delay_ns=round(dl_base, 6), drive_strength=1, vt_flavor="std",
    )
    cells["ROM_REF_LO"] = CellDef(
        name="ROM_REF_LO", cell_type="ref_lo",
        width_um=round(sz, 6), height_um=round(sz, 6),
        area_um2=round(sz * sz, 8),
        transistors=2, leakage_pa=round(lk_base * 2, 6),
        delay_ns=round(dl_base, 6), drive_strength=1, vt_flavor="std",
    )

    return cells, str(vdd), desc


class ROMCellLibrary:
    """ROM cell library for a specific process node.

    Manages ROM cell types (PLUS, MINUS, ZERO, REF) across multiple
    drive strengths and Vt flavors, and generates EDA tool input files
    (LEF, LIB, Verilog behavioral models).

    Bundled libraries span 30 process nodes from 180nm to 18A,
    with X1/X2/X4 drive strengths and std/lvt/hvt Vt flavors.

    Categories:
    - open_source: sky130, ihp130_sige (free PDKs)
    - legacy: 180nm, 90nm
    - mature: 65nm, 40nm, 28nm family
    - production: TSMC/Samsung/GF/SMIC 28nm
    - advanced: 22nm FD-SOI, 14-16nm FinFET
    - cutting_edge: 12nm, 7nm, 5nm
    - frontier: 3nm, Intel 18A

    Example:
        lib = ROMCellLibrary.from_bundle("sky130")
        lib.write_all("output/cells/")

        # List all available processes
        ROMCellLibrary.list_processes()
    """

    BUNDLES: Dict[str, dict] = {}

    # Default drive strengths and Vt flavors for each category
    _CATEGORY_DEFAULTS = {
        "legacy": {"drives": (1,), "vts": ("std",)},
        "open_source": {"drives": (1, 2), "vts": ("std", "lvt")},
        "mature": {"drives": (1, 2), "vts": ("std", "lvt", "hvt")},
        "production": {"drives": (1, 2, 4), "vts": ("std", "lvt", "hvt")},
        "advanced": {"drives": (1, 2, 4), "vts": ("std", "lvt", "hvt")},
        "cutting_edge": {"drives": (1, 2, 4), "vts": ("std", "lvt", "hvt")},
        "frontier": {"drives": (1, 2, 4), "vts": ("std", "lvt", "hvt")},
    }

    @classmethod
    def _build_all_bundles(cls):
        """Lazily build the full BUNDLES dictionary from PROCESS_DB."""
        if cls.BUNDLES:
            return
        for name, proc in PROCESS_DB.items():
            cat = proc["category"]
            defaults = cls._CATEGORY_DEFAULTS.get(cat, cls._CATEGORY_DEFAULTS["production"])
            cells, voltage, description = _build_cells_for_process(
                name, proc,
                drive_strengths=defaults["drives"],
                vt_flavors=defaults["vts"],
            )
            cls.BUNDLES[name] = {
                **cells,
                "voltage": voltage,
                "process": name,
                "description": description,
                "category": cat,
            }

    def __init__(
        self,
        cells: Dict[str, CellDef],
        voltage: float,
        process: str,
        description: str = "",
        category: str = "",
    ):
        self.cells = cells
        self.voltage = voltage
        self.process = process
        self.description = description
        self.category = category

    @classmethod
    def from_bundle(cls, name: str) -> "ROMCellLibrary":
        """Load a bundled cell library.

        Args:
            name: Process node identifier (e.g. 'sky130', 'tsmc7', 'intel18a').

        Raises:
            ValueError: If the process name is not in the database.
        """
        cls._build_all_bundles()
        if name not in cls.BUNDLES:
            raise ValueError(
                f"Unknown bundle '{name}'. "
                f"Available: {sorted(cls.BUNDLES.keys())}"
            )
        bundle = cls.BUNDLES[name]
        cells = {k: v for k, v in bundle.items() if isinstance(v, CellDef)}
        return cls(
            cells=cells,
            voltage=float(bundle["voltage"]),
            process=bundle["process"],
            description=bundle["description"],
            category=bundle.get("category", ""),
        )

    @classmethod
    def from_custom(
        cls,
        process_name: str,
        cell_size_um: float,
        voltage: float,
        leakage_per_transistor_pa: float,
        delay_ns: float,
        description: str = "",
        drive_strengths: Tuple[int, ...] = (1, 2, 4),
        vt_flavors: Tuple[str, ...] = ("std", "lvt", "hvt"),
    ) -> "ROMCellLibrary":
        """Create a custom cell library for a user-defined process.

        Args:
            process_name: Identifier for this process.
            cell_size_um: Base cell size in micrometers (square cell).
            voltage: Nominal supply voltage.
            leakage_per_transistor_pa: Leakage per transistor in pA.
            delay_ns: Base X1 std-Vt access delay in nanoseconds.
            description: Human-readable description.
            drive_strengths: Tuple of drive strengths (default: 1, 2, 4).
            vt_flavors: Tuple of Vt flavors (default: std, lvt, hvt).
        """
        proc = {
            "cell_size": cell_size_um,
            "voltage": voltage,
            "leakage_per_t": leakage_per_transistor_pa,
            "delay": delay_ns,
            "description": description or f"Custom {process_name}",
            "category": "custom",
        }
        cells, vdd_str, desc_str = _build_cells_for_process(
            process_name, proc,
            drive_strengths=drive_strengths,
            vt_flavors=vt_flavors,
        )
        return cls(
            cells=cells,
            voltage=voltage,
            process=process_name,
            description=desc_str,
            category="custom",
        )

    @classmethod
    def list_processes(cls) -> List[dict]:
        """List all available process nodes with metadata.

        Returns:
            List of dicts with keys: name, category, description, voltage,
            cell_size_um, n_cells.
        """
        cls._build_all_bundles()
        result = []
        for name, bundle in cls.BUNDLES.items():
            n_cells = sum(1 for v in bundle.values() if isinstance(v, CellDef))
            proc_db = PROCESS_DB[name]
            result.append({
                "name": name,
                "category": bundle.get("category", ""),
                "description": bundle["description"],
                "voltage": float(bundle["voltage"]),
                "cell_size_um": proc_db["cell_size"],
                "n_cells": n_cells,
            })
        return sorted(result, key=lambda x: PROCESS_DB[x["name"]]["cell_size"], reverse=True)

    @classmethod
    def list_categories(cls) -> Dict[str, List[str]]:
        """Group process names by category."""
        cls._build_all_bundles()
        groups: Dict[str, List[str]] = {}
        for name, bundle in cls.BUNDLES.items():
            cat = bundle.get("category", "custom")
            groups.setdefault(cat, []).append(name)
        return groups

    def get_cells_by_type(self, cell_type: str) -> Dict[str, CellDef]:
        """Filter cells by type ('plus', 'minus', 'zero', 'ref_hi', 'ref_lo')."""
        return {k: v for k, v in self.cells.items() if v.cell_type == cell_type}

    def get_cells_by_drive(self, drive: int) -> Dict[str, CellDef]:
        """Filter cells by drive strength (1, 2, or 4)."""
        return {k: v for k, v in self.cells.items() if v.drive_strength == drive}

    def get_cells_by_vt(self, vt: str) -> Dict[str, CellDef]:
        """Filter cells by Vt flavor ('std', 'lvt', 'hvt')."""
        return {k: v for k, v in self.cells.items() if v.vt_flavor == vt}

    def get_default_cell(self, cell_type: str) -> CellDef:
        """Get the default (X1 std-Vt) cell for a given type.

        Args:
            cell_type: 'plus', 'minus', or 'zero'.

        Raises:
            KeyError: If no default cell exists for this type.
        """
        prefix = f"ROM_{cell_type.upper()}_X1"
        # Try std first
        for name, cell in self.cells.items():
            if name == prefix or name == f"{prefix}_std":
                return cell
        # Fallback: any X1 variant
        for name, cell in self.cells.items():
            if name.startswith(prefix):
                return cell
        raise KeyError(f"No default cell found for type '{cell_type}'")

    # ------------------------------------------------------------------
    # EDA file generation
    # ------------------------------------------------------------------

    def generate_verilog(self) -> str:
        """Generate Verilog behavioral models for all cells.

        ROM_PLUS: when WL=1, BL = VDD (representing +1)
        ROM_MINUS: when WL=1, BL = VSS (representing -1)
        ROM_ZERO: BL = 0 (no connection)
        ROM_REF_HI: always drives BL to VDD (reference voltage high)
        ROM_REF_LO: always drives BL to VSS (reference voltage low)
        """
        lines: List[str] = []
        lines.append(f"// ternary-rom cell library: {self.process}")
        lines.append("// Generated by ROMCellLibrary")
        lines.append(f"// {self.description}")
        lines.append(f"// Cells: {len(self.cells)}")
        lines.append("")

        # Sort cells: PLUS, MINUS, ZERO, REF by drive strength then Vt
        type_order = {"plus": 0, "minus": 1, "zero": 2, "ref_hi": 3, "ref_lo": 4}
        sorted_cells = sorted(
            self.cells.items(),
            key=lambda kv: (
                type_order.get(kv[1].cell_type, 99),
                kv[1].drive_strength,
                kv[1].vt_flavor,
            ),
        )

        for name, cell in sorted_cells:
            lines.append(f"module {name} (WL, BL);")
            if cell.cell_type == "plus":
                lines.append(
                    "  // ROM_PLUS: when WL=1, drives BL to VDD (weight +1)"
                )
            elif cell.cell_type == "minus":
                lines.append(
                    "  // ROM_MINUS: when WL=1, drives BL to VSS (weight -1)"
                )
            elif cell.cell_type == "zero":
                lines.append(
                    "  // ROM_ZERO: no transistors, BL left floating (weight 0)"
                )
            elif cell.cell_type == "ref_hi":
                lines.append(
                    "  // ROM_REF_HI: always drives BL to VDD (reference high)"
                )
            elif cell.cell_type == "ref_lo":
                lines.append(
                    "  // ROM_REF_LO: always drives BL to VSS (reference low)"
                )
            lines.append(f"  // Drive: X{cell.drive_strength}, Vt: {cell.vt_flavor}")
            lines.append(f"  // Size: {cell.width_um} x {cell.height_um} um, Leakage: {cell.leakage_pa} pA")
            lines.append("  input WL;")
            lines.append("  output BL;")
            lines.append("")

            if cell.cell_type == "plus":
                lines.append("  assign BL = WL ? 1'b1 : 1'bz;")
            elif cell.cell_type == "minus":
                lines.append("  assign BL = WL ? 1'b0 : 1'bz;")
            elif cell.cell_type == "zero":
                lines.append("  assign BL = 1'bz;")
            elif cell.cell_type == "ref_hi":
                lines.append("  assign BL = 1'b1;")
            elif cell.cell_type == "ref_lo":
                lines.append("  assign BL = 1'b0;")

            lines.append("")
            lines.append("endmodule")
            lines.append("")

        while lines and lines[-1] == "":
            lines.pop()
        lines.append("")
        return "\n".join(lines)

    def generate_lef(self) -> str:
        """Generate LEF macro definitions for all cells.

        LEF defines the physical layout abstraction for P&R tools.
        Includes: MACRO, SIZE, PIN definitions with DIRECTION/LAYER/PLACEMENT,
        OBS (obstruction) for routing blockage.

        Drive-strength cells are wider (proportional to drive),
        Vt flavor is noted in comments only (same physical layout).
        """
        lines: List[str] = []
        lines.append("VERSION 5.8 ;")
        lines.append('BUSBITCHARS "[]" ;')
        lines.append(chr(68)+chr(73)+chr(86)+chr(73)+chr(68)+chr(69)+chr(82)+chr(67)+chr(72)+chr(65)+chr(82)+chr(32)+chr(34)+chr(47)+chr(34)+chr(32)+chr(59)+chr(10))
        lines.append("")

        type_order = {"plus": 0, "minus": 1, "zero": 2, "ref_hi": 3, "ref_lo": 4}
        sorted_cells = sorted(
            self.cells.items(),
            key=lambda kv: (
                type_order.get(kv[1].cell_type, 99),
                kv[1].drive_strength,
                kv[1].vt_flavor,
            ),
        )

        for name, cell in sorted_cells:
            w = cell.width_um
            h = cell.height_um
            pin_h = round(h * 0.1, 4)
            wl_y0 = h - pin_h
            bl_y1 = pin_h

            lines.append(f"MACRO {name}")
            lines.append(f"  CLASS CORE ;")
            lines.append(f"  SIZE {w:.4f} BY {h:.4f} ;")
            lines.append(f"  SYMMETRY X Y ;")
            lines.append(f"  // Drive: X{cell.drive_strength}, Vt: {cell.vt_flavor}, Leakage: {cell.leakage_pa} pA")
            lines.append("")

            lines.append(f"  PIN WL")
            lines.append(f"    DIRECTION INPUT ;")
            lines.append(f"    USE SIGNAL ;")
            lines.append(f"    PORT")
            lines.append(f"      LAYER Metal1 ;")
            lines.append(f"        RECT 0.0000 {wl_y0:.4f} {w:.4f} {h:.4f} ;")
            lines.append(f"    END")
            lines.append(f"  END WL")
            lines.append("")

            lines.append(f"  PIN BL")
            lines.append(f"    DIRECTION OUTPUT ;")
            lines.append(f"    USE SIGNAL ;")
            lines.append(f"    PORT")
            lines.append(f"      LAYER Metal2 ;")
            lines.append(f"        RECT 0.0000 0.0000 {w:.4f} {bl_y1:.4f} ;")
            lines.append(f"    END")
            lines.append(f"  END BL")
            lines.append("")

            lines.append(f"  OBS")
            lines.append(f"    LAYER Metal1 ;")
            lines.append(f"      RECT 0.0000 0.0000 {w:.4f} {wl_y0:.4f} ;")
            lines.append(f"    LAYER Metal2 ;")
            lines.append(f"      RECT 0.0000 {bl_y1:.4f} {w:.4f} {h:.4f} ;")
            lines.append(f"  END")
            lines.append("")

            lines.append(f"END {name}")
            lines.append("")

        lines.append("END LIBRARY")
        lines.append("")
        return "\n".join(lines)

    def generate_lib(self) -> str:
        """Generate Liberty (.lib) timing characterization.

        Liberty format for synthesis. Defines:
        - Cell area
        - Pin directions and capacitance
        - Timing arcs (WL->BL) with delay and power
        - Internal power (leakage)
        - Drive-strength-aware capacitance scaling
        """
        lines: List[str] = []
        lib_name = f"ternary_rom_{self.process}"
        lines.append(f"library({lib_name}) {{")
        lines.append(f"  technology (cmos) ;")
        lines.append(f"  delay_model : generic_cmos ;")
        lines.append(f'  time_unit : "1ns" ;')
        lines.append(f'  voltage_unit : "1V" ;')
        lines.append(f"  capacitive_load_unit (1.0, pf) ;")
        lines.append(f'  leakage_power_unit : "1pW" ;')
        lines.append("")
        lines.append(f"  default_operating_conditions (nom) {{")
        lines.append(f"    voltage : {self.voltage:.2f} ;")
        lines.append(f"  }}")
        lines.append("")
        lines.append(f"  lu_table_template(delay_template_1x1) {{")
        lines.append(f"    variable_1 : input_net_transition ;")
        lines.append(f"    variable_2 : total_output_net_capacitance ;")
        lines.append(f'    index_1 ("0.010") ;')
        lines.append(f'    index_2 ("0.020") ;')
        lines.append(f"  }}")
        lines.append("")

        type_order = {"plus": 0, "minus": 1, "zero": 2, "ref_hi": 3, "ref_lo": 4}
        sorted_cells = sorted(
            self.cells.items(),
            key=lambda kv: (
                type_order.get(kv[1].cell_type, 99),
                kv[1].drive_strength,
                kv[1].vt_flavor,
            ),
        )

        for name, cell in sorted_cells:
            leakage_pw = self.voltage * cell.leakage_pa
            # Input capacitance scales with drive strength
            input_cap = 0.500 * cell.drive_strength

            lines.append(f"  cell ({name}) {{")
            lines.append(f"    area : {cell.area_um2:.6f} ;")
            lines.append(f"    cell_leakage_power : {leakage_pw:.6f} ;")
            lines.append(f"    // Drive: X{cell.drive_strength}, Vt: {cell.vt_flavor}")
            lines.append("")

            lines.append(f"    pin (WL) {{")
            lines.append(f"      direction : input ;")
            lines.append(f"      capacitance : {input_cap:.3f} ;")
            lines.append(f"    }}")
            lines.append("")

            lines.append(f"    pin (BL) {{")
            lines.append(f"      direction : output ;")
            lines.append(f"      max_capacitance : 0.500 ;")

            if cell.cell_type not in ("zero",) and cell.delay_ns > 0:
                lines.append(f"      timing () {{")
                lines.append(f'        related_pin : "WL" ;')
                if cell.cell_type in ("plus", "ref_hi"):
                    lines.append(f"        timing_sense : positive_unate ;")
                else:
                    lines.append(f"        timing_sense : negative_unate ;")
                lines.append("")

                if cell.cell_type in ("plus", "ref_hi"):
                    lines.append(f"        cell_rise (delay_template_1x1) {{")
                    lines.append(f'          values ("{cell.delay_ns:.4f}") ;')
                    lines.append(f"        }}")
                    lines.append(f"        rise_transition (delay_template_1x1) {{")
                    lines.append(f'          values ("{0.100 / cell.drive_strength:.4f}") ;')
                    lines.append(f"        }}")
                    lines.append(f"        cell_fall (delay_template_1x1) {{")
                    lines.append(f'          values ("0.0000") ;')
                    lines.append(f"        }}")
                    lines.append(f"        fall_transition (delay_template_1x1) {{")
                    lines.append(f'          values ("0.0000") ;')
                    lines.append(f"        }}")
                else:  # minus, ref_lo
                    lines.append(f"        cell_rise (delay_template_1x1) {{")
                    lines.append(f'          values ("0.0000") ;')
                    lines.append(f"        }}")
                    lines.append(f"        rise_transition (delay_template_1x1) {{")
                    lines.append(f'          values ("0.0000") ;')
                    lines.append(f"        }}")
                    lines.append(f"        cell_fall (delay_template_1x1) {{")
                    lines.append(f'          values ("{cell.delay_ns:.4f}") ;')
                    lines.append(f"        }}")
                    lines.append(f"        fall_transition (delay_template_1x1) {{")
                    lines.append(f'          values ("{0.100 / cell.drive_strength:.4f}") ;')
                    lines.append(f"        }}")

                lines.append(f"      }}")

            lines.append(f"    }}")
            lines.append(f"  }}")
            lines.append("")

        lines.append(f"}}")
        lines.append("")
        return "\n".join(lines)

    def write_all(self, output_dir: str):
        """Write all cell library files to directory.

        Creates:
        - cells.v (Verilog behavioral models)
        - cells.lef (LEF macro definitions)
        - cells.lib (Liberty timing)
        - cells.vh (Verilog include header with parameter defines)
        - cells.json (machine-readable cell catalog)
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        (out / "cells.v").write_text(self.generate_verilog())
        (out / "cells.lef").write_text(self.generate_lef())
        (out / "cells.lib").write_text(self.generate_lib())
        (out / "cells.vh").write_text(self._generate_vh())
        (out / "cells.json").write_text(self._generate_json())

    def _generate_vh(self) -> str:
        """Generate Verilog header with parameter defines."""
        lines: List[str] = []
        lines.append(f"// ternary-rom cell library: {self.process}")
        lines.append("// Generated by ROMCellLibrary")
        lines.append(f"// {self.description}")
        lines.append("")

        default_plus = self.get_default_cell("plus")
        lines.append(f"`define ROM_CELL_WIDTH_UM {default_plus.width_um}")
        lines.append(f"`define ROM_CELL_HEIGHT_UM {default_plus.height_um}")
        lines.append(f"`define ROM_CELL_AREA_UM2 {default_plus.area_um2}")
        lines.append(f"`define ROM_VOLTAGE {self.voltage}")
        lines.append(f'`define ROM_PROCESS "{self.process}"')
        lines.append(f"`define ROM_NUM_CELLS {len(self.cells)}")
        lines.append("")

        for name, cell in self.cells.items():
            lines.append(f"`define {name}_DELAY_NS {cell.delay_ns}")
            lines.append(f"`define {name}_TRANSISTORS {cell.transistors}")
            lines.append(f"`define {name}_LEAKAGE_PA {cell.leakage_pa}")
            lines.append(f"`define {name}_DRIVE_X{cell.drive_strength}")
            lines.append(f'`define {name}_VT_{cell.vt_flavor.upper()}')
            lines.append("")
        return "\n".join(lines)

    def _generate_json(self) -> str:
        """Generate machine-readable JSON cell catalog."""
        import json

        catalog = {
            "process": self.process,
            "description": self.description,
            "category": self.category,
            "voltage": self.voltage,
            "num_cells": len(self.cells),
            "cells": {},
        }
        for name, cell in self.cells.items():
            catalog["cells"][name] = {
                "type": cell.cell_type,
                "width_um": cell.width_um,
                "height_um": cell.height_um,
                "area_um2": cell.area_um2,
                "transistors": cell.transistors,
                "leakage_pa": cell.leakage_pa,
                "delay_ns": cell.delay_ns,
                "drive_strength": cell.drive_strength,
                "vt_flavor": cell.vt_flavor,
            }
        return json.dumps(catalog, indent=2) + "\n"

    def summary(self) -> str:
        """Human-readable summary of the cell library."""
        lines: List[str] = []
        lines.append(f"ROM Cell Library: {self.process}")
        lines.append(f"  {self.description}")
        lines.append(f"  Category:   {self.category}")
        lines.append(f"  Voltage:    {self.voltage}V")
        lines.append(f"  Cells:      {len(self.cells)}")
        lines.append("")

        # Group by drive strength
        for ds in sorted(set(c.drive_strength for c in self.cells.values())):
            ds_cells = self.get_cells_by_drive(ds)
            lines.append(f"  Drive X{ds} ({len(ds_cells)} cells):")
            type_order = {"plus": 0, "minus": 1, "zero": 2, "ref_hi": 3, "ref_lo": 4}
            for name, cell in sorted(ds_cells.items(), key=lambda kv: (type_order.get(kv[1].cell_type, 99), kv[1].vt_flavor)):
                vt_tag = f" [{cell.vt_flavor}]" if cell.vt_flavor != "std" else ""
                lines.append(f"    {name}{vt_tag}:")
                lines.append(f"      Type:        {cell.cell_type}")
                lines.append(f"      Size:        {cell.width_um} x {cell.height_um} um")
                lines.append(f"      Area:        {cell.area_um2} um^2")
                lines.append(f"      Transistors: {cell.transistors}")
                lines.append(f"      Leakage:     {cell.leakage_pa} pA")
                lines.append(f"      Delay:       {cell.delay_ns} ns")
            lines.append("")

        # Density estimate (using smallest cell)
        x1_plus = self.get_default_cell("plus")
        if x1_plus.area_um2 > 0:
            cells_per_mm2 = 1e6 / x1_plus.area_um2
            bits_equiv = cells_per_mm2 * 1.585
            lines.append(f"  Density (X1):     {cells_per_mm2:.1f} cells/mm2")
            lines.append(f"                    ~{bits_equiv / 1e6:.1f} Mbit-equiv/mm2")

        return "\n".join(lines)
