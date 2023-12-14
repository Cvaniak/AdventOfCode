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
    assert part_1(data) == 136
    assert part_2(data) == 64


def part_1(data):
    n, m = len(data), len(data[0])

    load = 0
    for x in range(m):
        last_square = 0
        for y in range(n):
            if data[y][x] == "#":
                last_square = y+1
            elif data[y][x] == "O":
                load += n-last_square
                last_square += 1
        #     dbg.x(load)
        # dbg.y()
    dbg(load)
    return load

def calc(data, m, n):
    res = []
    for x in range(m):
        line = 0
        for y in range(n):
            if data[y][x] == "O":
                line += n-y
        res.append(line)
    return tuple(res), sum(res)
                
    # return sum([n-idx for idx, y in enumerate(data)  for x in y if x == "O"])

def part_2(data):
    g = 1_000_000_000
    # g = 30
    ...
    n, m = len(data), len(data[0])
    for y in range(n):
        data[y] = list(data[y])

    def foo(y, x, last_square_y, last_square_x):
        if data[y][x] == "#":
            return (y, x)
        elif data[y][x] == "O":
            data[y][x] = "."
            data[last_square_y][last_square_x] = "O"
            return True
        return False

    been = dict()
    step = 0
    b = False
    while step < g:
        step += 1
        for x in range(m):
            last_square = 0
            for y in range(n):
                f = foo(y, x, last_square, x)
                if f is True:
                    last_square += 1
                elif f is not False:
                    last_square = f[0]+1
        for y in range(n):
            last_square = 0
            for x in range(m):
                f = foo(y, x, y, last_square)
                if f is True:
                    last_square += 1
                elif f is not False:
                    last_square = f[1]+1
        for x in range(m):
            last_square = n-1
            for y in range(n-1, -1, -1):
                f = foo(y, x, last_square, x)
                if f is True:
                    last_square -= 1
                elif f is not False:
                    last_square = f[0]-1
        for y in range(n):
            last_square = m-1
            for x in range(m-1, -1, -1):
                f = foo(y, x, y, last_square)
                if f is True:
                    last_square -= 1
                elif f is not False:
                    last_square = f[1]-1
        hash, value = calc(data, m, n)
        if not b and hash in been:
            b = True
            s = (g-step)//(step-been[hash])
            step = step+s*(step-been[hash])

        been[hash] = step
    return calc(data, m, n)[1]


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
