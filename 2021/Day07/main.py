import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import math


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def part_test():
    data = read_data("test")
    # assert part_1(data) == 37
    assert part_1(data) == 168


def part_1(data):
    data = list(map(int, data[0].split(",")))
    mx = max(data)
    mn = min(data)
    c = defaultdict(int)
    for i in range(1, mx * 1000):
        c[i] = c[i - 1] + i

    r = mx * 10000000
    for i in range(mn, mx * 10):
        m = 0
        for j in data:
            m += c[abs(j - i)]
        r = min(r, m)
    return r


def part_2(data):
    ...


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    # print(part_2(data))
