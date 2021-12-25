import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import bisect
import math
import argparse
from rich import print
import parse
import operator
from heapq import heappop, heappush

debug = False


def dbg(*args, **kwargs):
    if debug:
        print(*args, **kwargs)


def set_debuger():
    global debug
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug")
    args = parser.parse_args()
    debug = args.debug


wsen = {"E": (1, 0), "S": (0, -1), "W": (-1, 0), "N": (0, 1)}
dir_4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
dir_8 = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]


def a_star(data):
    n = len(data)
    m = len(data[0])
    da = [[float("inf")] * (m) for _ in range(n)]
    dir = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    da[0][0] = 0

    dq = [(da[0][0], 0, 0)]
    while dq:
        d, y, x = heappop(dq)
        if d > da[y][x]:
            continue
        for i, j in dir:
            xi = x + i
            yj = y + j
            if 0 <= xi < m and 0 <= yj < n:
                a = d + data[yj][xi]
                if a < da[yj][xi]:
                    da[yj][xi] = a
                    heappush(dq, (a, yj, xi))
    return da[-1][-1]


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


def part_test():
    data = read_data("test")
    assert part_1(data) == None
    assert part_2(data) == None


def part_1(datat):
    data = datat[:]


def part_2(datat):
    data = datat[:]


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
