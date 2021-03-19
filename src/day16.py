from typing import List, Tuple


def read_input_part1() -> List[str]:
    with open("../input/day16-1.txt") as file:
        return [line.strip() for line in file.readlines()]


def read_input_part2() -> List[str]:
    with open("../input/day16-2.txt") as file:
        return [line.strip() for line in file.readlines()]

def to_list(line: str, sep: str = ",") -> List[int]:
    return list(map(int, line.split(sep + " ")))


def parse_input(lines: List[str]) -> List[Tuple[List[int], List[int], List[int]]]:
    res = []
    for i in range(0, len(lines), 4):
        before = to_list(lines[i][9:-1])
        instruction = to_list(lines[i + 1], sep="")
        after = to_list(lines[i + 2][9:-1])
        res.append((before, instruction, after))
    return res


def evaluate(opcode_name: str, args: List[int], registers: List[int]) -> List[int]:
    res = list(registers)
    if opcode_name == "addr":
        res[args[2]] = registers[args[0]] + registers[args[1]]
    elif opcode_name == "addi":
        res[args[2]] = registers[args[0]] + args[1]
    elif opcode_name == "mulr":
        res[args[2]] = registers[args[0]] * registers[args[1]]
    elif opcode_name == "muli":
        res[args[2]] = registers[args[0]] * args[1]
    elif opcode_name == "banr":
        res[args[2]] = registers[args[0]] & registers[args[1]]
    elif opcode_name == "bani":
        res[args[2]] = registers[args[0]] & args[1]
    elif opcode_name == "borr":
        res[args[2]] = registers[args[0]] | registers[args[1]]
    elif opcode_name == "bori":
        res[args[2]] = registers[args[0]] | args[1]
    elif opcode_name == "setr":
        res[args[2]] = registers[args[0]]
    elif opcode_name == "seti":
        res[args[2]] = args[0]
    elif opcode_name == "gtir":
        res[args[2]] = int(args[0] > registers[args[1]])
    elif opcode_name == "gtri":
        res[args[2]] = int(registers[args[0]] > args[1])
    elif opcode_name == "gtrr":
        res[args[2]] = int(registers[args[0]] > registers[args[1]])
    elif opcode_name == "eqir":
        res[args[2]] = int(args[0] == registers[args[1]])
    elif opcode_name == "eqri":
        res[args[2]] = int(registers[args[0]] == args[1])
    elif opcode_name == "eqrr":
        res[args[2]] = int(registers[args[0]] == registers[args[1]])

    return res


all_opcode_names = [
    "addr",
    "addi",
    "mulr",
    "muli",
    "banr",
    "bani",
    "borr",
    "bori",
    "setr",
    "seti",
    "gtir",
    "gtri",
    "gtrr",
    "eqir",
    "eqri",
    "eqrr",
]


def part1() -> int:
    lines = read_input_part1()
    samples = parse_input(lines)
    count = 0

    for before, instruction, after in samples:
        opcode_number, args = instruction[0], instruction[1:]
        opcode_names = find_candidate_names(before, args, after)
        if len(opcode_names) >= 3:
            count += 1

    return count


def find_candidate_names(
    before: List[int], args: List[int], after: List[int], candidate_opcode_names=None
) -> List[str]:
    if candidate_opcode_names is None:
        candidate_opcode_names = all_opcode_names

    opcode_names = []
    for opcode_name in candidate_opcode_names:
        if evaluate(opcode_name, args, before) == after:
            opcode_names.append(opcode_name)
    return opcode_names


def part2() -> int:
    lines = read_input_part1()
    samples = parse_input(lines)
    number_to_name = {}

    for before, instruction, after in samples:
        opcode_number, args = instruction[0], instruction[1:]
        if opcode_number in number_to_name:
            to_test = number_to_name[opcode_number]
        else:
            to_test = all_opcode_names

        opcode_names = find_candidate_names(before, args, after, to_test)
        number_to_name[opcode_number] = opcode_names

    final_mapping = {}
    while number_to_name:
        next_number = None
        next_name = None
        for number, names in number_to_name.items():
            if len(names) == 1:
                next_number = number
                next_name = names[0]
                break

        final_mapping[next_number] = next_name
        del number_to_name[next_number]

        for names in number_to_name.values():
            if next_name in names:
                names.remove(next_name)

    registers = [0, 0, 0, 0]
    lines = read_input_part2()
    for line in lines:
        opcode_number, *args = list(map(int, line.split(" ")))
        opcode_name = final_mapping[opcode_number]
        registers = evaluate(opcode_name, args, registers)

    return registers[0]



def test_part1_examples():
    actual = find_candidate_names([3, 2, 1, 1], [2, 1, 2], [3, 2, 2, 1])
    assert actual == ["addi", "mulr", "seti"]


def test_part1():
    print(part1())

def test_part2():
    print(part2())