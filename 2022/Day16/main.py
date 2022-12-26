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
    assert part_1(data) == 1651
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

    def floyd_warshall(graph):
        paths = defaultdict(lambda: defaultdict(lambda: float("inf")))

        for node, node_list in graph.items():
            paths[node][node] = 0

            for node_b in node_list:
                paths[node][node_b] = 1
                paths[node_b][node_b] = 0

        for i, j, k in product(graph, graph, graph):
            if paths[i][j] + paths[j][k] < paths[i][k]:
                paths[i][k] = paths[i][j] + paths[j][k]

        return paths

    def calc_score(score):
        return sum([rates[node] * time for node, time in score.items()])

    paths = floyd_warshall(graph)
    should_visit = set([x for x in graph if rates[x] != 0])

    queue = deque([("AA", should_visit, dict(), 30)])
    result_que = []

    while queue:
        node, to_visit, score, left = queue.pop()
        for new_node in to_visit:
            new_time = left - paths[node][new_node] - 1
            if new_time < 2:
                continue

            queue.append(
                (
                    new_node,
                    should_visit - {new_node},
                    score | {new_node: (new_time)},
                    new_time,
                )
            )
        result_que.append(score)

    result = max(calc_score(score) for score in result_que)

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

    def floyd_warshall(graph):
        paths = defaultdict(lambda: defaultdict(lambda: float("inf")))

        for node, node_list in graph.items():
            paths[node][node] = 0

            for node_b in node_list:
                paths[node][node_b] = 1
                paths[node_b][node_b] = 0

        for i, j, k in product(graph, graph, graph):
            if paths[j][i] + paths[i][k] < paths[j][k]:
                paths[j][k] = paths[j][i] + paths[i][k]

        return paths

    def calc_score(score):
        return sum([rates[node] * time for node, time in score.items()])

    paths = floyd_warshall(graph)
    should_visit = set([x for x in graph if rates[x]])

    def result_que(node, to_visit, score, left):
        for new_node in to_visit:
            new_time = left - paths[node][new_node] - 1
            if new_time < 2:
                continue

            yield from result_que(
                new_node,
                should_visit - {new_node},
                score | {new_node: (new_time)},
                new_time,
            )
        yield score

    nodes_score = defaultdict(int)

    # for score in result_que:
    for score in result_que("AA", should_visit, dict(), 26):
        set_score, calculated = frozenset(score), calc_score(score)
        if calculated > nodes_score[set_score]:
            nodes_score[frozenset(score)] = calc_score(score)

    result = max(
        score_a + score_b
        for (set_a, score_a), (set_b, score_b) in combinations(nodes_score.items(), 2)
        if not set_a & set_b
    )

    return result


if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    part1 = part_1(data[:])
    assert part1 == 1584
    print(part_2(data[:]))
