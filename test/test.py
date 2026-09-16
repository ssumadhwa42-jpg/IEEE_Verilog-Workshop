# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 10)

    dut.rst_n.value = 1

    dut._log.info("Testing 4-bit ALU")

    # =================================================
    # ADD
    # A = 5, B = 3
    # Operation = 000
    # Expected = 8
    # =================================================
    dut.ui_in.value = (3 << 4) | 5
    dut.uio_in.value = 0b000

    await ClockCycles(dut.clk, 1)

    assert (int(dut.uo_out.value) & 0x0F) == 8
    dut._log.info("ADD: 5 + 3 = 8 PASS")

    # =================================================
    # SUBTRACT
    # A = 7, B = 2
    # Operation = 001
    # Expected = 5
    # =================================================
    dut.ui_in.value = (2 << 4) | 7
    dut.uio_in.value = 0b001

    await ClockCycles(dut.clk, 1)

    assert (int(dut.uo_out.value) & 0x0F) == 5
    dut._log.info("SUB: 7 - 2 = 5 PASS")

    # =================================================
    # AND
    # A = 1100, B = 1010
    # Operation = 010
    # Expected = 1000
    # =================================================
    dut.ui_in.value = (0b1010 << 4) | 0b1100
    dut.uio_in.value = 0b010

    await ClockCycles(dut.clk, 1)

    assert (int(dut.uo_out.value) & 0x0F) == 0b1000
    dut._log.info("AND: 1100 & 1010 = 1000 PASS")

    # =================================================
    # OR
    # A = 1100, B = 1010
    # Operation = 011
    # Expected = 1110
    # =================================================
    dut.ui_in.value = (0b1010 << 4) | 0b1100
    dut.uio_in.value = 0b011

    await ClockCycles(dut.clk, 1)

    assert (int(dut.uo_out.value) & 0x0F) == 0b1110
    dut._log.info("OR: 1100 | 1010 = 1110 PASS")

    # =================================================
    # XOR
    # A = 1100, B = 1010
    # Operation = 100
    # Expected = 0110
    # =================================================
    dut.ui_in.value = (0b1010 << 4) | 0b1100
    dut.uio_in.value = 0b100

    await ClockCycles(dut.clk, 1)

    assert (int(dut.uo_out.value) & 0x0F) == 0b0110
    dut._log.info("XOR: 1100 ^ 1010 = 0110 PASS")

    # =================================================
    # NOT
    # A = 0101
    # Operation = 101
    # Expected = 1010
    # =================================================
    dut.ui_in.value = 0b0101
    dut.uio_in.value = 0b101

    await ClockCycles(dut.clk, 1)

    assert (int(dut.uo_out.value) & 0x0F) == 0b1010
    dut._log.info("NOT: ~0101 = 1010 PASS")

    # =================================================
    # LEFT SHIFT
    # A = 0011
    # Operation = 110
    # Expected = 0110
    # =================================================
    dut.ui_in.value = 0b0011
    dut.uio_in.value = 0b110

    await ClockCycles(dut.clk, 1)

    assert (int(dut.uo_out.value) & 0x0F) == 0b0110
    dut._log.info("LEFT SHIFT: 0011 << 1 = 0110 PASS")

    # =================================================
    # RIGHT SHIFT
    # A = 1100
    # Operation = 111
    # Expected = 0110
    # =================================================
    dut.ui_in.value = 0b1100
    dut.uio_in.value = 0b111

    await ClockCycles(dut.clk, 1)

    assert (int(dut.uo_out.value) & 0x0F) == 0b0110
    dut._log.info("RIGHT SHIFT: 1100 >> 1 = 0110 PASS")

    # =================================================
    # ALL TESTS PASSED
    # =================================================
    dut._log.info("========================================")
    dut._log.info("All 8 ALU operations passed!")
    dut._log.info("4-bit ALU TEST PASSED")
    dut._log.info("========================================")
