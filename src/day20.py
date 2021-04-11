import math
from abc import ABC
from collections import deque, defaultdict
from dataclasses import dataclass
from functools import singledispatch
from typing import Tuple, Dict, List, Set, Optional
import re


def read_input() -> str:
    with open("../input/day20.txt") as file:
        return file.readline().strip()


@dataclass
class Regex(ABC):
    pass


@dataclass
class Token(Regex):
    tok: str

    def __str__(self) -> str:
        return self.tok


@dataclass
class Sequence(Regex):
    steps: List[Regex]

    def __str__(self) -> str:
        return "".join(map(str, self.steps))


@dataclass
class Alternate(Regex):
    alt: List[Sequence]

    def __str__(self) -> str:
        return "(" + "|".join(map(str, self.alt)) + ")"


def parse_regex(regex: str) -> Sequence:
    tokens = re.split(r"([(|)])", regex[1:-1])
    res, _ = parse_sequence([t for t in tokens if t != ""])
    return res


def parse_sequence(tokens: List[str]) -> Tuple[Optional[Sequence], List[str]]:
    res = []
    new_tokens = tokens
    while new_tokens:
        next_expr, new_tokens = parse_expression(new_tokens)
        if next_expr is not None:
            res.append(next_expr)
        else:
            break

    return Sequence(res) if res else None, new_tokens


def parse_expression(tokens: List[str]) -> Tuple[Optional[Regex], List[str]]:
    if not tokens or tokens[0] in {")", "|", ""}:
        return None, tokens
    elif tokens[0] == "(":
        alternate, new_tokens = parse_sequence(tokens[1:])
        alternates = [alternate]
        while new_tokens[0] == "|":
            if new_tokens[1] == ")":
                alternate = Sequence([Token("")])
                new_tokens = new_tokens[1:]
            else:
                alternate, new_tokens = parse_sequence(new_tokens[1:])
            alternates.append(alternate)
        return Alternate(alternates), new_tokens[1:]
    else:
        return Token(tokens[0]), tokens[1:]


Coord = Tuple[int, int]
Graph = Dict[Coord, Set[Coord]]

MOVE = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}


def make_graph(initial_seq: Sequence) -> Graph:
    graph = defaultdict(set)
    add_to_graph(initial_seq, {(0, 0)}, graph)
    return graph


@singledispatch
def add_to_graph(_r: Regex, _coords: Set[Coord], _graph: Graph) -> Set[Coord]:
    pass


@add_to_graph.register
def _(t: Token, coords: Set[Coord], graph: Graph) -> Set[Coord]:
    res = set()
    for loc in coords:
        for c in t.tok:
            dr, dc = MOVE[c]
            new_loc = (loc[0] + dr, loc[1] + dc)
            graph[loc].add(new_loc)
            graph[new_loc].add(loc)
            loc = new_loc
        res.add(loc)

    return res


@add_to_graph.register
def _(s: Sequence, coords: Set[Coord], graph: Graph) -> Set[Coord]:
    for step in s.steps:
        coords = add_to_graph(step, coords, graph)

    return coords


@add_to_graph.register
def _(a: Alternate, coords: Set[Coord], graph: Graph) -> Set[Coord]:
    res = set()
    for alt in a.alt:
        res.update(add_to_graph(alt, coords, graph))

    return res


def shortest_paths(graph):
    q = deque([((0, 0), 0)])
    seen = {(0, 0): 0}
    while q:
        loc, steps = q.popleft()
        new_steps = steps + 1
        for next_loc in graph[loc]:
            if next_loc not in seen:
                seen[next_loc] = new_steps
                q.append((next_loc, new_steps))
    return seen


def print_graph(graph: Graph):
    min_r = min(r for r, _ in graph.keys())
    max_r = max(r for r, _ in graph.keys())
    min_c = min(c for _, c in graph.keys())
    max_c = max(c for _, c in graph.keys())
    num_cols = max_c - min_c + 1

    print()
    for _ in range(2 * num_cols + 1):
        print("#", end="")
    print()

    origin = (0, 0)
    for r in range(min_r, max_r + 1):
        print("#", end="")
        for c in range(min_c, max_c + 1):
            coord = (r, c)
            room_char = "X" if coord == origin else "."
            print(room_char, end="")

            door_coord = (r, c + 1)
            door_char = "|" if door_coord in graph[coord] else "#"
            print(door_char, end="")

        print()
        print("#", end="")
        for c in range(min_c, max_c + 1):
            coord = (r, c)
            door_coord = (r + 1, c)
            door_char = "-" if door_coord in graph[coord] else "#"
            print(door_char, end="")
            print("#", end="")
        print()

    print()


def part1(regex: str):
    seq = parse_regex(regex)
    graph = make_graph(seq)
    # print_graph(graph)
    seen = shortest_paths(graph)
    return max(seen.values())


def part2(regex: str):
    seq = parse_regex(regex)
    graph = make_graph(seq)
    # print_graph(graph)
    seen = shortest_paths(graph)
    return sum(1 for v in seen.values() if v >= 1000)


def test_part1_examples():
    assert part1("^WNE$") == 3
    assert part1("^ENWWW(NEEE|SSE(EE|N))$") == 10
    assert part1("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$") == 18
    assert part1("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$") == 23
    assert part1("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$") == 31


def test_part1():
    regex = read_input()
    assert part1(regex) == 3872


def test_part2():
    regex = read_input()
    assert part1(regex) == 8600
