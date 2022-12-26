import argparse
import bisect
import collections
import functools
import itertools
import math
import operator
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from itertools import combinations, pairwise, permutations, product

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
    assert part_1(data) == 18
    assert part_2(data) == 54


bliz = {">": 0, "v": 1, "<": 2, "^": 3}
dir_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def part_1(data):
    n, m = len(data) - 2, len(data[0]) - 2

    @functools.cache
    def add_tup(a, b):
        return ((a[0] + b[0]) % n, (a[1] + b[1]) % m)

    @functools.cache
    def add_tup_elfs(a, b):
        yy, xx = ((a[0] + b[0]), (a[1] + b[1]))
        if yy < 0 or yy >= n or xx < 0 or xx >= m:
            return a
        return (yy, xx)

    def print_grid(blizs, asdf):
        for i in range(-1, n + 1):
            for j in range(0, m):
                if (i, j) in asdf:
                    print("E", end="")
                elif (i, j) in blizs:
                    print(len(blizs[(i, j)]), end="")
                elif (i, j) == end:
                    print("X")
                else:
                    print(".", end="")
            print()
        print()

    start, end = (-1, 0), (n - 1, m - 1)
    blizs = defaultdict(set)
    for idxy, line in enumerate(data[1:-1]):
        for idxx, point in enumerate(line[1:-1]):
            if point != ".":
                blizs[(idxy, idxx)].add(bliz[point])

    queue = set([start])
    t = 0
    while True:
        new_blizs = defaultdict(set)
        for b in blizs:
            for i in blizs[b]:
                new_blizs[add_tup(b, dir_4[i])].add(i)
        blizs = new_blizs

        new_queue = set()
        while queue:
            point = queue.pop()
            if point not in blizs:
                new_queue.add(point)

            for yx in dir_4:
                n_point = add_tup_elfs(point, yx)
                if point == end:
                    return t + 1

                if n_point not in blizs:
                    new_queue.add(n_point)

        queue = new_queue
        t += 1


def part_2(data):
    n, m = len(data) - 2, len(data[0]) - 2
    start, end = (-1, 0), (n - 1, m - 1)

    @functools.cache
    def add_tup(a, b):
        return ((a[0] + b[0]) % n, (a[1] + b[1]) % m)

    @functools.cache
    def add_tup_elfs(a, b):
        yy, xx = ((a[0] + b[0]), (a[1] + b[1]))
        if (yy, xx) in [start, end]:
            return (yy, xx)
        if yy < 0 or yy >= n or xx < 0 or xx >= m:
            return a
        return (yy, xx)

    blizs = defaultdict(set)
    for idxy, line in enumerate(data[1:-1]):
        for idxx, point in enumerate(line[1:-1]):
            if point != ".":
                blizs[(idxy, idxx)].add(bliz[point])

    def foo(start, end):
        nonlocal blizs

        queue = set([start])
        t = 0
        while True:
            new_blizs = defaultdict(set)
            for b in blizs:
                for i in blizs[b]:
                    new_blizs[add_tup(b, dir_4[i])].add(i)
            blizs = new_blizs

            new_queue = set()
            while queue:
                point = queue.pop()
                if point not in blizs:
                    new_queue.add(point)

                for yx in dir_4:
                    n_point = add_tup_elfs(point, yx)
                    if point == end:
                        return t + 1

                    if n_point not in blizs:
                        new_queue.add(n_point)

            queue = new_queue
            t += 1

    fox = [[(-1, 0), (n - 1, m - 1)], [(n, m - 1), (0, 0)], [(-1, 0), (n - 1, m - 1)]]
    return sum(foo(start, end) for start, end in fox)


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
