def part1(count: int) -> str:
    ls = [3, 7]
    e1 = 0
    e2 = 1
    while len(ls) < count + 10:
        new_recipe = str(ls[e1] + ls[e2])
        for c in new_recipe:
            ls.append(int(c))

        e1 = (e1 + ls[e1] + 1) % len(ls)
        e2 = (e2 + ls[e2] + 1) % len(ls)

    return "".join(str(i) for i in ls[count : count + 10])


def part2(scores: str) -> int:
    ls = [3, 7]
    e1 = 0
    e2 = 1
    suffix = [int(c) for c in scores]
    while True:
        new_recipe = str(ls[e1] + ls[e2])
        for c in new_recipe:
            ls.append(int(c))
            if ls[-len(suffix) :] == suffix:
                return len(ls) - len(suffix)

        e1 = (e1 + ls[e1] + 1) % len(ls)
        e2 = (e2 + ls[e2] + 1) % len(ls)


def test_part1_examples():
    assert part1(9) == "5158916779"
    assert part1(5) == "0124515891"
    assert part1(18) == "9251071085"
    assert part1(2018) == "5941429882"


def test_part1():
    print(part1(260321))


def test_part2_examples():
    assert part2("51589") == 9
    assert part2("01245") == 5
    assert part2("92510") == 18
    assert part2("59414") == 2018


def test_part2():
    print(part2("260321"))
