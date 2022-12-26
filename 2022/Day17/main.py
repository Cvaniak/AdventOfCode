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
    assert part_1(data) == 3068
    assert part_2(data) == 1514285714288

blocks = [
        ["####"],
[
".#.",
"###",
".#."
 ],
[
"..#",
"..#",
"###",
 ]
,
["#",
"#",
"#",
"#"],
["##",
 "##"],
        ]

def part_1(data):
    data = data[0]
    board = set((0,x) for x in range(7))
    lr = 0
    last_h = 0

    @functools.lru_cache()
    def get_new(block_idx):
        s = set()
        for idx, i in enumerate(blocks[block_idx][::-1]):
            for idxj, j in enumerate(i):
                if j == "#":
                    s.add((idx, idxj))
        return s

    def add_move(block, move):       
        s1 = set()
        for point in block:
            if point[1]+move[1] < 0 or point[1]+move[1] >= 7:
                return False
            s1.add((point[0]+move[0], point[1]+move[1])) 
        if len(s1.intersection(board)):
            return False
        block.clear()
        block.update(s1)
        return True
        

    def drop(block_idx):
        nonlocal lr, last_h, board
        block = get_new(block_idx).copy()
        add_move(block, (last_h+4, 2))

        while True:
            if data[lr%len(data)] == "<":
                add_move(block, (0, -1))
            else:
                add_move(block, (0, 1))
            lr += 1
            if not add_move(block, (-1, 0)):
                last_h = max([h for h, _ in block] + [last_h])
                board.update(block)
                break

    def print_grid(b):
        for i in range(44, -1, -1):
            for j in range(7):
                if (i, j) in b:
                    print("#", end="")
                else:
                    print(".", end="")

    for i in range(2022):
        drop(i%len(blocks))

    return last_h


def part_2(data):
    data = [ 1 if x == ">" else -1 for x in data[0]]
    board = set((0,x) for x in range(7))
    lr = 0
    last_h = 0

    @functools.lru_cache()
    def get_new(block_idx):
        s = set()
        for idx, i in enumerate(blocks[block_idx][::-1]):
            for idxj, j in enumerate(i):
                if j == "#":
                    s.add((idx, idxj))
        return s

    def add_move(block, move):       
        s1 = set()
        for point in block:
            if point[1]+move[1] < 0 or point[1]+move[1] >= 7:
                return False
            s1.add((point[0]+move[0], point[1]+move[1])) 
        if len(s1.intersection(board)):
            return False
        block.clear()
        block.update(s1)
        return True
        

    def drop(block_idx):
        nonlocal lr, last_h, board
        block = get_new(block_idx).copy()
        add_move(block, (last_h+4, 2))
        while True:
            add_move(block, (0, data[lr]))
            lr = (lr+1)%len(data)
            if not add_move(block, (-1, 0)):
                new_h = max([h for h, _ in block] + [last_h])
                diff = new_h - last_h 
                last_h = new_h
                board.update(block)
                break
        return block_idx, lr, diff

    i = 0
    memo = dict()
    queue = deque([], maxlen=32)
    n = 1000000000000
    add_height = 0
    while i < n:
        idx, lr, diff = drop(i%len(blocks))
        queue.append(diff)
        last_heights = tuple(queue)
        key = (idx, lr, last_heights)
        if key in memo:
            lh, time = memo[key]
            diff_h, diff_t = last_h-lh, i-time

            repeats = (n-i)//diff_t

            add_height += diff_h*repeats
            i += diff_t*repeats

        memo[key] = (last_h, i)
        i += 1

    return last_h+add_height


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
