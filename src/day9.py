def part1(players: int, last: int) -> int:
    circle = [0]
    scores = [0] * players
    i = 0
    for marble in range(1, last + 1):
        if marble % 23 == 0:
            player = (marble - 1) % players
            scores[player] += marble

            i = (i - 7) % len(circle)
            scores[player] += circle[i]
            del circle[i]
            if i == len(circle):
                i = 0
        else:
            i = (i + 1) % len(circle)
            i += 1
            circle.insert(i, marble)

    return max(scores)


def test_part1_example():
    assert part1(9, 25) == 32
    assert part1(10, 1618) == 8317
    assert part1(13, 7999) == 146373
    assert part1(17, 1104) == 2764
    assert part1(21, 6111) == 54718
    assert part1(30, 5807) == 37305


def test_part1():
    print(part1(424, 71144))


def part2(players: int, last: int) -> int:
    marbles = [ [-1, -1] for _ in range(last + 1)]
    scores = [0] * players
    marbles[0] = [0, 0]

    i = 0
    for marble in range(1, last + 1):
        if marble % 23 == 0:
            player = (marble - 1) % players
            scores[player] += marble

            r = i
            for _ in range(7):
                r = marbles[r][0]

            scores[player] += r

            p = marbles[r][0]
            n = marbles[r][1]

            marbles[p][1] = n
            marbles[n][0] = p

            i = n
        else:
            p = marbles[i][1]
            n = marbles[p][1]

            marbles[marble][0] = p
            marbles[marble][1] = n
            marbles[p][1] = marble
            marbles[n][0] = marble
            i = marble

    return max(scores)


def test_part2_example():
    assert part2(9, 25) == 32
    assert part2(10, 1618) == 8317
    assert part2(13, 7999) == 146373
    assert part2(17, 1104) == 2764
    assert part2(21, 6111) == 54718
    assert part2(30, 5807) == 37305
    assert part2(424, 71144) == 405143


def test_part2():
    print(part2(424, 71144 * 100))
