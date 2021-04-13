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

    def is_cube_in_range(self, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> bool:
        # Cube is in range if:

        # 1. One of the cube corners is in range
        cube_points_in_range = any(
            self.is_point_in_range(x, y, z)
            for x in (x1, (x2 + x1 // 2), x2)
            for y in (y1, (y2 + y1 // 2), y2)
            for z in (z1, (z2 + z1 // 2), z2)
        )

        # 2. Any of the radius endpoints are in the cube.
        endpoints_in_cube = any(
            x1 <= self.x + x_d * sign * self.radius <= x2
            and y1 <= self.y + y_d * sign * self.radius <= y2
            and z1 <= self.z + z_d * sign * self.radius <= z2
            for sign in (-1, 1)
            for x_d, y_d, z_d in ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        )

        return cube_points_in_range or endpoints_in_cube


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


def max_overlap(ranges: List[Tuple[int, int]]) -> Tuple[int, int, int]:
    events = sorted(((c, op) for coord in ranges for c, op in zip(coord, ["x", "y"])))

    count = 0
    max_count = 0
    ret_x, ret_y = 0, 0
    for c, op in events:
        initial_count = count
        if op == "x":
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
    min_x = min(n.x - n.radius for n in nanobots)
    max_x = max(n.x + n.radius for n in nanobots)
    min_y = min(n.y - n.radius for n in nanobots)
    max_y = max(n.y + n.radius for n in nanobots)
    min_z = min(n.z - n.radius for n in nanobots)
    max_z = max(n.z + n.radius for n in nanobots)
    point = (min_x, min_y, min_z)
    dim = max((max_x - min_x, max_y - min_y, max_z - min_z))

    last_best = None
    while True:
        regions = []
        if max_x - min_x > 2:
            mid_x = (max_x + min_x) // 2
            x_intervals = [(min_x, mid_x), (mid_x + 1, max_x)]
        else:
            x_intervals = [(min_x, max_x)]

        if max_y - min_y > 2:
            mid_y = (max_y + min_y) // 2
            y_intervals = [(min_y, mid_y), (mid_y + 1, max_y)]
        else:
            y_intervals = [(min_y, max_y)]

        if max_z - min_z > 2:
            mid_z = (max_z + min_z) // 2
            z_intervals = [(min_z, mid_z), (mid_z + 1, max_z)]
        else:
            z_intervals = [(min_z, max_z)]

        for x1, x2 in x_intervals:
            for y1, y2 in y_intervals:
                for z1, z2 in z_intervals:
                    bots = [n for n in nanobots if n.is_cube_in_range(x1, x2, y1, y2, z1, z2)]
                    regions.append((x1, x2, y1, y2, z1, z2, len(bots)))

        max_bots = max(r[-1] for r in regions)
        best_regions = [r for r in regions if r[-1] == max_bots]
        if len(best_regions) > 1:
            best_region = min(best_regions, key=lambda r: abs(r[0]) + abs(r[2]) + abs(r[4]))
        else:
            best_region = best_regions[0]

        if last_best is not None and last_best == best_region:
            break
        else:
            last_best = best_region

        min_x, max_x, min_y, max_y, min_z, max_z, _ = best_region

    max_bots = 0
    dist = 10000000
    min_x, max_x, min_y, max_y, min_z, max_z, _ = best_region
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                num_bots = sum(1 for n in nanobots if n.is_point_in_range(x, y, z))
                point_dist = abs(x) + abs(y) + abs(z)
                if num_bots > max_bots:
                    max_bots = num_bots
                    dist = point_dist
                elif num_bots == max_bots and point_dist < dist:
                    dist = point_dist
    return dist


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
    # Too low: 127216436


def test_part3():
    lines = read_input()
    nanobots = parse_input(lines)
    point1 = (27_404_343, 159_381_107, 16_384_403, 120_279_732, 8_013_895, 11_802_623)
    point2 = (27_404_343, 93_392_725, 16_384_403, 68_332_067, 8_013_895, 63_020_064)
    n1 = [(i, n) for i, n in enumerate(nanobots) if n.is_cube_in_range(*point1)]
    n2 = [(i, n) for i, n in enumerate(nanobots) if n.is_cube_in_range(*point2)]
    print(len(n1), len(n2))

    print(nanobots[1].is_cube_in_range(*point1))
    print(nanobots[1].is_cube_in_range(*point2))
