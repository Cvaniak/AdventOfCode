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
    pattern = "fold along {axis}={number:d}"
    match = parse.search(pattern, data)
    return match.named["axis"], match.named["number"]


def part_test():
    data = read_data("test")
    assert part_1(data, 18) == 17
    assert part_2(data, 18) == 16


def part_1(datat, n):
    data = datat[:]
    dat = []
    for i in range(n):
        dat.append(list(map(int, datat[i].split(","))))

    fold = parser(data[n + 1])
    # print(dat)
    # print(fold)
    s = set()
    for i in dat:
        if fold[0] == "y":
            if i[1] > fold[1]:
                s.add((i[0], 2 * fold[1] - i[1]))
            else:
                s.add((i[0], i[1]))
        else:
            if i[0] > fold[1]:
                s.add((2 * fold[1] - i[0], i[1]))
            else:
                s.add((i[0], i[1]))

    # print(s)
    print(len(s))
    return len(s)


def part_2(datat, n):
    data = datat[:]
    dat = []
    for i in range(n):
        dat.append(tuple(map(int, datat[i].split(","))))

    folds = []
    for i in data[n + 1 :]:
        folds.append(parser(i))

    # print(dat)
    # print(folds)
    s1 = set(dat)
    # print(s1)
    mxx, mxy = 10000, 10000
    for fold in folds:
        s = set()
        for i in s1:
            if fold[0] == "y":
                if i[1] > fold[1]:
                    s.add((i[0], 2 * fold[1] - i[1]))
                else:
                    s.add((i[0], i[1]))
                mxy = min(mxy, fold[1])
            else:
                if i[0] > fold[1]:
                    s.add((2 * fold[1] - i[0], i[1]))
                else:
                    s.add((i[0], i[1]))
                mxx = min(mxx, fold[1])
        s1 = s

    # print(s)
    print(len(s))
    for i in range(mxy):
        for j in range(mxx):
            if (j, i) in s:
                print("#", end="")
            else:
                print(".", end="")
        print()
    return len(s)


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data, 799))
    print(part_2(data, 799))
