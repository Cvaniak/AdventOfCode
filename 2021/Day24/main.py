import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import bisect
import math
import argparse
from rich import print
import parse
import operator
from heapq import heappop, heappush

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
    pattern = "{op} {ax} {val:d}"
    match = parse.search(pattern, data)
    if match:
        return match.named

    pattern = "{op} {ax} {val}"
    match = parse.search(pattern, data)
    if match:
        return match.named

    pattern = "{op} {ax}"
    match = parse.search(pattern, data)
    if match:
        return match.named


def part_test():
    data = read_data("test")
    # assert part_1(data) == 1
    # assert part_2(data) == None


def op(d, nam, kk):
    ope = nam["op"]
    axi = nam["ax"]
    if ope == "inp":
        # d[axi] = int(number.pop(0))
        return
    if kk:
        ...

    val = nam["val"]
    if not isinstance(val, int):
        val = d[val]

    if ope == "add":
        d[axi] = d[axi] + val
    elif ope == "mul":
        d[axi] = d[axi] * val
    elif ope == "div":
        d[axi] = d[axi] // val
    elif ope == "mod":
        d[axi] = d[axi] % val
    elif ope == "eql":
        d[axi] = 1 if d[axi] == val else 0


def sol(pz, w, block, idx):
    x = pz % 26 + block[idx]["x"]
    pz = pz // block[idx]["z"]
    if x != w:
        pz *= 26
        pz += w + block[idx]["y"]
    return pz


def part_1(datat):
    data = datat[:]
    block = []
    for idx, i in enumerate(data):
        if idx % 18 == 0:
            block.append(dict())
        elif idx % 18 == 4:
            x = i.split("z")
            dbg(block, lvl="a")
            block[-1]["z"] = int(x[-1][1:])
        elif idx % 18 == 5:
            x = i.split("x")
            dbg(block, lvl="a")
            block[-1]["x"] = int(x[-1][1:])
        elif idx % 18 == 15:
            x = i.split("y")
            dbg(block, lvl="a")
            block[-1]["y"] = int(x[-1][1:])
    dbg(block, lvl="1")
    fox = []
    stack = []
    for idx, i in enumerate(block):
        if i["z"] == 1:
            stack.append((idx, i["y"]))
        else:
            fox.append((stack.pop(), (idx, i["x"])))
    dbg(fox, lvl="2")
    rd = dict()
    for pair in fox:
        a, b = pair[0], pair[1]
        off = a[1] + b[1]
        dbg(pair, lvl="3")
        dbg(pair, lvl="3")
        for i in range(9, 0, -1):
            if 0 < i + off < 10:
                rd[a[0]] = i
                rd[b[0]] = i + off
                break

    r = ""
    for i in range(14):
        r += str(rd[i])
    print(r)

    rd = dict()
    for pair in fox:
        a, b = pair[0], pair[1]
        off = a[1] + b[1]
        dbg(pair, lvl="4")
        dbg(off, lvl="4")
        for i in range(1, 10):
            if 0 < i + off < 10:
                rd[a[0]] = i
                rd[b[0]] = i + off
                break

    r = ""
    for i in range(14):
        r += str(rd[i])
    print(r)

    return


def part_2(datat):
    data = datat[:]


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
