import re
from typing import Tuple, List, Dict

Coord = Tuple[int, int]


def read_input() -> List[str]:
    with open("../input/day17.txt") as file:
        return [line.strip() for line in file.readlines()]


def parse_input(lines: List[str]) -> Dict[Coord, str]:
    res = {}
    for line in lines:
        match = re.match(r"(\w)=(\d+), (\w)=(\d+)..(\d+)", line)
        dim1, val1, dim2, val2, val3 = match.groups()
        for range_val in range(int(val2), int(val3) + 1):
            if dim1 == "x":
                col = int(val1)
                row = range_val
            else:
                row = int(val1)
                col = range_val

            res[(row, col)] = "#"

    return res


def print_slice(coords: Dict[Coord, str]):
    min_row = min(row for row, col in coords.keys())
    max_row = max(row for row, col in coords.keys())
    min_col = min(col for row, col in coords.keys())
    max_col = max(col for row, col in coords.keys())

    for row in range(min_row - 1, max_row + 1):
        line = []
        for col in range(min_col - 1, max_col + 2):
            coord = (row, col)
            if coord in coords:
                val = coords[(row, col)]
                line.append(val)
            else:
                line.append(".")

        print("".join(line))


def drop_water(coords: Dict[Coord, str], start: Coord, max_row: int):
    stack = [start]
    while stack:
        pos = stack.pop()

        # Fall until we hit something
        below = (pos[0] + 1, pos[1])
        while below not in coords and below[0] <= max_row:
            stack.append(pos)
            pos = below
            below = (pos[0] + 1, pos[1])
            coords[pos] = "|"

        if pos[0] < max_row and coords.get((pos[0] + 1, pos[1])) != "|":
            level_coords = [pos]
            level_open = False

            for col_d in [-1, 1]:
                inner_pos = pos

                while coords.get((side := (inner_pos[0], inner_pos[1] + col_d)), ".") != "#":
                    level_coords.append(side)
                    if (side[0] + 1, side[1]) not in coords:
                        level_open = True
                        stack.append(side)
                        break
                    inner_pos = side

            char = "|" if level_open else "~"
            for level_coord in level_coords:
                coords[level_coord] = char


def flow(coords: Dict[Coord, str], tile_set: Tuple[str] = ("~", "|")) -> int:
    max_row = max(row for row, col in coords.keys())
    min_row = min(row for row, col in coords.keys())
    drop_water(coords, (0, 500), max_row)
    return sum(v in tile_set for (row, col), v in coords.items() if row >= min_row)


example = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".splitlines()


def test_part1_examples():
    coords = parse_input(example)
    res = flow(coords)
    print()
    print_slice(coords)
    assert res == 57


def test_part2_examples():
    coords = parse_input(example)
    res = flow(coords, tile_set=("~",))
    print_slice(coords)
    assert res == 29


def test_part1():
    coords = parse_input(read_input())
    res = flow(coords)
    # print_slice(coords)
    assert res == 39367


def test_part2():
    coords = parse_input(read_input())
    res = flow(coords, tile_set=("~",))
    assert res == 33061
