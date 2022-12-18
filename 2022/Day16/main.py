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
    try:
        pattern = "Valve {va} has flow rate={rate}; tunnel leads to valve {vb}"
        match = parse.parse(pattern, data)
        return match.named
    except:
        pattern = "Valve {va} has flow rate={rate}; tunnels lead to valves {vb}"
        match = parse.parse(pattern, data)
        return match.named



# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    # assert part_1(data) == 1651
    assert part_2(data) == 1707


def part_1(data):
    graph = defaultdict(list)
    rates = dict()
    for line in data:
        parsed = parser(line)
        va, rate, vb = parsed["va"], parsed["rate"], parsed["vb"]
        vb = vb.split(", ")
        graph[va].extend(vb)
        rates[va] = int(rate)
    

    # @functools.lru_cache(maxsize=None)
    # def foo(node, left, opened):
    #     if left <= 0:
    #         return 0
    #
    #     mx = 0
    #     if node not in opened:
    #
    #         if rates[node] >= 0:
    #             n_opened = tuple(sorted((node,)+opened))
    #             n_val = rates[node] * (left-1)
    #             for tunel in graph[node]:
    #                 mx = max(mx, n_val+foo(tunel, left-2, n_opened))
    #
    #     for tunel in graph[node]:
    #         mx = max(foo(tunel, left-1, opened), mx)
    #
    #     return mx



    # result = foo("AA", 30, tuple())
    # result = maxflow("AA", tuple(), 30)

    # q = deque([("AA", 30, 0)])
    # mx = 0
    # while q:
    #     node, left, score = q.popleft() 
    #     if left <= 0:
    #         mx = max(mx, score)
    #         continue
    #     
    #     for tunel in graph[node]:
    #         q.append((tunel, left-1, score))
    #     score += left*rates[node]
    #     for tunel in graph[node]:
    #         q.append((tunel, left-1, score))

    # best = {}
    # mx = 0
    # while q:
    #
    #     node, opened, score, left = q.popleft()
    #     if left == 0:
    #         mx = max(score, mx)
    #
    #
    #     key = (node, opened)
    #     if key in best and score <= best[key]:
    #         continue
    #
    #     best[key] = score
    #
    #     flow_rate, lead_to = rates[node], graph[node]
    #     if node not in opened and flow_rate > 0:
    #
    #         q.append((node, tuple(sorted((node,)+opened)), score + flow_rate * (left-1), left-1))
    #     for dest in lead_to:
    #         q.append((dest, opened, score, left-1))
    # result = mx

    queue = [('AA', tuple(), 0)]

    best = {}

    for left in range(30,0,-1):

        new_queue = []
        for node, opened, score in queue:
            key = (node, opened)
            if key in best and score <= best[key]:
                continue

            best[key] = score

            rate, tunels = rates[node], graph[node]
            if node not in opened and rate > 0:
                new_queue.append((node, tuple(sorted((node,)+opened)), score + rate * (left-1)))

            for dest in tunels:
                new_queue.append((dest, opened, score))

        queue = new_queue

    result = max(score for _, _, score in queue)

    print(result)
    return result



def part_2(data):
    graph = defaultdict(list)
    rates = dict()
    for line in data:
        parsed = parser(line)
        va, rate, vb = parsed["va"], parsed["rate"], parsed["vb"]
        vb = vb.split(", ")
        graph[va].extend(vb)
        rates[va] = int(rate)

    # After so many attemts lets try with some new staff
    # Lesson for today floyd_warshall
    result = 0
    def floyd_warshall(graph):
        paths = defaultdict(lambda: defaultdict(lambda: float("inf")))

        for node, node_list in graph.items():
            paths[node][node] = 0

            for node_b in node_list:
                paths[node][node_b] = 1
                paths[node_b][node_b] = 0

        for i in paths:
            for j in paths:
                for k in paths:
                    if paths[i][j] + paths[j][k] < paths[i][k]:
                        paths[i][k] = paths[i][j]+paths[j][k]

        return paths

    paths = floyd_warshall(graph)
    should_visit = frozenset([x for x in graph if rates[x]])
    
    # queue = [('AA', tuple(), 0)]
    #
    # best = {}
    #
    # for left in range(30,0,-1):
    #
    #     new_queue = []
    #     for node, opened, score in queue:
    #         key = (node, opened)
    #         if key in best and score <= best[key]:
    #             continue
    #
    #         best[key] = score
    #
    #         rate, tunels = rates[node], graph[node]
    #         if node not in opened and rate > 0:
    #             new_queue.append((node, tuple(sorted((node,)+opened)), score + rate * (left-1)))
    #
    #         for dest in tunels:
    #             new_queue.append((dest, opened, score))
    #
    #     queue = new_queue
    #
    # result = max(score for _, _, score in queue)

    

    return result
    # return 1707


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    # print(part_1(data[:]))
    print(part_2(data[:]))
