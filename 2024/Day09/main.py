import argparse
import bisect
import collections
import functools
import itertools
import math
import operator
import dataclasses
from collections import Counter, defaultdict, deque, namedtuple
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
    assert part_1(data) == 1928
    assert part_2(data) == 2858

def right(line, start_idx):
    r = len(line)-1
    while r > 0:
        tmp = line[r]
        for _ in range(tmp):
            line[r] -= 1
            yield start_idx, r
        r -= 2
        start_idx -= 1
    return


def part_1(data):
    line = data[0]
    line = [int(x) for x in line]
    l, r = 0, len(line)-1
    r_idx = r//2
    l_idx = 0
    idx = 0
    res = 0
    right_gen = right(line, r_idx)
    last_r = r

    while l < last_r:
        for _ in range(line[l]):
            res += idx*l_idx
            idx += 1
        l_idx += 1
        l += 1
        for _ in range(line[l]):
            value, last_r = next(right_gen)
            if last_r <= l:
                break
            res += value*idx
            idx += 1
        l += 1
    for _ in range(line[l]):
        res += idx*l_idx
        idx += 1
    print(res)
    return res


def right_2(line, start_idx):
    r = len(line)-1
    while r > 0:
        tmp = line[r]
        for _ in range(tmp):
            line[r] -= 1
            yield start_idx, r
        r -= 2
        start_idx -= 1
    return



P = namedtuple("P", ["idx_list", "idx_res"])

F = namedtuple("F", ["idx_list", "idx_res", "size", "idx"])


def part_2(data):
    line = data[0]
    line = [int(x) for x in line]
    spaces = [deque() for _ in range(10)]
    files = []
    sm = 0
    idx = 0
    for space in range(len(line)):
        if space%2 == 0:
            files.append(F(space, sm, line[space], idx))
            idx += 1
            sm += line[space]
            continue
        spaces[line[space]].append(P(space, sm)) 
        sm += line[space]

    l, r = 0, len(line)-1
    end = sum(line)

    res = 0
    for file in files[::-1]:
        file_size = file.size
        tmp = -1
        smallest = P(1000000000, len(line))
        for x in range(file_size, 10):
            if spaces[x] and smallest.idx_list > spaces[x][0].idx_list:
                tmp = x
                smallest = spaces[x][0]

        nxt_end = end - file_size
        # Stays in place and counted
        if tmp == -1:
            for x in range(file.idx_res, file.idx_res + file.size):
                res += x * file.idx
        # Moved and couted
        else:
            t = spaces[tmp].popleft()
            for n_idx in range(t.idx_res, t.idx_res+file_size):
                res += n_idx * r//2
            if tmp-file_size:
                rest = P(t.idx_list, t.idx_res+file_size)
                bisect.insort(spaces[tmp-file_size], rest)
            
        r -= 1
        # Clean up spaces not available anymore 
        for x in range(10):
            if spaces[x] and spaces[x][-1].idx_list == r:
                spaces[x].pop()

        r -= 1
        end = nxt_end

    print(res)
    return res





if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
