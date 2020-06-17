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

# memory = [
#     PRINT_BEEJ,  # 1 bite long
#     PRINT_BEEJ,
#     PRINT_BEEJ,
#     99,
#     HALT
# ]

# memory = [
#     # SAVE_REG R1,37  #how can you encode this as a sequence of numbers
#     SAVE_REG,  # instruction that is 3 bite long
#     1,
#     37,
#     # PRINT_REG R1,
#     PRINT_REG,
#     1,
#     PRINT_BEEJ,
#     HALT
# ]

memory = [
    # SAVE_REG R1,37  #how can you encode this as a sequence of numbers
    SAVE_REG,  # instruction that is 3 bite long
    1,  # <--PRINT BEEJ only if it lands on it, but CPU lands on instruction
    99,
    SAVE_REG,  # instruction that is 3 bite long
    2,  # <--index into the register array
    11,  # <--value we want stored
    ADD,  # ADD R1 R2 => register[1]+register[2]
    1,
    2,
    PRINT_REG,  # PRINT_REG R1,
    1,
    PRINT_BEEJ,
    HALT
]


# for v in memory:
#     if v == PRINT_BEEJ:
#         print("Beej")
#     elif v == HALT:
#         break

# print("\nWith while loop\n")

# general purpose registers, like variable R0, R1, R2... R7 ..use them directly
# by default it initializes it to 0, that's when you turn your computer is 0
register = [0]*8
pc = 0  # program counter (special purpose)
running = True

# while running:
#     ir = memory[pc]  # instruction register
#     if ir == PRINT_BEEJ:
#         print("BEEJ!!!")
#         pc += 1
#     elif ir == HALT:
#         running = False
#         pc += 1
#     else:
#         print(f"Uknown instruttion {ir} at address {pc} ")
#         sys.exit(1)


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
    elif ir == HALT:
        running = False
        pc += 1
    else:
        print(f"Uknown instruttion {ir} at address {pc} ")
        sys.exit(1)
