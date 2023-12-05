import argparse
import bisect
import collections
import functools
import itertools
import math
import operator
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from itertools import combinations, permutations, product

import parse
from rich import print

debug = set("0")
debug_space = False


def dbg(*args, lvl="0", p_lvl=True, **kwargs):
    if lvl in debug:
        if p_lvl:
            print(f"Lvl: {lvl}")
        print(*args, **kwargs)
        if debug_space:
            print()


def set_debuger():
    global debug, debug_space
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", nargs="?", const="0", default="0", help="Debug List"
    )
    parser.add_argument(
        "-n", "--nodebug", action="store_true", help="Remove default debug"
    )
    parser.add_argument(
        "-s", "--addspace", action="store_true", help="Space between debug"
    )
    args = parser.parse_args()
    debug.update({x for x in args.debug})
    if args.nodebug:
        debug.remove("0")
    if args.addspace:
        debug_space = True


# ===== ^^ DEBUGER ^^ =====

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


def load_int_spaces(data):
    return list(map(int, data.split(" ")))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 35
    assert part_2(data) == 46


def part_1(data):
    seeds = load_int_spaces(data[0].partition(": ")[2])
    n = len(data)
    i = 3
    curr_map = 0

    def foo():
        nonlocal seeds
        dbg(mapper)
        seeds.sort()
        dbg(seeds)
        new_seeds = []
        for seed in seeds:
            x = bisect.bisect_right(mapper, seed, key=lambda x: x[0])
            if x == 0:
                new_seeds.append(seed)
                dbg(seed, seed, p_lvl=False)
                continue

            x = mapper[x - 1]
            if seed < x[0] + x[2]:
                diff = seed - x[0]
                new_seeds.append(x[1] + diff)
                dbg(x[1], diff, seed, x[1] + diff, p_lvl=False)
            else:
                new_seeds.append(seed)
                dbg(seed, seed, p_lvl=False)
        seeds = new_seeds

    mapper = []
    while i < n:
        if len(data[i]) == 0:
            foo()
            mapper = []
            i += 2
            continue
        loaded = load_int_spaces(data[i])
        rang = tuple([loaded[1], loaded[0], loaded[2]])
        bisect.insort(mapper, rang)
        i += 1
    foo()

    return min(seeds)


def part_2(data):
    seeds = load_int_spaces(data[0].partition(": ")[2])

    seeds = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    total = sum(x[1] - x[0] for x in seeds)
    n = len(data)
    i = 3

    def foo():
        nonlocal seeds, mapper
        seeds.sort(key=lambda x: x[0])

        new_mapper = []
        mapper.insert(0, (float("-inf"), mapper[0][0], 0))
        mapper.append((mapper[-1][1], float("inf"), 0))
        for a, b in zip(mapper[:-1], mapper[1:]):
            new_mapper.append(a)
            if b[0] - a[1] > 0:
                new_mapper.append((a[1], b[0], 0))
        new_mapper.append((new_mapper[-1][1], float("inf"), 0))
        mapper = new_mapper
        dbg(mapper, lvl="4")

        dbg(seeds, lvl="1")
        dbg(mapper, lvl="2")
        new_seeds = []
        nk = len(seeds)
        k = 0
        for m in mapper:
            st, end, diff = m
            dbg(st, end, diff, lvl="3")
            while k < nk and seeds[k][0] < end:
                dbg(seeds[k], lvl="3", p_lvl=False)
                if seeds[k][1] < end:
                    new_seeds.append((seeds[k][0] + diff, seeds[k][1] + diff))
                    k += 1
                else:
                    new_seeds.append((seeds[k][0] + diff, end + diff))
                    seeds[k] = (end, seeds[k][1])
                    break

        dbg(new_seeds, lvl="3", p_lvl=False)

        seeds = new_seeds

    mapper = []
    while i < n:
        if len(data[i]) == 0:
            foo()
            mapper = []
            i += 2
            continue
        loaded = load_int_spaces(data[i])
        rang = tuple([loaded[1], loaded[1] + loaded[2], loaded[0] - loaded[1]])
        bisect.insort(mapper, rang)
        i += 1
    foo()
    dbg(seeds, lvl="f")

    assert total == sum(x[1] - x[0] for x in seeds)
    dbg(min(seeds)[0], lvl="f")

    return min(seeds)[0]


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
