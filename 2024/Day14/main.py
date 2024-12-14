import argparse
import bisect
import collections
import functools
import itertools
import math
import operator
import dataclasses
import time
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
    pattern = "p={px:d},{py:d} v={vx:d},{vy:d}"
    match = parse.search(pattern, data)
    return match.named


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
    assert part_1(data, 11, 7) == 12


@dataclasses.dataclass
class P:
    x: int
    y: int


@dataclasses.dataclass()
class Foo:
    p: P
    v: P
    size: P

    def __init__(self, d, width, height) -> None:
        self.p = P(d["px"], d["py"])
        self.v = P(d["vx"], d["vy"])
        self.size = P(width, height)

    def pos_after_seconds(self, seconds=100):
        x = (self.p.x + self.v.x * seconds) % self.size.x
        y = (self.p.y + self.v.y * seconds) % self.size.y
        return y, x

    def choose_quatre(self, y, x):
        half_x = self.size.x // 2
        half_y = self.size.y // 2
        if y == half_y or x == half_x:
            return -1

        res = 0
        res += 0 if y < half_y else 2
        res += 0 if x < half_x else 1
        return res

    def solve(self):
        return self.choose_quatre(*self.pos_after_seconds(100))


def print_grid(size, robots):
    for i in range(-1, size.y):
        for j in range(-1, size.x):
            if (i, j) in robots:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def part_1(data, width, height):
    robots = [Foo(parser(line), width, height) for line in data]
    c = Counter()

    for robot in robots:
        c[robot.solve()] += 1

    del c[-1]

    return prod(c.values())


def part_2(data, width, height):
    robots = [Foo(parser(line), width, height) for line in data]
    print(robots)
    c = Counter()
    size = P(width, height)

    for step in range(100000):
        s = set([x.pos_after_seconds(step) for x in robots])
        # That was just gues that it might work
        if len(s) == len(robots):
            print_grid(size, s)
            time.sleep(0.1)
            print(step)


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:], 101, 103))
    print(part_2(data[:], 101, 103))
