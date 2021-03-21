from typing import List, Tuple, Optional

import day16


def read_input() -> List[str]:
    with open("../input/day19.txt") as file:
        return [line.strip() for line in file.readlines()]


Instruction = Tuple[str, int, int, int]


def parse_input(lines: List[str]) -> Tuple[int, List[Instruction]]:
    line1, instructions = lines[0], lines[1:]
    ip = int(line1.split(" ")[-1])
    ls = []
    for instruction in instructions:
        parts = instruction.split(" ")
        opcode, args = parts[0], parts[1:]
        ls.append((opcode,) + tuple(map(int, args)))

    return ip, ls


def part1(
    ip_register: int,
    instructions: List[Instruction],
    register0: int = 0,
    max_iterations: Optional[int] = None,
    debug: bool = False,
):
    registers = [0] * 6
    registers[0] = register0
    ip = 0
    iterations = 0
    res = []
    while ip < len(instructions) and (max_iterations is None or iterations < max_iterations):
        registers[ip_register] = ip
        opcode, *args = instructions[ip]
        new_registers = day16.evaluate(opcode, args, registers)

        if debug:
            print(f"{iterations} ip={ip} {registers} {' '.join(map(str, instructions[ip]))} {new_registers}")

        res.append((registers, ip, instructions[ip], new_registers))
        registers = new_registers
        ip = registers[ip_register] + 1
        iterations += 1

    return iterations, res


def test_part1_example():
    example = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".splitlines()
    ip_register, instructions = parse_input(example)
    iterations, registers = part1(ip_register, instructions)
    assert registers[-1][0][0] == 6


def test_part1():
    lines = read_input()
    ip_register, instructions = parse_input(lines)
    iterations, registers = part1(ip_register, instructions)
    assert registers[-1][0][0] == 2160


"""
 0 addi 1 16 1   reg1 += 16
 
 1 seti 1 4 5    reg5 = 1
 2 seti 1 4 2    reg2 = 1
 3 mulr 5 2 4    reg4 = reg5 * reg2
 4 eqrr 4 3 4    reg4 = reg4 == reg3
 5 addr 4 1 1    reg1 = reg4 + reg1
 6 addi 1 1 1    reg1 += 1
 7 addr 5 0 0    reg0 += reg5 
 8 addi 2 1 2    reg2 += 1
 9 gtrr 2 3 4    reg4 = reg2 > reg3
10 addr 1 4 1    reg1 = reg1 + reg4
11 seti 2 6 1    reg1 = 2

12 addi 5 1 5    reg5 += 1
13 gtrr 5 3 4    reg4 = reg5 > reg3
14 addr 4 1 1    reg1 = reg4 + reg1
15 seti 1 7 1    reg1 = 1
16 mulr 1 1 1    reg1 *= reg1

17 addi 3 2 3    reg3 += 2
18 mulr 3 3 3    reg3 *= reg3
19 mulr 1 3 3    reg3 *= reg1
20 muli 3 11 3   reg3 *= 11
21 addi 4 3 4    reg4 += 3
22 mulr 4 1 4    reg4 *= reg1
23 addi 4 18 4   reg4 += 18
24 addr 3 4 3    reg3 += reg4
25 addr 1 0 1    reg1 += reg0
26 seti 0 7 1    reg1 = 0

27 setr 1 4 4    reg4 = reg1
28 mulr 4 1 4    reg4 *= reg1
29 addr 1 4 4    reg4 += reg1
30 mulr 1 4 4    reg4 *= reg1
31 muli 4 14 4   reg4 *= 14
32 mulr 4 1 4    reg4 *= reg1
33 addr 3 4 3    reg3 += reg4
34 seti 0 0 0    reg0 = 0
35 seti 0 1 1    reg1 = 0
"""


def prog(part2: bool) -> int:
    reg0, reg1, reg2, reg3, reg4, reg5 = 0, 0, 0, 0, 0, 0

    # 17-26
    reg3 = 2 * 2 * 19 * 11
    reg4 = 3 * 22 + 18
    reg3 += reg4

    if part2:
        # 27-35
        reg4 = ((27 * 28 + 29) * 30 * 14) * 32
        reg3 += reg4

    reg5 = 1
    print(reg3)
    while reg5 <= reg3:
        if reg3 % reg5 == 0:
            reg0 += reg5

        # reg2 = 1
        # while reg2 <= reg3:
        #     if reg5 * reg2 == reg3:
        #         reg0 += reg5
        #
        #     reg2 += 1

        reg5 += 1

    return reg0


def test_prog_part1():
    assert prog(part2=False) == 2160


def test_part2():
    assert prog(part2=True) == 25945920
