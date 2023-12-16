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
    assert part_1(data) == 46
    assert part_2(data) == 51


def foo(data, start):
    n, m = len(data), len(data[0])

    q = [start]
    been = set()
    beenn = set()
    while q:
        vec, pos = q.pop()
        if (vec, pos) in been:
            continue
        been.add((vec, pos))
        beenn.add(pos)

        yy, xx = vec[0] + pos[0], vec[1] + pos[1]
        if yy < 0 or yy >= n or xx < 0 or xx >= m:
            continue
        w = data[yy][xx]
        if w == "-":
            if vec[0] != 0:
                q.append(((0, -1), (yy, xx)))
                q.append(((0, 1), (yy, xx)))
            else:
                q.append((vec, (yy, xx)))
        if w == "|":
            if vec[1] != 0:
                q.append(((-1, 0), (yy, xx)))
                q.append(((1, 0), (yy, xx)))
            else:
                q.append((vec, (yy, xx)))
        if w == "\\":
            # (0, 1) -> (1, 0)
            # (1, 0) -> (0, 1)
            # (0, -1) -> (-1, 0)
            # (-1, 0) -> (0, -1)
            q.append(((vec[1], vec[0]), (yy, xx)))

        if w == "/":
            # (0, 1) -> (-1, 0)
            # (-1, 0) -> (0, 1)
            q.append(((-vec[1], -vec[0]), (yy, xx)))
        if w == ".":
            q.append((vec, (yy, xx)))
    return len(beenn) - 1


def part_1(data):
    start = ((0, 1), (0, -1))
    return foo(data, start)


def part_2(data):
    n, m = len(data), len(data[0])
    mx = 0
    # vec, pos
    for i in range(n):
        mx = max(mx, foo(data, ((0, 1), (i, -1))))
        mx = max(mx, foo(data, ((0, -1), (i, n))))

    for i in range(m):
        mx = max(mx, foo(data, ((1, 0), (-1, i))))
        mx = max(mx, foo(data, ((-1, 0), (m, i))))

    return mx


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
