from abc import ABC
from collections import deque, defaultdict
from dataclasses import dataclass
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


@dataclass
class Sequence(Regex):
    steps: List[Regex]


@dataclass
class Alternate(Regex):
    alt: List[Sequence]


def parse_regex(regex: str) -> Sequence:
    tokens = re.split(r"([(|)])", regex[1:-1])
    res, _ = parse_sequence(tokens)
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
            if new_tokens[1] == "":
                alternate = Sequence([Token("")])
                new_tokens = new_tokens[2:]
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
    stack = [(initial_seq.steps, (0, 0))]

    while stack:
        steps, loc = stack.pop()
        if steps:
            step, next_steps = steps[0], steps[1:]
            if isinstance(step, Token):
                for t in step.tok:
                    dr, dc = MOVE[t]
                    new_loc = (loc[0] + dr, loc[1] + dc)
                    graph[loc].add(new_loc)
                    graph[new_loc].add(loc)
                    loc = new_loc
                stack.append((next_steps, loc))
            elif isinstance(step, Sequence):
                stack.append((step.steps + next_steps, loc))
            elif isinstance(step, Alternate):
                for alt in reversed(step.alt):
                    stack.append((alt.steps + next_steps, loc))

    return graph


def max_doors(graph: Graph) -> int:
    q = deque([((0, 0), 0)])
    seen = {(0, 0): 0}

    while q:
        loc, steps = q.popleft()
        new_steps = steps + 1
        for next_loc in graph[loc]:
            if next_loc not in seen:
                seen[next_loc] = new_steps
                q.append((next_loc, new_steps))

    return max(seen.values())


def part1(regex: str):
    seq = parse_regex(regex)
    graph = make_graph(seq)
    return max_doors(graph)


def test_part1_examples():
    assert part1("^WNE$") == 3
    assert part1("^ENWWW(NEEE|SSE(EE|N))$") == 10
    assert part1("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$") == 18
    assert part1("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$") == 23
    assert part1("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$") == 31


def test_part1():
    regex = read_input()
    print(part1(regex))
