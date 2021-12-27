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


def load_int_lines(datat):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = [x for x in i]
    return data


def load_int_commas(datat):
    return list(map(int, datat[0].split(",")))


def parser(data):
    pattern = "target area: x={x1:d}..{x2:d}, y={y2:d}..{y1:d}"
    match = parse.search(pattern, data)
    return match.named


def part_test():
    data = read_data("test")
    # assert part_1(data) == 45
    assert part_2(data) == 112


def foo(x, y, xd, yd, x1, x2, y1, y2):
    x += xd
    y += yd
    if x:
        x += 1 if x < 0 else -1
    y -= 1


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
    mx = 0
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
    print(data)
    data = parser(data)
    print(data)
    mx = 0
    for i in range(10000):
        r = fox(
            i,
            data["y1"],
            data["y2"],
        )
        mx = max(mx, r)
    return mx


def part_2(datat):
    data = datat[:][0]
    print(data)
    data = parser(data)
    print(data)
    mx = 0
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
        print(i, r)
        for k in r:
            sy.add(k)
            dy[k].add(i)
            dyy[k] += 1

    inter = s.intersection(sy)
    print(inter)
    r = 0
    rs = set()
    for i in inter:
        print(d[i])
        print(dy[i])
        per = itertools.product(d[i], dy[i])
        for j in per:
            rs.add(j)
    mxx = max(dx.keys())
    print("mxx", mxx)
    print(len(rs))

    #     a = """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
    # 25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
    # 8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
    # 26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
    # 20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
    # 25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
    # 25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
    # 8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
    # 24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
    # 7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
    # 23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
    # 27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
    # 8,-2    27,-8   30,-5   24,-7"""
    #     a = a.splitlines()
    #     c = []
    #     se = set()
    #     for b in a:
    #         b = b.split()
    #         for d in b:
    #             s = d.split(",")
    #             se.add((int(s[0]), int(s[1])))

    #     print(se.difference(rs))

    return len(rs)


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    # print(part_1(data))
    print(part_2(data))
