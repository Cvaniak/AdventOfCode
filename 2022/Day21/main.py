import argparse
import bisect
import collections
from decimal import Decimal
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
    assert part_1(data) == 152
    assert part_2(data) == 301


tok = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv}


def part_1(data):
    monkeys = dict()
    for line in data:
        name, value = line.split(": ")
        value = value.split(" ")
        if len(value) == 1:
            value = int(value[0])
        # else:
        #     monkey_a, oper, monkey_b = value
        monkeys[name] = value

    def foo(monkey):
        if isinstance(monkeys[monkey], int):
            return monkeys[monkey]
        monkey_a, oper, monkey_b = monkeys[monkey]
        return tok[oper](foo(monkey_a), foo(monkey_b))

    result = foo("root")
    print(result)
    return result


def part_2(data):
    monkeys = dict()
    for line in data:
        name, value = line.split(": ")
        value = value.split(" ")
        if len(value) == 1:
            value = int(value[0])
        monkeys[name] = value

    def foo(monkey):
        if isinstance(monkeys[monkey], int):
            return monkeys[monkey]
        if monkeys[monkey] is None:
            return monkeys[monkey]
        monkey_a, oper, monkey_b = monkeys[monkey]
        a, b = foo(monkey_a), foo(monkey_b)
        if a and b:
            return tok[oper](a, b)
        else:
            return None

    def fox(monkey, result):
        if isinstance(monkeys[monkey], int):
            return monkeys[monkey]

        if monkeys[monkey] is None:
            return result

        monkey_a, oper, monkey_b = monkeys[monkey]
        a, b = foo(monkey_a), foo(monkey_b)
        if a is None:
            return fox(
                monkey_a,
                {
                    "-": operator.add,
                    "+": operator.sub,
                    "/": operator.mul,
                    "*": operator.floordiv,
                }[oper](result, b),
            )
        elif b is None:
            return fox(
                monkey_b,
                {
                    "-": lambda x, y: y - x,
                    "+": operator.sub,
                    "/": lambda x, y: y // x,
                    "*": operator.floordiv,
                }[oper](result, a),
            )

    foo("root")
    monkeys["root"][1] = "-"
    monkeys["humn"] = None
    result = fox("root", 0)
    print(result)
    return result


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
