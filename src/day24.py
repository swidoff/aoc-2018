from __future__ import annotations

import dataclasses
import re
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple


def read_input() -> List[str]:
    with open("../input/day24.txt") as file:
        return [l.rstrip() for l in file.readlines()]


@dataclass
class Group(object):
    army: str
    number: int
    units: int
    hit_points: int
    immunities: List[str]
    weaknesses: List[str]
    attack: int
    attack_type: str
    initiative: int

    @property
    def effective_power(self) -> int:
        return self.units * self.attack

    def damage_to(self, other: Group) -> int:
        if self.attack_type in other.immunities:
            modifier = 0
        elif self.attack_type in other.weaknesses:
            modifier = 2
        else:
            modifier = 1
        return modifier * self.effective_power


def parse_group(army: str, number: int, line: str) -> Group:
    match = re.match(
        r"(\d+) units each with (\d+) hit points (\([\w;, ]+\))?\s?with an attack that does (\d+) (\w+) damage at "
        r"initiative (\d+)",
        line,
    )

    weaknesses = None
    immunities = None
    units, hit_points, weaknesses_and_immunities, attack, attack_type, initiative = match.groups()
    if weaknesses_and_immunities:
        for part in weaknesses_and_immunities.split("; "):
            weak_match = re.search(r"weak to ([\w+,; ]+)", part)
            if weak_match:
                weaknesses = weak_match.group(1).split(", ")

            immune_match = re.search(r"immune to ([\w+, ]+)", part)
            if immune_match:
                immunities = immune_match.group(1).split(", ")

    return Group(
        army,
        number,
        int(units),
        int(hit_points),
        immunities or [],
        weaknesses or [],
        int(attack),
        attack_type,
        int(initiative),
    )


def parse_input(lines: List[str]) -> List[List[Group], List[Group]]:
    res = []
    group = None
    army = ""
    number = 1
    for line in lines:
        if all(c.isspace() for c in line):
            res.append(group)
        elif line[0].isalpha():
            army = line[:-1]
            group = []
            number = 1
        else:
            group.append(parse_group(army, number, line))
            number += 1

    if group:
        res.append(group)
    return res


def part1(army1: List[Group], army2: List[Group], boost: int = 0, debug: bool = True) -> Tuple[int, bool]:
    army1 = [
        dataclasses.replace(g, attack=g.attack + boost)
        for g in army1
    ]
    army2 = deepcopy(army2)

    units_killed_in_last_fight = 1
    while army1 and army2 and units_killed_in_last_fight > 0:
        if debug:
            print("Immune System:")
            for g in army1:
                print("Group", g.number, "contains", g.units, "units")
            print("Infection:")
            for g in army2:
                print("Group", g.number, "contains", g.units, "units")
            print()

        # Selection phase
        selections = []
        selection_order = sorted(army1 + army2, key=lambda g: (g.effective_power, g.initiative), reverse=True)
        remaining1 = list(army1)
        remaining2 = list(army2)

        for attacker in selection_order:
            other_army = remaining1 if attacker in army2 else remaining2
            if other_army:
                target = max(other_army, key=lambda o: (attacker.damage_to(o), o.effective_power, o.initiative))
                damage = attacker.damage_to(target)
                if debug:
                    print(
                        attacker.army,
                        "group",
                        attacker.number,
                        "would deal defending group",
                        target.number,
                        damage,
                        "damage",
                    )
                if damage > 0:
                    selections.append((attacker, target))
                    other_army.remove(target)

        if debug:
            print()

        units_killed_in_last_fight = 0
        attackers = sorted(selections, key=lambda p: p[0].initiative, reverse=True)
        for attacker, target in attackers:
            damage = attacker.damage_to(target)
            units_killed = min(damage // target.hit_points, target.units)
            target.units = target.units - units_killed
            units_killed_in_last_fight += units_killed
            if debug:
                print(
                    attacker.army,
                    "group",
                    attacker.number,
                    "attacks defending group",
                    target.number,
                    "killing",
                    units_killed,
                    "units",
                )

        army1 = [g for g in army1 if g.units > 0]
        army2 = [g for g in army2 if g.units > 0]

        if debug:
            print()

    return sum(g.units for g in army1 + army2), len(army1) > 0 and units_killed_in_last_fight > 0


example = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".splitlines()


def test_part1():
    lines = read_input()
    immune, infection = parse_input(lines)
    assert part1(immune, infection, debug=False)[0] == 24009
    # Too low: 23339
    # Too low: 23340


def part2(army1: List[Group], army2: List[Group]) -> int:
    min_boost = 0
    max_boost = 10000
    last_score = None
    while min_boost < max_boost:
        boost = (min_boost + max_boost) // 2
        print("Trying boost", boost, "between", min_boost, "and", max_boost)
        score, win = part1(army1, army2, boost=boost, debug=False)
        print(win, score)
        if win:
            last_score = score
            max_boost = boost - 1
        else:
            min_boost = boost + 1

    return last_score


def test_part2_example():
    print()
    immune, infection = parse_input(example)
    assert part2(immune, infection) == 51


def test_part2():
    lines = read_input()
    immune, infection = parse_input(lines)
    print(part2(immune, infection))
    # Too low: 23339
    # Too low: 23340
