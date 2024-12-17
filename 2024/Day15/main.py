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
        data = [x.splitlines() for x in data.read().split("\n\n")]
        data[0] = [list(x) for x in data[0]]
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


@dataclasses.dataclass
class P:
    x: int
    y: int

    def __add__(self, other):
        added = tuple( a + b for a, b in zip(self, other) )
        return P(*added)

    def __sub__(self, other):
        subbed = tuple( a - b for a, b in zip(self, other) )
        return P(*subbed)

    def __iter__(self):
        return [self.x, self.y].__iter__()


@dataclasses.dataclass
class Matrix:
    data: list[list[int]]
    moves: str
    n: int
    m: int
    pos: P

    def __init__(self, mp, moves) -> None:
        self.data = mp
        self.moves = "".join(moves)
        self.n = len(mp)
        self.m = len(mp[0])

        for y, line in enumerate(mp):
            for x, value in enumerate(line):
                if value == "@":
                    self.pos = P(x, y)

    def s_get_p(self, p: P, default=None):
        return self.s_get(p.y, p.x)

    def s_get(self, y, x, default=None):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return default
        return self.data[y][x]

    def s_set_p(self, p, value):
        self.s_set(p.y, p.x, value)

    def s_set(self, y, x, value):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return
        self.data[y][x] = value

    def s_move(self, dir):
        new_pos = self.pos + dir
        new_value = self.s_get_p(new_pos)
        if new_value == ".":
            self.s_set_p(self.pos, ".")
            self.s_set_p(new_pos, "@")
            self.pos = new_pos
        elif new_value == "#":
            return
        elif new_value == "O":
            nxt = new_pos
            while self.s_get_p(nxt) == "O":
                nxt += dir
            if self.s_get_p(nxt) == "#":
                return
            self.s_set_p(self.pos, ".")
            self.s_set_p(new_pos, "@")
            self.s_set_p(nxt, "O")
            self.pos = new_pos
            
    def solve(self):
        mv = {"<": (-1, 0), "v": (0, 1), ">": (1, 0), "^": (0, -1)}
        for x in self.moves:
            self.s_move(P(*mv[x]))

    def calculate(self):
        res = 0
        for y, line in enumerate(self.data):
            for x, value in enumerate(line):
                if value == "O":
                    res += y * 100 + x
        return res

class Matrix2(Matrix):
    def __init__(self, mp, moves) -> None:
        for y, line in enumerate(mp):
            nline = ["."]*(len(line)*2) 
            for x, value in enumerate(line):
                if value == "@":
                    nline[x*2] = value
                    nline[x*2+1] = "."
                elif value == "O":
                    nline[x*2] = "["
                    nline[x*2+1] = "]"
                else:
                    nline[x*2] = value
                    nline[x*2+1] = value
            mp[y] = nline

        super().__init__(mp, moves)

    def s_move(self, dir):
        new_pos = self.pos + dir
        new_value = self.s_get_p(new_pos)
        if new_value == ".":
            self.s_set_p(self.pos, ".")
            self.s_set_p(new_pos, "@")
            self.pos = new_pos
            return
        if new_value == "#":
            return

        q = [(self.pos, "@")]
        data_backup = [row[:] for row in self.data]
        self.s_set_p(self.pos, ".")

        while q:
            pos, val = q.pop()
            nxt_pos = pos + dir
            nxt_val = self.s_get_p(nxt_pos)
            if nxt_val == "#":
                self.data = data_backup
                return
            if nxt_val == ".":
                self.s_set_p(nxt_pos, val)
                continue
            if nxt_val == "[":
                q.append((nxt_pos, nxt_val))
                q.append((nxt_pos+P(1, 0), "]"))
                self.s_set_p(nxt_pos, val)
                self.s_set_p(nxt_pos+P(1, 0), ".")
            if nxt_val == "]":
                q.append((nxt_pos, nxt_val))
                q.append((nxt_pos+P(-1, 0), "["))
                self.s_set_p(nxt_pos, val)
                self.s_set_p(nxt_pos+P(-1, 0), ".")
        self.pos = self.pos + dir

                
    def calculate(self):
        res = 0
        for y, line in enumerate(self.data):
            for x, value in enumerate(line):
                if value == "[":
                    res += y * 100 + x
        return res

# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data[:]) == 10092
    # Weird bug if not readed again
    data = read_data("test")
    assert part_2(data[:]) == 9021


def part_1(data):
    matrix = Matrix(data[0], data[1])
    matrix.solve()
    c = matrix.calculate()
    return c


def part_2(data): 
    matrix = Matrix2(data[0], data[1])
    matrix.solve()
    c = matrix.calculate()
    print(c)
    return c


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    # Weird bug if not readed again
    data = read_data("input")
    print(part_2(data[:]))
