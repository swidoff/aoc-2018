from typing import List, Tuple


def read_input() -> List[str]:
    with open("../input/day6.txt") as file:
        return file.readlines()


def parse_inputs(lines: List[str]) -> List[Tuple[int, int]]:
    res = []
    for line in lines:
        x, y = line.split(", ")
        res.append((int(x), int(y)))
    return res


def part1(points: List[Tuple[int, int]]) -> int:
    min_x = min(p[0] for p in points) - 1
    min_y = min(p[1] for p in points) - 1
    max_x = max(p[0] for p in points) + 1
    max_y = max(p[1] for p in points) + 1
    counts = [0] * len(points)

    def closest(x1: int, y1: int) -> int:
        return min(range(len(points)), key=lambda j: abs(x1 - points[j][0]) + abs(y1 - points[j][1]))

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            i = closest(x, y)
            counts[i] += 1

    candidates = set(range(len(points)))
    for y in range(min_x - 1, max_x + 2):
        x_range = range(min_x - 1, max_x + 2) if y == min_x - 1 or y == max_x + 1 else [min_y - 1, max_y + 1]

        for x in x_range:
            i = closest(x, y)
            if i in candidates:
                candidates.remove(i)

    res = max(candidates, key=lambda j: counts[j])
    return counts[res]


def test_part1_example():
    example = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".splitlines()
    assert part1(parse_inputs(example)) == 17


def test_part1():
    print(part1(parse_inputs(read_input())))


def part2(points: List[Tuple[int, int]], threshold: int) -> int:
    min_x = min(p[0] for p in points) - threshold // 4
    min_y = min(p[1] for p in points) - threshold // 4
    max_x = max(p[0] for p in points) + threshold // 4
    max_y = max(p[1] for p in points) + threshold // 4
    res = 0

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if sum(abs(x - px) + abs(y - py) for px, py in points) < threshold:
                res += 1

    return res


def test_part2_example():
    example = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".splitlines()
    assert part2(parse_inputs(example), 32) == 16


def test_part2():
    print(part2(parse_inputs(read_input()), 10_000))
