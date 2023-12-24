import argparse
import bisect
import collections
import functools
import itertools
import math
import operator
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
dir_4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
dir_8 = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]


def prod(factors):
    return functools.reduce(operator.mul, factors, 1)


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def load_int_lines(data):
    data = data[:]
    for idx, i in enumerate(data):
        data[idx] = [int(x) for x in i]
    return data


def load_ints_seperated(data, sep=","):
    return list(map(int, data.split(sep)))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 5
    assert part_2(data) == 7


def part_1(data):
    bricks = []
    for idx, line in enumerate(data):
        a, b = line.split("~")
        x1, y1, z1 = load_ints_seperated(a)
        x2, y2, z2 = load_ints_seperated(b)
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        if z2 < z1:
            z1, z2 = z2, z1
        bisect.insort(bricks, [[x1, y1, z1], [x2, y2, z2]], key=lambda x: x[0][2])

    def foo(skip=-1, should_fall=False):
        ...
        falling_bricks = 0
        h = defaultdict(int)
        for idx, brick in enumerate(bricks):
            if idx == skip:
                continue
            (x1, y1, z1), (x2, y2, z2) = brick
            xy = set()
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    xy.add((x, y))
            mx_h = max([h[a] for a in xy])
            diff = z1 - mx_h - 1
            if diff:
                falling_bricks += 1
                if should_fall:
                    brick[0][2] -= diff
                    brick[1][2] -= diff

            for a in xy:
                h[a] = brick[1][2]
        return falling_bricks

    foo(should_fall=True)
    w = [1 if foo(skip=brick) == 0 else 0 for brick in range(len(bricks))]
    dbg(sum(w))
    return sum(w)


def part_2(data):
    bricks = []
    for idx, line in enumerate(data):
        a, b = line.split("~")
        x1, y1, z1 = load_ints_seperated(a)
        x2, y2, z2 = load_ints_seperated(b)
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        if z2 < z1:
            z1, z2 = z2, z1
        bisect.insort(bricks, [[x1, y1, z1], [x2, y2, z2]], key=lambda x: x[0][2])

    def foo(skip=-1, should_fall=False):
        falling_bricks = 0
        h = defaultdict(int)
        for idx, brick in enumerate(bricks):
            if idx == skip:
                continue
            (x1, y1, z1), (x2, y2, z2) = brick
            xy = set()
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    xy.add((x, y))
            mx_h = max([h[a] for a in xy])
            diff = z1 - mx_h - 1
            if diff:
                falling_bricks += 1
                z2 -= diff
                if should_fall:
                    brick[0][2] -= diff
                    brick[1][2] -= diff

            for a in xy:
                h[a] = z2
        return falling_bricks

    foo(should_fall=True)
    w = [foo(skip=brick) for brick in range(len(bricks))]
    dbg(sum(w))
    return sum(w)


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
