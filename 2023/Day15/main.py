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
from math import lcm
from typing import Optional

import parse
from rich import print
import inspect

debug_space = False


class Debuger:
    levels: set[str] = set()
    excluded_parts: set[str] = set()
    state: bool = True

    def _print(self, *args, lvl="", **kwargs):
        if not self.state:
            return

        if self.levels and lvl not in self.levels:
            return

        c1, c2 = inspect.stack()[1].function, inspect.stack()[2].function
        if c1 in self.excluded_parts or c2 in self.excluded_parts:
            return

        print(f" ▄▄▄▄▄ {lvl} ▄▄▄▄▄ ")
        print("  ", end="")
        print(*args, **kwargs)

    def __getattr__(self, lvl):
        return functools.partial(self._print, lvl=lvl)

    def __call__(self, *args, **kwargs):
        self._print(lvl="0", *args, **kwargs)

    def set_levels(self, lvls):
        if not lvls:
            return
        for lvl in lvls.split(","):
            self.levels.add(lvl)

    def exclude_parts(self, parts):
        for part in parts:
            self.excluded_parts.add(f"part_{part}")

    def turn_on_off(self, state):
        self.state = state


dbg = Debuger()


def set_debuger():
    global dbg
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", nargs="?", default=None, help="Debug List")
    parser.add_argument(
        "-n", "--nodebug", action="store_false", help="Remove default debug"
    )
    parser.add_argument(
        "-p",
        "--excludepart",
        nargs="?",
        default="",
    )
    args = parser.parse_args()
    dbg.set_levels(args.debug)
    dbg.turn_on_off(args.nodebug)
    dbg.exclude_parts(args.excludepart)


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


def load_int_lines(data):
    data = data[:]
    for idx, i in enumerate(data):
        data[idx] = [int(x) for x in i]
    return data


def load_ints_seperated(data, sep=","):
    return list(map(int, data.split(sep)))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 1320
    assert part_2(data) == 145


def part_1(data):
    data = data[0].split(',')
    ans = 0
    for text in data:
        tmp = 0
        for char in text:
            tmp += ord(char)
            tmp = (tmp*17)%256
        ans += tmp

    dbg(ans)
    return ans


@dataclass
class Linked:
    label: str
    val: int
    prv: Optional["Linked"]
    nxt: Optional["Linked"]


def hash(text):
    tmp = 0
    for char in text:
        tmp += ord(char)
        tmp = (tmp*17)%256
    return tmp

def d_labels(labels):
    for idx, i in enumerate(labels):
        if i.nxt == None:
            continue
        dbg.l(idx)
        s = ""
        while i != None:
            s += " (" + i.label + " " + str(i.val) + ") "
            i = i.nxt
        dbg.l(s)

def part_2(data):
    data = data[0].split(',')
    boxes = [[] for _ in range(256)]
    labels = dict()
    for text in data:
        if text[-1] == "-":
            label, hsh = text[:-1], hash(text[:-1])
            if label in boxes[hsh]:
                boxes[hsh].remove(label)

        else:
            label, hsh, foc = text[:-2], hash(text[:-2]), text[-1]
            if label not in boxes[hsh]:
                boxes[hsh].append(label)
            labels[label] = int(foc)

        # dbg()
    # d_labels(boxes)

    ans = 0
    for idx, label in enumerate(boxes, 1):
        i = 0
        tmp = 0
        for x in label:
            i += 1
            tmp += idx*i*labels[x]
        ans += tmp
    dbg(ans)

    return ans




if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
