from dataclasses import dataclass
from functools import cached_property
from typing import List, Tuple
import re


def read_input() -> List[str]:
    with open("../input/day10.txt") as file:
        return file.readlines()


Coord = List[int]


def parse_input(lines: List[str]) -> List[Tuple[Coord, Coord]]:
    res = []
    for line in lines:
        match = re.match(r"position=<\s*([-\d]+),\s*([-\d]+)> velocity=<\s*([-\d]+),\s*([-\d]+)>", line)
        coord1 = [int(match.group(1)), int(match.group(2))]
        coord2 = [int(match.group(3)), int(match.group(4))]
        res.append((coord1, coord2))
    return res


def part1(coords: List[Tuple[Coord, Coord]]):
    all_coords_pos = False
    seconds = 0
    while not all_coords_pos:
        seconds += 1
        all_coords_pos = True
        for coord, vel in coords:
            coord[0] += vel[0]
            coord[1] += vel[1]
            if all_coords_pos and (coord[0] < 0 or coord[0] > 210 or coord[1] < 0 or coord[1] > 210):
                all_coords_pos = False

    max_x = max(c[0][0] for c in coords)
    max_y = max(c[0][1] for c in coords)
    rows = max_y + 1
    cols = max_x + 1
    grid = [[" "] * cols for _ in range(rows + 1)]
    for (c, r), _ in coords:
        grid[r][c] = "#"

    res = "\n".join("".join(row) for row in grid)
    print("After", seconds, "seconds")
    print(res)


def test_part1_example():
    example = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""
    part1(parse_input(example.splitlines()))


def test_part1():
    part1(parse_input(read_input()))