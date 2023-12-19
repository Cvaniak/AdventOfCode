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
from math import lcm

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
    assert part_1(data) == 19114
    assert part_2(data) == 167409079868000


import json


def part_1(data):
    parts = []
    rules = {}
    for line in data:
        if line and line[0] == "{":
            line = line.replace("=", '":').replace("{", '{"').replace(",", ',"')
            parts.append(json.loads(line))

        elif line:
            name, rule = line.split("{")
            rule = rule[:-1].split(",")
            if len(rule[-1]) < 2 or rule[-1][1] not in "<>":
                rule[-1] = "x>0:" + rule[-1]
            rules[name] = rule

    ans = 0
    for part in parts:
        curr = "in"
        while curr not in "AR":
            for rule in rules[curr]:
                x, s = rule[0], rule[1]
                value, next = rule[2:].split(":")
                value = int(value)
                if s == ">":
                    if part[x] > value:
                        curr = next
                        break
                else:
                    if part[x] < value:
                        curr = next
                        break

                if curr in "AR":
                    dbg("Break", curr)
                    break
        if curr == "A":
            ans += sum(part.values())

    dbg(ans)
    return ans


def part_2(data):
    rules = {}
    for line in data:
        if line and line[0] == "{":
            ...
        elif line:
            name, rule = line.split("{")
            rule = rule[:-1].split(",")
            if len(rule[-1]) < 2 or rule[-1][1] not in "<>":
                rule[-1] = "x<4002:" + rule[-1]
            rules[name] = rule
    rules["R"] = []
    possible = []

    @functools.lru_cache()
    def foo(node: str, s_rules: set[str]):
        if node == "A":
            possible.append(s_rules)
            return
        cumm = set()
        for rule in rules[node]:
            x, s = rule[0], rule[1]
            value, next = rule[2:].split(":")
            foo(next, s_rules | cumm | {x + s + value})
            if s == ">":
                cumm.add(x + "<" + str(int(value) + 1))
            else:
                cumm.add(x + ">" + str(int(value) - 1))

    foo("in", frozenset())
    xmas = "xmas"
    default = {}
    for x in xmas:
        default[x + "n"] = 0
        default[x + "x"] = 4001
    ans = 0
    for rules in possible:
        nd = default.copy()
        for rule in rules:
            x, s = rule[0], rule[1]
            value = rule[2:]
            value = int(value)
            if s == "<":
                nd[x + "x"] = min(nd[x + "x"], value)
            else:
                nd[x + "n"] = max(nd[x + "n"], value)
        w = 1
        for x in xmas:
            z = nd[x + "x"] - nd[x + "n"] - 1
            if z < 1:
                z = 0
            w *= z

        ans += w

    return ans


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
