import argparse
import bisect
import collections
import functools
import itertools
import math
import operator
import dataclasses
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from itertools import combinations, permutations, product
from math import lcm

import parse
from rich import print
import inspect

debug_space = False


class Debuger:
    levels: set[str] = set()
    excluded_parts: set[str] = set()
    state: bool = True

    def _print(self, *args, lvl="", **kwargs):
        if not self.state:
            return

        if self.levels and lvl not in self.levels:
            return

        c1, c2 = inspect.stack()[1].function, inspect.stack()[2].function
        if c1 in self.excluded_parts or c2 in self.excluded_parts:
            return

        print(f" ▄▄▄▄▄ {lvl} ▄▄▄▄▄ ")
        print("  ", end="")
        print(*args, **kwargs)

    def __getattr__(self, lvl):
        return functools.partial(self._print, lvl=lvl)

    def __call__(self, *args, **kwargs):
        self._print(lvl="0", *args, **kwargs)

    def set_levels(self, lvls):
        if not lvls:
            return
        for lvl in lvls.split(","):
            self.levels.add(lvl)

    def exclude_parts(self, parts):
        for part in parts:
            self.excluded_parts.add(f"part_{part}")

    def turn_on_off(self, state):
        self.state = state


dbg = Debuger()


def set_debuger():
    global dbg
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", nargs="?", default=None, help="Debug List")
    parser.add_argument(
        "-n", "--nodebug", action="store_false", help="Remove default debug"
    )
    parser.add_argument(
        "-p",
        "--excludepart",
        nargs="?",
        default="",
    )
    args = parser.parse_args()
    dbg.set_levels(args.debug)
    dbg.turn_on_off(args.nodebug)
    dbg.exclude_parts(args.excludepart)


# ===== ^^ DEBUGER ^^ =====

wsen = {"E": (1, 0), "S": (0, -1), "W": (-1, 0), "N": (0, 1)}
dir_4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
dir_4c = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
dir_8 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


def prod(factors):
    return functools.reduce(operator.mul, factors, 1)


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().split("\n\n")
        return data


def load_int_lines(data):
    data = data[:]
    for idx, i in enumerate(data):
        data[idx] = [int(x) for x in i]
    return data


def load_ints_seperated(data, sep=","):
    return list(map(int, data.split(sep)))


def parser(data):
    pattern = "Button A: X+{ax:d}, Y+{ay:d}\nButton B: X+{bx:d}, Y+{by:d}\nPrize: X={prize_x:d}, Y={prize_y:d}"
    match = parse.search(pattern, data)
    return match.named


class Matrix:
    data: list[list[int]]
    n: int
    m: int

    def __init__(self, data) -> None:
        self.data = data
        self.n = len(data)
        self.m = len(data[0])

    def s_get(self, y, x, default=None):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return default
        return self.data[y][x]

    def s_set(self, y, x, value):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return
        self.data[y][x] = value


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 480


@dataclasses.dataclass
class P:
    x: int
    y: int


@dataclasses.dataclass
class Foo:
    a: P
    b: P
    prize: P

    def __init__(self, d, add=0) -> None:
        self.a = P(d["ax"], d["ay"])
        self.b = P(d["bx"], d["by"])
        self.prize = P(d["prize_x"] + add, d["prize_y"] + add)


def solve(f: Foo) -> int:
    py, px = f.prize.y, f.prize.x
    xa, ya = f.a.x, f.a.y
    xb, yb = f.b.x, f.b.y

    b = (py * xa - ya * px) / (yb * xa - xb * ya)
    a = (px - b * xb) / xa

    if b != int(b) or a != int(a) or b > 100 or a > 100:
        return 0

    return int(a * 3 + b)


def part_1(data):
    values = [Foo(parser(line)) for line in data]
    res = 0

    for value in values:
        res += solve(value)

    return res


def solve_2(f: Foo) -> int:
    py, px = f.prize.y, f.prize.x
    xa, ya = f.a.x, f.a.y
    xb, yb = f.b.x, f.b.y

    b = (py * xa - ya * px) / (yb * xa - xb * ya)
    a = (px - b * xb) / xa

    if b != int(b) or a != int(a):
        return 0

    return int(a * 3 + b)


def part_2(data):
    N = 10000000000000
    values = [Foo(parser(line), N) for line in data]
    res = 0

    for value in values:
        res += solve_2(value)

    return res


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
