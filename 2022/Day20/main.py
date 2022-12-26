from __future__ import annotations
import argparse
import bisect
import collections
from dataclasses import dataclass
import functools
import itertools
import math
import operator
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from itertools import combinations, permutations, product
from typing import Optional

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
    assert part_1(data) == 3
    assert part_2(data) == 1623178306


@dataclass
class Linking:
    val: int
    prev: Optional[Linking]
    next: Optional[Linking]


def part_1(data):
    link_list = [Linking(int(data[0]), None, None)]

    for i in data[1:]:
        node = Linking(int(i), link_list[-1], None)
        link_list[-1].next = node
        link_list.append(node)

    link_list[-1].next = link_list[0]
    link_list[0].prev = link_list[-1]

    n = len(data)

    node_0 = None
    for link in link_list:
        ...
        if link.val == 0:
            node_0 = link
            continue

        prev, next = link.prev, link.next
        link.prev, link.next = None, None

        prev.next = next
        next.prev = prev

        val = link.val % n
        if n - val < val:
            val = val - n

        if val < 0:
            for i in range(abs(val)):
                prev = prev.prev
            a, b = prev, prev.next
        else:
            for i in range(val):
                next = next.next
            a, b = next.prev, next

        a.next = link
        link.prev = a

        b.prev = link
        link.next = b

    result = 0
    for _ in range(3):
        for _ in range(1000 % n):
            node_0 = node_0.next
        result += node_0.val
    print(result)
    return result


@dataclass
class Linking2:
    val: int
    n_val: int
    prev: Optional[Linking2]
    next: Optional[Linking2]


def part_2(data):
    n = len(data)
    link_list = [
        Linking2((int(data[0]) * 811589153) % (n - 1), int(data[0]), None, None)
    ]

    for i in data[1:]:
        node = Linking2((int(i) * 811589153) % (n - 1), int(i), link_list[-1], None)
        link_list[-1].next = node
        link_list.append(node)

    link_list[-1].next = link_list[0]
    link_list[0].prev = link_list[-1]

    node_0 = None
    for _ in range(10):
        for link in link_list:
            if link.n_val == 0:
                node_0 = link

            prev, next = link.prev, link.next
            link.prev, link.next = None, None

            prev.next = next
            next.prev = prev

            val = link.val
            if n - 1 - val < val:
                val = val - n + 1

            if val < 0:
                for i in range(abs(val)):
                    prev = prev.prev
                a, b = prev, prev.next
            else:
                for i in range(val):
                    next = next.next
                a, b = next.prev, next

            a.next = link
            link.prev = a

            b.prev = link
            link.next = b

    result = 0
    for _ in range(3):
        for _ in range(1000 % n):
            node_0 = node_0.next
        result += node_0.n_val * 811589153
        print(node_0.n_val * 811589153)
    print(result)
    return result


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
