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


def dbg(*args, lvl="0", **kwargs):
    if lvl in debug:
        print(lvl)
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


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 24
    assert part_2(data) == 93


def get_mn_mx(data):
    mny, mnx = float('inf'), float('inf')
    mxy, mxx = float('-inf'), float('-inf')
    for line in data:
        d = line.split(" -> ")
        for xy in d:
            x, y = list(map(int, xy.split(",")))
            mnx = min(mnx, x)
            mny = min(mny, y)
            mxx = max(mxx, x)
            mxy = max(mxy, y)
    return mny, mnx, mxy, mxx


def part_1(data):
    mny, mnx, mxy, mxx = get_mn_mx(data)

    hor = defaultdict(list)
    ver = defaultdict(list)
    for line in data:
        d = line.split(" -> ")
        d = [tuple(map(int, xy.split(","))) for xy in d]
        for l, r in zip(d[:-1], d[1:]):
            if l[0] == r[0]:

                ver[l[0]].append(tuple(sorted([l[1], r[1]])))
            else:
                hor[l[1]].append(tuple(sorted([l[0], r[0]])))
    # x, y
    # while True:
    def move(pos, mov):
        n_pos = (pos[0]+mov[0], pos[1]+mov[1])
        if n_pos in sand:
            return False

        x, y = n_pos
        if n_pos[0] in ver:
            for y1, y2 in ver[n_pos[0]]:
                if y1 <= y and y2 >= y:
                    return False

        if n_pos[1] in hor:
            for x1, x2 in hor[n_pos[1]]:
                if x1 <= x and x2 >= x:
                    return False
        return True


    generator = (500, 0)
    sand = set()
    grain = [generator[0], generator[1]]        

    # for _ in range(1000):
    while True:
        dbg(grain, lvl='b')
        if move(grain, (0, 1)):
            grain[1] += 1
        elif move(grain, (-1, 1)):
            grain[1] += 1
            grain[0] -= 1
        elif move(grain, (1, 1)):
            grain[1] += 1
            grain[0] += 1
        else:
            sand.add((grain[0], grain[1]))
            grain = [generator[0], generator[1]]        

        if grain[1] > mxy+1:
            break
    return len(sand)
        

def part_2(data):
    mny, mnx, mxy, mxx = get_mn_mx(data)

    hor = defaultdict(list)
    ver = defaultdict(list)
    for line in data:
        d = line.split(" -> ")
        d = [tuple(map(int, xy.split(","))) for xy in d]
        for l, r in zip(d[:-1], d[1:]):
            if l[0] == r[0]:

                ver[l[0]].append(tuple(sorted([l[1], r[1]])))
            else:
                hor[l[1]].append(tuple(sorted([l[0], r[0]])))
    # x, y
    print(len(hor), len(ver))
    # while True:
    def move(pos, mov):
        n_pos = (pos[0]+mov[0], pos[1]+mov[1])
        if n_pos in sand:
            return False
        dbg(lvl='1')

        x, y = n_pos
        if y == mxy+2:
            return False

        if x in ver:
            for y1, y2 in ver[x]:
                if y1 <= y and y2 >= y:
                    return False
        dbg(lvl='2')

        if y in hor:
            for x1, x2 in hor[y]:
                if x1 <= x and x2 >= x:
                    return False
        dbg(lvl='3')

        return True


    generator = (500, 0)
    sand = set()
    grain = [generator[0], generator[1]]        
    dbg(ver, hor, lvl='h')

    # for _ in range(1000):
    while True:
        dbg(grain, lvl='b')
        if move(grain, (0, 1)):
            grain[1] += 1
        elif move(grain, (-1, 1)):
            grain[1] += 1
            grain[0] -= 1
        elif move(grain, (1, 1)):
            grain[1] += 1
            grain[0] += 1
        else:
            sand.add((grain[0], grain[1]))
            grain = [generator[0], generator[1]]        

        if (500, 0) in sand:
            break
    dbg(sand)
    return len(sand)
        


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
