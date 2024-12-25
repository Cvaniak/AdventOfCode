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
dir_4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
dir_4c = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
dir_8 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


def prod(factors):
    return functools.reduce(operator.mul, factors, 1)


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = [x.splitlines() for x in data.read().split("\n\n")]
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

def foo(a, gate, b):
    if gate == "OR":
        return a or b
    if gate == "XOR":
        return a ^ b
    if gate == "AND":
        return a and b
    assert False

@dataclasses.dataclass()
class A:
    state: Any
    gates: Any
    alll: Any

    def __init__(self, data) -> None:
        self.alll = set()
        self.state = dict()
        for line in data[0]:
            a, _, b = line.partition(": ")
            self.state[a] = int(b)
            self.alll.add(a)
        self.gates = dict()
        for line in data[1]:
            a, gate, b, _, c = line.split(" ")
            self.gates[c] = (a, gate, b)
            self.alll.add(a)
            self.alll.add(b)
            self.alll.add(c)

    def job(self):
        while len(self.state) != len(self.alll):
            for k, (a, gate, b) in self.gates.items():
                if a in self.state and b in self.state:
                    self.state[k] = foo(self.state[a], gate, self.state[b])
            
        
    def solution(self, xyz):
        res = 0
        for i in range(100):
            w = f"{xyz}{i:02d}"
            if w not in self.state:
                break
            res = res + (self.state[w]<<i)
        return res

        
    def solution_2(self):
        for i in range(100):
            a = f"x{i:02d}"
            b = f"y{i:02d}"
            c = f"z{i:02d}"
            if a not in self.state:
                break

    def show(self, value, depth):
        if value not in self.gates or depth == 0:
            return value
        a, operator, b = self.gates[value]
        aa = self.show(a, depth-1)
        bb = self.show(b, depth-1)

        op = {"AND": "&", "OR": "|", "XOR": "^"}
        return f"{value}( {aa} {op[operator]} {bb} )"


def part_test():
    data = read_data("test")
    assert part_1(data) == 4
    data = read_data("test1")
    assert part_1(data) == 2024


def part_1(data):
    a = A(data) 
    a.job()

    return a.solution("z")


def part_2(data):
    a = A(data) 
    a.job()
    x, y ,z = a.solution("x"), a.solution("y"), a.solution("z")
    print(x, y, z)
    print("x+y", bin(x+y))
    print("z  ", bin(z))

    # Done by manually swaping.
    # Hope to revisit...
    print(a.show("z03", 4))

    return a.solution_2()


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
