from collections import Counter
from typing import List

import itertools
import toolz


def read_input() -> List[str]:
    with open("../input/day2.txt") as file:
        return file.readlines()


def part1(ids: List[str]) -> int:
    count_2, count_3 = 0, 0
    for i in ids:
        counter = Counter(i)
        if 2 in counter.values():
            count_2 += 1
        if 3 in counter.values():
            count_3 += 1

    return count_2 * count_3


def test_part1_examples():
    example = [
        "abcdef",
        "bababc",
        "abbcde",
        "abcccd",
        "aabcdd",
        "abcdee",
        "ababab",
    ]
    assert part1(example) == 12


def test_part1():
    print(part1(read_input()))


def shared_chars(ids1: str, id2: str) -> List[str]:
    return [c1 for c1, c2 in zip(ids1, id2) if c1 == c2]


def part2(ids: List[str]) -> str:
    return toolz.first(
        "".join(ch) for id1, id2 in itertools.product(ids, ids) if len(ch := shared_chars(id1, id2)) == len(id1) - 1
    )


def test_part2_example():
    example = [
        "abcde",
        "fghij",
        "klmno",
        "pqrst",
        "fguij",
        "axcye",
        "wvxyz",
    ]
    assert part2(example) == "fgij"


def test_part2():
    print(part2(read_input()))
