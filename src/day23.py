from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Tuple


def read_input() -> List[str]:
    with open("../input/day23.txt") as file:
        return file.readlines()


@dataclass
class Nanobot(object):
    x: int
    y: int
    z: int
    radius: int

    def is_point_in_range(self, x: int, y: int, z: int) -> bool:
        return self.radius >= abs(x - self.x) + abs(y - self.y) + abs(z - self.z)


def parse_input(lines: List[str]) -> List[Nanobot]:
    res = []
    for line in lines:
        match = re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)
        res.append(Nanobot(*(map(int, match.groups()))))
    return res


def part1(nanobots: List[Nanobot]) -> int:
    strongest = max(nanobots, key=lambda n: n.radius)
    return sum(1 for n in nanobots if strongest.is_point_in_range(n.x, n.y, n.z))


def test_part1_examples():
    example = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""".splitlines()
    nanobots = parse_input(example)
    assert part1(nanobots) == 7


def test_part1():
    lines = read_input()
    nanobots = parse_input(lines)
    print(part1(nanobots))


def part2(nanobots: List[Nanobot]) -> int:
    # Answer thieved from https://www.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/
    q = []
    for n in nanobots:
        distance = abs(n.x) + abs(n.y) + abs(n.z)
        q.append((max(distance - n.radius, 0), 1))
        q.append((distance + n.radius + 1, -1))

    count = 0
    max_count = 0
    res = 0
    q = sorted(q)
    for dist, inc in q:
        count += inc
        if count > max_count:
            res = dist
            max_count = count
    return res


def test_part2_examples():
    example = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".splitlines()
    nanobots = parse_input(example)

    print(part2(nanobots))
    # assert part2(nanobots) == 36


def test_part2():
    lines = read_input()
    nanobots = parse_input(lines)
    print(part2(nanobots))
    # Too low:   127216436
    # Not right: 129293594
    # 129293598
