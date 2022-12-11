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
from typing import Union

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


def load_int_commas(data):
    return list(map(int, data.split(",")))


def parser(data):
    pattern = "{test} foo {test1:d}"
    match = parse.search(pattern, data)
    match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 10605
    assert part_2(data) == 2713310158


@dataclass
class Monkey:
    items: list[int] = field(default_factory=deque)
    operation: str = "+"
    num_old: Union[int, str] = "old"
    test: int = 1
    if_true: int = 0
    if_false: int = 0


def parse_monkeys(data):
    monkeys = []
    for line in data:
        if line.startswith("Monkey"):
            monkeys.append(Monkey())
            continue
        line = line.strip()
        if line.startswith("Starting"):
            numbers = line.split(":")
            monkeys[-1].items.extend(load_int_commas(numbers[1]))
            continue

        num = line.split(" ")
        if line.startswith("Operation"):
            sign, number = num[-2], num[-1]
            monkeys[-1].operation = sign
            try:
                number = int(number)
            except:
                pass
            monkeys[-1].num_old = number
        elif line.startswith("Test"):
            monkeys[-1].test = int(num[-1])
        elif line.startswith("If true"):
            monkeys[-1].if_true = int(num[-1])
        elif line.startswith("If false"):
            monkeys[-1].if_false = int(num[-1])

    return monkeys


def part_1(data):
    c = Counter()
    monkeys = parse_monkeys(data)
    for _ in range(20):
        monkey: Monkey
        for idx, monkey in enumerate(monkeys):
            while monkey.items:
                c[idx] += 1
                item = monkey.items.popleft()
                if isinstance(monkey.num_old, int):
                    num = monkey.num_old
                else:
                    num = item

                if monkey.operation == "*":
                    item = item * num
                else:
                    item = item + num

                item = item // 3
                if item % monkey.test == 0:
                    monkeys[monkey.if_true].items.append(item)
                else:
                    monkeys[monkey.if_false].items.append(item)

    result = prod([value[1] for value in c.most_common(2)])
    return result


def part_2(data):
    c = Counter()
    monkeys = parse_monkeys(data)
    mods = prod([x.test for x in monkeys])
    for _ in range(10000):
        monkey: Monkey
        for idx, monkey in enumerate(monkeys):
            while monkey.items:
                c[idx] += 1
                item = monkey.items.popleft()
                if isinstance(monkey.num_old, int):
                    num = monkey.num_old
                else:
                    num = item
                if monkey.operation == "*":
                    item = item * num
                else:
                    item = item + num

                item = item % mods
                if item % monkey.test == 0:
                    monkeys[monkey.if_true].items.append(item)
                else:
                    monkeys[monkey.if_false].items.append(item)

    result = prod([value[1] for value in c.most_common(2)])
    return result


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
