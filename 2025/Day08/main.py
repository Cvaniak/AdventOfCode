import argparse
import bisect
import collections
import functools
import itertools
import math
import operator
from collections import Counter, defaultdict, deque, namedtuple
from heapq import heappop, heappush
from itertools import combinations, permutations, product
from math import lcm, sqrt
from typing import NamedTuple

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
dir_4c = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
dir_8 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


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


class Matrix:
    data: list[list[int]]
    n: int
    m: int

    def __init__(self, data) -> None:
        self.data = data
        self.n = len(data)
        self.m = len(data[0])

    def s_get(self, y, x, default=None):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return default
        return self.data[y][x]

    def s_set(self, y, x, value):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return
        self.data[y][x] = value


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 40
    assert part_2(data) == 25272


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Union:
    def __init__(self, data: list[Point]) -> None:
        self.parent = {k: k for k in data}
        self.nodes = {k: 1 for k in data}

    def find(self, point: Point):
        if self.parent[point] == point:
            return point
        return self.find(self.parent[point])

    def union(self, a: Point, b: Point):
        ap = self.find(a)
        bp = self.find(b)
        if ap != bp:
            self.parent[bp] = ap
            self.nodes[ap] += self.nodes[bp]
            del self.nodes[bp]
            return ap


def distance(a: Point, b: Point):
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def part_1(data, connections=10):
    points = [Point(*load_ints_seperated(x)) for x in data]
    union = Union(points)
    dist = []

    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            heappush(dist, (distance(points[i], points[j]), points[i], points[j]))
    for _ in range(connections):
        _, a, b = heappop(dist)
        union.union(a, b)
    biggest = sorted(union.nodes.values(), reverse=True)[:3]
    return prod(biggest)


def part_2(data):
    points = [Point(*load_ints_seperated(x)) for x in data]
    union = Union(points)
    dist = []

    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            heappush(dist, (distance(points[i], points[j]), points[i], points[j]))

    a, b = Point(0, 0, 0), Point(0, 0, 0)
    while len(union.nodes) != 1:
        _, a, b = heappop(dist)
        union.union(a, b)

    return a.x * b.x


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:], 1000))
    print(part_2(data[:]))
