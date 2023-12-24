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
    assert part_1(data[:]) == 94
    assert part_2(data[:]) == 154


def part_1(data):
    n, m = len(data), len(data[0])
    start = (1, data[0].find("."))
    end = (len(data) - 2, data[-1].find("."))
    data[0] = data[0].replace(".", "#")
    data[-1] = data[-1].replace(".", "#")
    dbg(start, end)

    nodes = set([start, end])
    for x in range(1, n - 1):
        for y in range(1, m - 1):
            ln = sum([data[y + dy][x + dx] in "<>^v" for dy, dx in dir_4])
            if data[y][x] == "." and ln > 1:
                nodes.add((y, x))

    graph = defaultdict(list)
    g = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    for node in nodes:
        if node == end:
            continue

        q = [(node, 0, (0, 0))]
        while q:
            (y, x), step, prev = q.pop()
            if (y, x) != node and (y, x) in nodes:
                graph[node].append(((y, x), step))
                continue
            for dy, dx in dir_4:
                if (-dy, -dx) == prev:
                    continue
                yy, xx = y + dy, x + dx
                if data[yy][xx] == ".":
                    q.append(((yy, xx), step + 1, (dy, dx)))
                elif data[yy][xx] != "#":
                    if g[data[yy][xx]] == (dy, dx):
                        q.append(((yy, xx), step + 1, (dy, dx)))
    dbg(graph)
    q = [(start, 1)]
    mx = 1
    while q:
        node, step = q.pop()
        if node == end:
            mx = max(mx, step)
            continue
        for nxt, nxt_step in graph[node]:
            q.append((nxt, step + nxt_step))

    dbg(mx)
    return mx + 1


def part_2(data):
    n, m = len(data), len(data[0])
    start = (1, data[0].find("."))
    end = (len(data) - 2, data[-1].find("."))
    data[0] = data[0].replace(".", "#")
    data[-1] = data[-1].replace(".", "#")
    dbg(start, end)

    nodes = set([start, end])
    for x in range(1, n - 1):
        for y in range(1, m - 1):
            ln = sum([data[y + dy][x + dx] in "<>^v" for dy, dx in dir_4])
            if data[y][x] == "." and ln > 1:
                nodes.add((y, x))

    graph = defaultdict(list)
    g = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    for node in nodes:
        if node == end:
            continue

        q = [(node, 0, (0, 0))]
        while q:
            (y, x), step, prev = q.pop()
            if (y, x) != node and (y, x) in nodes:
                graph[node].append(((y, x), step))
                continue
            for dy, dx in dir_4:
                if (-dy, -dx) == prev:
                    continue
                yy, xx = y + dy, x + dx
                if data[yy][xx] != "#":
                    q.append(((yy, xx), step + 1, (dy, dx)))
    dbg(graph)
    q = [(start, 1, frozenset())]
    mx = 1
    while q:
        node, step, been = q.pop()
        if node in been:
            continue
        if node == end:
            if step >= mx:
                mx = max(mx, step)
                dbg(mx + 1)
            continue
        for nxt, nxt_step in graph[node]:
            q.append((nxt, step + nxt_step, been | {node}))

    dbg(mx)
    return mx + 1


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
