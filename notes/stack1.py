"""
Comuter emulator
Software that pretends to be hardware
Turing Complete -- it can solve any problem for which there is an algorithm

Memory -- like a big array
 "index into the memory array" == "address" == "pointer"

"""
import sys

a = [1, 2, 3]
print(a[0])
a[0] = 99

# memory = [0] * 256 #RAM

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3  # SAVE_REG, R1, 37 r1=37   register[1]=37
PRINT_REG = 4  # PRINT_REG R1   print(register[1])
ADD = 5
PUSH = 6
POP = 7


memory = [0]*256

# general purpose registers, like variable R0, R1, R2... R7 ..use them directly
# by default it initializes it to 0, that's when you turn your computer is 0
register = [0]*8  # general purpose
SP = 7
pc = 0  # program counter (special purpose)
register[SP] = 0xf4
running = True


filename = sys.argv[1]
# ----catch everything-------
with open(filename) as f:
    address = 0

    for line in f:
        line = line.split("#")
        try:
            v = int(line[0], 10)
        except ValueError:
            continue
        memory[address] = v
#         address += 1
# print(memory[:15])  # first 15
# print(sys.argv)

sys.exit(0)

# == run loop

while running:
    ir = memory[pc]  # instruction register
    if ir == PRINT_BEEJ:
        print("BEEJ!!!")
        pc += 1
    elif ir == SAVE_REG:
        reg_num = memory[pc+1]
        value = memory[pc+2]
        register[reg_num] = value
        pc += 3
    elif ir == PRINT_REG:
        reg_num == memory[pc + 1]
        print(register[reg_num])
        pc += 2  # incrementing by 3 since there are 2 instructions
    elif ir == ADD:
        reg_num1 = memory[pc + 1]
        reg_num2 = memory[pc + 2]
        register[reg_num1] += register[reg_num2]
        pc += 3  # incrementing by 3 since there are 3 instructions
    elif ir == PUSH:
        # decrement stack pointer
        register[SP] -= 1
        # register number, grab that fromt the memory
        reg_num = memory[pc + 1]
        value = register[reg_num]  # < -- this is the value we want to push

        # figre out where to store it
        top_of_stack_addr = register[SP]

        # store it
        memory[top_of_stack_addr] = value
        pc += 2

    elif ir == HALT:
        running = False
        pc += 1
    else:
        print(f"Uknown instruttion {ir} at address {pc} ")
        sys.exit(1)
