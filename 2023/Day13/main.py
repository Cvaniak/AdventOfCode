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
    assert part_1(data) == 405
    assert part_2(data) == 400


def part_1(data):
    def foo(fields):
        def process(fields):
            set_field = [
                {idx for idx, x in enumerate(line) if x == "#"} for line in fields
            ]
            n = len(set_field)
            for i in range(1, n):
                for j in range(min(i, n - i)):
                    if set_field[i - j - 1] != set_field[i + j]:
                        break
                else:
                    return i
            return 0

        return 100 * process(fields) or process(list(zip(*fields)))

    field = []
    ans = 0
    for line in data:
        if len(line) == 0:
            ans += foo(field)
            field = []
            continue
        field.append(line)
    ans += foo(field)

    return ans


def part_2(data):
    def foo(fields):
        def process(fields):
            set_field = [
                {idx for idx, x in enumerate(line) if x == "#"} for line in fields
            ]
            n = len(set_field)
            for i in range(1, n):
                count = 0
                for j in range(min(i, n - i)):
                    inter = len(
                        set_field[i - j - 1].symmetric_difference(set_field[i + j])
                    )
                    if inter <= 1:
                        count += inter
                    else:
                        break
                    if count > 1:
                        break
                else:
                    if count == 1:
                        return i
            return 0

        return 100 * process(fields) or process(list(zip(*fields)))

    field = []
    ans = 0
    for line in data:
        if len(line) == 0:
            ans += foo(field)
            field = []
            continue
        field.append(line)
    ans += foo(field)

    return ans


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
