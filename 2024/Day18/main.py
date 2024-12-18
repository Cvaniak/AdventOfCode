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

    def __init__(self, data, size, kbs) -> None:
        self.n = size.y
        self.m = size.x
        self.data = [["."]*self.m for _ in range(self.n)]
        self.raw_data = data
        self.kbs = kbs

        for (x, y) in self.raw_data[:kbs]:
            self.data[y][x] = "#"
        self.backup = [x[:] for x in self.data]
        
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

# ===== ^^ PART OF TEMPLATE ^^ =====

    def solve(self):
        self.start = P(0, 0)
        self.end = P(self.n-1, self.m-1)
        
        q = [(self.start)]
        step = 0
        been = set()
        while q:
            nq = []
            for  point in q:
                for d_point in dir_4:
                    n_point = point + d_point
                    if n_point == self.end:
                        return step+1
                    if n_point in been:
                        continue
                    if self.s_get_p(n_point, "!") == ".":
                        nq.append((n_point))
                        been.add(n_point)
            q = nq
            step += 1
        return -1

    def prepare(self, m):
        self.data = [x[:] for x in self.backup]

        for (x, y) in self.raw_data[self.kbs:self.kbs+m]:
            self.data[y][x] = "#"

    def solve_2(self):
        self.start = P(0, 0)
        self.end = P(self.n-1, self.m-1)

        l = 0
        r = len(self.raw_data) - self.kbs-1
        
        while l <= r:
            m = (l+r)//2
            self.prepare(m)
            if self.solve() != -1:
                l = m+1
            else:
                r = m-1
        x, y =  self.raw_data[self.kbs+r]
        return P(y, x)


def part_test():
    data = read_data("test")
    assert part_1(data, P(7,7),12) == 22
    assert part_2(data, P(7,7),12) == "6,1"


def part_1(data, size, kbs):
    data = [load_ints_seperated(x) for x in data]
    m = Matrix(data, size, kbs)
    
    res = m.solve()
    return res


def part_2(data, size, kbs):
    data = [load_ints_seperated(x) for x in data]
    m = Matrix(data, size, kbs)
    
    res = m.solve_2()
    return f"{res.x},{res.y}"


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:], P(71,71), 1024))
    print(part_2(data[:], P(71,71), 1024))