import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import bisect
import math
import argparse
from rich import print
import parse
import operator
from heapq import heappop, heappush

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


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def part_test():
    data = read_data("test")
    assert part_1(data) == 58
    assert part_2(data) == None


def pri(south, east, n, m):
    zeros = [["."] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if (i, j) in south:
                zeros[i][j] = "v"
            elif (i, j) in east:
                zeros[i][j] = ">"
        zeros[i] = "".join(zeros[i])
    zeros.append("." * m)
    zeros.append("." * m)
    zeros.append("." * m)
    return zeros


def part_1(datat):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = list(
            map(int, i.replace(".", "0").replace(">", "1").replace("v", "2"))
        )
    dbg(data, lvl="1")

    east = set()
    south = set()
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 1:
                east.add((i, j))
            elif data[i][j] == 2:
                south.add((i, j))

    n, m = len(data), len(data[0])
    c = 0
    while True:
        neast = set()
        nsouth = set()
        for y, x in east:
            if (y, (x + 1) % m) in east or (y, (x + 1) % m) in south:
                neast.add((y, x))
            else:
                neast.add((y, (x + 1) % m))

        for y, x in south:
            if ((y + 1) % n, x) in neast or ((y + 1) % n, x) in south:
                nsouth.add((y, x))
            else:
                nsouth.add(((y + 1) % n, x))
        c += 1
        dbg(east, neast, lvl="3")
        if c % 10 == 0:
            dbg(pri(nsouth, neast, n, m), lvl="4")
        if neast == east and nsouth == south:
            break
        south = set(nsouth)
        east = set(neast)
        dbg(c, lvl="c")
    return c


def part_2(datat):
    data = datat[:]


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
