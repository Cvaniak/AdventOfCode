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

import parse
from rich import print

debug = set("0")
debug_space = False


def dbg(*args, lvl="0", **kwargs):
    if lvl in debug:
        print(lvl)
        print(*args, **kwargs)
        if debug_space:
            print()


def set_debuger():
    global debug, debug_space
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", nargs="?", const="0", default="0", help="Debug List"
    )
    parser.add_argument(
        "-n", "--nodebug", action="store_true", help="Remove default debug"
    )
    parser.add_argument(
        "-s", "--addspace", action="store_true", help="Space between debug"
    )
    args = parser.parse_args()
    debug.update({x for x in args.debug})
    if args.nodebug:
        debug.remove("0")
    if args.addspace:
        debug_space = True


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


def load_int_lines(datat):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = [x for x in i]
    return data


def load_int_commas(datat):
    return list(map(int, datat[0].split(",")))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 110
    assert part_2(data) == 20


moves = [
    ((-1, 1), (-1, 0), (-1, -1)),
    ((1, 1), (1, 0), (1, -1)),
    ((-1, -1), (0, -1), (1, -1)),
    ((-1, 1), (0, 1), (1, 1)),
]


def part_1(data):
    elfs = set()
    for idxy, line in enumerate(data):
        for idxx, point in enumerate(line):
            if point == "#":
                elfs.add((idxy, idxx))

    for mv in range(10):
        ...
        plan_move = defaultdict(set)
        new_elfs = set()
        for yy, xx in elfs:
            if any((yy + ny, xx + nx) in elfs for ny, nx in dir_8):
                for i in range(4):
                    for ny, nx in moves[(mv + i) % 4]:
                        if (yy + ny, xx + nx) in elfs:
                            break
                    else:
                        ny, nx = moves[(mv + i) % 4][1]
                        plan_move[(yy + ny, xx + nx)].add((yy, xx))
                        break
                else:
                    plan_move[(yy, xx)].add((yy, xx))
            else:
                plan_move[(yy, xx)].add((yy, xx))

        for a, sa in plan_move.items():
            if len(sa) == 1:
                new_elfs.add(a)
            else:
                new_elfs.update(sa)
        elfs = new_elfs

    mny = min(x[0] for x in elfs)
    mnx = min(x[1] for x in elfs)
    mxy = max(x[0] for x in elfs)
    mxx = max(x[1] for x in elfs)
    return (mxx - mnx + 1) * (mxy - mny + 1) - len(elfs)


def part_2(data):
    elfs = set()
    for idxy, line in enumerate(data):
        for idxx, point in enumerate(line):
            if point == "#":
                elfs.add((idxy, idxx))

    for mv in range(1000):
        plan_move = defaultdict(set)
        new_elfs = set()
        for yy, xx in elfs:
            if any((yy + ny, xx + nx) in elfs for ny, nx in dir_8):
                for i in range(4):
                    for ny, nx in moves[(mv + i) % 4]:
                        if (yy + ny, xx + nx) in elfs:
                            break
                    else:
                        ny, nx = moves[(mv + i) % 4][1]
                        plan_move[(yy + ny, xx + nx)].add((yy, xx))
                        break
                else:
                    plan_move[(yy, xx)].add((yy, xx))
            else:
                plan_move[(yy, xx)].add((yy, xx))

        for a, sa in plan_move.items():
            if len(sa) == 1:
                new_elfs.add(a)
            else:
                new_elfs.update(sa)
        if elfs == new_elfs:
            return mv + 1
        elfs = new_elfs


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
