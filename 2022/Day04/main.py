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
    pattern = "{x1:d}-{y1:d},{x2:d}-{y2:d}"
    match = parse.search(pattern, data)
    match.named
    return match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 2
    assert part_2(data) == 4


def part_1(datat):
    r = 0
    for data in datat:
        d = parser(data)
        if d["x1"] <= d["x2"] and d["y1"] >= d["y2"]:
            r += 1
        if d["x1"] >= d["x2"] and d["y1"] <= d["y2"]:
            r += 1
    return r


def part_2(datat):
    r = 0
    for data in datat:
        d = parser(data)
        if d["x1"] <= d["x2"] and d["y1"] >= d["x2"]:
            r += 1
        elif d["x1"] <= d["y2"] and d["y1"] >= d["y2"]:
            r += 1
        elif d["x2"] <= d["x1"] and d["y2"] >= d["x1"]:
            r += 1
        elif d["x2"] <= d["y1"] and d["y2"] >= d["y1"]:
            r += 1
    return r


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
