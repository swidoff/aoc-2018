from collections import Counter
from typing import List

Grid = List[List[str]]


def read_input() -> List[str]:
    with open("../input/day18.txt") as file:
        return [line.strip() for line in file.readlines()]


def parse_input(lines: List[str]) -> Grid:
    return [[c for c in line] for line in lines]


def simulate(grid: Grid, minutes: int = 10) -> Grid:
    dim = len(grid)
    seen = {}
    for minute in range(1, minutes+1):
        new_grid = []

        for row_num, row in enumerate(grid):
            new_row = []
            for col_num, char in enumerate(row):
                counts = Counter(
                    grid[r][c]
                    for r in range(row_num - 1, row_num + 2)
                    for c in range(col_num - 1, col_num + 2)
                    if 0 <= r < dim
                    if 0 <= c < dim
                    if not (r == row_num and c == col_num)
                )

                if char == "." and counts["|"] >= 3:
                    new_char = "|"
                elif char == "|" and counts["#"] >= 3:
                    new_char = "#"
                elif char == "#" and not (counts["#"] >= 1 and counts["|"] >= 1):
                    new_char = "."
                else:
                    new_char = char

                new_row.append(new_char)

            new_grid.append(new_row)

        grid = new_grid

        # print()
        # for row in grid:
        #     print("".join(row))
        #
        wooded = sum(c == "|" for row in new_grid for c in row)
        lumberyard = sum(c == "#" for row in new_grid for c in row)
        product = wooded * lumberyard
        print(minute, wooded, lumberyard, dim * dim - wooded - lumberyard, product, seen.get((wooded, lumberyard), None))
        if (wooded, lumberyard) not in seen:
            seen[(wooded, lumberyard)] = minute

    return grid


def part1(grid: Grid) -> int:
    new_grid = simulate(grid)
    wooded = sum(c == "|" for row in new_grid for c in row)
    lumberyard = sum(c == "#" for row in new_grid for c in row)
    return wooded * lumberyard


def test_part1_example():
    lines = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".splitlines()
    grid = parse_input(lines)
    assert part1(grid) == 1147

def test_part1():
    lines = read_input()
    grid = parse_input(lines)
    print(part1(grid))


def test_part2():
    lines = read_input()
    grid = parse_input(lines)
    simulate(grid, 1000)