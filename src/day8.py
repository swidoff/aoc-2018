from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import List, Tuple


def read_input() -> str:
    with open("../input/day8.txt") as file:
        return file.readline().strip()


@dataclass
class Node(object):
    metadata: List[int]
    children: List[Node]

    @cached_property
    def value(self):
        if self.children:
            return sum(self.children[m - 1].value for m in self.metadata if m <= len(self.children))
        else:
            return sum(self.metadata)


def parse_input(line: str) -> List[int]:
    return list(map(int, line.split(" ")))


def parse_node(ls: List[int], i: int = 0) -> Tuple[Node, int]:
    num_children, num_metadata = ls[i], ls[i + 1]

    j = i + 2
    children = []
    for _ in range(num_children):
        child, j = parse_node(ls, j)
        children.append(child)

    metadata = ls[j : j + num_metadata]
    return Node(metadata, children), j + num_metadata


def part1(node: Node) -> int:
    return sum(node.metadata) + sum(part1(n) for n in node.children)


def part2(node: Node) -> int:
    return node.value


def test_part1_example():
    example = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    node, _ = parse_node(parse_input(example))
    assert part1(node) == 138


def test_part1():
    node, _ = parse_node(parse_input(read_input()))
    print(part1(node))


def test_part2_example():
    example = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    node, _ = parse_node(parse_input(example))
    assert part2(node) == 66


def test_part2():
    node, _ = parse_node(parse_input(read_input()))
    print(part2(node))
