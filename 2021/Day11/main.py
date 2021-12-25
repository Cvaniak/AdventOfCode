import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import math
from pprint import pprint


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def part_test():
    data = read_data("test")
    step, flash_sum = sol(data, 100)
    assert (step, flash_sum) == (100, 1656)
    assert sol(data)[0] == 195


def sol(datat, n=None):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = [int(x) for x in i]

    def foo(y, x):
        flashed.add((y, x))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if y + i < 0 or x + j < 0 or y + i > 9 or x + j > 9:
                        continue
                    data[y + i][x + j] += 1
                    if data[y + i][x + j] > 9 and (y + i, x + j) not in flashed:
                        foo(y + i, x + j)

    flash_sum = 0
    for step in range(1000000):
        flashed = set()
        sf = []
        for iidx, i in enumerate(data):
            for jidx, j in enumerate(i):
                data[iidx][jidx] += 1
                if data[iidx][jidx] > 9:
                    flashed.add((iidx, jidx))
                    sf.append((iidx, jidx))
        for k, h in sf:
            foo(k, h)
        r = 0
        for iidx, i in enumerate(data):
            for jidx, j in enumerate(i):
                if j > 9:
                    r += 1
                    data[iidx][jidx] = 0
        flash_sum += r
        if r == 100:
            return (step + 1, flash_sum)
        if n and step == n - 1:
            return step + 1, flash_sum

    return None


def part_1(datat):
    return sol(datat, 100)[1]


def part_2(datat):
    return sol(datat)[0]


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
