def part1(reg0: int = 0):
    seen = set()
    while True:
        # 0 seti 123 0 1
        reg1 = 123

        # 1 bani 1 456 1
        reg1 = reg1 & 456

        # 2 eqri 1 72 1
        reg1 = reg1 == 72

        # 3 addr 1 4 4
        # 4 seti 0 0 4
        if reg1:
            break

    # 5 seti 0 7 1
    reg1 = 0
    while True:
        # 6 bori 1 65536 5
        reg5 = reg1 | 65536

        # 7 seti 8595037 6 1
        reg1 = 8595037
        while True:
            # 8 bani 5 255 3
            reg3 = reg5 & 255

            # 9 addr 1 3 1
            reg1 = reg1 + reg3

            # 10 bani 1 16777215 1
            reg1 = reg1 & 16777215

            # 11 muli 1 65899 1
            reg1 = reg1 * 65899

            # 12 bani 1 16777215 1
            reg1 = reg1 & 16777215

            # 13 gtir 256 5 3
            if 256 > reg5:
                # 14 addr 3 4 4
                # 15 addi 4 1 4
                # 16 seti 27 4 4
                break

            # 17 seti 0 2 3
            # while True:
            #     # 18 addi 3 1 2
            #     reg2 = reg3 + 1
            #
            #     # 19 muli 2 256 2
            #     reg2 = reg2 * 256
            #
            #     # 20 gtrr 2 5 2
            #     if reg2 > reg5:
            #         # 21 addr 2 4 4
            #         # 22 addi 4 1 4
            #         # 23 seti 25 4 4
            #         break
            #
            #     # 24 addi 3 1 3
            #     reg3 = reg3 + 1
            #
            #     # 25 seti 17 8 4

            # 26 setr 3 8 5
            reg5 = reg5 // 256

            # 27 seti 7 5 4

        # 28 eqrr 1 0 3
        # 29 addr 3 4 4
        # 30 seti 5 9 4
        if reg1 not in seen:
            print(reg1)
            seen.add(reg1)

        # print(reg1)
        if reg1 == reg0:
            break

# def test_part1():
#     part1(1_000_000_000_000)

if __name__ == '__main__':
    part1()