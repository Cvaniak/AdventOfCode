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
dir3d_6 = [(-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (0, 0, 1)]


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
    assert part_1(data) == 64
    assert part_2(data) == 58


def part_1(data):
    cubes = set()
    on_minus = 0
    for line in data:
        cube = tuple(map(int, [x for x in line.split(",")]))
        for xx, yy, zz in dir3d_6:
            if (cube[0] + xx, cube[1] + yy, cube[2] + zz) in cubes:
                on_minus += 2
        cubes.add(cube)
    return len(cubes) * 6 - on_minus


# It is so ugly that I do not know how to finish this line of comment
def part_2(data):
    cubes = set()
    on_minus = 0
    airs = Counter()
    xd, yd, zd = defaultdict(list), defaultdict(list), defaultdict(list)
    for line in data:
        cube = tuple(map(int, [x for x in line.split(",")]))
        xd[cube[0]].append((cube[1], cube[2]))
        yd[cube[1]].append((cube[2], cube[0]))
        zd[cube[2]].append((cube[0], cube[1]))
        for xx, yy, zz in dir3d_6:
            if (cube[0] + xx, cube[1] + yy, cube[2] + zz) in cubes:
                on_minus += 2
        cubes.add(cube)

    air_cubes = set()
    for x in xd:
        x_list = xd[x]
        for i in range(len(x_list)):
            for j in range(i + 1, len(x_list)):
                if x_list[i][0] != x_list[j][0]:
                    continue
                a, b = x_list[i][1], x_list[j][1]
                y = x_list[i][0]
                if a > b:
                    a, b = b, a
                if any([(x, y, z) in cubes for z in range(a + 1, b)]):
                    continue
                for z in range(a + 1, b):
                    airs[(x, y, z)] += 2

    for y in yd:
        y_list = yd[y]
        for i in range(len(y_list)):
            for j in range(i + 1, len(y_list)):
                if y_list[i][0] != y_list[j][0]:
                    continue
                a, b = y_list[i][1], y_list[j][1]
                z = y_list[i][0]
                if a > b:
                    a, b = b, a
                if any([(x, y, z) in cubes for x in range(a + 1, b)]):
                    continue
                for x in range(a + 1, b):
                    airs[(x, y, z)] += 2

    for z in zd:
        z_list = zd[z]
        for i in range(len(z_list)):
            for j in range(i + 1, len(z_list)):
                if z_list[i][0] != z_list[j][0]:
                    continue
                a, b = z_list[i][1], z_list[j][1]
                x = z_list[i][0]
                if a > b:
                    a, b = b, a
                if any([(x, y, z) in cubes for y in range(a + 1, b)]):
                    continue
                for y in range(a + 1, b):
                    airs[(x, y, z)] += 2

    len_cubes = 0
    air_cubes = set()
    for cube, num in airs.items():
        if num == 6 and cube not in cubes:
            air_cubes.add(cube)

    while air_cubes:
        air_cube = air_cubes.pop()
        temp_set = set()
        is_ok = True
        queue = [air_cube]
        while queue:
            cube = queue.pop()
            temp_set.add(cube)
            for xx, yy, zz in dir3d_6:
                temp_cube = (cube[0] + xx, cube[1] + yy, cube[2] + zz)
                if temp_cube in cubes:
                    continue
                elif temp_cube in air_cubes:
                    air_cubes.discard(temp_cube)
                    temp_set.add(temp_cube)
                    queue.append(temp_cube)
                elif temp_cube in temp_set:
                    continue
                else:
                    is_ok = False
        if is_ok:
            for cube in temp_set:
                for xx, yy, zz in dir3d_6:
                    if (cube[0] + xx, cube[1] + yy, cube[2] + zz) in cubes:
                        on_minus += 1

    print(len(cubes) * 6, len_cubes, on_minus)
    return len(cubes) * 6 - on_minus


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
