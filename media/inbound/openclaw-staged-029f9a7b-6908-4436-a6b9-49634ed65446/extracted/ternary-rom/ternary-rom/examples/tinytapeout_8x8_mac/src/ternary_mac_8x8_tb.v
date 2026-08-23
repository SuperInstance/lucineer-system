//////////////////////////////////////////////////////////////////////////////
// Testbench for ternary_mac_8x8
//
// Tests all 8 output columns of the 8x8 ternary MAC tile.
// Uses the hardcoded weight matrix from the design.
//////////////////////////////////////////////////////////////////////////////

`timescale 1ns / 1ps

module ternary_mac_8x8_tb;

    // Inputs
    reg         clk;
    reg         rst_n;
    reg  [7:0]  ui_in;
    reg  [7:0]  uio_in;

    // Outputs
    wire [7:0]  uo_out;
    wire [7:0]  uio_out;
    wire [7:0]  uio_oe;

    // Test parameters
    reg [7:0] test_input [0:7];
    integer   col, row, errors;

    // DUT
    ternary_mac_8x8 dut (
        .clk(clk),
        .rst_n(rst_n),
        .ui_in(ui_in),
        .uo_out(uo_out),
        .uio_in(uio_in),
        .uio_out(uio_out),
        .uio_oe(uio_oe)
    );

    // Clock: 10ns period (100 MHz)
    initial clk = 0;
    always #5 clk = ~clk;

    // Expected weight matrix (matching the hardcoded weights)
    // Encoded: 2'b00=+1, 2'b01=0, 2'b10=-1
    // Row 0: + . - + + - +  => [+1, 0, -1, +1, +1, 0, -1, +1]
    // Row 1: . + . - + . + .  => [0, +1, 0, -1, +1, 0, +1, 0]
    // Row 2: - . + . - + . +  => [-1, 0, +1, 0, -1, +1, 0, +1]
    // Row 3: . - + + + - . +  => [0, -1, +1, +1, +1, -1, 0, +1]
    // Row 4: + . - + . + - .  => [+1, 0, -1, +1, 0, +1, -1, 0]
    // Row 5: - + . + - . + -  => [-1, +1, 0, +1, -1, 0, +1, -1]
    // Row 6: . - + . + - + .  => [0, -1, +1, 0, +1, -1, +1, 0]
    // Row 7: + . - - + . + -  => [+1, 0, -1, -1, +1, 0, +1, -1]

    // Expected output for input = [1,2,3,4,5,6,7,8]:
    // col0: 1*1 + 2*0 + 3*(-1) + 4*0 + 5*1 + 6*(-1) + 7*0 + 8*1 = 1+0-3+0+5-6+0+8 = 5
    // col1: 1*0 + 2*1 + 3*0 + 4*(-1) + 5*0 + 6*1 + 7*(-1) + 8*0 = 0+2+0-4+0+6-7+0 = -3
    // col2: 1*(-1) + 2*0 + 3*1 + 4*1 + 5*(-1) + 6*0 + 7*1 + 8*(-1) = -1+0+3+4-5+0+7-8 = 0
    // col3: 1*1 + 2*(-1) + 3*0 + 4*1 + 5*1 + 6*1 + 7*0 + 8*(-1) = 1-2+0+4+5+6+0-8 = 6
    // col4: 1*1 + 2*1 + 3*(-1) + 4*1 + 5*0 + 6*(-1) + 7*1 + 8*1 = 1+2-3+4+0-6+7+8 = 13
    // col5: 1*0 + 2*0 + 3*1 + 4*(-1) + 5*1 + 6*0 + 7*(-1) + 8*0 = 0+0+3-4+5+0-7+0 = -3
    // col6: 1*(-1) + 2*1 + 3*0 + 4*0 + 5*(-1) + 6*1 + 7*1 + 8*1 = -1+2+0+0-5+6+7+8 = 17
    // col7: 1*1 + 2*0 + 3*1 + 4*1 + 5*0 + 6*(-1) + 7*0 + 8*(-1) = 1+0+3+4+0-6+0-8 = -6

    // Expected results (signed 8-bit two's complement)
    reg [7:0] expected [0:7];

    initial begin
        // Set expected values
        expected[0] = 8'd5;    // 5
        expected[1] = 8'd253;  // -3 in two's complement
        expected[2] = 8'd0;    // 0
        expected[3] = 8'd6;    // 6
        expected[4] = 8'd13;   // 13
        expected[5] = 8'd253;  // -3
        expected[6] = 8'd17;   // 17
        expected[7] = 8'd250;  // -6

        // Set test input vector
        test_input[0] = 8'd1;
        test_input[1] = 8'd2;
        test_input[2] = 8'd3;
        test_input[3] = 8'd4;
        test_input[4] = 8'd5;
        test_input[5] = 8'd6;
        test_input[6] = 8'd7;
        test_input[7] = 8'd8;

        // Waveform dump
        $dumpfile("ternary_mac_8x8_tb.vcd");
        $dumpvars(0, ternary_mac_8x8_tb);

        errors = 0;

        // ── Reset ──
        $display("\n=== ternary_mac_8x8 Testbench ===");
        $display("%0t: Resetting...", $time);
        rst_n = 0;
        ui_in = 8'd0;
        uio_in = 8'd0;
        #(20);
        rst_n = 1;
        #(10);

        // ── Test all 8 columns ──
        for (col = 0; col < 8; col = col + 1) begin
            $display("\n%0t: Testing column %0d...", $time, col);

            // Set column select and assert start
            uio_in = {1'b1, 1'b0, col[2:0]}; // start=1, col_select=col
            #(10);

            // Feed input vector over 8 cycles
            for (row = 0; row < 8; row = row + 1) begin
                ui_in = test_input[row];
                #(10);
            end

            // Wait for DONE state
            #(20);

            // Check result
            $display("  Column %0d: output=%0d, expected=%0d", col, uo_out, expected[col]);
            if (uo_out !== expected[col]) begin
                $display("  ERROR: mismatch!");
                errors = errors + 1;
            end else begin
                $display("  PASS");
            end

            // De-assert start to return to IDLE
            uio_in = {1'b0, 1'b0, col[2:0]};
            #(10);
        end

        // ── Report ──
        $display("\n=== Test Summary ===");
        if (errors == 0)
            $display("TEST PASSED - All 8 columns match");
        else
            $display("TEST FAILED - %0d errors", errors);
        $display("===================\n");

        #(20);
        $finish;
    end

    // Timeout watchdog
    initial begin
        #(10000);
        $display("ERROR: Simulation timeout!");
        $finish;
    end

endmodule
