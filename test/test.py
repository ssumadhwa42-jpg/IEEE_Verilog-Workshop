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

    # -------------------------------------------------
    # ADD: A + B
    # Operation = 000
    # -------------------------------------------------
    dut.ui_in.value = (3 << 4) | 5
    dut.uio_in.value = 0b000
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value & 0x0F == 8
    dut._log.info("ADD: 5 + 3 = 8 PASS")

    # -------------------------------------------------
    # SUB: A - B
    # Operation = 001
    # -------------------------------------------------
    dut.ui_in.value = (2 << 4) | 7
    dut.uio_in.value = 0b001
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value & 0x0F == 5
    dut._log.info("SUB: 7 - 2 = 5 PASS")

    # -------------------------------------------------
    # AND
    # Operation = 010
    # -------------------------------------------------
    dut.ui_in.value = (0b1010 << 4) | 0b1100
    dut.uio_in.value = 0b010
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value & 0x0F == 0b1000
    dut._log.info("AND: 1100 & 1010 = 1000 PASS")

    # -------------------------------------------------
    # OR
    # Operation = 011
    # -------------------------------------------------
    dut.ui_in.value = (0b1010 << 4) | 0b1100
    dut.uio_in.value = 0b011
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value & 0x0F == 0b1110
    dut._log.info("OR: 1100 | 1010 = 1110 PASS")

    # -------------------------------------------------
    # XOR
    # Operation = 100
    # -------------------------------------------------
    dut.ui_in.value = (0b1010 << 4) | 0b1100
    dut.uio_in.value = 0b100
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value & 0x0F == 0b0110
    dut._log.info("XOR: 1100 ^ 1010 = 0110 PASS")

    # -------------------------------------------------
    # NOT A
    # Operation = 101
    # -------------------------------------------------
    dut.ui_in.value = 0b0101
    dut.uio_in.value = 0b101
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value & 0x0F == 0b1010
    dut._log.info("NOT: ~0101 = 1010 PASS")

    # -------------------------------------------------
    # LEFT SHIFT
    # Operation = 110
    # -------------------------------------------------
    dut.ui_in.value = 0b0011
    dut.uio_in.value = 0b110
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value & 0x0F == 0b0110
    dut._log.info("LEFT SHIFT: 0011 << 1 = 0110 PASS")

    # -------------------------------------------------
    # RIGHT SHIFT
    # Operation = 111
    # -------------------------------------------------
    dut.ui_in.value = 0b1100
    dut.uio_in.value = 0b111
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value & 0x0F == 0b0110
    dut._log.info("RIGHT SHIFT: 1100 >> 1 = 0110 PASS")

    dut._log.info("All 8 ALU operations passed!")
