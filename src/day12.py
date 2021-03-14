from dataclasses import dataclass
from typing import List, Tuple, Iterator, Set

import toolz


def read_input() -> Tuple[str, List[str]]:
    with open("../input/day12.txt") as file:
        lines = file.readlines()
        initial_state = lines[0][len("initial state: ") : -1]
        rules = [line.strip() for line in lines[2:]]
        return initial_state, rules


def part1(initial_state: str, rules: List[str]) -> Iterator[int]:
    plants = set(i for i, c in enumerate(initial_state) if c == "#")
    plant_rules = set(rule[0:5] for rule in rules if rule[-1] == "#")

    for i in range(125):
        new_plants = set()
        min_plant = min(plants)
        max_plant = max(plants)

        for i in range(min_plant - 5, max_plant + 5):
            match = "".join("#" if j in plants else "." for j in range(i - 2, i + 3))
            if match in plant_rules:
                new_plants.add(i)

        yield sum(new_plants)
        plants = new_plants


@dataclass
class Plants(object):
    plants: Set[int]

    @property
    def min(self):
        return min(self.plants)

    @property
    def max(self):
        return max(self.plants)

    @property
    def count(self):
        return len(self.plants)

    @property
    def sum(self):
        return sum(self.plants)

    def at(self, i: int) -> str:
        return "".join("#" if j in self.plants else "." for j in range(i - 2, i + 3))

    def __str__(self):
        return "".join("#" if j in self.plants else "." for j in range(self.min - 5, self.max + 5))


def part2(initial_state: str, rules: List[str]) -> Iterator[Plants]:
    plants = Plants(set(i for i, c in enumerate(initial_state) if c == "#"))
    plant_rules = set(rule[0:5] for rule in rules if rule[-1] == "#")

    while True:
        new_plants = set()
        for i in range(plants.min - 5, plants.max + 5):
            if plants.at(i) in plant_rules:
                new_plants.add(i)

        plants = Plants(new_plants)
        yield plants


def test_part1_example():
    initial_state = "#..#.#..##......###...###"
    rules = """...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""".splitlines()

    assert toolz.nth(20, part1(initial_state, rules)) == 325


def test_part1():
    initial_state, rules = read_input()
    print(part1(initial_state, rules))


def test_part2():
    initial_state, rules = read_input()
    for i, plants in enumerate(toolz.take(125, part2(initial_state, rules))):
        print(i, plants.count, plants.min, plants.max, plants.sum, str(plants))

    print(3151 + 22 * (50_000_000_000 - 120))