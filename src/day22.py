from __future__ import annotations

import dataclasses
import heapq
from dataclasses import dataclass
from enum import Enum
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


def print_cave(me_x: int, me_y: int, target_x: int, target_y, depth: int):
    print()
    for y in range(0, target_y + 1):
        for x in range(0, target_x + 1):
            if x == 0 and y == 0:
                ch = "M"
            elif x == me_x and y == me_y:
                ch = "X"
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
    assert part1(10, 10, 510) == 114


def test_part1():
    print(part1(13, 726, 3066))


TOOLS_IN_REGION = [
    [1, 2],
    [0, 1],
    [0, 2],
]


@dataclass(frozen=True, order=True)
class State:
    time: int
    distance: int
    x: int
    y: int
    tool: int


def part2(target_x: int, target_y, depth: int) -> int:
    q = []
    initial_state = State(0, target_x + target_y, 0, 0, 2)
    seen = {initial_state}
    heapq.heappush(q, initial_state)

    while q:
        state = heapq.heappop(q)
        # print_cave(state.x, state.y, target_x, target_y, depth)

        if state.x == target_x and state.y == target_y and state.tool == 2:
            return state.time
        else:
            typ = region_type(state.x, state.y, target_x, target_y, depth)
            for x_d, y_d in [(1, 0), (0, 1), (0, 0), (0, -1), (-1, 0)]:
                new_x = state.x + x_d
                new_y = state.y + y_d
                if new_x >= 0 and new_y >= 0:
                    new_typ = region_type(new_x, new_y, target_x, target_y, depth)
                    new_distance = abs(target_x - new_x) + abs(target_y - new_y)
                    if new_distance <= initial_state.distance:
                        for new_tool in TOOLS_IN_REGION[new_typ]:
                            if new_tool in TOOLS_IN_REGION[typ]:
                                new_time = state.time + 1
                                if new_tool != state.tool:
                                    new_time += 7
                                new_state = State(new_time, new_distance, new_x, new_y, new_tool)
                                if new_state not in seen:
                                    heapq.heappush(q, new_state)
                                    seen.add(new_state)

    return -1


def test_part2_example():
    assert part2(10, 10, 510) == 45


def test_part2():
    print(part2(13, 726, 3066))
