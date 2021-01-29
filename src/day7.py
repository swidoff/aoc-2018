import re
from collections import defaultdict
from typing import List, Dict, Set


def read_input() -> List[str]:
    with open("../input/day7.txt") as file:
        return file.readlines()


def parse_input(lines: List[str]) -> Dict[str, Set[str]]:
    res = defaultdict(set)

    for line in lines:
        match = re.match(r"Step (\w) must be finished before step (\w) can begin.", line)
        res[match.group(2)].add(match.group(1))

    return res


def part1(dependencies: Dict[str, Set[str]]) -> str:
    all_nodes = set()
    for n1, values in dependencies.items():
        all_nodes.add(n1)
        for n2 in values:
            all_nodes.add(n2)

    res = []
    q = sorted(n for n in all_nodes if n not in dependencies)

    while q:
        n1 = q[0]
        res.append(n1)
        for n2, values in dependencies.items():
            if n1 in values:
                values.remove(n1)
                if not values:
                    q.append(n2)

        q = sorted(q[1:])

    return "".join(res)


def test_part1_example():
    example = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".splitlines()
    assert part1(parse_input(example)) == "CABDFE"


def test_part1():
    print(part1(parse_input(read_input())))


def part2(dependencies: Dict[str, Set[str]], workers: int, delay: int) -> str:
    all_nodes = set()
    for n1, values in dependencies.items():
        all_nodes.add(n1)
        for n2 in values:
            all_nodes.add(n2)

    q = sorted(n for n in all_nodes if n not in dependencies)
    w = []
    time = 0

    while all_nodes:
        to_append = []
        while len(w) < workers and q:
            n1 = q[0]
            q = q[1:]
            w.append((n1, time + (ord(n1) - ord("A") + 1) + delay))

        w = sorted(w, key=lambda p: p[1])

        if w:
            n, time = w[0]
            all_nodes.remove(n)
            w = w[1:]
            for n2, values in dependencies.items():
                if n in values:
                    values.remove(n)
                    if not values:
                        q.append(n2)

            q = sorted(q + to_append)

    return time


def test_part2_example():
    example = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".splitlines()
    assert part2(parse_input(example), 2, 0) == 15


def test_part2():
    print(part2(parse_input(read_input()), 5, 60))
