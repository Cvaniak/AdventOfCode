import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import bisect
import math
from rich import print
import parse
import operator
from heapq import heappop, heappush

wsen = {"E": (1, 0), "S": (0, -1), "W": (-1, 0), "N": (0, 1)}
dir_4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
dir_8 = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
dir_9 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


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


def part_test():
    data = read_data("test")
    assert part_1(data) == 35
    assert part_2(data) == 3351


def conv(i, j, data, line):
    r = ""
    for y, x in dir_9:
        r += str(data[(i+y, j+x)])

    rb = int(r, 2)
    return line[rb]


def printt(n, m, h, d):
    for i in range(-h * 2, n + h * 2):
        for j in range(-h * 2, m + h * 2):
            print(d[(i, j)], end="")
        print()


def solution(datat, h):
    data = datat[:]
    line = data[0]
    line = list(map(int, list(line.replace(".", "0").replace("#", "1"))))
    data = data[2:]
    for i in range(len(data)):
        data[i] = list(map(int, list(data[i].replace(".", "0").replace("#", "1"))))

    d = defaultdict(lambda: 0)
    for i in range(len(data)):
        for j in range(len(data[0])):
            d[(i, j)] = data[i][j]

    n = len(data)
    m = len(data[0])
    for w in range(h):
        nd = defaultdict(lambda: 0)
        for i in range(-2 * h, n + h * 2):
            for j in range(-2 * h, m + h * 2):
                nd[(i, j)] = conv(i, j, d, line)
        d = nd

    return sum(
        [d[key] for key in d if -h <= key[0] <= n + h - 1 and -h <= key[1] <= m + h - 1]
    )


def part_1(datat):
    return solution(datat, 2)


def part_2(datat):
    return solution(datat, 50)


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
