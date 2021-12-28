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

def prod(factors):
    return functools.reduce(operator.mul, factors, 1)


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def parser(data):
    pattern = "{x:d},{y:d},{z:d}"
    match = parse.search(pattern, data)
    return match


def part_test():
    data = read_data("test")
    assert part_1(data) == 79
    assert part_2(data) == None


def all_o(d):
    x = int(d[0])
    y = int(d[1])
    z = int(d[2])
    r = []
    for i, j, k in zip([x, y, z], [y, z, x], [z, x, y]):
        r.append((i, j, k))
        r.append((-j, i, k))
        r.append((j, -i, k))
        r.append((-i, -j, k))
        r.append((j, i, -k))
        r.append((i, -j, -k))
        r.append((-i, j, -k))
        r.append((-j, -i, -k))
    return r


def overlap(x, y):
    print("overlap")
    for i in range(len(x)):
        print(i)


def rel(x, y, z):
    return x, y, z


def mi(x, y):
    ne = (x[0] - y[0], x[1] - y[1], x[2] - y[2])
    return ne


def pl(x, y):
    ne = (x[0] + y[0], x[1] + y[1], x[2] + y[2])
    return ne


def transpose(m):
    return [list(e) for e in zip(*m)]

def foo(a, b):
    all_b = [all_o(x) for x in b]
    all_b = transpose(all_b)
    for rotated in all_b:
        c = Counter()
        for z1 in a:
            for z2 in rotated:
                sa = mi(z1, z2)
                c[sa] += 1
        off, num = c.most_common()[0]
        if num >= 12:
            return rotated, off
    return None


def part_1(datat):
    data_t = datat[:]
    data = []
    for i in data_t:
        x = parser(i)
        if x:
            named = x.named
            if named.get("x", None) is not None:
                data[-1].append(named)
                for w in data[-1][-1]:
                    data[-1][-1][w] = int(data[-1][-1][w])
        elif x == None and i:
            data.append([])


    for i in range(len(data)):
        first = rel(**data[i][0])
        for j in range(len(data[i])):
            data[i][j] = rel(**data[i][j])

    n = len(data)
    prt2 = []
    s_sean = {s for s in data[0]}
    been = set()
    n = len(data)
    for i in range(n):
        for j in range(1, n):
            if j in been:
                continue
            fo = foo(s_sean, data[j])
            if fo is not None:
                been.add(j)
                rotated, off = fo
                prt2.append(off)

                for k in rotated:
                    k = pl(k, off)
                    s_sean.add(k)
                break
    
    print(len(s_sean))
    mx = 0
    for i in prt2:
        for j in prt2:
            mx = max(mx, sum(abs(x) for x in mi(i, j)))
    print(mx)

    return len(s_sean)

def part_2(datat):
    data = datat[:]


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
