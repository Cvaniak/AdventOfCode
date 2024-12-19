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


class Trie:
    def __init__(self, towels):
        _trie = lambda: defaultdict(_trie)
        self.trie = _trie()
        for towel in towels:
            self.insert(towel)

    def insert(self, word: str) -> None:
        trie = self.trie
        for w in word:
            trie = trie[w]
        trie.setdefault("#")

    def match(self, word: str) -> list[int]:
        trie = self.trie
        step = 0
        for w in word:
            if w not in trie:
                return
            trie = trie[w]
            step += 1
            if "#" in trie:
                yield step

        return


@functools.lru_cache
def check(trie, pattern, pos):
    if pos >= len(pattern):
        return 1

    for plus_idx in trie.match(pattern[pos:]):
        if check(trie, pattern, pos+plus_idx):
            return 1

    return 0


@functools.lru_cache
def check_2(trie, pattern, pos):
    if pos >= len(pattern):
        return 1

    res = 0
    for plus_idx in trie.match(pattern[pos:]):
        res += check_2(trie, pattern, pos+plus_idx)

    return res


def part_test():
    data = read_data("test")
    assert part_1(data) == 6
    assert part_2(data) == 16


def part_1(data):
    towels = [x for x in data[0].split(", ")]
    patterns = [x for x in data[2:]]
    t = Trie(towels)

    res = 0
    for pattern in patterns:
        res += check(t, pattern, 0)

    return res

def part_2(data):
    towels = [x for x in data[0].split(", ")]
    patterns = [x for x in data[2:]]
    t = Trie(towels)

    res = 0
    for pattern in patterns:
        res += check_2(t, pattern, 0)

    return res


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))