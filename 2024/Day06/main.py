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
dir_4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
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
    assert part_1(data) == 41
    assert part_2(data) == 6

def part_1_bck(data):
    n, m = len(data), len(data[0])
    map_horizontal = [[] for _ in range(n)]
    map_vertical = [[] for _ in range(m)]
    sy, sx = -1, -1
    for idy, line in enumerate(data):
        for idx, value in enumerate(line):
            if value == "^":
                sy, sx = idy, idx
                continue
            if value != "#":
                continue
            map_horizontal[idy].append(idx)
            map_vertical[idx].append(idy)
    direction = 0
    y, x = sy, sx
    for _ in range(10000):
        if direction == 0:
            nx = x

def print_grid(n, m, been, mp):
    for i in range(-1, n + 1):
        for j in range(-1, m+1):
            if (i, j) in mp:
                print("#", end="")
            elif (i, j) in been:
                print("o", end="")
            else:
                print(".", end="")
        print()
    print()

def solve(mp, sy, sx, n, m):
    direction = 0
    y, x = sy, sx
    been = {(y, x)}
    for _ in range(1000000):
        dy, dx = dir_4[direction%4]
        yy, xx = y+dy, x+dx
        if 0 > yy or yy >= n or 0 > xx or xx >= m: 
            break
        if (yy, xx) in mp:
            direction = (direction+1)%4
            continue
        been.add((yy, xx))
        y, x = yy, xx
    return len(been)

def part_1(data):
    n, m = len(data), len(data[0])
    mp = set()
    sy, sx = -1, -1
    for idy, line in enumerate(data):
        for idx, value in enumerate(line):
            if value == "^":
                sy, sx = idy, idx
                continue
            if value != "#":
                continue
            mp.add((idy, idx))

    res = solve(mp, sy, sx, n, m)
    # print_grid(n, m, been, mp)
    return res



def pos_generator(mp, n, m, sy, sx):
    direction = 0
    y, x = sy, sx
    been = {(y, x, direction)}
    for _ in range(1000000):
        dy, dx = dir_4[direction%4]
        yy, xx = y+dy, x+dx
        if 0 > yy or yy >= n or 0 > xx or xx >= m: 
            break
        if (yy, xx) in mp:
            direction = (direction+1)%4
            continue
        been.add((yy, xx, direction))
        y, x = yy, xx
        yield (y, x), been

def solve_2(mp, sy, sx, n, m, been):
    direction = 0
    y, x = sy, sx
    been = {(y, x, direction)}
    for _ in range(1000000):
        dy, dx = dir_4[direction%4]
        yy, xx = y+dy, x+dx
        if 0 > yy or yy >= n or 0 > xx or xx >= m: 
            break
        if (yy, xx) in mp:
            direction = (direction+1)%4
            continue
        if (yy, xx, direction) in been:
            return 1
        been.add((yy, xx, direction))
        y, x = yy, xx
    return 0


def part_2(data):
    n, m = len(data), len(data[0])
    mp = set()
    sy, sx = -1, -1
    for idy, line in enumerate(data):
        for idx, value in enumerate(line):
            if value == "^":
                sy, sx = idy, idx
                continue
            if value != "#":
                continue
            mp.add((idy, idx))

    res = 0
    been_tested = set()
    for (y, x), been in pos_generator(mp, n, m, sy, sx):
        if (y, x) in been_tested:
            continue
        been_tested.add((y, x))
        mp.add((y, x))
        if solve_2(mp, sy, sx, n, m, been.copy()):
            res += 1
        mp.discard((y, x))
    print(res)
    return res



if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
