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
    # assert part_1(data, 1) == """6594254334
    # 3856965822
    # 6375667284
    # 7252447257
    # 7468496589
    # 5278635756
    # 3287952832
    # 7993992245
    # 5957959665
    # 6394862637
    # """
    # assert part_1(data, 2) == """8807476555
    # 5089087054
    # 8597889608
    # 8485769600
    # 8700908800
    # 6600088989
    # 6800005943
    # 0000007456
    # 9000000876
    # 8700006848
    # """
    # assert part_1(data, 3) == """0050900866
    # 8500800575
    # 9900000039
    # 9700000041
    # 9935080063
    # 7712300000
    # 7911250009
    # 2211130000
    # 0421125000
    # 0021119000
    # """
    # assert part_1(data, 100) == """0397666866
    # 0749766918
    # 0053976933
    # 0004297822
    # 0004229892
    # 0053222877
    # 0532222966
    # 9322228966
    # 7922286866
    # 6789998766
    # """, 1656
    assert part_1(data, 100) == 1656
    assert part_2(data, 100) == 195


def part_1(datat, n):
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
                    #     foo(y+i, x+j, (y+i, x+j))

    r = 0
    for _ in range(n):
        flashed = set()
        sf = []
        for iidx, i in enumerate(data):
            for jidx, j in enumerate(i):
                data[iidx][jidx] += 1
                if data[iidx][jidx] > 9:
                    flashed.add((iidx, jidx))
                    sf.append((iidx, jidx))
        # pprint(data)
        d = defaultdict(tuple)
        for k, h in sf:
            foo(k, h)
        # pprint(data)
        for iidx, i in enumerate(data):
            for jidx, j in enumerate(i):
                if j > 9:
                    r += 1
                    data[iidx][jidx] = 0
        # pprint(data)
        # print()

    w = ""
    for idx, i in enumerate(data):
        for j in i:
            w += str(j)
        w += "\n"
    # print(w)
    return r


def part_2(datat, n):
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
                    #     foo(y+i, x+j, (y+i, x+j))

    for step in range(1000000):
        flashed = set()
        sf = []
        for iidx, i in enumerate(data):
            for jidx, j in enumerate(i):
                data[iidx][jidx] += 1
                if data[iidx][jidx] > 9:
                    flashed.add((iidx, jidx))
                    sf.append((iidx, jidx))
        # pprint(data)
        d = defaultdict(tuple)
        for k, h in sf:
            foo(k, h)
        # pprint(data)
        r = 0
        for iidx, i in enumerate(data):
            for jidx, j in enumerate(i):
                if j > 9:
                    r += 1
                    data[iidx][jidx] = 0
        if r == 100:
            # print(step)
            return step + 1
        # pprint(data)

        # print()
    print(None)
    return None


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data, 100))
    print(part_2(data, 100))
