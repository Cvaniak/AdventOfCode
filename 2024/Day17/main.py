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

@dataclasses.dataclass
class Registers:
    A: int
    B: int
    C: int
    pos: int
    instructions: list[int]
    output: list[int] = dataclasses.field(default_factory=list)

    def adv(self, value):
        self.A = self.A//(2**self.combo(value))
        self.jump()

    def bxl(self, value):
        self.B = self.B ^ value
        self.jump()

    def bst(self, value):
        self.B = self.combo(value)%8
        self.jump()

    def jnz(self, value):
        if self.A == 0:
            self.jump()
            return
        self.jump(value)

    def bxc(self, value):
        self.B = self.B ^ self.C
        self.jump()

    def out(self, value):
        self.output.append(self.combo(value)%8)
        self.jump()
    
    def bdv(self, value):
        self.B = self.A//(2**self.combo(value))
        self.jump()

    def cdv(self, value):
        self.C = self.A//(2**self.combo(value))
        self.jump()

    def operator(self, value):
        return (self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv)[value]

    def combo(self, value):
        return [0, 1, 2, 3, self.A, self.B, self.C][value]

    def jump(self, d=None):
        if d is None:
            self.pos += 2
        else:
            self.pos = d

    def solve(self):
        for _ in range(10000000):
            if self.pos >= len(self.instructions):
                break
            a = self.instructions[self.pos]
            b = self.instructions[self.pos+1]
            self.operator(a)(b)

def part_test():
    r = Registers(0,0,9,0,[2,6])
    r.solve()
    assert r.B == 1
    data = read_data("test")
    assert part_1(data) == "4,6,3,5,6,3,5,2,1,0"
    

def part_1(data):
    a = int(data[0].partition(": ")[2])
    b = int(data[1].partition(": ")[2])
    c = int(data[2].partition(": ")[2])
    instructions = list(map(int, (data[4].partition(": ")[2].split(','))))
    v = Registers(a,b,c,0,instructions)
    v.solve()
    print(v)

    return ",".join([str(x) for x in v.output])


def part_2(data):
    a = int(data[0].partition(": ")[2])
    b = int(data[1].partition(": ")[2])
    c = int(data[2].partition(": ")[2])
    instructions = list(map(int, (data[4].partition(": ")[2].split(','))))
    print()

    q = [0]
    ln = len(instructions)
    for offset in range(len(instructions)):
        nq = []
        for a in q:
            for i in range(8):
                v = Registers(a*8+i,b,c,0,instructions)
                v.solve()
                if v.output and v.output == instructions[ln-offset-1:]:
                    output = v.output
                    nq.append(a*8+i)
        q = nq
    return min(q)
            

if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))