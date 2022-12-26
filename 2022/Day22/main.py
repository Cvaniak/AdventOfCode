import argparse
import bisect
import collections
from dataclasses import dataclass
import functools
import itertools
import math
import operator
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from itertools import combinations, permutations, product
import re

import parse
from rich import print

debug = set("0")
debug_space = False


def dbg(*args, lvl="0", **kwargs):
    if lvl in debug:
        print(lvl)
        print(*args, **kwargs)
        if debug_space:
            print()


def set_debuger():
    global debug, debug_space
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", nargs="?", const="0", default="0", help="Debug List"
    )
    parser.add_argument(
        "-n", "--nodebug", action="store_true", help="Remove default debug"
    )
    parser.add_argument(
        "-s", "--addspace", action="store_true", help="Space between debug"
    )
    args = parser.parse_args()
    debug.update({x for x in args.debug})
    if args.nodebug:
        debug.remove("0")
    if args.addspace:
        debug_space = True


# ===== ^^ DEBUGER ^^ =====

wsen = {"E": (1, 0), "S": (0, -1), "W": (-1, 0), "N": (0, 1)}
dir_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_8 = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]


def prod(factors):
    return functools.reduce(operator.mul, factors, 1)


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def load_int_lines(datat):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = [x for x in i]
    return data


def load_int_commas(datat):
    return list(map(int, datat[0].split(",")))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 6032
    # assert part_2(data) == 5031


@dataclass
class Player:
    y: int
    x: int
    facing: int
    board: list[str]

    def move(self, x):
        d = dir_4[self.facing]
        h = len(self.board)
        yyn, xxn = self.y, self.x

        while x:
            w = len(self.board[yyn])
            xxn = (self.x + d[1]) % w
            yyn = (self.y + d[0]) % h
            while xxn >= len(self.board[yyn]) or self.board[yyn][xxn] == " ":

                yyn = (yyn + d[0]) % h
                if d[1] != 0:
                    xxn = (xxn + d[1]) % w
            if self.board[yyn][xxn] == "#":
                return
            self.y, self.x = yyn, xxn
            x -= 1

    def rotate(self, r):
        if r == "R":
            self.facing = (self.facing + 1) % 4
        elif r == "L":
            self.facing = (self.facing - 1) % 4
        else:
            assert False


def part_1(data):
    for i in range(len(data[0])):
        if data[0][i] not in (" ", "#"):
            player = Player(0, i, 0, data[:-2])
            break
    dirs = re.split("(\d+)", data[-1])
    dirs = [int(x) if x.isdigit() else x for x in dirs][1:-1]

    for mov in dirs:
        if isinstance(mov, int):
            player.move(mov)
        else:
            player.rotate(mov)

    col, row, facing = player.y + 1, player.x + 1, player.facing
    print(col, row, facing)

    return col * 1000 + row * 4 + facing


def rot(grid: list[list[str]]):
    return list(zip(*grid[::-1]))


@dataclass
class PlayerCube:
    y: int
    x: int
    facing: int
    board: list[str]

    def move(self, x):
        d = dir_4[self.facing]
        yyn, xxn = self.y, self.x

        while x:

            d = dir_4[self.facing]
            yyn, xxn = (self.y + d[0]), (self.x + d[1])

            facingn = self.facing

            ry, rx = self.y // 50, self.x // 50
            rry, rrx = yyn // 50, xxn // 50
            if (ry, rx) != (rry, rrx):
                yyn, xxn, facingn = self.wrap()

            if self.board[yyn][xxn] == "#":
                return
            self.y, self.x = yyn, xxn
            self.facing = facingn
            x -= 1

    def wrap(self):
        ry, rx = self.y // 50, self.x // 50
        ny, nx = self.y % 50, self.x % 50
        print(ry, rx, self.facing, ny, nx)

        yy, xx, facing = {
            (0, 1): {
                0: (self.y, self.x + 1, 0),  # Ok
                1: (self.y + 1, self.x, 1),  # Ok
                2: (149 - ny, 0, 0),  # f - (2, 0)
                3: (150 + nx, 0, 0),  # g - (3, 0)
            },
            (0, 2): {
                0: (149 - ny, 99, 2),  # d - (2, 1)
                1: (50 + nx, 99, 2),  # b - (1, 1)
                2: (self.y, self.x - 1, 2),  # Ok
                3: (199, nx, 3),  # e - (3, 0)
            },
            (1, 1): {
                0: (49, 100 + ny, 3),  # b - (0, 2)
                1: (self.y + 1, self.x, 1),  # Ok
                2: (100, ny, 1),  # a - (2, 0)
                3: (self.y - 1, self.x, 3),  # Ok
            },
            (2, 0): {
                0: (self.y, self.x + 1, 0),  # Ok
                1: (self.y + 1, self.x, 1),  # Ok
                2: (49 - ny, 50, 0),  # f - (0, 1)
                3: (50 + nx, 50, 0),  # a - (1, 1)
            },
            (2, 1): {
                0: (49 - ny, 149, 2),  # d - (0, 2)
                1: (150 + nx, 49, 2),  # c - (3, 0)
                2: (self.y, self.x - 1, 2),  # Ok
                3: (self.y - 1, self.x, 3),  # Ok
            },
            (3, 0): {
                0: (149, 50 + ny, 3),  # c - (2, 1)
                1: (0, 100 + nx, 1),  # e - (0, 2)
                2: (0, 50 + ny, 1),  # g - (0, 1)
                3: (self.y - 1, self.x, 3),  # Ok
            },
        }[(ry, rx)][self.facing]
        return yy, xx, facing

    def rotate(self, r):
        if r == "R":
            self.facing = (self.facing + 1) % 4
        elif r == "L":
            self.facing = (self.facing - 1) % 4
        else:
            assert False


# dir_4 = [(0, 1),(1, 0), (0, -1), (-1, 0)]
#         +-------+-------+
#         |   g   |   e   |
#         |f 0 1  |  0 2 d|
#         |       |   b   |
#         +-------+-------+
#         |       |
#         |a 1 1 b|
#         |       |
# +-------+-------+
# |   a   |       |
# |f 2 0  |  2 1 d|
# |       |   c   |
# +-------+-------+
# |       |
# |g 3 0 c|
# |   e   |
# +-------+


def part_2(data):
    def test(a):
        player.y, player.x, player.facing = a
        player.y, player.x, player.facing = player.wrap()
        player.rotate("R")
        player.y, player.x, player.facing = player.wrap()
        player.rotate("R")
        w, w1 = player.wrap()[0:2], a[0:2]
        assert w == w1

    kk = 0
    for i in range(len(data[0])):
        if data[0][i] not in (" ", "#"):
            kk = i
            break

    dirs = re.split("(\d+)", data[-1])
    dirs = [int(x) if x.isdigit() else x for x in dirs][1:-1]

    player = PlayerCube(0, kk, 0, data[:-2])

    test((49, 50, 1))
    test((49, 100, 1))
    test((99, 50, 1))
    test((149, 50, 1))
    test((199, 0, 1))
    test((149, 0, 1))

    player = PlayerCube(0, kk, 0, data[:-2])

    for mov in dirs:
        if isinstance(mov, int):
            player.move(mov)
        else:
            player.rotate(mov)

    col, row, facing = player.y + 1, player.x + 1, player.facing

    return col * 1000 + row * 4 + facing


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
