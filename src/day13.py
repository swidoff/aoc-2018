from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Dict


def read_input() -> List[str]:
    with open("../input/day13.txt") as file:
        return file.readlines()


class Turn(Enum):
    Left = 0
    Straight = 1
    Right = 2

    @property
    def next(self):
        return Turn((self.value + 1) % 3)


class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

    def turn(self, turn: Turn):
        if turn == Turn.Left:
            return Direction(self.value - 1) if self != Direction.Up else Direction.Left
        elif turn == Turn.Right:
            return Direction((self.value + 1) % 4)
        else:
            return self


DIRECTION_VECTOR = {
    Direction.Up: (-1, 0),
    Direction.Right: (0, 1),
    Direction.Down: (1, 0),
    Direction.Left: (0, -1),
}


Coord = Tuple[int, int]


@dataclass
class Cart(object):
    location: Coord
    direction: Direction
    next_turn: Turn = Turn.Left
    crashed: bool = False


Course = Tuple[Dict[Coord, str], List[Cart]]

CART_CHARS = {
    ">": Direction.Right,
    "<": Direction.Left,
    "^": Direction.Up,
    "v": Direction.Down,
}

DIR_CHARS = {d: c for c, d in CART_CHARS.items()}

COURSE_CHARS = {"+", "/", "\\", "|", "-"}


def parse_input(lines: List[str]) -> Tuple[Dict[Tuple[int, int], str], List[Cart]]:
    course = {}
    carts = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char in CART_CHARS:
                carts.append(Cart((row, col), CART_CHARS[char]))
            elif char in COURSE_CHARS:
                course[(row, col)] = char

    return course, carts


def part1(lines: List[str]) -> Tuple[int, int]:
    course, carts = parse_input(lines)
    carts = sorted(carts, key=lambda c: c.location)

    while True:
        # print_course(course, carts, len(lines))
        # print()

        for cart in carts:
            row, col = cart.location
            row_d, col_d = DIRECTION_VECTOR[cart.direction]
            new_row, new_col = row + row_d, col + col_d
            new_location = (new_row, new_col)

            if any(c.location == new_location for c in carts):
                return new_col, new_row
            elif new_location in course:
                if course[new_location] == "+":
                    cart.direction = cart.direction.turn(cart.next_turn)
                    cart.next_turn = cart.next_turn.next
                elif course[new_location] == "/":
                    if cart.direction == Direction.Up or cart.direction == Direction.Down:
                        cart.direction = cart.direction.turn(Turn.Right)
                    else:
                        cart.direction = cart.direction.turn(Turn.Left)
                elif course[new_location] == "\\":
                    if cart.direction == Direction.Up or cart.direction == Direction.Down:
                        cart.direction = cart.direction.turn(Turn.Left)
                    else:
                        cart.direction = cart.direction.turn(Turn.Right)

            cart.location = new_location

        carts = sorted(carts, key=lambda c: c.location)


def part2(lines: List[str]) -> Tuple[int, int]:
    course, carts = parse_input(lines)
    carts = sorted(carts, key=lambda c: c.location)

    while len(carts) > 1:
        # print_course(course, carts, len(lines))
        # print()
        for cart in carts:
            if cart.crashed:
                continue

            row, col = cart.location
            row_d, col_d = DIRECTION_VECTOR[cart.direction]
            new_row, new_col = row + row_d, col + col_d
            new_location = (new_row, new_col)

            if any(c.location == new_location for c in carts):
                cart.crashed = True
                for c in carts:
                    if c.location == new_location:
                        c.crashed = True
                        break
            elif new_location in course:
                if course[new_location] == "+":
                    cart.direction = cart.direction.turn(cart.next_turn)
                    cart.next_turn = cart.next_turn.next
                elif course[new_location] == "/":
                    if cart.direction == Direction.Up or cart.direction == Direction.Down:
                        cart.direction = cart.direction.turn(Turn.Right)
                    else:
                        cart.direction = cart.direction.turn(Turn.Left)
                elif course[new_location] == "\\":
                    if cart.direction == Direction.Up or cart.direction == Direction.Down:
                        cart.direction = cart.direction.turn(Turn.Left)
                    else:
                        cart.direction = cart.direction.turn(Turn.Right)

            cart.location = new_location

        carts = sorted((c for c in carts if not c.crashed), key=lambda c: c.location)

    if carts:
        return carts[0].location


def print_course(course: Dict[Coord, str], carts: List[Cart], dim: int):
    max_row = max(c[0] for c in course)
    max_col = max(c[1] for c in course)
    for row in range(max_row + 1):
        line = []
        for col in range(max_col + 1):
            coord = (row, col)

            if any(c.location == coord for c in carts):
                for c in carts:
                    if c.location == coord:
                        line.append(DIR_CHARS[c.direction])
                        break
            elif coord in course:
                line.append(course[coord])
            else:
                line.append(" ")

        print("".join(line))


def test_part1_example():
    lines = """
/->-\        
|   |  /----\ 
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
""".splitlines()[
        1:
    ]
    print()
    assert part1(lines) == (7, 3)


def test_part1():
    lines = read_input()
    print(part1(lines))


def test_part2():
    lines = read_input()
    print(part2(lines))