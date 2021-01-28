from collections import defaultdict
from typing import List, Tuple
import re

import toolz


def read_input() -> List[str]:
    with open("../input/day3.txt") as file:
        return file.readlines()


Coord = Tuple[int, int]
Rectangle = Tuple[Coord, Coord]


def parse_input(lines: List[str]) -> List[Rectangle]:
    res = []
    for line in lines:
        match = re.match(r"#\d+ @ (\d+),(\d+): (\d+)x(\d+)", line)
        values = list(map(int, match.groups()))
        rect = ((values[0], values[1]), (values[0] + values[2], values[1] + values[3]))
        res.append(rect)

    return res


def part1(rectangles: List[Rectangle]) -> int:
    inches = covered_inches(rectangles)
    return sum(c > 1 for c in inches.values())


def covered_inches(rectangles):
    inches = defaultdict(lambda: 0)
    for (x1, y1), (x2, y2) in rectangles:
        for x in range(x1, x2):
            for y in range(y1, y2):
                inches[(x, y)] += 1
    return inches


example = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".splitlines()


def test_part1_example():
    assert part1(parse_input(example)) == 4


def test_part1():
    print(part1(parse_input(read_input())))


def part2(rectangles: List[Rectangle]) -> int:
    inches = covered_inches(rectangles)

    return toolz.first(
        i + 1
        for i, ((x1, y1), (x2, y2)) in enumerate(rectangles)
        if all(inches[(x, y)] == 1 for x in range(x1, x2) for y in range(y1, y2))
    )


def test_part2_example():
    assert part2(parse_input(example)) == 3


def test_part2():
    print(part2(parse_input(read_input())))
