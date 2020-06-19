"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010  # MUL R0,R1
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256  # memory
        self.reg = [0] * 8  # general purpose registers
        self.pc = 0
        self.branchtable = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            MUL: self.mul,
            PUSH: self.push_op,
            POP: self.pop_op,
            CALL: self.call_op,
            RET: self.ret,
            ADD: self.add_op,
            CMP: self.cmp_op,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne

        }
        self.running = True
        self.sp = 7  # stack pointer
        self.flag = 0b00000000

    def ram_read(self, index):
        """hould accept the address to read and return the value stored
there."""
        return self.ram[index]

    def ram_write(self, index, value):
        """should accept a value to write, and the address to write it to"""
        self.ram[index] = value

    def load(self, filename):
        """Load a program into memory."""

        # LOAD PROGRAM

        address = 0
        # ----catch everything-------
        with open(filename) as f:
            # address = 0

            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.ram_write(address, v)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        if op == "CMP":  # flags are internal registers
            # cmp = 0b10100111 flags are last 3
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            else:
                self.flag = 0b00000000

        else:
            raise Exception("Unsupported ALU operation")
            # sys.exit(1)

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:

            value_operand1 = self.ram_read(self.pc + 1)
            value_operand2 = self.ram_read(self.pc + 2)

            ir = self.ram_read(self.pc)

            if ir in self.branchtable:
                self.branchtable[ir](value_operand1, value_operand2)

            else:
                print(f"Uknown instructions {ir} at address {self.pc}")
                sys.exit(1)

    def hlt(self, value_operand1, value_operand2):
        self.running = False

    def ldi(self, value_operand1, value_operand2):
        self.reg[value_operand1] = value_operand2
        self.pc += 3

    def prn(self, value_operand1, value_operand2):
        print(self.reg[value_operand1])
        self.pc += 2

    def mul(self, value_operand1, value_operand2):

        self.reg[value_operand1] = self.reg[value_operand1] * \
            self.reg[value_operand2]
        self.pc += 3

    def push_op(self, value_operand1, value_operand2):
        val = self.reg[value_operand1]  # this is the value we want to push
        self.reg[self.sp] -= 1  # decrementing stack pointer

        # registering number, grabbing from the memory and strore it
        self.ram_write(self.reg[self.sp], val)
        self.pc += 2

    def pop_op(self, value_operand1, value_operand2):

        val = self.ram[self.reg[self.sp]]
        self.reg[value_operand1] = val
        self.reg[self.sp] += 1

        self.pc += 2

    def call_op(self, value_operand1, value_operand2):

        val = self.pc + 2
        reg_index = value_operand1

        subroutine_addr = self.reg[reg_index]
        self.reg[self.sp] -= 1

        self.ram[self.reg[self.sp]] = val

        self.pc = subroutine_addr

    def ret(self, value_operand1, value_operand2):
        return_addr = self.reg[self.sp]  # return from subroutine

        # pop value from top of the stack and store it in the PC
        self.pc = self.ram_read(return_addr)

        # increment sp
        self.reg[self.sp] += 1

    def add_op(self, value_operand1, value_operand2):
        # self.reg[value_operand1] += self.reg[value_operand2]
        self.alu('ADD', value_operand1, value_operand2)
        self.pc += 3

    def cmp_op(self, value_operand1, value_operand2):

        self.alu("CMP", value_operand1, value_operand2)

        self.pc += 3

    def jeq(self, value_operand1, value_operand2):

        # if flag is true:
        if self.flag == 0b00000001:
            # if self.flag == [1]:
            self.pc = self.reg[value_operand1]
            # self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def jne(self, value_operand1, value_operand2):

        # if flag is false:
        if self.flag != 0b00000001:
            # self.pc = self.reg[self.ram[self.pc + 1]]

            self.pc = self.reg[value_operand1]

        else:
            self.pc += 2

    def jmp(self, value_operand1, value_operand2):

        # seting pc to address stored in the register
        self.pc = self.reg[value_operand1]
        print(f'pc instruction stored in {self.pc}')
