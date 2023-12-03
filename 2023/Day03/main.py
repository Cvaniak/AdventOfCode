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
    assert part_1(data) == 4361
    assert part_2(data) == 467835


def part_1(data):
    symbols_overlap = set()
    for y, line in enumerate(data):
        s: str
        for x, s in enumerate(line):
            if not s.isnumeric() and s != ".":
                for yy, xx in dir_8:
                    symbols_overlap.add((y+yy, x+xx))

    sm = 0
    for y, line in enumerate(data):
        s: str
        curr = 0
        valid = False
        for x, s in enumerate(line):
            if s.isnumeric():
                curr = 10*curr + int(s)
                if curr > 0 and (y, x) in symbols_overlap:
                    valid = True
            else:
                if valid:
                    sm += curr
                valid = False
                curr = 0
        if valid:
            sm += curr
    return sm


def part_2(data):
    symbols_overlap = dict()
    for y, line in enumerate(data):
        s: str
        for x, s in enumerate(line):
            if s == "*":
                for yy, xx in dir_8:
                    symbols_overlap[(y+yy, x+xx)] = (y, x)

    gears_ratios = defaultdict(list)
    for y, line in enumerate(data):
        s: str
        curr = 0
        valid = False
        curr_gear = (-1,-1)
        for x, s in enumerate(line):
            if s.isnumeric():
                curr = 10*curr + int(s)
                if curr > 0 and (y, x) in symbols_overlap:
                    valid = True
                    curr_gear = symbols_overlap[(y, x)]
            else:
                if valid:
                    gears_ratios[curr_gear].append(curr)
                valid = False
                curr = 0
        if valid:
            gears_ratios[curr_gear].append(curr)

            
    sm = 0
    for rations_list in gears_ratios.values():
        if len(rations_list) == 2:
            sm += rations_list[0]*rations_list[1]
    return sm


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
