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


def part_test():
    # data = read_data("test2")
    # assert part_1(data) == 112
    # data = read_data("input")
    # assert part_1(data) == 11516
    # assert part_2(data) == 40272
    # data = read_data("test")
    # assert part_1(data) == 12521
    # assert part_2(data) == 44169
    ...


def _cost(dist, pp):
    return dist * (10 ** pp)


def can_move(hall, hp, pp):
    d = {0: 2, 1: 4, 2: 6, 3: 8}
    ss = {2, 4, 6, 8}
    sp = d[pp]
    if hp in ss:
        return False
    if hp < sp:
        return not any(hall[hp + 1 : sp])
    else:
        return not any(hall[sp + 1 : hp])


def can_to_slot(hall, spot, hp, pp):
    # dbg(can_move(hall, pp[0], hp))
    if can_move(hall, hp, pp):
        if not all(
            [isinstance(x, bool) for x in spot[pp * room_size : (pp + 1) * room_size]]
        ):
            return False
        for i in range(room_size):
            y = spot[pp * room_size : (pp + 1) * room_size]
            t = (True,) * (room_size - i) + (False,) * (i)
            if y == t:
                dbg(t, y, t == y, lvl="4")
                dbg("can_to_slot", lvl="3")
                return True
    else:
        return False


def _to_slot(slot, pp):
    for i in range(room_size * (pp + 1) - 1, room_size * pp - 1, -1):
        if slot[i] is True:
            return update_tuple(slot, i, False), i - room_size * pp + 1


def _dist(hp, pp):
    d = {0: 2, 1: 4, 2: 6, 3: 8}
    return abs(hp - d[pp])


def to_slot(hall, slot, hp):
    pp = hall[hp]
    hall, hdist = update_tuple(hall, hp, None), _dist(hp, pp)
    slot, sdist = _to_slot(slot, pp)
    cost = _cost(hdist + sdist, pp)

    return hall, slot, cost


def _to_hall(hall, spot, hall_idx, spot_idx):
    return (
        update_tuple(hall, hall_idx, spot[spot_idx]),
        update_tuple(spot, spot_idx, True),
        _cost(
            _dist(hall_idx, spot_idx // room_size) + spot_idx % room_size + 1,
            spot[spot_idx],
        ),
    )


def in_ok(spot):
    for i in range(len(spot) // room_size):
        for j in range(room_size - 1, -1, -1):
            if spot[i * room_size + j] == i:
                spot = update_tuple(spot, i * room_size + j, False)
            else:
                break
    dbg(spot, lvl="k")
    return spot


def is_done(spot):
    dbg(spot, "is_done", lvl="h")
    return all(x == False for x in spot)


def update_tuple(tup, x, y):
    tup = list(tup)
    tup[x] = y
    return tuple(tup)


# mn = [float("inf")]
@functools.lru_cache(None)
def foo(spot, hall):
    if is_done(spot):
        dbg("Done", lvl="z")
        return 0

    dbg(spot, hall, lvl="f")

    mn = float("inf")
    for idx, i in enumerate(hall):
        if i is not None:
            if can_to_slot(hall, spot, idx, i):
                nhall, nspot, ncost = to_slot(hall, spot, idx)
                dbg(nspot, nhall, lvl="g")
                foo_cost = foo(nspot, nhall)
                mn = min(mn, foo_cost + ncost)

    mv = {0, 1, 3, 5, 7, 9, 10}
    for i in range(len(spot) // room_size):
        for j in range(room_size):
            if not isinstance(spot[i * room_size + j], bool):
                # dbg(spot[i*room_size + j], lvl="x")
                for m in mv:
                    if hall[m] is None and can_move(hall, m, i):
                        nhall, nspot, ncost = _to_hall(hall, spot, m, i * room_size + j)
                        dbg(nspot, nhall, ncost, lvl="k")
                        foo_cost = foo(nspot, nhall)
                        mn = min(mn, foo_cost + ncost)
                break
    return mn


room_size = 0


def solution(spot):
    global room_size
    # room_size = 2
    # room_size = 4

    hall = (None,) * 11

    dbg(spot, lvl="1")
    dbg(hall, spot, lvl="a")
    # assert foo((False,)*len(spot), hall) == 0
    # assert in_ok((0,0,1,2,2,3,1,3)) == (False, False, 1, 2, 2, 3, 1, False)
    # assert can_move((2, None, None, None, None, None, None, None, None, None, None, None), 0, 1) == True
    # assert can_move((2, 1, None, None, None, None, None, None, None, None, None, None), 0, 1) == False
    # for i in range(room_size):
    #     ...
    #     dbg((True,)*(room_size-i)+(False,)*(i), lvl="u")
    # dbg((True, True, True)[1:3],lvl="u")

    spot = in_ok(spot)
    dbg(hall, spot, lvl="b")

    # while is_done(spot, hall):
    # pp = spot[2][0]
    # spot[2][0] = True
    # hall[5] = (2, 1)

    # dbg(can_to_slot(hall, spot, 5, (2,1)))
    # dbg(hall, done, spot)
    cost = foo(spot, hall)
    dbg(hall, spot, lvl="e")
    print(spot, hall, cost)
    return cost


def part_1(datat):
    data = datat[:]
    global room_size
    room_size = 2
    spot = []
    aa = ord("A")
    for i in range(3, 10, 2):
        spot.append(ord(data[2][i]) - aa)
        spot.append(ord(data[3][i]) - aa)

    spot = tuple(spot)
    return solution(spot)


def part_2(datat):
    data = datat[:]
    global room_size
    room_size = 4

    spot = []
    part2 = ["  #D#C#B#A#  ", "  #D#B#A#C#  "]

    aa = ord("A")
    for i in range(3, 10, 2):
        spot.append(ord(data[2][i]) - aa)
        spot.append(ord(part2[0][i]) - aa)
        spot.append(ord(part2[1][i]) - aa)
        spot.append(ord(data[3][i]) - aa)

    spot = tuple(spot)
    return solution(spot)


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
