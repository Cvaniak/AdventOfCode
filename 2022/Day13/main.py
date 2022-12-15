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
import json

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
    assert part_1(data) == 13
    assert part_2(data) == None


def list_wrap(x):
    if isinstance(x, int):
        return list([x])
    else:
        return x


def foo(x, y):
    dbg(x, y, lvl='x')

    for i in range(len(x)):
        if i >= len(y):
            return False
        if all(isinstance(w, list) for w in [x[i], y[i]]):
            res = foo(x[i], y[i])
            if res is None:
                continue
            return res
        elif all(isinstance(w, int) for w in [x[i], y[i]]):
            if x[i] > y[i]:
                return False
            if x[i] < y[i]:
                return True
        else:
            res = foo(list_wrap(x[i]), list_wrap(y[i]))
            if res is None:
                continue
            return res
    if len(x) == len(y):
        return None
    return True

def part_1(data):
    result = 0
    for idx in range(0, len(data), 3): 
        a = data[idx]
        b = data[idx+1]
        a, b = json.loads(a), json.loads(b)
        dbg(idx//3+1, lvl='b')
        if foo(a, b):
            dbg(a, b, idx//3+1, lvl='a')
            result += idx//3+1

    dbg(result, lvl='r')
    return result


def part_2(data):
    data = [json.loads(x) for x in data if x != '']
    data.append([[2]])
    data.append([[6]])
    data.sort(key=lambda x ,y: foo(x, y))
    print(data)



if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    # print(part_2(data[:]))
