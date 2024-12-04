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
    assert part_1(data) == 161
    data = read_data("test1")
    assert part_2(data) == 48


def part_1(data: list[str]):
    def check(data, idx):
        w = idx
        if len(data) < idx + 5 or data[idx:idx+4] != "mul(":
            return 0
        idx += 4
        a = 0
        if not data[idx].isnumeric():
            return 0

        while data[idx].isnumeric():
            a = a*10 + int(data[idx])
            idx += 1

        if not data[idx] == ",":
            return 0
        idx += 1

        b = 0
        if not data[idx].isnumeric():
            return 0

        while data[idx].isnumeric():
            b = b*10 + int(data[idx])
            idx += 1
        
        if not data[idx] == ")":
            return 0
        ww = idx
        print(data[w:ww])


        return a*b        
        
    res = 0

    for line in data:
        for idx, x in enumerate(line):
            if x != "m":
                continue

            if z := check(line, idx):
                res += z
    print(res)
    return res
            



def part_2(data):
    def check(data, idx):
        w = idx
        if len(data) < idx + 5 or data[idx:idx+4] != "mul(":
            return 0
        idx += 4
        a = 0
        if not data[idx].isnumeric():
            return 0

        while data[idx].isnumeric():
            a = a*10 + int(data[idx])
            idx += 1

        if not data[idx] == ",":
            return 0
        idx += 1

        b = 0
        if not data[idx].isnumeric():
            return 0

        while data[idx].isnumeric():
            b = b*10 + int(data[idx])
            idx += 1
        
        if not data[idx] == ")":
            return 0
        ww = idx


        return a*b        
        
    res = 0

    dd = True
    for line in data:
        line= line.replace("#", ".").replace("$", ".").replace("don't()", "#").replace("do()", "$")
        for idx, x in enumerate(line):
            if x == "#":
                dd = False
            if x == "$":
                dd = True
            if not dd:
                continue
            if x != "m":
                continue
            if z := check(line, idx):
                res += z

    return res


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
