from __future__ import annotations

import operator
from dataclasses import dataclass
from typing import List, Tuple
import re


def read_input() -> List[str]:
    with open("../input/day23.txt") as file:
        return file.readlines()


@dataclass
class Nanobot(object):
    x: int
    y: int
    z: int
    radius: int

    def in_range(self, x: int, y: int, z: int) -> bool:
        return self.radius >= abs(x - self.x) + abs(y - self.y) + abs(z - self.z)


def parse_input(lines: List[str]) -> List[Nanobot]:
    res = []
    for line in lines:
        match = re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)
        res.append(Nanobot(*(map(int, match.groups()))))
    return res


def part1(nanobots: List[Nanobot]) -> int:
    strongest = max(nanobots, key=lambda n: n.radius)
    return sum(1 for n in nanobots if strongest.in_range(n.x, n.y, n.z))


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


def max_overlap(ranges: List[Tuple[int, int]]) -> Tuple[int, int, int]:
    events = sorted((
        (c, op)
        for coord in ranges
        for c, op in zip(coord, ['x', 'y'])
    ))

    count = 0
    max_count = 0
    ret_x, ret_y = 0, 0
    for c, op in events:
        initial_count = count
        if op == 'x':
            count += 1
        else:
            count -= 1

        if initial_count == max_count:
            if count > initial_count:
                ret_x = c
                max_count = count
            elif count < initial_count:
                ret_y = c

    return ret_x, ret_y, max_count


def part2(nanobots: List[Nanobot]):
    x1, x2, count = max_overlap([(n.x - n.radius, n.x + n.radius) for n in nanobots])
    print(x1, x2, count)

    y1, y2, count = max_overlap([(n.y - n.radius, n.y + n.radius) for n in nanobots])
    print(y1, y2, count)

    z1, z2, count = max_overlap([(n.z - n.radius, n.z + n.radius) for n in nanobots])
    print(z1, z2, count)

    x_pos = {n.x for n in nanobots if x1 <= n.x <= x2}
    y_pos = {n.y for n in nanobots if y1 <= n.y <= y2}
    z_pos = {n.z for n in nanobots if z1 <= n.z <= z2}

    max_bots = 0
    res_bots = 0
    max_coord = None
    for x in x_pos:
        for y in y_pos:
            for z in z_pos:
                bots = [n for n in nanobots if n.in_range(x, y, z)]
                num_bots = len(bots)
                if num_bots >= max_bots:
                    max_coord = (x, y, z, num_bots)
                    max_bots = num_bots
                    res_bots = bots


    x_pos = {n.x for n in res_bots}
    y_pos = {n.y for n in res_bots}
    z_pos = {n.z for n in res_bots}
    print(len(x_pos))
    print(len(y_pos))
    print(len(z_pos))

    return max_coord



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