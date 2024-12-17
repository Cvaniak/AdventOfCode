import argparse
import bisect
import collections
import functools
import heapq
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
dir_4c = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
dir_8 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


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


@dataclasses.dataclass(frozen=True)
class P:
    y: int
    x: int
    
    def __add__(self, other):
        added = tuple(a + b for a, b in zip(self, other))
        return P(*added)

    def __mul__(self, scalar):
        return P(self.y * scalar, self.x * scalar)

    def __sub__(self, other):
        subbed = tuple(a - b for a, b in zip(self, other))
        return P(*subbed)

    def __iter__(self):
        return [self.y, self.x].__iter__()

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __hash__(self):
        return hash((self.y, self.x))

dir_4 = [P(-1, 0), P(0, 1), P(1, 0), P(0, -1)]


@dataclasses.dataclass
class Matrix:
    data: list[list[int]]
    n: int
    m: int
    start: P
    end: P

    def __init__(self, data) -> None:
        self.data = data
        self.n = len(data)
        self.m = len(data[0])

        for y, line in enumerate(data):
            for x, value in enumerate(line):
                if value == "S":
                    self.start = P(y, x)
                if value == "E":
                    self.end = P(y, x)

    def s_get(self, y, x, default=None):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return default
        return self.data[y][x]

    def s_get_p(self, p: P, default=None):
        return self.s_get(p.y, p.x, default)

    def s_set(self, y, x, value):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return
        self.data[y][x] = value

    def s_set_p(self, p, value):
        self.s_set(p.y, p.x, value)

    def solve(self):
        q = [(0, self.start, 1)]
        been = set()

        while q:
            points, pos, dir = heappop(q)
            if (pos, dir) in been:
                continue
            been.add((pos, dir))
            if pos == self.end:
                return points

            if self.s_get_p(pos + dir_4[dir], "!") in ".E":
                z = 1
                heappush(q, (points + z, pos + dir_4[dir]*z, dir))

            for d_dir in [-1, 1]:
                n_dir = (dir + d_dir) % 4
                if self.s_get_p(pos + dir_4[n_dir], "!") in ".E":
                    heappush(q, (points + 1001, pos + dir_4[n_dir], n_dir))

        return -1

# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 7036
    data = read_data("test2")
    assert part_1(data) == 11048
    data = read_data("test")
    assert part_2(data) == 45
    data = read_data("test2")
    assert part_2(data) == 64


def part_1(data):
    matrix = Matrix(data)
    res = matrix.solve()
    print(res)
    return res


def part_2(data): 
    ...


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
