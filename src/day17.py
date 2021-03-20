import re
from typing import Tuple, List, Dict, Optional

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


def drop_water(coords: Dict[Coord, str], start: Coord = (0, 500)) -> Optional[Tuple[Coord, bool]]:
    max_row = max(row for row, col in coords.keys())
    prev_pos = None
    pos = start
    while pos != prev_pos:
        row, col = pos
        prev_pos = pos

        # Fall if we can.
        down_pos = (row + 1, col)
        if down_pos in coords:
            if coords[down_pos] != "|":
                # Scan left for an open spot. If found go there.
                if (left_pos := find_open_spot(coords, pos, -1, max_row)) is not None:
                    pos = left_pos
                    if (pos[0] + 1, pos[1]) in coords:
                        break

                # Scan right for an open spot. If found go there.
                elif (right_pos := find_open_spot(coords, pos, 1, max_row)) is not None:
                    pos = right_pos
                    if (pos[0] + 1, pos[1]) in coords:
                        break

            # Else start here
        elif down_pos[0] <= max_row:
            pos = down_pos

    if pos == start:
        res = None
    else:
        if pos[0] == max_row:
            falling = True
        elif coords.get((pos[0] + 1, pos[1]), None) == "|":
            falling = True
        elif coords.get((pos[0], pos[1] - 1), None) == "|":
            falling = True
        elif coords.get((pos[0], pos[1] + 1), None) == "|":
            falling = True
        else:
            falling = False

        res = pos, falling

    return res


def find_open_spot(coords: Dict[Coord, str], start: Coord, delta_c: int, max_row: int) -> Optional[Coord]:
    start_row, start_col = start
    next_row, next_col = start_row, start_col + delta_c
    pos = start
    next_pos = (next_row, next_col)
    while next_pos not in coords:
        beneath_coord = (next_pos[0] + 1, next_pos[1])
        if beneath_coord not in coords:
            if beneath_coord[0] == max_row:
                return None
            elif coords[(pos[0] + 1, pos[1])] == "|":
                return pos
            else:
                return next_pos

        pos = next_pos
        next_pos = pos[0], pos[1] + delta_c

    return pos if pos != start else None


def part1(coords: Dict[Coord, str], debug: bool = False, max_iterations: int = 1e6) -> int:
    iterations = 0
    while (drop_res := drop_water(coords)) is not None and iterations < max_iterations:
        pos, falling = drop_res
        coords[pos] = "|" if falling else "~"
        if debug:
            print(iterations)
            print_slice(coords)
        iterations += 1

    return sum(v != "#" for v in coords.values())


def test_part1_examples():
    example = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".splitlines()
    coords = parse_input(example)
    assert part1(coords) == 57


def test_part1():
    coords = parse_input(read_input())
    print(part1(coords))
    print_slice(coords)
