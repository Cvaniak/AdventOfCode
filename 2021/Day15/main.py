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


def prod(factors):
    return functools.reduce(operator.mul, factors, 1)


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def load_int_lines(datat):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = [int(x) for x in i]
    return data


def load_int_commas(datat):
    return list(map(int, datat[0].split(",")))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


def part_test():
    data = read_data("test")
    assert part_1(data) == 40
    assert part_2(data) == 315


def part_1(datat):
    data = datat[:]
    data = load_int_lines(data)
    n = len(data)
    # data[0][0] = 0
    # been = set()
    # def foo(x, y, z):
    #     if y < 0 or y >= n:
    #         return float("inf")
    #     if x < 0 or x >= n:
    #         return float("inf")
    #     if (x, y) in been:
    #         return float("inf")
    #     if (x, y) == (n-1, n-1):
    #         return data[n-1][n-1]
    #     been.add((x, y))
    #     a = []
    #     if z != (-1, 0):
    #         a.append(foo(x+1, y, (1, 0)))
    #     if z != (0, -1):
    #         a.append(foo(x, y+1, (0, 1)))
    #     if z != (1, 0):
    #         a.append(foo(x-1, y, (-1, 0)))
    #     if z != (0, 1):
    #         a.append(foo(x, y-1, (0, -1)))
    #     print((x, y), a)
    #     return data[y][x] + min(a)
    # r = foo(0, 0, (0,0))
    # print(r)
    # return r

    # # for i in range(1, n+1):
    #     # for j in range(1, n+1):
    #         # if i == j == 0:
    #         #     continue
    #         # elif i == 0:
    #         #     mn = data[i][j-1]
    #         # elif j == 0:
    #         #     mn = data[i-1][j]
    #         # else:
    #         #     mn = min(data[i][j-1], data[i-1][j])
    #         # data[i][j] += mn
    # # print(data)
    # return data[n-1][n-1]
    da = [[float("inf")] * n for _ in range(n)]
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    da[0][0] = 0

    dq = [(da[0][0], 0, 0)]
    while dq:
        d, y, x = heappop(dq)
        if d > da[y][x]:
            continue
        for i, j in dir:
            nx, ny= x + i, y + j
            if 0 > nx or nx >= n or 0 > ny or ny >= n:
                continue
            a = d + data[ny][nx]
            if a < da[ny][nx]:
                da[ny][nx] = a
                heappush(dq, (a, ny, nx))
    return da[-1][-1]


def part_2(datat):
    data = datat[:]
    data = load_int_lines(data)
    n = len(data)
    for i in range(n):
        line = list(data[i])
        for j in range(4):
            data[i] += [(x + j) % 9 + 1 for x in line]
    block = list(data)
    for i in range(4):
        for line in block:
            data += [[(x + i) % 9 + 1 for x in line]]

    n = len(data)
    da = [[float("inf")] * n for _ in range(n)]
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    da[0][0] = 0

    dq = [(da[0][0], 0, 0)]
    while dq:
        d, y, x = heappop(dq)
        if d > da[y][x]:
            continue
        for i, j in dir:
            nx, ny= x + i, y + j
            if 0 > nx or nx >= n or 0 > ny or ny >= n:
                continue
            a = d + data[ny][nx]
            if a < da[ny][nx]:
                da[ny][nx] = a
                heappush(dq, (a, ny, nx))
    return da[-1][-1]


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
