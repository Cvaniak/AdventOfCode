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
    assert part_1(data, (0, 0), (2, 5)) == 31
    assert part_2(data, (0, 0), (2, 5)) == 29


def part_1(data, start, end, size=(5, 8)):
    grid = []
    for line in data:
        grid.append([ord(x) for x in line])

    visited = dict()
    y, x = start
    grid[y][x] = 97
    y, x = end
    grid[y][x] = 122
    visited[start] = 0

    q = deque([start])

    while q:
        y, x = q.popleft()

        for yy, xx in dir_4:
            yy, xx = yy + y, xx + x
            if yy < 0 or yy >= size[0] or xx < 0 or xx >= size[1]:
                continue

            if grid[y][x] >= grid[yy][xx] - 1:
                if (yy, xx) in visited and visited[(y, x)] + 1 >= visited[(yy, xx)]:
                    continue

                visited[(yy, xx)] = visited[(y, x)] + 1
                q.append((yy, xx))

    return visited[(end)]


def part_2(data, start, end, size=(5, 8)):
    grid = []
    for line in data:
        grid.append([ord(x) for x in line])

    y, x = start
    grid[y][x] = 97
    y, x = end
    grid[y][x] = 122
    visited = dict()
    visited[start] = 0

    q = deque([start])

    while q:
        y, x = q.popleft()

        for yy, xx in dir_4:
            yy, xx = yy + y, xx + x
            if yy < 0 or yy >= size[0] or xx < 0 or xx >= size[1]:
                continue

            if grid[y][x] >= grid[yy][xx] - 1:
                if (yy, xx) in visited and visited[(y, x)] + 1 >= visited[(yy, xx)]:
                    continue

                if grid[yy][xx] == 97:
                    visited[(yy, xx)] = 0
                else:
                    visited[(yy, xx)] = visited[(y, x)] + 1

                q.append((yy, xx))

    result = visited[end]
    return result


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:], (20, 0), (20, 52), (41, 77)))
    print(part_2(data[:], (20, 0), (20, 52), (41, 77)))
