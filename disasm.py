#!/usr/bin/env python3
#
# RISC-V Disassembler
# Copyright (c) 2020 by Jeff Tranter <tranter@pobox.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# To Do:
# - Test offsets for branches
# - Add common pseudo instructions
# - Add support for floating-point extension
# - Add support for compressed extensions

import sys
import argparse

# Functions


def registerName(regNo):
    "Return register name given a number from 0-31."
    assert 0 <= regNo <= 31

    if not args.abinames:
        s = "x{0:d}".format(regNo)
    if regNo == 0:
        s = "zero"
    elif regNo == 1:
        s = "ra"
    elif regNo == 2:
        s = "sp"
    elif regNo == 3:
        s = "gp"
    elif regNo == 4:
        s = "tp"
    elif 5 <= regNo <= 7:
        s = "t{0:d}".format(regNo-5)
    elif regNo == 8:
        s = "fp"
    elif regNo == 9:
        s = "s1"
    elif 10 <= regNo <= 17:
        s = "a{0:d}".format(regNo-10)
    elif 18 <= regNo <= 27:
        s = "s{0:d}".format(regNo-18)
    else:
        s = "t{0:d}".format(regNo-28)

    return s

# Parse command line options
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Binary file to disassemble")
parser.add_argument("-a", "--address", help="Specify decimal starting address (defaults to 0)", default=0, type=int)
parser.add_argument("-n", "--nolist", help="Don't list  instruction bytes (make output suitable for assembler)", action="store_true")
parser.add_argument("-p", "--pseudo", help="Use common pseudo instructions (e.g. nop)", action="store_true")
parser.add_argument("-r", "--abinames", help="Use ABI register names (e.g. sp)", action="store_true")
args = parser.parse_args()


# Get filename from command line arguments.
filename = args.filename

# Get initial instruction address from command line arguments.
address = args.address

try:
    f = open(args.filename, "rb")
except FileNotFoundError:
    print(("error: input file '{}' not found.".format(args.filename)), file=sys.stderr)
    sys.exit(1)

while True:
    b1 = f.read(1)
    b2 = f.read(1)
    b3 = f.read(1)
    b4 = f.read(1)

    if b1 and b2 and b3 and b4:
        instruction = ord(b1) + ord(b2) * 256 + ord(b3) * 65536 + ord(b4) * 16777216

        opcode = instruction & 0b1111111
        rd = (instruction >> 7) & 0b11111
        funct3 = (instruction >> 12) & 0b111
        rs1 = (instruction >> 15) & 0b11111
        rs2 = (instruction >> 20) & 0b11111
        funct7 = (instruction >> 25) & 0b1111111
        funct5 = (instruction >> 27) & 0b11111

# RV32I Based Integer Instructions

        if opcode == 0b0110011 and funct3 == 0x0 and funct7 == 0x00:
            mnem = "add {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x0 and funct7 == 0x20:
            mnem = "sub {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x4 and funct7 == 0x00:
            mnem = "xor {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x6 and funct7 == 0x00:
            mnem = "or {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x7 and funct7 == 0x00:
            mnem = "and {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x1 and funct7 == 0x00:
            mnem = "sll {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x5 and funct7 == 0x00:
            mnem = "srl {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x5 and funct7 == 0x20:
            mnem = "sra {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x2 and funct7 == 0x00:
            mnem = "slt {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x3 and funct7 == 0x00:
            mnem = "sltu {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0010011 and funct3 == 0x0:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "addi {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0010011 and funct3 == 0x4:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "xori {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0010011 and funct3 == 0x6:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "ori {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0010011 and funct3 == 0x7:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "andi {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0010011 and funct3 == 0x1:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "slli {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0010011 and funct3 == 0x5:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "srli {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0010011 and funct3 == 0x5:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "srai {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0010011 and funct3 == 0x2:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "slti {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0010011 and funct3 == 0x3:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "sltiu {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0000011 and funct3 == 0x0:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "lb {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0000011 and funct3 == 0x1:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "lh {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0000011 and funct3 == 0x2:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "lw {0:s},{2:08x}({1:s})".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0000011 and funct3 == 0x4:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "lbu {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0000011 and funct3 == 0x5:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "lhu {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0100011 and funct3 == 0x0:
            imm = (instruction >> 20) & 0b1111111 + (instruction >> 7) & 0b11111
            mnem = "sb {0:s},{2:08x}({1:s})".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0100011 and funct3 == 0x1:
            imm = (instruction >> 20) & 0b1111111 + (instruction >> 7) & 0b11111
            mnem = "sh {0:s},{1:s},#${2:08x}".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0100011 and funct3 == 0x2:
            imm = (instruction >> 20) & 0b1111111 + (instruction >> 7) & 0b11111
            mnem = "sw {0:s},{2:08x}({1:s})".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b1100011 and funct3 == 0x0:
            imm = (((instruction >> 31) & 0b1) << 12) + \
                (((instruction >> 25) & 0b111111) << 10) + \
                (((instruction >> 7) & 0b1) << 11) + \
                (((instruction >> 8) & 0b1111) << 1)
            mnem = "beq {0:s},{1:s},*+${2:08x}".format(registerName(rs1), registerName(rs2,), imm)

        elif opcode == 0b1100011 and funct3 == 0x1:
            imm = (((instruction >> 31) & 0b1) << 12) + \
                (((instruction >> 25) & 0b111111) << 10) + \
                (((instruction >> 7) & 0b1) << 11) + \
                (((instruction >> 8) & 0b1111) << 1)
            mnem = "bne {0:s},{1:s},*+${2:08x}".format(registerName(rs1), registerName(rs2,), imm)

        elif opcode == 0b1100011 and funct3 == 0x4:
            imm = (((instruction >> 31) & 0b1) << 12) + \
                (((instruction >> 25) & 0b111111) << 10) + \
                (((instruction >> 7) & 0b1) << 11) + \
                (((instruction >> 8) & 0b1111) << 1)
            mnem = "blt {0:s},{1:s},*+${2:08x}".format(registerName(rs1), registerName(rs2,), imm)

        elif opcode == 0b1100011 and funct3 == 0x5:
            imm = (((instruction >> 31) & 0b1) << 12) + \
                (((instruction >> 25) & 0b111111) << 10) + \
                (((instruction >> 7) & 0b1) << 11) + \
                (((instruction >> 8) & 0b1111) << 1)
            mnem = "bge {0:s},{1:s},*+${2:08x}".format(registerName(rs1), registerName(rs2,), imm)

        elif opcode == 0b1100011 and funct3 == 0x6:
            imm = (((instruction >> 31) & 0b1) << 12) + \
                (((instruction >> 25) & 0b111111) << 10) + \
                (((instruction >> 7) & 0b1) << 11) + \
                (((instruction >> 8) & 0b1111) << 1)
            mnem = "bltu {0:s},{1:s},*+${2:08x}".format(registerName(rs1), registerName(rs2,), imm)

        elif opcode == 0b1100011 and funct3 == 0x7:
            imm = (((instruction >> 31) & 0b1) << 12) + \
                (((instruction >> 25) & 0b111111) << 10) + \
                (((instruction >> 7) & 0b1) << 11) + \
                (((instruction >> 8) & 0b1111) << 1)
            mnem = "bgeu {0:s},{1:s},*+${2:08x}".format(registerName(rs1), registerName(rs2,), imm)

        elif opcode == 0b1101111:
            imm = (((instruction >> 31) & 0b1) << 20) + \
                (((instruction >> 30) & 0b1111111111) << 1) + \
                (((instruction >> 20) & 0b1) << 11) + \
                (((instruction >> 19) & 0b11111111) << 12)
            mnem = "jal {0:s},{1:s},*+${2:08x}".format(registerName(rs1), registerName(rs2,), imm)

        elif opcode == 0b1100111 and funct3 == 0x0:
            imm = (instruction >> 20) & 0b111111111111
            mnem = "jalr {0:s},{2:08x}({1:s})".format(registerName(rd), registerName(rs1,), imm)

        elif opcode == 0b0110111:
            imm = (instruction >> 12) & 0b11111111111111111111
            mnem = "lui {0:s},#${1:08x}".format(registerName(rd), imm)

        elif opcode == 0b0010111:
            imm = (instruction >> 12) & 0b11111111111111111111
            mnem = "auipc {0:s},*+${1:08x}".format(registerName(rd), imm)

        elif opcode == 0b1110011 and funct3 == 0x0:
            imm = (instruction >> 20) & 0b111111111111
            if imm == 0x0:
                mnem = "ecall"
            elif imm == 0x1:
                mnem = "ebreak"
            else:
                mnem = "???"

# RV32M Multiply Extensions

        elif opcode == 0b0110011 and funct3 == 0x0 and funct7 == 0x01:
            mnem = "mul {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x1 and funct7 == 0x01:
            mnem = "mulh {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x2 and funct7 == 0x01:
            mnem = "mulsh {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x3 and funct7 == 0x01:
            mnem = "mulu {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x4 and funct7 == 0x01:
            mnem = "div {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x5 and funct7 == 0x01:
            mnem = "divu {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x6 and funct7 == 0x01:
            mnem = "rem {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0110011 and funct3 == 0x7 and funct7 == 0x01:
            mnem = "remu {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

# RV32A Atomic Extensions

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x02:
            mnem = "lr.w {0:s},{1:s}".format(registerName(rd), registerName(rs1,))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x03:
            mnem = "sc.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x01:
            mnem = "amoswap.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x00:
            mnem = "amoadd.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x0c:
            mnem = "amoand.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x0a:
            mnem = "amoor.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x04:
            mnem = "amoxor.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x14:
            mnem = "amomax.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x10:
            mnem = "amomin.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x1c:
            mnem = "amomaxu.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))

        elif opcode == 0b0101111 and funct3 == 0x2 and funct5 == 0x18:
            mnem = "amominu.w {0:s},{1:s},{2:s}".format(registerName(rd), registerName(rs1,), registerName(rs2))


        else:
            mnem = "???"

# Output line of disassembly

        if args.nolist:
            print(" {0:s}".format(mnem))
        else:
            print("{0:08x}  {1:08x}  {2:s}".format(address, instruction, mnem))

        address += 1
    else:
        break
