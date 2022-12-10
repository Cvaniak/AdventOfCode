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
    data = read_data("test_1")
    assert part_1(data) == 13140
    assert part_2(data) == None


def part_1(data):
    ...
    cycle = 0
    value = 1
    n_val = 0
    result = 0
    moment = [20, 60, 100, 140, 180, 220]
    for line in data:
        value += n_val
        n_val = 0
        if line.startswith("noop"):
            ...
        else:
            _, num = line.split(" ")
            n_val = int(num)
            cycle += 1
        if moment and cycle == moment[0]:
            result += moment.pop(0)*value
        cycle += 1
        if moment and cycle == moment[0]:
            result += moment.pop(0)*value
    return result





def part_2(data):
    cycle = -1
    value = 0
    n_val = 0
    result = ["."]*260 
    for line in data:
        value += n_val
        n_val = 0
        if line.startswith("noop"):
            ...
        else:
            _, num = line.split(" ")
            n_val = int(num)
            cycle += 1
            if  value <= cycle%40 and cycle%40 <= value+2:
                result[cycle] = "#"
            else:
                result[cycle] = "."
            #     result += moment.pop(0)*value

        # if cycle%40 == 0:
        #     value += 40
        cycle += 1
        if value <= cycle%40 and cycle%40 <= value+2:
            result[cycle] = "#"
        else:
            result[cycle] = "."
        # if cycle%40 == 0:
        #     value += 40
        # if moment and cycle == moment[0]:
        #     result += moment.pop(0)*value
        #     print(cycle, value, result)

    for i in range(7):
        print("".join(result[40*i:40*i+40]))


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
