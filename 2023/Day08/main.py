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


def load_int_lines(datat):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = [x for x in i]
    return data


def load_ints_seperated(datat, sep=","):
    return list(map(int, datat[0].split(sep)))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 2
    data = read_data("test_2")
    assert part_1(data) == 6
    data = read_data("test_3")
    assert part_2(data) == 6


def part_1(data):
    lr = data[0]
    lr = [ int(x) for x in lr.replace("L",  "0").replace("R", "1")]
    dbg(lr)

    graph = dict()
    for line in data[2:]:
        start, _, to = line.partition(" = ")
        l, _,r = to[1:-1].partition(", ")
        graph[start] = (l, r)
    dbg(graph)

    start = "AAA"
    steps = 0
    n = len(lr)
    while start != "ZZZ":
        l_r = lr[steps%n]
        start = graph[start][l_r]
        steps += 1

    dbg(steps)
    return steps


def part_2(data):
    lr = data[0]
    lr = [ int(x) for x in lr.replace("L",  "0").replace("R", "1")]
    dbg(lr)

    starting = set()
    ending = set()
    graph = dict()
    for line in data[2:]:
        start, _, to = line.partition(" = ")
        l, _,r = to[1:-1].partition(", ")
        graph[start] = (l, r)
        if start[2] == "A":
            starting.add(start)
        elif start[2] == "Z":
            ending.add(start)
    # dbg(graph)
    dbg(ending)

    steps = 0
    n = len(lr)
    while True:
        # dbg(starting)

        l_r = lr[steps%n]
        new_starting = set()
        for node in starting:
            start = graph[node][l_r]
            new_starting.add(start)
        steps += 1

        if new_starting.issubset(ending):
            break

        starting = new_starting


    dbg(steps)
    return steps



if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
