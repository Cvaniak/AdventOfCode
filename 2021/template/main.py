import collections
from collections import defaultdict, Counter
import functools
from functools import cache
import itertools
from itertools import product, permutations, combinations
import math 
from math import sqrt, sin, cos, log, fab

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == None
    assert part_2(data) == None

def part_1(data):
    ...
 
def part_2(data):
    ...

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    