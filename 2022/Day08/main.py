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
        data[idx] = [int(x) for x in i]
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
    data = load_int_lines(data)
    assert part_1(data) == 21
    assert part_2(data) == 8


def part_1(data):
    n = len(data)
    grid = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        mx = 0
        for j in range(n):
            if data[i][j] > mx:
                grid[i][j] += 1
                mx = data[i][j]
    for i in range(n):
        mx = 0
        for j in range(n-1, -1, -1):
            if data[i][j] > mx:
                grid[i][j] += 1
                mx = data[i][j]
    for j in range(n):
        mx = 0
        for i in range(n):
            if data[i][j] > mx:
                grid[i][j] += 1
                mx = data[i][j]
    for j in range(n):
        mx = 0
        for i in range(n-1, -1, -1):
            if data[i][j] > mx:
                grid[i][j] += 1
                mx = data[i][j]
    result = 0
    for i in range(1, n-1):
        for j in range(1, n-1):
            if grid[i][j] > 0:
                result += 1

    result += n*4-4

    dbg(result, lvl = "r")
    return result


def part_2(data):
    mx = 0
    n = len(data)
    def foo(y, x, dir, last):
        yy, xx = y+dir[0], x+dir[1]
        if xx < 0 or xx >= n or yy < 0 or yy >= n:
            return 0
        if data[yy][xx] >= last:
            return 1
        return 1 + foo(yy, xx, dir, last)

    for i in range(1, n-1):
        for j in range(1, n-1):
            new_mx = prod([foo(i, j, dir, data[i][j]) for dir in dir_4])
            if mx <= new_mx:
                mx = max(mx, new_mx)

    return mx
                

if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    data = load_int_lines(data)
    print(part_1(data[:]))
    print(part_2(data[:]))
