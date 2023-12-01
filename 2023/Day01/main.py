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
    assert part_1(data) == 142
    data = read_data("test2")
    assert part_2(data) == 281


def part_1(data):
    sm = 0
    for line in data:
        line = [x for x in line if x.isnumeric()]
        num = int(line[0]) * 10 + int(line[-1])
        sm += num
    return sm


def part_2(data):
    nums = "one, two, three, four, five, six, seven, eight, nine".split(", ")
    rev_nums = [x[::-1] for x in nums]

    sm = 0

    def t_find(val, t_nums):
        n = len(val)
        line_nums = [(idx, x) for idx, x in enumerate(val) if x.isnumeric()]
        if line_nums:
            first_idx, first_val = line_nums[0]
        else:
            first_idx, first_val = n, -1

        letnum = -1
        letpos = n
        for idx, num in enumerate(t_nums):
            w = val.find(num, 0, first_idx)
            if w != -1 and w < letpos:
                letnum = idx + 1
                letpos = w
        if letnum == -1:
            return int(first_val)
        elif first_val == -1:
            return int(letnum)
        else:
            return int(first_val) if first_idx < letpos else int(letnum)

    for line in data:
        a = 10 * t_find(line, nums)
        b = t_find(line[::-1], rev_nums)
        sm += a + b
    return sm


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
