from functools import lru_cache


@lru_cache(maxsize=None)
def geologic_index(x: int, y: int, target_x: int, target_y: int, depth: int) -> int:
    if x == 0 and y == 0:
        res = 0
    elif x == target_x and y == target_y:
        res = 0
    elif y == 0:
        res = x * 16807
    elif x == 0:
        res = y * 48271
    else:
        res = erosion_level(x - 1, y, target_x, target_y, depth) * erosion_level(x, y - 1, target_x, target_y, depth)

    return res


@lru_cache(maxsize=None)
def erosion_level(x: int, y: int, target_x: int, target_y: int, depth: int) -> int:
    return (geologic_index(x, y, target_x, target_y, depth) + depth) % 20183


@lru_cache(maxsize=None)
def region_type(x: int, y: int, target_x: int, target_y: int, depth: int) -> int:
    return erosion_level(x, y, target_x, target_y, depth) % 3


def part1(target_x: int, target_y, depth: int) -> int:
    return sum(
        region_type(x, y, target_x, target_y, depth) for x in range(0, target_x + 1) for y in range(0, target_y + 1)
    )


def print_cave(target_x: int, target_y, depth: int):
    print()
    for y in range(0, target_y + 1):
        for x in range(0, target_x + 1):
            if x == 0 and y == 0:
                ch = "M"
            elif x == target_x and y == target_y:
                ch = "T"
            else:
                typ = region_type(x, y, target_x, target_y, depth)
                if typ == 0:
                    ch = "."
                elif typ == 1:
                    ch = "="
                else:
                    ch = "|"
            print(ch, end="")
        print()
    print()


def test_part1_example():
    assert region_type(0, 0, 10, 10, 510) == 0
    assert region_type(1, 0, 10, 10, 510) == 1
    assert region_type(0, 1, 10, 10, 510) == 0
    assert region_type(1, 1, 10, 10, 510) == 2
    assert region_type(10, 10, 10, 10, 510) == 0
    print_cave(10, 10, 510)
    assert part1(10, 10, 510) == 114


def test_part1():
    print(part1(13, 726, 3066))
