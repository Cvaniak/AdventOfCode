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
    assert part_1(data, 7, 27) == 2
    assert part_2(data) == 47


def part_1(data, mn=200000000000000, mx=400000000000000):
    def find_intersection(m1, b1, m2, b2):
        if m1 == m2:
            if b1 == b2:
                return None
            return None

        x = (b2 - b1) / (m1 - m2)

        y = m1 * x + b1

        return (y, x)

    slopes = []
    for line in data:
        a, _, b = line.partition("@")
        a = load_ints_seperated(a, ", ")
        b = load_ints_seperated(b, ", ")

        m = b[1] / b[0]
        bb = a[1] - m * a[0]
        slopes.append(((a[1], a[0]), (m, bb), (b[1] / abs(b[1]), b[0] / abs(b[0]))))

    ans = 0
    for i in range(len(slopes)):
        for j in range(i + 1, len(slopes)):
            inter = find_intersection(*slopes[i][1], *slopes[j][1])
            if inter is not None and mn <= inter[0] <= mx and mn <= inter[1] <= mx:
                # dbg(slo)
                if (slopes[i][0][0] - inter[0]) / slopes[i][2][0] < 0 and (
                    slopes[j][0][0] - inter[0]
                ) / slopes[j][2][0] < 0:
                    if (slopes[i][0][1] - inter[1]) / slopes[i][2][1] < 0 and (
                        slopes[j][0][1] - inter[1]
                    ) / slopes[j][2][1] < 0:
                        ans += 1
    return ans


def part_2(data):
    slopes = []
    for line in data:
        a, _, b = line.partition("@")
        a = load_ints_seperated(a, ", ")
        b = load_ints_seperated(b, ", ")
        slopes.append((a, b))

    import sympy

    equations = []
    xyz = [sympy.var("x"), sympy.var("y"), sympy.var("z")]
    vxyz = [sympy.var("xv"), sympy.var("yv"), sympy.var("zv")]
    for i in range(3):
        t = sympy.var(f"t{i}")
        p, v = slopes[i]
        for j in range(3):
            equations.append(sympy.Eq(xyz[j] + t * vxyz[j], p[j] + v[j] * t))

    d = sympy.solve(equations)[0]
    ans = sum(d[v] for v in xyz)
    return ans


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
