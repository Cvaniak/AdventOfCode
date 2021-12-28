import collections
from collections import defaultdict, Counter
import functools
from functools import lru_cache
import itertools
from itertools import product, permutations, combinations
import bisect
import math
import argparse
from rich import print
import parse
import operator
from heapq import heappop, heappush
import dataclasses

debug = False


def dbg(*args, **kwargs):
    if debug:
        print(*args, **kwargs)


def set_debuger():
    global debug
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug")
    args = parser.parse_args()
    debug = args.debug


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
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


def part_test():
    data = read_data("test")
    assert part_1(data, 4, 8) == 739785
    assert part_2(data, 4, 8) == 444356092776315


def part_1(datat, a, b):
    # a, b = 10, 2
    a1, b1 = 0, 0
    i = 0
    ab = True
    ir = 0
    while a1 < 1000 and b1 < 1000:
        for _ in range(3):
            i += 1
            ir += i

        if ab:
            a = (a + ir) % 10
            if not a:
                a1 += 10
            else:
                a1 += a
        else:
            b = (b + ir) % 10
            if not b:
                b1 += 10
            else:
                b1 += b

        ir = 0
        ab = not ab

    print(a, b, i, a1, b1)
    return min(a1, b1) * i


def part_2(datat, a, b):

    @lru_cache(None)
    def how_many(points, position):
        pos = position + points
        pos = (pos % 10) + 10 * (pos % 10 == 0)
        return pos

    @lru_cache(None)
    def sol(p1, p2, who_play):
        c = Counter()

        for roll in itertools.product([1, 2, 3], repeat=3):
            roll = sum(roll)

            if who_play:
                p = p1
                pos = how_many(roll, p[1])
                p = (p[0] + pos, pos)
                if p[0] >= 21:
                    c[False] += 1
                else:
                    s = sol(p, p2, False)
                    c.update(s)
            else:
                p = p2
                pos = how_many(roll, p[1])
                p = (p[0] + pos, pos)
                if p[0] >= 21:
                    c[True] += 1
                else:
                    s = sol(p1, p, True)
                    c.update(s)
        return c


    p1 = (0, a)
    p2 = (0, b)
    r = sol(p1, p2, True)
    print(r)
    print(r.most_common(1)[0])
    return r.most_common(1)[0][1]


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data, 10, 2))
    print(part_2(data, 10, 2))
