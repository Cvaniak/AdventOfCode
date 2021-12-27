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


def load_int_lines(datat):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = [x for x in i]
    return data


def part_test():
    assert x4("101111111000101000") == (15, 2021)
    assert part_1(["38006F45291200"]) == 9
    assert part_1(["EE00D40C823060"]) == 14
    assert part_1(["8A004A801A8002F478"]) == 16
    assert part_1(["620080001611562C8802118E34"]) == 12
    assert part_1(["C0015000016115A2E0802F182340"]) == 23
    assert part_1(["A0016C880162017C3686B18A3D4780"]) == 31
    assert part_2(["C200B40A82"]) == 3
    assert part_2(["04005AC33890"]) == 54
    assert part_2(["D8005AC2A8F0"]) == 1
    assert part_2(["F600BC2D8F"]) == 0


def hex_to_bin(data):
    d = [int(x, 16) for x in data]
    r = ""
    for i in d:
        r += "{0:04b}".format(i)
    return r


def x4(data):
    r = 0
    numbers = ""
    while data[r] != "0":
        numbers += data[r + 1 : r + 5]
        r += 5
    numbers += data[r + 1 : r + 5]
    r += 5
    return r, int(numbers, 2)


def foo(data):
    a = 0
    V = int(data[a : a + 3], 2)
    a += 3
    T = int(data[a : a + 3], 2)
    a += 3
    if T == 4:
        b, numbers = x4(data[a:])
        a += b
        return V, a, numbers
    else:
        I = data[a]
        a += 1
        numbers = []
        if I == "0":
            L = data[a : a + 15]
            a += 15
            aL = int(L, 2) + a
            while a < aL:
                xV, xA, xNumbers = foo(data[a:])
                a += xA
                V += xV
                numbers.append(xNumbers)
        else:
            L = data[a : a + 11]
            a += 11
            for i in range(int(L, 2)):
                xV, xA, xNumbers = foo(data[a:])
                a += xA
                V += xV
                numbers.append(xNumbers)

        if T == 0:
            numbers = sum(numbers)
        elif T == 1:
            numbers = math.prod(numbers)
        elif T == 2:
            numbers = min(numbers)
        elif T == 3:
            numbers = max(numbers)
        elif T == 5:
            numbers = 1 if numbers[0] > numbers[1] else 0
        elif T == 6:
            numbers = 1 if numbers[0] < numbers[1] else 0
        elif T == 7:
            numbers = 1 if numbers[0] == numbers[1] else 0

        return V, a, numbers


def part_1(datat):
    data = datat[:][0]
    data = hex_to_bin(data)
    V, A, Numbers = foo(data)
    return V


def part_2(datat):
    data = datat[:][0]
    data = hex_to_bin(data)
    V, A, Numbers = foo(data)
    return Numbers


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
