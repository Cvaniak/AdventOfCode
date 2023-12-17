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
    assert part_1(data) == 102
    assert part_2(data) == 94
    data = read_data("test_2")
    assert part_2(data) == 71


dr = {1: (1, 0), 2: (0, -1), 3: (-1, 0), 0: (0, 1)}


def part_1(data):
    data = load_int_lines(data)
    n, m = len(data), len(data[0])
    been = set()
    h = [(0, 0, 0, 0, 0), (0, 0, 0, 1, 0)]
    ...
    while h:
        score, y, x, vec, con = heappop(h)
        if (y, x, vec, con) in been:
            continue
        been.add((y, x, vec, con))

        if (y, x) == (n - 1, m - 1):
            dbg(score)
            return score

        if con < 3:
            yy, xx = dr[vec][0] + y, dr[vec][1] + x
            if not (yy < 0 or yy >= n or xx < 0 or xx >= m):
                heappush(h, (data[yy][xx] + score, yy, xx, vec, con + 1))

        t_vec = (vec + 3) % 4
        yy, xx = dr[t_vec][0] + y, dr[t_vec][1] + x
        if not (yy < 0 or yy >= n or xx < 0 or xx >= m):
            heappush(h, (data[yy][xx] + score, yy, xx, t_vec, 1))

        t_vec = (vec + 5) % 4
        yy, xx = dr[t_vec][0] + y, dr[t_vec][1] + x
        if not (yy < 0 or yy >= n or xx < 0 or xx >= m):
            heappush(h, (data[yy][xx] + score, yy, xx, t_vec, 1))
    dbg(-1)
    return -1


def part_2(data):
    data = load_int_lines(data)
    n, m = len(data), len(data[0])
    been = set()
    h = [(0, 0, 0, 0, 0), (0, 0, 0, 1, 0)]
    ...
    while h:
        score, y, x, vec, con = heappop(h)
        if (y, x, vec, con) in been:
            continue
        been.add((y, x, vec, con))

        if (y, x) == (n - 1, m - 1) and con >= 4:
            dbg(score)
            return score

        if con < 10:
            yy, xx = dr[vec][0] + y, dr[vec][1] + x
            if not (yy < 0 or yy >= n or xx < 0 or xx >= m):
                heappush(h, (data[yy][xx] + score, yy, xx, vec, con + 1))

        if con <= 3:
            continue

        t_vec = (vec + 3) % 4
        yy, xx = dr[t_vec][0] + y, dr[t_vec][1] + x
        if not (yy < 0 or yy >= n or xx < 0 or xx >= m):
            heappush(h, (data[yy][xx] + score, yy, xx, t_vec, 1))

        t_vec = (vec + 5) % 4
        yy, xx = dr[t_vec][0] + y, dr[t_vec][1] + x
        if not (yy < 0 or yy >= n or xx < 0 or xx >= m):
            heappush(h, (data[yy][xx] + score, yy, xx, t_vec, 1))
    dbg(-1)
    return -1


# 1133 and 1152 and 1153

if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
