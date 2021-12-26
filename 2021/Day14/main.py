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


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def part_test():
    data = read_data("test")
    assert sol(data, 4) == 18
    assert sol(data, 10) == 1588
    assert sol(data, 40) == 2188189693529


def sol(datat, n):
    data = datat[:]
    st = list(data[0])
    d = dict()
    for i in data[2:]:
        x, y = i[:2], i[-1]
        d[(x[0], x[1])] = y

    a = list(zip(st[:-1], st[1:]))
    c = Counter(a)
    for _ in range(n):
        c1 = Counter([])
        for i, j in c.items():
            ne = d[i]
            c1[(i[0], ne)] += j
            c1[(ne, i[1])] += j
        c = c1

    c1 = Counter([])
    for i, j in c.items():
        c1[i[0]] += j
    c1[st[-1]] += 1

    most_common = c1.most_common()
    mx, mn = most_common[0], most_common[-1]
    return mx[1] - mn[1]


def part_1(datat):
    return sol(datat, 10)


def part_2(datat):
    return sol(datat, 40)


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
