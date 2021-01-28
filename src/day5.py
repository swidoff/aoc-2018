import re

def read_input() -> str:
    with open("../input/day5.txt") as file:
        return file.readline().strip()


def react(ch1: str, ch2: str) -> bool:
    return ch1 != ch2 and (ch1.upper() == ch2 or ch1.lower() == ch2)


def part1(line: str) -> int:
    chars_removed = 1
    chars = [c for c in line]
    while chars_removed > 0:
        chars_removed = 0
        i = 0
        new_chars = []
        while i < len(chars):
            if i == len(chars) - 1 or not react(chars[i], chars[i + 1]):
                new_chars.append(chars[i])
                i += 1
            else:
                chars_removed += 1
                i += 2
        chars = new_chars

    return len(chars)


def test_part1_examples():
    assert part1("aA") == 0
    assert part1("abBA") == 0
    assert part1("abAB") == 4
    assert part1("aabAAB") == 6
    assert part1("dabAcCaCBAcCcaDA") == 10


def test_part1():
    print(part1(read_input()))


def part2(line: str):
    return min(
        part1(line.replace(chr(o), "").replace(chr(o).lower(), ""))
        for o in range(ord('A'), ord('Z'))
        if chr(o) in line
    )

def test_part2_examples():
    assert part2("dabAcCaCBAcCcaDA") == 4

def test_part2():
    print(part2(read_input()))
