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

def parse_command(data):
    pattern = "$ cd {cmd}"
    match = parse.search(pattern, data)
    return match.named

def parse_output(data):
    pattern = "{size:d} {name}"
    match = parse.parse(pattern, data)
    return match.named

# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 95437
    assert part_2(data) == 24933642


def part_1(data):
    current = [" "]
    out_put = defaultdict(int)
    for d in data:
        if d.startswith("$ ls"):
            ...
        elif d.startswith("dir"):
            ...
        elif d.startswith("$"):
            cmd = parse_command(d)
            if cmd["cmd"] == ".":
                current.pop()
            elif cmd["cmd"] == "/":
                current = [""]
            else:
                sig, cd, cmd = d.split(" ") 
                current.append(cmd)

        else:
            file = parse_output(d)
            out_put[tuple(current+[file["name"]])] += file["size"]

    res_output = defaultdict(int)

    for dir, file_size in out_put.items():
        for j in range(len(dir)):
            res_output[dir[:j]] += file_size

    result = sum([x for x in res_output.values() if x <= 100000])    
    return result
    

def part_2(data):
    current = [" "]
    out_put = defaultdict(int)
    for d in data:
        if d.startswith("$ ls"):
            ...
        elif d.startswith("dir"):
            ...
        elif d.startswith("$"):
            cmd = parse_command(d)
            if cmd["cmd"] == ".":
                current.pop()
            elif cmd["cmd"] == "/":
                current = [""]
            else:
                sig, cd, cmd = d.split(" ") 
                current.append(cmd)

        else:
            file = parse_output(d)
            out_put[tuple(current+[file["name"]])] += file["size"]

    res_output = defaultdict(int)

    for dir, file_size in out_put.items():
        for j in range(len(dir)):
            res_output[dir[:j]] += file_size

    # result = sum([x for x in res_output.values() if x <= 100000])    

    a, b = 30000000, 70000000

    needed = b - res_output[("", )]
    needed = a - needed
    w = [ x for x in res_output.values() if x >= needed ]
    w.sort()
    dbg(w, w[0], lvl="w")

    return w[0]


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
