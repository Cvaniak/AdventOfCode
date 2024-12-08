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
    assert part_1(data) == 14
    assert part_2(data) == 34


def foo(pa, pb):
    vector = pa - pb
    return {pb-vector, pa+vector}

def bounds(n, m, w: complex):
    yy, xx = w.real, w.imag
    if 0 > yy or yy >= n or 0 > xx or xx >= m: 
        return False
    return True

def part_1(data):
    mp = defaultdict(list)
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            if value == ".":
                continue
            mp[value].append(complex(y, x))

    n, m = len(data), len(data[0])
    been = set()
    for letter in mp.keys():
        for pa, pb in combinations(mp[letter], 2):
            w = foo(pa, pb)
            for nw in w:
                if not bounds(n, m, nw):
                    continue
                been.add(nw)
            

    print(been, len(been))
    return len(been)


def bar(pa, pb, n, m):
    res = set()
    vector = pa - pb
    for i in range(1, max(n, m)):
        nxt = pb-vector*i
        if not bounds(n, m, nxt):
            break
        res.add(nxt)

    for i in range(1, max(n, m)):
        nxt = pa+vector*i
        if not bounds(n, m, nxt):
            break
        res.add(nxt)

    return res


def part_2(data):
    mp = defaultdict(list)
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            if value == ".":
                continue
            mp[value].append(complex(y, x))

    been = set()
    n, m = len(data), len(data[0])
    for letter in mp.keys():
        for pa, pb in combinations(mp[letter], 2):
            w = bar(pa, pb, n, m)
            been.update(w)
            been.add(pa)
            been.add(pb)

    print(been, len(been))
    return len(been)


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
