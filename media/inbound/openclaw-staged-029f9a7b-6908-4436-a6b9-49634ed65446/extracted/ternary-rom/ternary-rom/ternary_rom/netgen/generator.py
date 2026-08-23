"""Structural Verilog netlist generator from ternary weight matrices.

Converts dictionaries of ternary weight matrices (-1, 0, +1) into
structural Verilog that instantiates ROM_PLUS, ROM_MINUS cells in
a regular grid pattern with an adder tree for accumulation.

The generated netlist targets mask-programmed ROM where the metal
mask defines which cell type occupies each grid position.
"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class ROMArraySpec:
    """Specification for a single ROM array."""
    name: str
    rows: int                 # input dimension (K)
    cols: int                 # output dimension (N)
    weights: np.ndarray       # int8, shape (rows, cols), values in {-1, 0, +1}
    plus_count: int           # number of +1 cells
    minus_count: int          # number of -1 cells
    zero_count: int           # number of 0 cells
    zero_fraction: float      # fraction of cells that are zero
    estimated_area_mm2: float # rows * cols * cell_area
    estimated_leakage_uw: float  # (plus_count + minus_count) * 2.37 pA


@dataclass
class NetlistConfig:
    """Configuration for netlist generation."""
    cell_lib: str = "sky130"           # any process from ROMCellLibrary
    word_width: int = 16               # accumulator width in bits
    pipeline_depth: int = 0            # 0 = combinational, 1+ = pipelined
    adder_style: str = "ripple"        # "ripple" or "tree"
    time_mux_factor: int = 1           # if >1, time-multiplex the array
    include_testbench: bool = False    # append a verification testbench
    include_decoupling: bool = True    # add decoupling cap comments in footer
    drive_strength: int = 1            # 1 (X1), 2 (X2), or 4 (X4)
    vt_flavor: str = "std"             # "std", "lvt", or "hvt"


class NetlistGenerator:
    """Generate structural Verilog netlist from ternary weights.

    Converts a dictionary of ternary weight matrices into structural
    Verilog that instantiates ROM_PLUS, ROM_MINUS, and ROM_ZERO cells
    in a regular grid pattern.

    The generated netlist is designed for mask-programmed ROM where
    the metal mask defines which cell type occupies each position.

    Example:
        weights = {"layer1": np.array([[1,0,-1],[0,1,0]], dtype=np.int8)}
        gen = NetlistGenerator(weights, cell_lib="sky130")
        gen.write_verilog("output/model.v")
        gen.write_summary("output/model_summary.txt")
    """

    CELL_INSTANTIATION_TEMPLATES = {
        "sky130": {
            "ROM_PLUS": (
                "    ROM_PLUS_X1 rom_{row}_{col} "
                "(.WL(wl[{row}]), .BL(bl[{col}]), .VDD(VDD), .VSS(VSS));"
            ),
            "ROM_MINUS": (
                "    ROM_MINUS_X1 rom_{row}_{col} "
                "(.WL(wl[{row}]), .BL(bl[{col}]), .VDD(VDD), .VSS(VSS));"
            ),
            "ROM_ZERO": (
                "    // rom_{row}_{col}: ZERO weight "
                "\u2014 no cell instantiated"
            ),
        },
        "generic_28nm": {
            "ROM_PLUS": (
                "    ROM_PLUS_X1 rom_{row}_{col} "
                "(.wl(wl[{row}]), .bl(bl[{col}]), .vdd(vdd), .vss(vss));"
            ),
            "ROM_MINUS": (
                "    ROM_MINUS_X1 rom_{row}_{col} "
                "(.wl(wl[{row}]), .bl(bl[{col}]), .vdd(vdd), .vss(vss));"
            ),
            "ROM_ZERO": (
                "    // rom_{row}_{col}: ZERO weight "
                "\u2014 no cell instantiated"
            ),
        },
    }

    @staticmethod
    def _get_cell_names(cell_lib: str, drive: int = 1, vt: str = "std") -> dict:
        """Get ROM_PLUS, ROM_MINUS, ROM_ZERO cell names for any process.

        Falls back to legacy templates if cell library not available.
        """
        try:
            from ternary_rom.cells.library import ROMCellLibrary
            lib = ROMCellLibrary.from_bundle(cell_lib)
            suffix = f"_X{drive}"
            if vt != "std":
                suffix += f"_{vt}"
            return {
                "ROM_PLUS": f"ROM_PLUS{suffix}",
                "ROM_MINUS": f"ROM_MINUS{suffix}",
                "ROM_ZERO": f"ROM_ZERO{suffix}",
            }
        except (ValueError, ImportError):
            return {
                "ROM_PLUS": "ROM_PLUS_X1",
                "ROM_MINUS": "ROM_MINUS_X1",
                "ROM_ZERO": "ROM_ZERO_X1",
            }

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        weights: Dict[str, np.ndarray],
        config: Optional[NetlistConfig] = None,
    ):
        if not weights:
            raise ValueError("weights dictionary must not be empty")

        self.weights: Dict[str, np.ndarray] = {}
        for name, w in weights.items():
            w_arr = np.asarray(w, dtype=np.int8).copy()
            if w_arr.ndim != 2:
                raise ValueError(
                    f"Weight matrix '{name}' must be 2D, "
                    f"got shape {w_arr.shape}"
                )
            if w_arr.size == 0:
                raise ValueError(
                    f"Weight matrix '{name}' must not be empty"
                )
            unique_vals = np.unique(w_arr)
            for v in unique_vals:
                if int(v) not in (-1, 0, 1):
                    raise ValueError(
                        f"Weight matrix '{name}' contains invalid value {v}, "
                        f"must be in {{-1, 0, +1}}"
                    )
            self.weights[name] = w_arr

        self.config = config or NetlistConfig()
        self._specs: Optional[List[ROMArraySpec]] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze_arrays(self) -> List[ROMArraySpec]:
        """Analyze all weight matrices and return ROM array specs.

        Returns specs for the full logical weight matrices
        (time-multiplexing is an implementation detail handled
        during netlist generation, not analysis).
        """
        if self._specs is not None:
            return self._specs

        specs: List[ROMArraySpec] = []
        for name, w in self.weights.items():
            rows, cols = w.shape
            plus = int(np.sum(w == 1))
            minus = int(np.sum(w == -1))
            zero = int(np.sum(w == 0))
            total = rows * cols
            specs.append(
                ROMArraySpec(
                    name=name,
                    rows=rows,
                    cols=cols,
                    weights=w,
                    plus_count=plus,
                    minus_count=minus,
                    zero_count=zero,
                    zero_fraction=(zero / total) if total > 0 else 0.0,
                    estimated_area_mm2=self.rom_area_estimate(rows, cols),
                    estimated_leakage_uw=self.rom_leakage_estimate(plus, minus),
                )
            )
        self._specs = specs
        return specs

    def generate(self) -> str:
        """Generate complete structural Verilog netlist as string.

        Structure (per layer):
        1. Module declaration with word lines, bit lines, clk, vdd, vss
        2. Wire declarations
        3. ROM cell instantiations (one per non-zero weight)
        4. Adder tree for accumulation
        5. Output register (if pipelined)
        6. Endmodule
        7. Optional testbench

        If multiple layers are present, they are concatenated with
        separator comments.
        """
        specs = self.analyze_arrays()
        if not specs:
            return ""

        parts: List[str] = []
        for i, spec in enumerate(specs):
            if i > 0:
                parts.append("")
                parts.append("// " + "=" * 78)
                parts.append("")
            parts.append(self._generate_single(self._get_effective_spec(spec)))
        return "\n".join(parts)

    def write_verilog(
        self, output_path: str, layer_name: Optional[str] = None
    ):
        """Write Verilog netlist to file.

        If *layer_name* is ``None`` and multiple layers exist,
        writes one file per layer (``<stem>_<layer><ext>``).
        """
        path = Path(output_path)
        specs = self.analyze_arrays()

        if layer_name is not None:
            spec = next((s for s in specs if s.name == layer_name), None)
            if spec is None:
                raise ValueError(
                    f"No layer named '{layer_name}' found; "
                    f"available: {[s.name for s in specs]}"
                )
            verilog = self._generate_single(self._get_effective_spec(spec))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(verilog, encoding="utf-8")
        elif len(specs) == 1:
            verilog = self._generate_single(self._get_effective_spec(specs[0]))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(verilog, encoding="utf-8")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            for spec in specs:
                layer_path = (
                    path.parent / f"{path.stem}_{spec.name}{path.suffix}"
                )
                verilog = self._generate_single(self._get_effective_spec(spec))
                layer_path.write_text(verilog, encoding="utf-8")

    def write_summary(self, output_path: str):
        """Write a human-readable summary of all ROM arrays.

        Includes: name, shape, cell counts, zero fraction, area, leakage.
        """
        lines: List[str] = [
            "Ternary ROM Array Summary",
            "=" * 50,
        ]
        for spec in self.analyze_arrays():
            lines.append("")
            lines.append(f"Layer: {spec.name}")
            lines.append(f"  Shape:            {spec.rows} x {spec.cols}")
            lines.append(f"  ROM_PLUS cells:   {spec.plus_count}")
            lines.append(f"  ROM_MINUS cells:  {spec.minus_count}")
            lines.append(f"  ROM_ZERO cells:   {spec.zero_count}")
            lines.append(f"  Zero fraction:    {spec.zero_fraction:.4f}")
            lines.append(f"  Estimated area:   {spec.estimated_area_mm2:.6f} mm^2")
            lines.append(f"  Est. leakage:     {spec.estimated_leakage_uw:.6f} uW")
        lines.append("")
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")

    def write_weight_map(self, output_path: str):
        """Write a human-readable weight map showing ROM cell types.

        Format: grid of ``+`` / ``-`` / ``.`` characters
        for ``+1`` / ``-1`` / ``0``.
        """
        lines: List[str] = []
        for spec in self.analyze_arrays():
            lines.append(
                f"// Weight map for {spec.name} "
                f"({spec.rows} x {spec.cols})"
            )
            for r in range(spec.rows):
                row_chars: List[str] = []
                for c in range(spec.cols):
                    w = int(spec.weights[r, c])
                    if w == 1:
                        row_chars.append("+")
                    elif w == -1:
                        row_chars.append("-")
                    else:
                        row_chars.append(".")
                lines.append("".join(row_chars))
            lines.append("")
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")

    # ------------------------------------------------------------------
    # Static utility methods
    # ------------------------------------------------------------------

    @staticmethod
    def rom_area_estimate(
        rows: int, cols: int, cell_area_um2: float = 0.048
    ) -> float:
        """Estimate ROM array area in mm\u00b2.

        Default cell area: 0.048 um\u00b2 (28 nm, 0.22 um \u00d7 0.22 um).
        """
        return rows * cols * cell_area_um2 * 1e-6

    @staticmethod
    def rom_leakage_estimate(
        plus_count: int,
        minus_count: int,
        leakage_per_cell_pa: float = 2.37,
        voltage: float = 1.0,
    ) -> float:
        """Estimate ROM leakage power in microwatts.

        Zero cells (no transistor) have zero leakage.
        Non-zero cells leak at *leakage_per_cell_pa* pA each at *voltage* V.
        """
        return (plus_count + minus_count) * leakage_per_cell_pa * voltage * 1e-6

    # ------------------------------------------------------------------
    # Internal: effective spec (time-multiplexing)
    # ------------------------------------------------------------------

    def _get_effective_spec(self, spec: ROMArraySpec) -> ROMArraySpec:
        """Return an effective spec that accounts for time multiplexing.

        When ``time_mux_factor > 1`` the physical ROM array only
        stores the first ``rows // mux`` rows.  The remaining rows
        are cycled through in subsequent time steps.
        """
        if self.config.time_mux_factor <= 1:
            return spec

        mux = self.config.time_mux_factor
        eff_rows = max(spec.rows // mux, 1)
        eff_weights = spec.weights[:eff_rows, :]

        plus = int(np.sum(eff_weights == 1))
        minus = int(np.sum(eff_weights == -1))
        zero = int(np.sum(eff_weights == 0))
        total = eff_rows * spec.cols

        return ROMArraySpec(
            name=spec.name,
            rows=eff_rows,
            cols=spec.cols,
            weights=eff_weights,
            plus_count=plus,
            minus_count=minus,
            zero_count=zero,
            zero_fraction=(zero / total) if total > 0 else 0.0,
            estimated_area_mm2=self.rom_area_estimate(eff_rows, spec.cols),
            estimated_leakage_uw=self.rom_leakage_estimate(plus, minus),
        )

    # ------------------------------------------------------------------
    # Internal: single-layer Verilog generation
    # ------------------------------------------------------------------

    def _generate_single(self, spec: ROMArraySpec) -> str:
        """Generate Verilog for a single ROM array layer."""
        parts: List[str] = [
            self._generate_header(spec.name, spec),
            self._generate_rom_cells(spec),
            self._generate_adder_tree(spec),
            self._generate_output_stage(spec),
        ]

        if self.config.include_decoupling:
            parts.append(self._generate_decoupling_footer(spec))

        parts.append("endmodule\n")

        if self.config.include_testbench:
            parts.append(self._generate_testbench(spec.name, spec))

        return "".join(parts)

    # ------------------------------------------------------------------
    # Internal: header (module + wires)
    # ------------------------------------------------------------------

    def _generate_header(
        self, layer_name: str, spec: ROMArraySpec
    ) -> str:
        """Generate module declaration and wire declarations."""
        K = spec.rows
        N = spec.cols
        W = self.config.word_width
        lib = self.config.cell_lib

        lines: List[str] = [
            f"// Ternary ROM: {layer_name}",
            "// Generated by ternary-rom NetlistGenerator",
            (
                f"// Array: {K} x {N}, "
                f"{spec.plus_count} PLUS, {spec.minus_count} MINUS, "
                f"{spec.zero_count} ZERO"
            ),
            f"// Cell library: {lib}",
            f"// Adder style: {self.config.adder_style}, "
            f"Pipeline depth: {self.config.pipeline_depth}",
        ]

        if self.config.time_mux_factor > 1:
            lines.append(
                f"// Time multiplex factor: {self.config.time_mux_factor} "
                f"(physical rows: {K}, full logical rows: "
                f"{K * self.config.time_mux_factor})"
            )

        # Module ports
        lines.append(f"module ternary_rom_{layer_name} (")
        lines.append(f"    input  wire [{K-1}:0] wl,")
        lines.append(f"    input  wire clk,")
        if lib == "sky130":
            lines.append(f"    input  wire VDD,")
            lines.append(f"    input  wire VSS,")
        else:
            lines.append(f"    input  wire vdd,")
            lines.append(f"    input  wire vss,")

        if self.config.pipeline_depth > 0:
            lines.append(f"    output reg  [{N*W-1}:0] result")
        else:
            lines.append(f"    output wire [{N*W-1}:0] result")
        lines.append(");")

        # Wire declarations
        lines.append("")
        lines.append("// Bit line wires (physical interconnect for ROM cells)")
        lines.append(f"wire [{N-1}:0] bl;")
        lines.append("")
        lines.append(
            "// Column accumulator wires (signed, one per output column)"
        )
        lines.append(f"wire signed [{W-1}:0] col_accum [0:{N-1}];")
        lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal: ROM cell grid
    # ------------------------------------------------------------------

    def _generate_rom_cells(self, spec: ROMArraySpec) -> str:
        """Generate ROM cell instantiations for all positions.

        * ``+1``  →  instantiate ``ROM_PLUS``
        * ``-1``  →  instantiate ``ROM_MINUS``
        * `` 0``  →  comment only (no transistor, saves leakage)
        """
        templates = self.CELL_INSTANTIATION_TEMPLATES[self.config.cell_lib]

        lines: List[str] = [
            "// " + "-" * 70,
            "// ROM Cell Instantiations",
            (
                f"// Total: {spec.plus_count} ROM_PLUS, "
                f"{spec.minus_count} ROM_MINUS, "
                f"{spec.zero_count} ZERO (no cell)"
            ),
            "// " + "-" * 70,
        ]

        for r in range(spec.rows):
            for c in range(spec.cols):
                w = int(spec.weights[r, c])
                if w == 1:
                    tmpl = templates["ROM_PLUS"]
                elif w == -1:
                    tmpl = templates["ROM_MINUS"]
                else:
                    tmpl = templates["ROM_ZERO"]
                lines.append(tmpl.format(row=r, col=c))

        lines.append("")
        return "\n".join(lines) + "\n"

    # ------------------------------------------------------------------
    # Internal: adder tree
    # ------------------------------------------------------------------

    def _generate_adder_tree(self, spec: ROMArraySpec) -> str:
        """Generate adder tree to accumulate column results.

        Each bit line conceptually sums contributions from all word
        lines::

            bl_accum[col] = \u03a3( rom[r,c] \u00d7 wl[r] )  for all r

        ``ROM_PLUS`` contributes ``+wl[r]``, ``ROM_MINUS`` contributes
        ``-wl[r]``, and ``ROM_ZERO`` contributes nothing.

        Uses either ripple-carry or tree adder based on config.
        """
        K = spec.rows
        N = spec.cols
        W = self.config.word_width

        lines: List[str] = [
            "// " + "-" * 70,
            "// Adder Tree: accumulate +/- word line contributions per column",
            "// " + "-" * 70,
        ]

        for c in range(N):
            plus_rows = [r for r in range(K) if int(spec.weights[r, c]) == 1]
            minus_rows = [r for r in range(K) if int(spec.weights[r, c]) == -1]

            # Build ordered term list: all positives first, then negatives
            terms: List[Tuple[int, bool]] = [
                (r, True) for r in plus_rows
            ] + [
                (r, False) for r in minus_rows
            ]

            lines.append(
                f"// Column {c}: {len(plus_rows)} PLUS, "
                f"{len(minus_rows)} MINUS"
            )

            if not terms:
                # Column is entirely zero
                lines.append(f"assign col_accum[{c}] = {W}'sd0;")
                lines.append("")
                continue

            # ---- generate per-cell term wires ----
            term_wires: List[str] = []
            for i, (r, is_plus) in enumerate(terms):
                wire_name = f"col{c}_t{i}_r{r}"
                if W > 1:                                          
                    # Build Verilog zero-extension: {N{1'b0}, wl[r]}
                    # Use string concat to avoid f-string brace escaping hell
                    zext = "{" + str(W - 1) + "{1'b0}}"          
                    concat = "{" + zext + ", wl[" + str(r) + "]}"  
                    if is_plus:                                        
                        lines.append(                                   
                            f"wire signed [{W-1}:0] {wire_name} "       
                            f"= {concat};"                              
                        )                                                 
                    else:                                                
                        lines.append(                                   
                            f"wire signed [{W-1}:0] {wire_name} "       
                            f"= -{concat};"                             
                        )
                else:
                    if is_plus:
                        lines.append(
                            f"wire signed [0:0] {wire_name} = wl[{r}];"
                        )
                    else:
                        lines.append(
                            f"wire signed [0:0] {wire_name} = -wl[{r}];"
                        )
                term_wires.append(wire_name)

            # ---- sum all terms ----
            if len(term_wires) == 1:
                lines.append(
                    f"assign col_accum[{c}] = {term_wires[0]};"
                )
            elif self.config.adder_style == "tree":
                self._gen_tree_adder(lines, c, W, term_wires)
                lines.append(f"assign col_accum[{c}] = {term_wires[0]};")
                # Note: _gen_tree_adder reduces term_wires in-place to [final]
            else:
                self._gen_ripple_adder(lines, c, W, term_wires)
                lines.append(
                    f"assign col_accum[{c}] = {term_wires[-1]};"
                )

            lines.append("")

        return "\n".join(lines) + "\n"

    @staticmethod
    def _gen_tree_adder(
        lines: List[str],
        col: int,
        width: int,
        terms: List[str],
    ) -> None:
        """Append tree-style adder wires.  *terms* is mutated to [result]."""
        level = 0
        current = list(terms)
        while len(current) > 1:
            nxt: List[str] = []
            for i in range(0, len(current), 2):
                if i + 1 < len(current):
                    s = f"col{col}_s{level}_{i // 2}"
                    lines.append(
                        f"wire signed [{width-1}:0] {s} = "
                        f"{current[i]} + {current[i + 1]};"
                    )
                    nxt.append(s)
                else:
                    nxt.append(current[i])
            current = nxt
            level += 1
        terms.clear()
        terms.append(current[0])

    @staticmethod
    def _gen_ripple_adder(
        lines: List[str],
        col: int,
        width: int,
        terms: List[str],
    ) -> None:
        """Append ripple-style adder wires.  Last element of *terms* is result."""
        s = f"col{col}_r0"
        lines.append(
            f"wire signed [{width-1}:0] {s} = "
            f"{terms[0]} + {terms[1]};"
        )
        for i in range(2, len(terms)):
            ns = f"col{col}_r{i - 1}"
            lines.append(
                f"wire signed [{width-1}:0] {ns} = {s} + {terms[i]};"
            )
            s = ns
        terms[-1] = s

    # ------------------------------------------------------------------
    # Internal: output stage
    # ------------------------------------------------------------------

    def _generate_output_stage(self, spec: ROMArraySpec) -> str:
        """Generate output register and optional pipeline stages."""
        N = spec.cols
        W = self.config.word_width

        lines: List[str] = [
            "// " + "-" * 70,
            "// Output Stage",
            "// " + "-" * 70,
        ]

        if self.config.pipeline_depth > 0:
            lines.append("always @(posedge clk) begin")
            for c in range(N):
                lo = c * W
                hi = (c + 1) * W - 1
                lines.append(
                    f"    result[{hi}:{lo}] <= col_accum[{c}];"
                )
            lines.append("end")
        else:
            for c in range(N):
                lo = c * W
                hi = (c + 1) * W - 1
                lines.append(
                    f"assign result[{hi}:{lo}] = col_accum[{c}];"
                )

        lines.append("")
        return "\n".join(lines) + "\n"

    # ------------------------------------------------------------------
    # Internal: decoupling cap footer
    # ------------------------------------------------------------------

    def _generate_decoupling_footer(self, spec: ROMArraySpec) -> str:
        """Generate comments / placeholders for decoupling capacitors."""
        N = spec.cols
        lines: List[str] = [
            "// " + "-" * 70,
            "// Decoupling Capacitors (footer)",
            f"// {N} columns \u00d7 1 cap per column recommended",
            "// " + "-" * 70,
        ]
        for c in range(N):
            lines.append(
                f"// decap_{c}: decoupling cap for column {c} bit line"
            )
        lines.append("")
        return "\n".join(lines) + "\n"

    # ------------------------------------------------------------------
    # Internal: testbench
    # ------------------------------------------------------------------

    def _generate_testbench(
        self, layer_name: str, spec: ROMArraySpec
    ) -> str:
        """Generate a simple testbench for verification.

        Applies three sets of test vectors:

        1. All word lines inactive (expect all-zero output)
        2. Each row activated individually (expect per-row weights)
        3. All word lines active (expect column sums)

        Reports PASS / FAIL via ``$display``.
        """
        K = spec.rows
        N = spec.cols
        W = self.config.word_width
        pipelined = self.config.pipeline_depth > 0
        lib = self.config.cell_lib

        # Choose appropriate delay: for pipelined, wait for clock edge;
        # for combinational, just wait for propagation.
        delay = "@(posedge clk); #1;" if pipelined else "#10;"

        # Power/net names depend on library
        if lib == "sky130":
            pwr, gnd = "VDD", "VSS"
        else:
            pwr, gnd = "vdd", "vss"

        lines: List[str] = [
            f"module tb_ternary_rom_{layer_name};",
            f"    reg  [{K-1}:0] wl;",
            "    reg  clk;",
            f"    reg  {pwr};",
            f"    reg  {gnd};",
            f"    wire [{N*W-1}:0] result;",
            "",
            f"    ternary_rom_{layer_name} dut (",
            f"        .wl(wl),",
            f"        .clk(clk),",
            f"        .{pwr}({pwr}),",
            f"        .{gnd}({gnd}),",
            f"        .result(result)",
            f"    );",
            "",
            "    // Clock: 10 ns period (50 MHz)",
            "    initial clk = 1'b0;",
            "    always #5 clk = ~clk;",
            "",
            "    // Power supplies",
            "    initial begin",
            f"        {pwr} = 1'b1;",
            f"        {gnd} = 1'b0;",
            "    end",
            "",
            "    integer errors = 0;",
            "",
        ]

        # ---- helper to emit a column check ----
        def _check(col: int, expected: int) -> None:
            lo = col * W
            hi = (col + 1) * W - 1
            lines.append(
                f"        if ($signed(result[{hi}:{lo}]) != {expected}) begin"
            )
            lines.append(
                f"            $display(\"FAIL: col {col} expected "
                f"{expected}, got %d\", "
                f"$signed(result[{hi}:{lo}]));"
            )
            lines.append("            errors = errors + 1;")
            lines.append("        end")

        lines.append("    initial begin")

        # --- Test 1: all word lines inactive ---
        lines.append("        // Test 1: all word lines inactive")
        lines.append("        wl = 0;")
        lines.append(f"        {delay}")
        for c in range(N):
            _check(c, 0)
        lines.append("")

        # --- Test 2: each row individually ---
        for r in range(K):
            lines.append(f"        // Test 2.{r}: activate row {r}")
            lines.append(f"        wl = 0; wl[{r}] = 1'b1;")
            lines.append(f"        {delay}")
            for c in range(N):
                expected = int(spec.weights[r, c])
                if expected != 0:
                    _check(c, expected)
                else:
                    _check(c, 0)
            lines.append("")

        # --- Test 3: all word lines active ---
        lines.append("        // Test 3: all word lines active")
        all_ones = (1 << K) - 1
        lines.append(f"        wl = {all_ones};")
        lines.append(f"        {delay}")
        for c in range(N):
            expected = int(np.sum(spec.weights[:, c]))
            _check(c, expected)
        lines.append("")

        # --- Summary ---
        lines.append("        if (errors == 0)")
        lines.append(
            f"            $display(\"PASS: all tests passed for {layer_name}\");"
        )
        lines.append("        else")
        lines.append(
            f"            $display(\"FAIL: %0d errors in {layer_name}\", errors);"
        )
        lines.append("        $finish;")
        lines.append("    end")
        lines.append("endmodule")
        lines.append("")

        return "\n".join(lines) + "\n"
