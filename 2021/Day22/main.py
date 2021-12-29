import collections
from collections import defaultdict, Counter, namedtuple
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
    pattern = "{state} x={x1:d}..{x2:d},y={y1:d}..{y2:d},z={z1:d}..{z2:d}"
    match = parse.search(pattern, data)
    return match.named


def part_test():
    data = read_data("test")
    assert part_1(data) == 39
    data = read_data("test2")
    assert part_2(data) == 2758514936282235


def part_1(datat):
    data = datat[:]
    dic = defaultdict(lambda: False)
    for i in data:
        line = parser(i)
        if line["state"] == "on":
            st = True
        else:
            st = False
        for x in range(max(-50, line["x1"]), min(line["x2"] + 1, 51)):
            for y in range(max(line["y1"], -50), min(51, line["y2"] + 1)):
                for z in range(max(line["z1"], -50), min(51, line["z2"] + 1)):
                    dic[(x, y, z)] = st
        # print(dic)
    line["x1"], line["x2"] = -50, 50
    line["y1"], line["y2"] = -50, 50
    line["z1"], line["z2"] = -50, 50
    c = 0
    for x in range(line["x1"], line["x2"] + 1):
        for y in range(line["y1"], line["y2"] + 1):
            for z in range(line["z1"], line["z2"] + 1):
                if dic[(x, y, z)]:
                    c += 1

    print(c)
    return c


def part_2(datat):
    data = datat[:]
    se = set()

    fox = namedtuple("fox", "x1 x2 y1 y2 z1 z2 state")
    for i in data:
        w1 = parser(i)
        sgn = 1 if w1.get("state") == "on" else -1
        w1["state"] = sgn
        # dbg(sgn)
        ns = set()
        for i in se:
            x1, x2 = max(w1["x1"], i.x1), min(w1["x2"], i.x2)
            if x1 > x2:
                continue

            y1, y2 = max(w1["y1"], i.y1), min(w1["y2"], i.y2)
            if y1 > y2:
                continue

            z1, z2 = max(w1["z1"], i.z1), min(w1["z2"], i.z2)
            if z1 > z2:
                continue

            nstate = 0
            for ii in range(-5, 5):
                ww = fox(x1, x2, y1, y2, z1, z2, ii)
                if ww in ns:
                    nstate += ii
                    ns.remove(ww)

            ns.add(fox(x1, x2, y1, y2, z1, z2, nstate - i.state))

        if sgn == 1:
            w = fox(**w1)
            if w in ns:
                dbg(w)
            ns.add(w)

        se = se.union(ns)

    s = sum(
        [
            (w.x2 - w.x1 + 1) * (w.y2 - w.y1 + 1) * (w.z2 - w.z1 + 1) * w.state
            for w in se
        ]
    )
    print(s)
    return s


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
