import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import math 
import pprint

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 5
    assert part_2(data) == 12

def part_1(data):
    # print(data)
    d = []
    for i in data:
        i = i.split(" -> ")
        d.append((tuple(map(int, i[0].split(","))), tuple(map(int, i[1].split(",")))))
    e = []
    for a, b in d:
        if a[0] == b[0] or a[1] == b[1]:
            e.append((a, b))
    matrix = [[0]*1000 for i in range(1000)]
    s = set()
    for a, b in e:
        g, h = a[0], b[0]
        f, t = a[1], b[1]
        if g > h:
            g, h = h, g
        if f > t:
            t, f = f, t
        for x in range(g, h+1):
            for y in range(f, t+1):
                matrix[x][y] += 1
                if matrix[x][y] >1:
                    s.add((x, y))

    # pprint.pprint(matrix)
    # print(s)
    return len(s)
    
def part_2(data):
    d = []
    for i in data:
        i = i.split(" -> ")
        d.append((tuple(map(int, i[0].split(","))), tuple(map(int, i[1].split(",")))))
    e = []
    for a, b in d:
        if a[0] == b[0] or a[1] == b[1]:
            e.append((a, b))
    matrix = [[0]*1000 for i in range(1000)]
    # matrix = [[0]*10 for i in range(10)]
    s = set()
    for a, b in e:
        g, h = a[0], b[0]
        f, t = a[1], b[1]
        if g > h:
            g, h = h, g
        if f > t:
            t, f = f, t
        for x in range(g, h+1):
            for y in range(f, t+1):
                matrix[y][x] += 1
                if matrix[y][x] >1:
                    s.add((y, x))
    # print(s)
    e = []
    for a, b in d:
        if abs(a[0]-b[0]) ==abs(a[1]- b[1]):
            print(a, b)
            e.append((a, b))
    for a, b in e:
        v, c = 1, 1
        g, h = a[0], b[0]
        f, t = a[1], b[1]
        if g > h:
            # g, h = h, g
            c = -1
        if f > t:
            # t, f = f, t
            v = -1
        diff = abs(a[0]-b[0])

        for x in range(diff+1):
            x1, y1 = g + c*x, f + v*x
            matrix[y1][x1] += 1
            if matrix[y1][x1] >1:
                s.add((y1, x1))
    # pprint.pprint(matrix)
    # print(s)
    return len(s)
 

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    # print(part_1(data))
    print(part_2(data))

    