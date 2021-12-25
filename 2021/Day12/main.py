import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import bisect
import math
from rich import print
import operator


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def part_test():
    data = read_data("test")
    assert part_1(data) == 10
    data = read_data("test1")
    assert part_1(data) == 19
    data = read_data("test2")
    assert part_1(data) == 226
    data = read_data("test")
    assert part_2(data) == 36
    data = read_data("test1")
    assert part_2(data) == 103
    data = read_data("test2")
    assert part_2(data) == 3509


def part_1(datat):
    data = datat[:]
    data = [(x.split("-")[0], x.split("-")[1]) for x in data]
    d = defaultdict(list)
    for i, j in data:
        if i != "start":
            d[j].append(i)
        d[i].append(j)

    def foo(x, y, z):
        if x == "end":
            return 1
        if x.islower() and x in y:
            return 0
        y.add(x)

        r = 0
        for i in d[x]:
            z.append(i)
            tmp = foo(i, y, z)
            z.pop()
            r += tmp

        y.discard(x)

        return r

    n = foo("start", set(), ["start"])
    return n


def part_2(datat):
    data = datat[:]
    data = [(x.split("-")[0], x.split("-")[1]) for x in data]
    d = defaultdict(list)
    small = set()
    for i, j in data:
        if i != "start":
            d[j].append(i)
        d[i].append(j)
        if i.islower() and i not in ["start", "end"]:
            small.add(i)
        if j.islower() and j not in ["start", "end"]:
            small.add(j)
    res = set()

    def foo(x, y, z):
        if x == "end":
            res.add(tuple(z))
            return 1
        if x.islower() and (x == cantwo and y[x] >= 2):
            return 0
        if x.islower() and (x != cantwo and y[x] >= 1):
            return 0
        y[x] += 1

        r = 0
        for i in d[x]:
            z.append(i)
            tmp = foo(i, y, z)
            z.pop()
            r += tmp

        y[x] -= 1

        return r

    mx = 0
    for i in small:
        cantwo = i
        n = foo("start", defaultdict(int), ["start"])
        mx = max(mx, n)

    return len(res)


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))