import re
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import List


def read_input() -> List[str]:
    with open("../input/day4.txt") as file:
        return file.readlines()


@dataclass
class Record(object):
    guard: int
    date: str
    start: int
    end: int


def parse_input(lines: List[str]) -> List[Record]:
    guard = 0
    start = 0
    end = 0
    date = ""
    res = []
    for line in lines:
        if match := re.match(r"\[\d+\-\d+\-\d+ \d+:\d+] Guard #(\d+) begins shift", line):
            guard = int(match.group(1))
        elif match := re.match(r"\[(\d+\-\d+\-\d+) \d+:(\d+)] falls asleep", line):
            date = match.group(1)
            start = int(match.group(2))
        elif match := re.match(r"\[\d+\-\d+\-\d+ \d+:(\d+)] wakes up", line):
            end = int(match.group(1))
            res.append(Record(guard, date, start, end))

    return res


def part1(records: List[Record]) -> int:
    res = defaultdict(lambda: 0)
    for record in records:
        res[record.guard] += record.end - record.start

    guard = max(res.keys(), key=lambda g: res[g])
    [(minute, _)] = Counter(
        minute for r in records if r.guard == guard for minute in range(r.start, r.end)
    ).most_common(1)

    return guard * minute

example = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".splitlines()


def test_part1_examples():
    assert part1(parse_input(example)) == 240


def test_part1():
    print(part1(parse_input(read_input())))


def part2(records: List[Record]) -> int:
    res = defaultdict(Counter)
    for r in records:
        for minute in range(r.start, r.end):
            res[minute][r.guard] += 1

    max_count = 0
    max_guard = 0
    max_minute = 0
    for minute, counter in res.items():
        [(guard, count)] = counter.most_common(1)
        if count > max_count:
            max_guard = guard
            max_minute = minute
            max_count = count

    return max_guard * max_minute


def test_part2_examples():
    assert part2(parse_input(example)) == 4455


def test_part2():
    print(part2(parse_input(read_input())))
