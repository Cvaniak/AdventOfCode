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
    assert part_1(data) == 21
    assert part_2(data) == 525152


def part_1(data):
    def foo(idx, curr, num_idx) -> int:
        if idx == n:
            if num_idx == m and curr == 0:
                return 1
            if num_idx == m-1 and curr == nums[num_idx]:
                return 1
            return 0

        if num_idx >= m:
            if any(x == "#" for x in unk[idx:n]):
                return 0
            return 1

        x = unk[idx]
        ans = 0

        if x == "?":
            x = ".#"

        for y in x:
            if y == ".":
                if curr == 0:
                    ans += foo(idx+1, 0, num_idx)
                elif curr < nums[num_idx]:
                    continue
                elif curr == nums[num_idx]:
                    ans += foo(idx+1, 0, num_idx+1)
            else:
                if curr < nums[num_idx]:  
                    ans += foo(idx+1, curr+1, num_idx)
                elif curr >= nums[num_idx]:
                    continue

        return ans

    res = 0
    for line in data:
        unk, _, nums = line.partition(" ")
        nums = load_ints_seperated(nums)
        n, m = len(unk), len(nums)
        x = foo(0, 0, 0)
        res += x

    return res


def part_2(data):
    def foo(idx, curr, num_idx) -> int:
        if idx == n:
            if num_idx == m and curr == 0:
                return 1
            if num_idx == m-1 and curr == nums[num_idx]:
                return 1
            return 0

        if num_idx >= m:
            if any(x == "#" for x in unk[idx:n]):
                return 0
            return 1

        x = unk[idx]
        ans = 0

        if x == "?":
            x = ".#"

        for y in x:
            if y == ".":
                if curr == 0:
                    ans += foo(idx+1, 0, num_idx)
                elif curr < nums[num_idx]:
                    continue
                elif curr == nums[num_idx]:
                    ans += foo(idx+1, 0, num_idx+1)
            else:
                if curr < nums[num_idx]:  
                    ans += foo(idx+1, curr+1, num_idx)
                elif curr >= nums[num_idx]:
                    continue

        return ans

    zz = len(data)
    res = 0
    for idx, line in enumerate(data):
        unk, _, nums = line.partition(" ")
        nums = load_ints_seperated(nums)
        unk += "?"
        unk = unk*5
        unk = unk[:-1]
        nums = nums*5
        n, m = len(unk), len(nums)
        x = foo(0, 0, 0)
        res += x
        dbg(f"{idx}/{zz}", x)

    return res




if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
