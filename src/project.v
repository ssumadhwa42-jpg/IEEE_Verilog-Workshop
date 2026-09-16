/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // A = ui_in[3:0]
    // B = ui_in[7:4]
    wire [3:0] A = ui_in[3:0];
    wire [3:0] B = ui_in[7:4];

    // Operation select
    wire [2:0] op = uio_in[2:0];

    // 5-bit result
    reg [4:0] result;

    always @(*) begin
        case (op)

            3'b000: result = {1'b0, A} + {1'b0, B}; // ADD
            3'b001: result = {1'b0, A} - {1'b0, B}; // SUB
            3'b010: result = {1'b0, (A & B)};       // AND
            3'b011: result = {1'b0, (A | B)};       // OR
            3'b100: result = {1'b0, (A ^ B)};       // XOR
            3'b101: result = {1'b0, (~A)};          // NOT
            3'b110: result = {A[2:0], 1'b0};        // LEFT SHIFT
            3'b111: result = {1'b0, (A >> 1)};      // RIGHT SHIFT

            default: result = 5'b00000;

        endcase
    end

    // Result
    assign uo_out[3:0] = result[3:0];

    // Carry / borrow
    assign uo_out[4] = result[4];

    // Unused outputs
    assign uo_out[7:5] = 3'b000;

    // Bidirectional pins unused
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Unused inputs
    wire _unused = &{ena, clk, rst_n, uio_in[7:3], 1'b0};

endmodule

`default_nettype wire
