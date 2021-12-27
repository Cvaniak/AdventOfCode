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


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def parser(data):
    pattern = "target area: x={x1:d}..{x2:d}, y={y2:d}..{y1:d}"
    match = parse.search(pattern, data)
    return match.named


def part_test():
    data = read_data("test")
    assert part_1(data) == 45
    assert part_2(data) == 112

def fox(y, y1, y2):
    yy = 0
    mx = 0
    steps = []
    i = 0
    while yy >= y2:
        i += 1
        yy += y
        y -= 1
        mx = max(yy, mx)
        if yy <= y1 and yy >= y2:
            steps.append(i)
    return steps


def foox(x, x1, x2):
    xx = 0
    steps = []
    i = 0
    while x:
        i += 1
        xx += x
        if x:
            x += 1 if x < 0 else -1
        if xx >= x1 and xx <= x2:
            steps.append(i)
    if not x and xx >= x1 and xx <= x2:
        for i in range(max(steps), max(steps) + 500):
            steps.append(i)
    return steps


def part_1(datat):
    data = datat[:][0]
    data = parser(data)
    return ((data["y2"]+1)*data["y2"]//2)


def part_2(datat):
    data = datat[:][0]
    data = parser(data)
    d = defaultdict(set)
    dx = defaultdict(int)
    s = set()
    for i in range(max(data["x2"] * 2, data["y1"] * 2)):
        r = foox(i, data["x1"], data["x2"])
        for k in r:
            s.add(k)
            d[k].add(i)
            dx[k] += 1

    dy = defaultdict(set)
    dyy = defaultdict(int)
    sy = set()
    for i in range(-100, 100):
        r = fox(
            i,
            data["y1"],
            data["y2"],
        )
        for k in r:
            sy.add(k)
            dy[k].add(i)
            dyy[k] += 1

    inter = s.intersection(sy)
    r = 0
    rs = set()
    for i in inter:
        per = itertools.product(d[i], dy[i])
        for j in per:
            rs.add(j)

    return len(rs)


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
