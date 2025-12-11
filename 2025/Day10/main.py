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
from math import lcm
from typing import NamedTuple
from fractions import Fraction

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
dir_4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
dir_4c = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
dir_8 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


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


class Matrix:
    data: list[list[int]]
    n: int
    m: int

    def __init__(self, data) -> None:
        self.data = data
        self.n = len(data)
        self.m = len(data[0])

    def s_get(self, y, x, default=None):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return default
        return self.data[y][x]

    def s_set(self, y, x, value):
        if 0 > y or y >= self.n or 0 > x or x >= self.m:
            return
        self.data[y][x] = value


# ===== ^^ PART OF TEMPLATE ^^ =====


def part_test():
    data = read_data("test")
    assert part_1(data) == 7
    assert part_2(data) == 33

class Line(NamedTuple):
    lights: int
    masks: list[int]

def load(data):
    res = []
    for line in data:
        line_data = line.split(" ")
        light_result = int(str(line_data[0][1:-1]).translate(str.maketrans(".#", "01"))[::-1], 2)
        masks = []
        for nums in line_data[1:-1]:
            nums = load_ints_seperated(nums[1:-1])
            x = 0
            for num in nums:
                x += 1 << num 
            masks.append(x)
        res.append(Line(light_result, masks))
    return res

def solve(line):
    q = deque((x, tuple([x])) for x in line.masks)
    q = deque([(0, tuple())])
    # for i in range(70):
    while True:
        for _ in range(len(q)):
            value, nums = q.popleft()
            for x in line.masks:
                next_value = value ^ x
                if next_value == line.lights:
                    return nums+(x,)
                q.append((next_value, nums+tuple([x])))
    return -1

def part_1(data):
    lines = load(data)
    answer = 0
    for line in lines:
        print(bin(line.lights))
        s = solve(line)
        answer += len(s)
        print(s, len(s))
    return answer

class Line2(NamedTuple):
    positions: list[int]
    joltage: list[int]


def load_2(data):
    res = []
    for line in data:
        line_data = line.split(" ")
        positions = []
        for nums in line_data[1:-1]:
            positions.append(tuple(load_ints_seperated(nums[1:-1])))
        joltage = tuple(load_ints_seperated(line_data[-1][1:-1]))
        res.append(Line2(positions, joltage))
    return res

def build_matrix(line):
    m = len(line.positions)
    n = len(line.joltage)
    
    matrix = [[Fraction(0, 1) for _ in range(m + 1)] for _ in range(n)]
    
    for y in range(n):
        for x, positions in enumerate(line.positions):
            if y in positions:
                matrix[y][x] = Fraction(1, 1)
        
        matrix[y][-1] = Fraction(line.joltage[y], 1)
        
    return matrix

def convert_to_rref(matrix):
    dbg("convert")
    rows = len(matrix)
    cols = len(matrix[0]) - 1
    last_row = 0
    non_zero_cols = []

    for c in range(cols):
        if last_row >= rows:
            break

        # Find non zero
        for j in range(last_row, rows):
            curr_row = j
            if matrix[curr_row][c] == 0:
                continue
            break
        else:
            # Or ommit
            continue

        # Add this is not zero
        non_zero_cols.append(c)
        
        # Move to current top
        matrix[curr_row], matrix[last_row] = matrix[last_row] , matrix[curr_row]
        curr_row = last_row

        # Normalize
        value = matrix[curr_row][c]
        for i in range(cols+1):
            matrix[curr_row][i] /= value

        # Substract from other (make other in this column zero)
        for row_idx in range(rows):
            if row_idx == curr_row:
                continue
            if matrix[row_idx][c] == 0:
                continue
            times = matrix[row_idx][c]
            for col_idx in range(cols+1):
                matrix[row_idx][col_idx] -= times*matrix[curr_row][col_idx]

        last_row += 1

    return matrix, non_zero_cols


def free_variables(line, non_zero_cols):
    free_rows = []
    for i in range(len(line.positions)):
        if i not in non_zero_cols:
            free_rows.append(i)
    return free_rows


def build_equations(matrix, non_zero_cols, free_cols):
    equations = {}
    for row, nzc_idx in enumerate(non_zero_cols):
        constant = matrix[row][-1]

        eq = {"const": constant, "coef": {}}

        for col in free_cols:
            if matrix[row][col] == 0: 
                continue
            eq["coef"][col] = matrix[row][col]

        equations[nzc_idx] = eq

    return equations

def solve_equations(equations, free_cols, line):
    min_takes = float('inf')
    solution = []

    mx = max(line.joltage)
    ranges = (range(mx) for _ in free_cols)


    for values in product(*ranges):
        curr_free_vals = {col: value for col, value in zip(free_cols, values)}

        solution = [0]*len(line.positions)

        for col, val in curr_free_vals.items():
            solution[col] = val

        for non_free_idx, eq in equations.items():
            val = eq["const"]
            for free_value_idx, value in eq["coef"].items():
                val -= value*curr_free_vals[free_value_idx]

            if val.denominator != 1 or val < 0:
                break

            solution[non_free_idx] = int(val)

        else:
            if sum(solution) < min_takes:
                min_takes = sum(solution)
                answer = solution

    return answer, min_takes


def part_2(data):
    lines = load_2(data)

    answer = 0
    for line in lines:
        matrix = build_matrix(line)
        dbg.x("Matrix", matrix)
        matrix, non_zero_cols = convert_to_rref(matrix)
        dbg.x("Matrix rref", matrix)
        dbg.x("Non zero", non_zero_cols)
        free_cols = free_variables(line, non_zero_cols)
        dbg.x("Free cols", free_cols)
        equations = build_equations(matrix, non_zero_cols, free_cols)
        dbg.x("Equations", equations)
        values, min_takes = solve_equations(equations, free_cols, line)
        dbg.x("Values", values)
        dbg.x("Solution", min_takes)
        answer += min_takes
    return answer

if __name__ == "__main__":
    set_debuger()

    part_test()
    data = read_data("input")
    # print(part_1(data[:]))
    print(part_2(data[:]))
