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
    ...


def part_test():
    data = read_data("test")
    assert part_1(data) == 18
    assert part_2(data, 4) == 18
    assert part_2(data, 10) == 1588
    assert part_2(data, 40) == 2188189693529


def part_1(datat):
    data = datat[:]
    st = list(data[0])
    d = dict()
    for i in data[2:]:
        x, y = i[:2], i[-1]
        d[x] = y

    for _ in range(4):
        ne = []
        for i, j in zip(st[:-1], st[1:]):
            ne.append(d[i + j])
        for idx, i in enumerate(ne):
            st.insert(1 + idx * 2, i)
    c = Counter(st)
    mx, mn = c.most_common()[0], c.most_common()[-1]
    print(st)
    print(mx, mn)
    return mx[1] - mn[1]


def part_2(datat, n):
    data = datat[:]
    st = list(data[0])
    d = dict()
    for i in data[2:]:
        x, y = i[:2], i[-1]
        d[(x[0], x[1])] = y

    a = list(zip(st[:-1], st[1:]))
    c = Counter(a)
    for _ in range(n):
        keys = [x for x in list(c.keys()) if c[x] > 0]
        c1 = Counter([])
        for i, j in c.items():
            ne = d[i]
            c1[(i[0], ne)] += j
            c1[(ne, i[1])] += j

        c = c1
        # print(c)
    c1 = Counter([])
    for i, j in c.items():
        c1[i[0]] += j
    c1[st[-1]] += 1

    most_common = c1.most_common()
    mx, mn = most_common[0], most_common[-1]
    return mx[1] - mn[1]


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data, 40))
