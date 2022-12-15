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
    pattern = "Sensor at x={sx:d}, y={sy:d}: closest beacon is at x={bx:d}, y={by:d}"
    match = parse.parse(pattern, data)
    return match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data, 10) == 26
    assert part_2(data, 20) == 56000011

def dist(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def part_1(data, end_y):
    result = set()
    beacon = set()
    for line in data:
        par = parser(line)
        s, b = (par["sy"],par["sx"]), (par["by"],par["bx"])
        if b[0] == end_y:
            beacon.add(b[1])

        distance = dist(s, b)
        y_dist = dist(s, (end_y, s[1]))
        change = distance - y_dist
        for i in range(change+1):
            result.add((s[1]-i))
            result.add((s[1]+i))
        
    result ^= beacon

    return len(result)


def part_2(data, max_s):
    result = 0
    sensors = dict()
    for line in data:
        par = parser(line)
        s, b = (par["sy"],par["sx"]), (par["by"],par["bx"])
        sensors[s] = dist(s, b)

    q =  deque([((0,0), (max_s, max_s))])
    # for i in range(10):
    while q:
        c1, c3 = q.popleft()
        c2, c4 = (c1[0], c3[1]), (c3[0], c1[1])
        # dbg(c1, c2, c3, c4)
        is_covered = False
        for sensor in sensors:
            if all(dist(corner, sensor) <= sensors[sensor] for corner in (c1, c2,c3,c4)):
                is_covered = True
                break
        if is_covered:
            continue



        if dist(c1, c3) == 0:
            dbg(c1)
            result = c1
            break
        if c3[0]-c1[0] > c3[1]-c1[1]:
            ...
            ca, cb = ((c3[0]+c1[0])//2, c3[1]), ((c3[0]+c1[0])//2+1, c1[1])

            q.append((c1, ca))
            q.append((cb, c3))
        else:
            ...
            ca, cb = (c3[0], (c3[1]+c1[1])//2), (c1[0], (c3[1]+c1[1])//2+1)
            q.append((c1, ca))
            q.append((cb, c3))

        # dbg()
        
        # q.append(())

    # x*4_000_000 + y
    return result[1]*4_000_000+result[0]

if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:], 2_000_000))
    print(part_2(data[:], 4_000_000))
