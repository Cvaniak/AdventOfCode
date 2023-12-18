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

lurd = {"R": (1, 0), "D": (0, -1), "L": (-1, 0), "U": (0, 1)}
rdlu = {"0": (1, 0), "1": (0, -1), "2": (-1, 0), "3": (0, 1)}
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
    assert part_1(data) == 62
    assert part_2(data) == 952408144115


def part_1(data):
    y, x = 0, 0
    been = set([(0, 0)])
    mnx, mxx = 0, 0
    mny, mxy = 0, 0
    for line in data:
        d, num, _ = line.split(" ")
        vec = lurd[d]
        for i in range(1, int(num) + 1):
            y, x = (y + vec[0], x + vec[1])
            mnx, mxx = min(mnx, x), max(mxx, x)
            mny, mxy = min(mny, y), max(mxy, y)
            been.add((y, x))
    start = (mny, mnx)
    while start not in been:
        start = (start[0] + 1, start[1] + 1)
    start = (start[0] + 1, start[1] + 1)
    h = [start]

    infil = set()
    while h:
        pos = h.pop()
        if pos in infil or pos in been:
            continue
        infil.add(pos)
        for yy, xx in dir_4:
            h.append((pos[0] + yy, pos[1] + xx))
    return len(been) + len(infil)


def part_2(data):
    y, x = 0, 0
    points = []
    param = 0
    for line in data:
        _, _, color = line.split(" ")
        vec, num = rdlu[color[-2]], int(color[2:-2], 16)
        y, x = y + vec[0] * num, x + vec[1] * num
        points.append((y, x))
        param += num

    n = len(points)
    s1, s2 = 0, 0
    for i in range(n):
        p1, p2 = points[i], points[(i + 1) % n]
        s1 += p1[0] * p2[1]
        s2 += p1[1] * p2[0]
    w = abs(s1 - s2) // 2 + param // 2 + 1
    return w


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
