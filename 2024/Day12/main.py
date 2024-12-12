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


class Matrix:
    data: list[list[int]]
    y: int
    x: int

    def __init__(self, data) -> None:
        self.data = data
        self.n = len(data)
        self.m = len(data[0])

    def get_safely(self, y, x, default=None):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return default
        return self.data[y][x]

    def set_safely(self, y, x, value):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return
        self.data[y][x] = value

    def expand(self, sy, sx):
        base = self.get_safely(sy, sx)
        res = 0
        q = [(sy, sx)]
        been = set([])
        while q:
            y, x = q.pop()
            if (y, x) in been:
                continue
            been.add((y, x))
            for dy, dx in dir_4:
                yy, xx = y + dy, x + dx
                if self.get_safely(yy, xx) != base:
                    res += 1
                elif (yy, xx) not in been:
                    q.append((yy, xx))

        for yy, xx in been:
            self.set_safely(yy, xx, "#")

        return res * len(been)

    def count_sides(self, sy, sx):
        base = self.get_safely(sy, sx)
        q = [(sy, sx)]
        been = set([])
        sides = defaultdict(list)
        while q:
            y, x = q.pop()
            if (y, x) in been:
                continue
            been.add((y, x))
            for idx, (dy, dx) in enumerate(dir_4):
                yy, xx = y + dy, x + dx
                if self.get_safely(yy, xx) != base:
                    sides[(idx, y * abs(dy) + x * abs(dx))].append(x * abs(dy) + y * abs(dx))
                elif (yy, xx) not in been:
                    q.append((yy, xx))
        res = 0
        for positions in sides.values():
            positions.sort()
            curr = positions[0]
            res += 1
            for pos in positions[1:]:
                if (curr + 1) != pos:
                    res += 1
                curr = pos

        for yy, xx in been:
            self.set_safely(yy, xx, "#")

        return res * len(been)


def part_test():
    data = read_data("test")
    assert part_1(data[:]) == 1930
    data = read_data("test2")
    assert part_2(data[:]) == 236
    data = read_data("test1")
    assert part_2(data[:]) == 368
    data = read_data("test")
    assert part_2(data[:]) == 1206


def part_1(data):
    for y in range(len(data)):
        data[y] = list(data[y])

    res = 0
    matrix = Matrix(data)
    for y, line in enumerate(matrix.data):
        for x, value in enumerate(line):
            if matrix.get_safely(y, x, "#") == "#":
                continue
            res += matrix.expand(y, x)

    return res


def part_2(data):
    for y in range(len(data)):
        data[y] = list(data[y])

    res = 0
    matrix = Matrix(data)
    for y, line in enumerate(matrix.data):
        for x, value in enumerate(line):
            if matrix.get_safely(y, x, "#") == "#":
                continue
            res += matrix.count_sides(y, x)

    return res


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
