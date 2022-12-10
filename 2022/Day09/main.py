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
lrud = {"R": (1, 0), "D": (0, -1), "L": (-1, 0), "U": (0, 1)}
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
def sum_list(x, y):
    for i in range(len(x)):
        x[i] += y[i]


def part_test():
    data = read_data("test")
    assert part_1(data) == 13
    assert part_2(data) == 1
    data = read_data("test_2")
    assert part_2(data) == 36


def part_1(data):
    t = [0,0]
    h = [0,0]
    visited = set()

    def jump(x, y):
        ...
        # if abs(x[0]-y[0]) + abs(x[1]-y[1]) >= 3:

        if tuple(x) == tuple(y):
            return 
        if any((x[0]+xx, x[1]+yy) == tuple(y) for xx, yy in dir_8):
            return

        for xx, yy in dir_8:
            for xx4, yy4 in dir_4:
                if (x[0]+xx+xx4, x[1]+yy+yy4) == tuple(y):
                    x[0] += xx
                    x[1] += yy
                    return


    for dir_num in data:
        dir, num = dir_num.split(" ")
        for _ in range(int(num)):
            sum_list(h, lrud[dir])
            jump(t, h)

            visited.add(tuple(t))

    return len(visited)


        


def part_2(data):

    # grid = [[0 for _ in range(7)] for _ in range(7)]
    t = [[0,0] for _ in range(10)]
    visited = set()

    def jump(x, y):
        ...
        if abs(x[0]-y[0]) + abs(x[1]-y[1]) > 4:
            raise


        if tuple(x) == tuple(y):
            return 
        if any((x[0]+xx, x[1]+yy) == tuple(y) for xx, yy in dir_8):
            return

        for xx, yy in dir_8:
            for xx4, yy4 in dir_4:
                if (x[0]+xx+xx4, x[1]+yy+yy4) == tuple(y):
                    x[0] += xx
                    x[1] += yy
                    return
        for xx, yy in dir_8:
            for xx4, yy4 in dir_8:
                if (x[0]+xx+xx4, x[1]+yy+yy4) == tuple(y):
                    x[0] += xx
                    x[1] += yy
                    return


    for dir_num in data:
        dir, num = dir_num.split(" ")
        for _ in range(int(num)):
            sum_list(t[0], lrud[dir])
            for r in range(9):
                jump(t[r+1], t[r])

            visited.add(tuple(t[9]))

    return len(visited)


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
