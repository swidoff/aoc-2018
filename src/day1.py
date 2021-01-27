import itertools
import operator
from functools import reduce
from typing import List, Iterator

import toolz


def read_input() -> List[int]:
    with open("../input/day1.txt") as file:
        return list(map(int, file.readlines()))


def part1(freq: List[int]) -> int:
    return reduce(operator.add, freq, 0)


def test_part1_examples():
    assert part1([1, 1, 1]) == 3
    assert part1([1, 1, -2]) == 0
    assert part1([-1, -2, -3]) == -6


def test_part1():
    print(part1(read_input()))


def dups(iterator: Iterator[int]) -> Iterator[int]:
    values = set()
    for v in iterator:
        if v in values:
            yield v
        else:
            values.add(v)


def part2(freq: List[int]) -> int:
    return toolz.first(dups(toolz.accumulate(operator.add, itertools.cycle(freq), 0)))


def test_part2_examples():
    assert part2([1, -1]) == 0
    assert part2([+3, +3, +4, -2, -4]) == 10
    assert part2([-6, +3, +8, +5, -6]) == 5
    assert part2([+7, +7, -2, -7, -4]) == 14


def test_part2():
    print(part2(read_input()))
