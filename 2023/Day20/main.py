import argparse
import bisect
import collections
from dataclasses import dataclass, field
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
    assert part_1(data) == 32000000
    data = read_data("test_2")
    assert part_1(data) == 11687500


@dataclass
class Node:
    type: int
    name: str
    output: list["Node"]
    state: bool
    input: set
    rem: dict

    # "" broadcast, "%" flip flop, "&" conjuction
    def __init__(self, typename, output) -> None:
        if typename[0] == "%":
            self.type = 1
            self.name = typename[1:]
        elif typename[0] == "&":
            self.type = 2
            self.name = typename[1:]
        else:
            self.type = 0
            self.name = typename
        if output:
            out = output.split(", ")
            self.output = out
        else:
            self.output = []
        self.state = False
        self.input = set()
        self.rem = defaultdict(lambda: False)

    def apply(self, input, sign):
        if self.type == 0:
            self.state = sign
            return [(self.name, name, sign) for name in self.output]
        if self.type == 1:
            if sign:
                return []
            self.state = not self.state
            return [(self.name, name, self.state) for name in self.output]
        else:
            self.rem[input] = sign
            if all(self.rem[x] for x in self.input):
                return [(self.name, name, False) for name in self.output]
            else:
                return [(self.name, name, True) for name in self.output]


def part_1(data):
    nodes = {}

    for line in data:
        signal, _, dest = line.partition(" -> ")
        n = Node(signal, dest)
        nodes[n.name] = n

    for node in nodes:
        for next in nodes[node].output:
            ...
            if next in nodes:
                nodes[next].input.add(nodes[node].name)
    dbg(nodes)

    ans = [0, 0]
    steps = 1000
    for _ in range(steps):

        signals = deque([("button", "broadcaster", False)])
        while signals:
            f, t, sign = signals.popleft()
            # dbg.s(f"{f} -{sign}-> {t}")
            ans[int(sign)] += 1
            if t in nodes:
                nxt = nodes[t].apply(f, sign)
                signals.extend(nxt)
    w = ans[0] * ans[1]
    dbg(w, ans)
    return w
    dbg("Done")


def part_2(data):
    nodes = {}
    rx_in = []

    for line in data:
        signal, _, dest = line.partition(" -> ")
        n = Node(signal, dest)
        nodes[n.name] = n

    for node in nodes:
        for next in nodes[node].output:
            ...
            if next == "rx":
                rx_in = node
            if next in nodes:
                nodes[next].input.add(nodes[node].name)
    dbg(rx_in)

    rx_in_in = {x: 0 for x in nodes[rx_in].input}

    dbg(rx_in_in)

    steps = 100000000
    c = 0
    for step in range(1, steps):
        if step % 10000 == 0:
            dbg(step)
            dbg(rx_in_in)

        if all(rx_in_in.values()):
            dbg(rx_in_in)
            return lcm(*rx_in_in.values())

        signals = deque([("button", "broadcaster", False)])
        while signals:
            f, t, sign = signals.popleft()
            if t in nodes:
                nxt = nodes[t].apply(f, sign)
                signals.extend(nxt)
            if t == rx_in:
                for k, v in nodes[rx_in].rem.items():
                    if v:
                        rx_in_in[k] = step
                        print(k, t, step, v)
        if c > 0:
            dbg.c(c)
        if c > 1:
            return step

if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
