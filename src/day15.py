from collections import deque, Counter
from dataclasses import dataclass
from typing import List, Tuple, Optional


def read_input() -> List[str]:
    with open("../input/day15.txt") as file:
        return [line.strip() for line in file.readlines()]


Coord = Tuple[int, int]

directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]


@dataclass
class Result(object):
    score: int
    winner: str
    losses: int
    rounds: int


def part1(lines: List[str], elf_attack: int = 3, debug: bool = False) -> Result:
    grid = []
    units = {}
    attack = {"E": elf_attack, "G": 3}
    losses = {"E": 0, "G": 0}

    for row, line in enumerate(lines):
        grid_row = []
        for col, char in enumerate(line):
            if char in {"G", "E"}:
                units[(row, col)] = 200
            grid_row.append(str(char))

        grid.append(grid_row)

    rounds = 0
    while True:
        if debug:
            print(rounds)
            print("\n".join("".join(row) for row in grid))

        unit_order = sorted(units.keys())
        for coord in unit_order:
            if coord not in units:
                continue

            hp = units[coord]
            unit_type = grid[coord[0]][coord[1]]
            targets = [c for c, hp in units.items() if grid[c[0]][c[1]] != unit_type]

            if not targets:
                return Result(rounds * sum(units.values()), unit_type, losses[unit_type], rounds)

            if not any(adjacent(coord, t) for t in targets):
                new_coord = next_move(coord, unit_type, grid)
                if new_coord:
                    units[new_coord] = hp
                    grid[new_coord[0]][new_coord[1]] = unit_type
                    del units[coord]
                    grid[coord[0]][coord[1]] = "."
                    coord = new_coord

            if adjacent_targets := [t for t in targets if adjacent(coord, t)]:
                min_target_hp = min(units[t] for t in adjacent_targets)
                next_target = sorted((t for t in adjacent_targets if units[t] == min_target_hp))[0]
                new_target_hp = min_target_hp - attack[unit_type]
                if new_target_hp <= 0:
                    target_type = grid[next_target[0]][next_target[1]]
                    grid[next_target[0]][next_target[1]] = "."
                    del units[next_target]
                    losses[target_type] += 1
                else:
                    units[next_target] = new_target_hp

        rounds += 1


def part2(lines: List[str]) -> Result:
    elf_attack = 4
    while elf_attack < 100:
        res = part1(lines, elf_attack)
        print(elf_attack, res)
        if res.winner == "E" and res.losses == 0:
            return res

        elf_attack += 1


def next_move(start: Coord, unit_type: str, grid: List[List[str]]) -> Optional[Coord]:
    q = deque([[start]])
    seen = {start}

    in_range = []
    while q:
        path = q.popleft()
        row, col = path[-1]
        for row_d, col_d in directions:
            new_row = row + row_d
            new_col = col + col_d
            new_coord = (new_row, new_col)
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid) and new_coord not in seen:
                grid_char = grid[new_row][new_col]
                if grid_char == ".":
                    new_path = list(path) + [new_coord]
                    q.append(new_path)
                    seen.add(new_coord)
                elif not (grid_char == unit_type or grid_char == "#"):
                    in_range.append(path)

    if in_range:
        shortest_len = min(len(p) for p in in_range)
        shortest_paths = [p for p in in_range if len(p) == shortest_len]

        chosen_point = sorted(p[-1] for p in shortest_paths)[0]
        chosen_paths = [p for p in shortest_paths if p[-1] == chosen_point]

        step = sorted(p[1] for p in chosen_paths)[0]
        return step
    else:
        return None


def adjacent(c1: Tuple[int, int], c2: Tuple[int, int]) -> bool:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) == 1


def test_part1_example():
    lines = """#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######
""".splitlines()
    assert part1(lines).score == 27730

    lines = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
####### 
""".splitlines()
    assert part1(lines).score == 36334

    lines = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""".splitlines()
    assert part1(lines).score == 39514

    lines = """#######   
#E.G#.#
#.#G..#
#G.#.G#   
#G..#.#
#...E.#
#######
""".splitlines()
    assert part1(lines).score == 27755

    lines = """#######
#.E...#   
#.#..G#
#.###.#   
#E#G#G#   
#...#G#
####### 
""".splitlines()
    assert part1(lines).score == 28944

    lines = """#########   
#G......#
#.E.#...#
#..##..G#
#...##..#   
#...#...#
#.G...G.#   
#.....G.#   
#########
""".splitlines()
    assert part1(lines).score == 18740


def test_part1():
    lines = read_input()
    assert part1(lines).score == 190012


def test_part2_example():
    lines = """#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######
""".splitlines()
    assert part2(lines).score == 4988

    print()
    lines = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""".splitlines()
    assert part2(lines).score == 31284

    print()
    lines = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""".splitlines()
    assert part2(lines).score == 3478

    print()
    lines = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""".splitlines()
    assert part2(lines).score == 6474

    print()
    lines = """#########   
#G......#   
#.E.#...#
#..##..G#   
#...##..#   
#...#...#   
#.G...G.#   
#.....G.#   
#########
""".splitlines()
    assert part2(lines).score == 1140


def test_part2():
    lines = read_input()
    print(part2(lines))
