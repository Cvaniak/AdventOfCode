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
    assert part_1(data) == 4
    data = read_data("test_2")
    assert part_1(data) == 8
    data = read_data("test_4")
    assert part_2(data) == 4
    data = read_data("test_5")
    assert part_2(data) == 8
    data = read_data("test_3")
    assert part_2(data, (1, 0)) == 10


d = {
    "|": ((1, 0), (-1, 0)),
    "-": ((0, 1), (0, -1)),
    "L": ((-1, 0), (0, 1)),
    "J": ((-1, 0), (0, -1)),
    "7": ((1, 0), (0, -1)),
    "F": ((1, 0), (0, 1)),
}


def part_1(data):
    n, m = len(data), len(data[0])
    start_idx = -1
    start = (-1, -1)
    for idx, line in enumerate(data):
        start_idx = line.find("S")
        if start_idx != -1:
            start = (idx, start_idx)
            break
    assert start != (-1, -1)

    sy, sx = start
    first = (0, 0)
    for dy, dx in dir_4:
        val = data[sy + dy][sx + dx]
        if val in ".":
            continue
        for yy, xx in d[val]:
            if (dy + yy, dx + xx) == (0, 0):
                first = (sy + dy, sx + dx)

    assert first != (0, 0)
    dbg(start, first)

    q = [(first, start, 0)]
    been = set([start])

    step = 0
    while q:
        node, prev, step = q.pop()
        if node in been:
            break
        been.add(node)
        y, x = node
        for yy, xx in d[data[y][x]]:
            if (y + yy, x + xx) == prev:
                continue
            q.append(((y + yy, x + xx), node, step + 1))

    return (step + 1) // 2


def part_2(data, first=(0, 1)):
    n, m = len(data), len(data[0])
    start_idx = -1
    start = (-1, -1)
    for idx, line in enumerate(data):
        start_idx = line.find("S")
        if start_idx != -1:
            start = (idx, start_idx)
            break
    assert start != (-1, -1)

    sy, sx = start
    first = (0, 0)
    for dy, dx in dir_4:
        val = data[sy + dy][sx + dx]
        if val in ".":
            continue
        for yy, xx in d[val]:
            if (dy + yy, dx + xx) == (0, 0):
                first = (sy + dy, sx + dx)

    assert first != (0, 0)

    dbg(n, m, start)
    q = [(first, start, 0)]
    been = set([start])
    dbg(q)

    step = 0
    mnx = m
    mny = n
    mxx = 0
    mxy = 0
    while q:
        node, prev, step = q.pop()
        if node in been:
            break
        been.add(node)

        y, x = node
        mnx = min(mnx, x)
        mny = min(mny, y)
        mxx = max(mxx, x)
        mxy = max(mxy, y)
        for yy, xx in d[data[y][x]]:
            if (y + yy, x + xx) == prev:
                continue
            q.append(((y + yy, x + xx), node, step + 1))

    dbg(mnx, mny, mxx, mxy)
    dbg(len(been))

    ans = 0
    for yy in range(mny - 1, mxy + 2):
        count = 0
        last = ""
        for xx in range(mnx - 1, mxx + 2):
            if (yy, xx) in been:
                g = data[yy][xx]
                if g == "|":
                    count = 1 - count
                elif g in "LF":
                    last = g
                elif g == "J":
                    if last == "F":
                        count = 1 - count
                    last = ""
                elif g == "7":
                    if last == "L":
                        count = 1 - count
                    last = ""
            else:
                if count:
                    dbg.w(yy, xx)
                    ans += 1

    dbg(ans)
    return ans


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
