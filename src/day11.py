from typing import Tuple, List, Dict


def power_level(x: int, y: int, serial: int) -> int:
    rack_id = x + 10
    level = (rack_id * y + serial) * rack_id
    hundreds = int(str(level)[-3])
    return hundreds - 5


def part1(serial: int) -> Tuple[int, int, int]:
    power = [[power_level(x, y, serial) for x in range(300)] for y in range(300)]

    return max(
        (
            (x, y, sum(power[y + yd][x + xd] for yd in range(3) for xd in range(3)))
            for y in range(300 - 3)
            for x in range(300 - 3)
        ),
        key=lambda p: p[2],
    )


def test_part1_example():
    assert power_level(3, 5, 8) == 4
    assert power_level(122, 79, 57) == -5
    assert power_level(217, 196, 39) == 0
    assert power_level(101, 153, 71) == 4
    assert part1(18) == (33, 45, 29)
    assert part1(42) == (21, 61, 30)


def test_part1():
    print(part1(9435))


def part2(serial: int) -> Tuple[int, int, int, int]:
    power = [[power_level(x, y, serial) for x in range(300)] for y in range(300)]
    total_power = [[0 for _ in range(300)] for y in range(300)]
    max_power = -1_000_000
    max_x = -1
    max_y = -1
    max_dim = 0

    for dim in range(1, 301):
        for y in range(0, 301 - dim):
            for x in range(0, 301 - dim):
                tp = total_power[y][x]

                for yd in range(0, dim):
                    tp += power[y + yd][x + dim - 1]
                for xd in range(0, dim - 1):
                    tp += power[y + dim - 1][x + xd]

                total_power[y][x] = tp
                if tp > max_power:
                    max_power = tp
                    max_x = x
                    max_y = y
                    max_dim = dim

    return max_x, max_y, max_dim, max_power


def test_part2_example():
    # assert part2(18) == (90, 269, 16, 113)
    assert part2(42) == (232, 251, 12, 119)


def test_part2():
    print(part2(9435))
