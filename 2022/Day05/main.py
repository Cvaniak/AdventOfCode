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
    pattern = "move {n:d} from {fr:d} to {to:d}"
    match = parse.search(pattern, data)
    return match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data[:]) == "CMZ"
    assert part_2(data[:]) == "MCD"


def part_1(data, ns=3):
    stacks = [list() for _ in range(ns)]
    ii = 0
    for i in range(len(data)):
        ii = i
        if data[i].startswith(" 1"):
            break
        for j in range(ns):
            stacks[j].append(data[i][1 + j * 4])

    stack = []
    for s in stacks:
        stack.append([x for x in s[::-1] if x != " "])

    for d in data[ii + 2 :]:
        d = parser(d)
        for _ in range(d["n"]):
            stack[d["to"] - 1].append(stack[d["fr"] - 1].pop())

    return "".join([x[-1] for x in stack])


def part_2(data, ns=3):
    stacks = [list() for _ in range(ns)]
    ii = 0
    for i in range(len(data)):
        ii = i
        if data[i].startswith(" 1"):
            break
        for j in range(ns):
            stacks[j].append(data[i][1 + j * 4])

    stack = []

    for s in stacks:
        stack.append([x for x in s[::-1] if x != " "])

    for d in data[ii + 2 :]:
        d = parser(d)
        tmp = []
        for _ in range(d["n"]):
            tmp.append(stack[d["fr"] - 1].pop())
        stack[d["to"] - 1].extend(tmp[::-1])

    return "".join([x[-1] for x in stack])


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:], ns=9))
    print(part_2(data[:], ns=9))
