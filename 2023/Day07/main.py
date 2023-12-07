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


def load_int_lines(datat):
    data = datat[:]
    for idx, i in enumerate(data):
        data[idx] = [x for x in i]
    return data


def load_ints_seperated(datat, sep=","):
    return list(map(int, datat[0].split(sep)))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 6440
    assert part_2(data) == 5905


def part_1(data):
    ...
    in_order = defaultdict(list)
    for line in data:
        hand, _, bid = line.partition(" ")
        bid = int(bid)
        hand = hand.replace("T", "a").replace("J", "b").replace("Q", "c").replace("K", "d").replace("A", "e")
        c = Counter(hand)
        hash = tuple(sorted(c.values(), reverse=True))
        bisect.insort(in_order[hash], (hand, bid))
    possible = list(reversed([(5,), (4,1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1,1,1), (1,1,1,1,1)]))
    dbg(in_order)

    ans = 0
    i = 1
    for group in possible:
        dbg.g(group)
        for hand, score in in_order[group]:
            dbg(hand, score)
            ans += score*i
            i +=1

    dbg(ans)
    return ans


def part_2(data):
    in_order = defaultdict(list)
    for line in data:
        hand, _, bid = line.partition(" ")
        bid = int(bid)
        hand = hand.replace("T", "a").replace("J", "1").replace("Q", "c").replace("K", "d").replace("A", "e")
        c = Counter(hand)
        if c["1"] > 0:
            if c["1"] == 5:
                dbg.z(c)
                hash = tuple(sorted(c.values(), reverse=True))
                dbg.z(hash)
            else:   

                dbg.y(c)
                one = c["1"]
                c["1"] = 0
                c[c.most_common(1)[0][0]] += one
                del c["1"]
                dbg.y(c)

        hash = tuple(sorted(c.values(), reverse=True))
        bisect.insort(in_order[hash], (hand, bid))
    possible = list(reversed([(5,), (4,1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1,1,1), (1,1,1,1,1)]))
    dbg.y(in_order)

    ans = 0
    i = 1
    for group in possible:
        dbg.g(group)
        for hand, score in in_order[group]:
            dbg.y(hand, score)
            ans += score*i
            i +=1

    dbg(ans)
    return ans



if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
