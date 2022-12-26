import argparse
import bisect
import collections
import functools
import itertools
import math
import operator
from collections import Counter, defaultdict, deque, namedtuple
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
    # pattern = "{test} foo {test1:d}"
    # Blueprint 1:    Each ore robot costs 4 ore.               Each clay robot costs 2 ore.          Each obsidian robot costs 3 ore and 14 clay.                 Each geode robot costs 2 ore and 7 obsidian.
    print(data)
    pattern = "Blueprint {id}: Each {ore_ore} robot costs {ore_ore} ore. Each clay robot costs {clay_ore} ore. Each obsidian robot costs {obs_ore} ore and {obs_clay} clay. Each geode robot costs {geo_ore} ore and {geo_obs} obsidian."
    match = parse.parse(pattern, data)
    return match.named


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    # assert part_1(data) == 33
    # assert part_2(data) == None


Line = namedtuple(
    "Line", ["id", "ore_ore", "clay_ore", "obs_ore", "obs_clay", "geo_ore", "geo_obs"]
)


def new_tuple(a, b):
    return tuple(x + y for x, y in zip(a, b))


def part_1(data):
    blueprints = []
    for line in data:
        splited = line.split(" ")
        values = []
        values.append(int(splited[1][:-1]))
        for i in splited:
            try:
                value = int(i)
                values.append(value)
            except:
                pass
        blueprints.append(Line(*values))

    @functools.lru_cache(maxsize=None)
    def foo(time_left, o0, o1, o2, r0, r1, r2, r3):
        if time_left <= 0:
            return 0

        if robot_cost[3][2] <= o2 and robot_cost[3][0] <= o0:
            return r3 + foo(
                time_left - 1,
                o0 - robot_cost[3][0] + r0,
                o1 + r1,
                o2 - robot_cost[3][2] + r2,
                r0,
                r1,
                r2,
                r3 + 1,
            )

        possible_obsidian = o2
        for i in range(0, time_left - 2):
            possible_obsidian += r2 + i
        if possible_obsidian < robot_cost[3][2]:
            return r3 * time_left

        ways = []
        if robot_cost[0][0] <= o0:
            ways.append(
                foo(
                    time_left - 1,
                    o0 - robot_cost[0][0] + r0,
                    o1 + r1,
                    o2 + r2,
                    r0 + 1,
                    r1,
                    r2,
                    r3,
                )
            )
        if robot_cost[1][0] <= o0:
            ways.append(
                foo(
                    time_left - 1,
                    o0 - robot_cost[1][0] + r0,
                    o1 + r1,
                    o2 + r2,
                    r0,
                    r1 + 1,
                    r2,
                    r3,
                )
            )
        if robot_cost[2][0] <= o0 and robot_cost[2][1] <= o1:
            ways.append(
                foo(
                    time_left - 1,
                    o0 - robot_cost[2][0] + r0,
                    o1 - robot_cost[2][1] + r1,
                    o2 + r2,
                    r0,
                    r1,
                    r2 + 1,
                    r3,
                )
            )

        ways.append(foo(time_left - 1, o0 + r0, o1 + r1, o2 + r2, r0, r1, r2, r3))

        return r3 + max(ways)

    result = 0
    for bp in blueprints:
        foo.cache_clear()
        robot_cost = [
            {0: bp.ore_ore},
            {0: bp.clay_ore},
            {0: bp.obs_ore, 1: bp.obs_clay},
            {0: bp.geo_ore, 2: bp.geo_obs},
        ]
        best = foo(24, 0, 0, 0, 1, 0, 0, 0)
        print(bp, robot_cost, best)
        result += best * bp.id

    print(result)
    return result


def part_2(data):
    blueprints = []
    for line in data:
        splited = line.split(" ")
        values = []
        values.append(int(splited[1][:-1]))
        for i in splited:
            try:
                value = int(i)
                values.append(value)
            except:
                pass
        blueprints.append(Line(*values))

    @functools.lru_cache(maxsize=None)
    def foo(time_left, o0, o1, o2, r0, r1, r2, r3):
        if time_left <= 0:
            return 0

        if robot_cost[3][2] <= o2 and robot_cost[3][0] <= o0:
            return r3 + foo(
                time_left - 1,
                o0 - robot_cost[3][0] + r0,
                o1 + r1,
                o2 - robot_cost[3][2] + r2,
                r0,
                r1,
                r2,
                r3 + 1,
            )

        possible_obsidian = o2
        for i in range(0, time_left - 2):
            possible_obsidian += r2 + i
        if possible_obsidian < robot_cost[3][2]:
            return r3 * time_left

        ways = []
        if robot_cost[0][0] <= o0 and r0 < max_ore:
            ways.append(
                foo(
                    time_left - 1,
                    o0 - robot_cost[0][0] + r0,
                    o1 + r1,
                    o2 + r2,
                    r0 + 1,
                    r1,
                    r2,
                    r3,
                )
            )
        if robot_cost[1][0] <= o0 and r1 < max_clay:
            ways.append(
                foo(
                    time_left - 1,
                    o0 - robot_cost[1][0] + r0,
                    o1 + r1,
                    o2 + r2,
                    r0,
                    r1 + 1,
                    r2,
                    r3,
                )
            )
        if robot_cost[2][0] <= o0 and robot_cost[2][1] <= o1 and r2 < max_obs:
            ways.append(
                foo(
                    time_left - 1,
                    o0 - robot_cost[2][0] + r0,
                    o1 - robot_cost[2][1] + r1,
                    o2 + r2,
                    r0,
                    r1,
                    r2 + 1,
                    r3,
                )
            )

        ways.append(foo(time_left - 1, o0 + r0, o1 + r1, o2 + r2, r0, r1, r2, r3))

        return r3 + max(ways)

    result = 1
    for bp in blueprints[:3]:
        max_ore_robots = max([bp.ore_ore, bp.clay_ore, bp.obs_ore, bp.geo_ore])

        foo.cache_clear()
        robot_cost = [
            {0: bp.ore_ore},
            {0: bp.clay_ore},
            {0: bp.obs_ore, 1: bp.obs_clay},
            {0: bp.geo_ore, 2: bp.geo_obs},
        ]
        max_ore, max_clay, max_obs = max_ore_robots, bp.obs_clay, bp.geo_obs
        best = foo(32, 0, 0, 0, 1, 0, 0, 0)
        print(bp, robot_cost, best)
        result *= best

    print(result)
    return result


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data[:]))
    print(part_2(data[:]))
