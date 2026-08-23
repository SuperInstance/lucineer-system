//////////////////////////////////////////////////////////////////////////////
// Ternary 8x8 MAC Tile for TinyTapeout (sky130)
//
// Computes: output[col] = SUM(input[row] * W[row][col]) for row=0..7
//
// Weights are mask-programmed in ROM cells:
//   ROM_PLUS:  drives +input onto bitline (weight = +1)
//   ROM_MINUS: drives -input onto bitline (weight = -1)
//   ROM_ZERO:  no connection (weight = 0, zero leakage)
//
// Time-multiplexed: 8 clock cycles to process one complete input vector.
// FSM: IDLE -> COMPUTING (8 cycles) -> DONE
//////////////////////////////////////////////////////////////////////////////

module ternary_mac_8x8 (
    input  wire        clk,
    input  wire        rst_n,
    input  wire [7:0]  ui_in,     // input activation element
    output reg  [7:0]  uo_out,    // accumulated result
    input  wire [7:0]  uio_in,    // [2:0] col_select, [3] start
    output reg  [7:0]  uio_out,
    output reg  [7:0]  uio_oe
);

    // ── Input decomposition ──
    wire [2:0] col_select = uio_in[2:0];
    wire       start      = uio_in[3];
    wire [7:0] input_val  = ui_in;

    // ── FSM states ──
    localparam IDLE     = 3'd0;
    localparam COMPUTING = 3'd1;
    localparam DONE     = 3'd2;

    reg [2:0] state;
    reg [2:0] row_cnt;      // current row (0-7)
    reg [7:0] accumulator;  // signed accumulator
    reg       valid;        // output valid flag

    // ── Hardcoded ternary weight matrix (mask-programmed) ──
    // Each row: 8 weights, each in {-1, 0, +1}
    // This matrix is determined by the metal mask during fabrication.
    // To change weights, re-fabricate with a new mask.
    //
    // Encoding per weight: 2'b00 = +1, 2'b01 = 0, 2'b10 = -1
    localparam [15:0] WEIGHTS_ROW0 = 16'b00_01_10_00_01_01_10_01;  // row 0: + . - + + - +
    localparam [15:0] WEIGHTS_ROW1 = 16'b01_00_01_10_01_00_01_00;  // row 1: . + . - + . + .
    localparam [15:0] WEIGHTS_ROW2 = 16'b10_00_01_00_10_01_00_01;  // row 2: - . + . - + . +
    localparam [15:0] WEIGHTS_ROW3 = 16'b01_10_00_01_01_10_00_01;  // row 3: . - + + + - . +
    localparam [15:0] WEIGHTS_ROW4 = 16'b00_01_10_01_00_01_10_00;  // row 4: + . - + . + - .
    localparam [15:0] WEIGHTS_ROW5 = 16'b10_01_00_01_10_00_01_10;  // row 5: - + . + - . + -
    localparam [15:0] WEIGHTS_ROW6 = 16'b01_10_01_00_01_10_01_00;  // row 6: . - + . + - + .
    localparam [15:0] WEIGHTS_ROW7 = 16'b00_01_10_10_01_00_01_10;  // row 7: + . - - + . + -

    // ── Weight extraction for current row and selected column ──
    reg [1:0] weight_encoded;
    reg       weight_sign;  // 0 = zero/skip, 1 = use weight
    reg       weight_neg;   // 0 = positive, 1 = negative

    always @(*) begin
        case (row_cnt)
            3'd0: weight_encoded = WEIGHTS_ROW0[col_select*2 +: 2];
            3'd1: weight_encoded = WEIGHTS_ROW1[col_select*2 +: 2];
            3'd2: weight_encoded = WEIGHTS_ROW2[col_select*2 +: 2];
            3'd3: weight_encoded = WEIGHTS_ROW3[col_select*2 +: 2];
            3'd4: weight_encoded = WEIGHTS_ROW4[col_select*2 +: 2];
            3'd5: weight_encoded = WEIGHTS_ROW5[col_select*2 +: 2];
            3'd6: weight_encoded = WEIGHTS_ROW6[col_select*2 +: 2];
            3'd7: weight_encoded = WEIGHTS_ROW7[col_select*2 +: 2];
            default: weight_encoded = 2'b01; // zero
        endcase
    end

    // Decode weight: 00=+1, 01=0, 10=-1
    always @(*) begin
        case (weight_encoded)
            2'b00: begin weight_sign = 1; weight_neg = 0; end  // +1
            2'b01: begin weight_sign = 0; weight_neg = 0; end  // 0
            2'b10: begin weight_sign = 1; weight_neg = 1; end  // -1
            default: begin weight_sign = 0; weight_neg = 0; end
        endcase
    end

    // ── Signed add/subtract for accumulation ──
    wire [7:0] add_result  = accumulator + input_val;
    wire [7:0] sub_result  = accumulator - input_val;

    // ── FSM ──
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state       <= IDLE;
            row_cnt     <= 3'd0;
            accumulator <= 8'd0;
            valid       <= 1'b0;
            uo_out      <= 8'd0;
            uio_out     <= 8'd0;
            uio_oe      <= 8'd0;
        end else begin
            case (state)
                IDLE: begin
                    valid <= 1'b0;
                    uio_oe <= 8'd0;
                    if (start) begin
                        state       <= COMPUTING;
                        row_cnt     <= 3'd0;
                        accumulator <= 8'd0;
                    end
                end

                COMPUTING: begin
                    // Accumulate: add or subtract based on weight
                    if (weight_sign && !weight_neg)
                        accumulator <= add_result;      // weight = +1
                    else if (weight_sign && weight_neg)
                        accumulator <= sub_result;      // weight = -1
                    // weight = 0: skip (no change to accumulator)

                    if (row_cnt == 3'd7) begin
                        state   <= DONE;
                        valid   <= 1'b1;
                    end else begin
                        row_cnt <= row_cnt + 3'd1;
                    end
                end

                DONE: begin
                    // Output the result
                    uo_out  <= accumulator;
                    uio_out <= {5'd0, valid, row_cnt};
                    uio_oe  <= 8'hFF;
                    if (!start) begin
                        state <= IDLE;
                        valid <= 1'b0;
                    end
                end

                default: state <= IDLE;
            endcase
        end
    end

endmodule
