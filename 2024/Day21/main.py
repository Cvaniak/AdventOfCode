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
from typing import Any

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


@dataclasses.dataclass(frozen=True)
class P:
    y: int
    x: int

    def __add__(self, other):
        added = tuple(a + b for a, b in zip(self, other))
        return P(*added)

    def __mul__(self, scalar):
        return P(self.y * scalar, self.x * scalar)

    def __sub__(self, other):
        subbed = tuple(a - b for a, b in zip(self, other))
        return P(*subbed)

    def __iter__(self):
        return [self.y, self.x].__iter__()

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __hash__(self):
        return hash((self.y, self.x))

    def dist_p(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def dist(self, y, x):
        return abs(self.y - y) + abs(self.x - x)


dir_4 = [P(-1, 0), P(0, 1), P(1, 0), P(0, -1)]
dir_4_v = "^>v<"


@dataclasses.dataclass
class Matrix:
    data: list[list[int]]
    size: P
    start: P
    func: Any

    def __init__(self, data, func) -> None:
        self.size = P(len(data), len(data[0]))
        self.data = data
        self.func = func
        self.start = P(-1, -1)

        self.set_start("A")

    def set_start(self, value):
        for y in range(self.size.y):
            for x in range(self.size.x):
                if self.s_get_p(P(y, x)) == value:
                    self.start = P(y, x)
                    break

    def s_get(self, y, x, default=None):
        if 0 > y or y >= self.size.y or 0 > x or x >= self.size.x:
            return default
        return self.data[y][x]

    def s_get_p(self, p: P, default=None):
        return self.s_get(p.y, p.x, default)

    def s_set(self, y, x, value):
        if 0 > y or y >= self.size.y or 0 > x or x >= self.size.x:
            return
        self.data[y][x] = value

    def s_set_p(self, p, value):
        self.s_set(p.y, p.x, value)


# ===== ^^ PART OF TEMPLATE ^^ =====

a = [list("#^A"), list("<v>")]
b = [list("789"), list("456"), list("123"), list("#0A")]
arrows = {
    P(y, x): value
    for y, line in enumerate(a)
    for x, value in enumerate(line)
    if value != "#"
}
arrows.update({v:k for k, v in arrows.items()})
numbers = {
    P(y, x): value
    for y, line in enumerate(b)
    for x, value in enumerate(line)
    if value != "#"
}
numbers.update({v:k for k, v in numbers.items()})

def foo(a, b, pad=True):
    if pad:
        pad = arrows
    else:
        pad = numbers
    pos_a = pad[a]
    pos_b = pad[b]
    diff = pos_b-pos_a

    v = "v"*diff.y+"^"*(-diff.y)
    h = ">"*diff.x+"<"*(-diff.x)

    # order inspired from other solutions
    if diff.x > 0 and P(pos_b.y,pos_a.x) in pad:
        return v+h+"A"
    if P(pos_a.y,pos_b.x) in pad:
        return h+v+"A"
    if P(pos_b.y,pos_a.x) in pad:
        return v+h+"A"


def solve(path, pad):
    res = []
    for a, b in zip(["A"]+list(path[:-1]), path):
        res.append(foo(a, b, pad))
    return "".join(res)

def solve_2(path, pad, count=1):
    res = Counter()
    for a, b in zip(["A"]+list(path[:-1]), path):
        res[foo(a, b, pad)] += count
    return res


def part_test():
    data = read_data("test")
    assert part_1(data) == 126384
    assert part_2(data) == 154115708116294


def part_1(data):
    nums = [solve(path, False) for path in data]
    robots = [solve(path, True) for path in nums]
    colds = [solve(path, True) for path in robots]

    res = 0
    for line, solution in zip(data, colds):
        res += len(solution) * int(line[:-1])

    return res


def part_2(data):
    prev = [solve_2(path, False) for path in data]
    for _ in range(25):
        for i in range(len(prev)):
            updated = Counter()
            for new_path, count in prev[i].items():
                new_solved = solve_2(new_path, True, count)
                updated.update(new_solved)
            prev[i] = updated

    res = 0
    for line, solution in zip(data, prev):
        w = sum(len(k)*v for k, v in solution.items())
        res += w * int(line[:-1])
    return res


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
