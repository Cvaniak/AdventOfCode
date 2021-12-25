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
    # assert part_1(data) == None
    assert part_2(data) == 230


def part_1(data):
    a = [0] * len(data[0])
    b = [0] * len(data[0])
    for i in data:
        for k, j in enumerate(i):
            if j == "0":
                a[k] += 1
            else:
                b[k] += 1
    print(a)
    print(b)
    r = ""
    r1 = ""
    for i in range(len(a)):
        if a[i] > b[i]:
            r += "0"
            r1 += "1"
        else:
            r += "1"
            r1 += "0"

    print(int(r))
    print(int(r))

    print(int(r, 2))
    print(int(r1, 2))
    print(int(r, 2) * int(r1, 2))

    ...


def part_2(data):
    a = [0] * len(data[0])
    b = [0] * len(data[0])
    for i in data:
        for k, j in enumerate(i):
            if j == "0":
                a[k] += 1
            else:
                b[k] += 1
    print(a, b)
    ds = set(data)
    ds1 = set(data)
    print("-----")
    z, z1 = "", ""
    for i in range(len(data[0])):
        ds2 = ds.copy()
        print()
        a[i] = 0
        b[i] = 0
        for w in ds:
            if w[i] == "0":
                a[i] += 1
            else:
                b[i] += 1

        for j in ds2:
            if a[i] == b[i]:
                if j[i] == "0":
                    ds.remove(j)
            elif a[i] > b[i]:
                if j[i] == "1":
                    ds.remove(j)
                else:
                    ...
            else:
                if j[i] == "0":
                    ds.remove(j)
        if len(ds) == 1:
            for d in ds:
                z = d
            break
        print(ds)
    ds = ds1
    for i in range(len(data[0])):
        a[i] = 0
        b[i] = 0
        for w in ds:
            if w[i] == "0":
                a[i] += 1
            else:
                b[i] += 1

        ds2 = ds.copy()
        for j in ds2:
            if a[i] == b[i]:
                if j[i] == "1":
                    ds.remove(j)
            elif a[i] > b[i]:
                if j[i] == "0":
                    ds.remove(j)
                else:
                    ...
            else:
                if j[i] == "1":
                    ds.remove(j)
        print(ds)
        if len(ds) == 1:
            for d in ds:
                z1 = d
            break

    print(int(z, 2) * int(z1, 2))
    print(int(z, 2))
    print(z)
    print(int(z1, 2))
    return int(z, 2) * int(z1, 2)


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    # print(part_1(data))
    print(part_2(data))
