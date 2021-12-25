import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import math
import bisect


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def part_test():
    data = read_data("test")
    # assert part_1(data) == 5934
    assert part_2(data) == 26984457539


def part_1(data):
    data = list(map(int, data[0].split(",")))
    data.sort()
    print(data)
    for _ in range(80):
        datac = data[:]
        w = 0
        ne6 = 0
        for idx, i in enumerate(data):
            # print(datac)
            if i == 0:
                w += 1
                datac.pop(0)
                ne6 += 1
            else:
                datac[idx - w] -= 1
        data = datac[:]
        for i in range(ne6):
            bisect.insort(data, 6)
        for i in range(ne6):
            data.append(8)
        # print(data, "---")
    print(len(data))
    return len(data)


def part_2(data):
    data = list(map(int, data[0].split(",")))
    data.sort()
    data = Counter(data)
    print(data)
    for _ in range(256):
        # datac = data[:]
        w = data[0]
        for i in range(1, 10):
            data[i - 1] = data[i]
        data[6] += w
        data[8] += w
    r = sum([data[x] for x in data])
    print(r)
    return r


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    # print(part_1(data))
    print(part_2(data))
