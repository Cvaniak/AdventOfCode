import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import math 

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    # assert part_1(data) == 26
    assert part_2(data) == 61229

def part_1(data):

    d = {2:1, 3:7, 4:4, 7:8}
    r = 0
    for i in range(len(data)):
        data[i] = data[i].split("|")[1].split(" ")
        for j in data[i]:
            if len(j) in d:
                r += 1
    print(r)
    return r

 
def part_2(data):

    d = {2:1, 3:7, 4:4, 7:8, 6:[0,6,9], 5:[2,3,5]}
    b = defaultdict(int)
    r = 0
    for i in range(len(data)):
        data[i] = data[i].split("|")
        for k in range(2):
            data[i][k] = data[i][k].split()

        for j in data[i][0]:
            if len(j) in [2,3,4,7]:
                b[d[len(j)]] = set(j)
        w = set()
        for j in data[i][0]:
            lj = len(j)
            if lj == 5:
                if len(set(j).intersection(b[1])) == 2:
                    w = set(j)
        b[3] = set(w)
        for j in data[i][0]:
            lj = len(j)
            if lj == 6:
                if len(set(j).intersection(b[3])) == 5:
                    w = set(j)
        b[9] = set(w)
        for j in data[i][0]:
            lj = len(j)
            if lj == 6 and len(b[9].difference(set(j))) == 1:
                if len(set(j).intersection(b[1])) == 2:
                    w = set(j)
        b[0] = set(w)
        for j in data[i][0]:
            lj = len(j)
            if lj == 6 and set(j) not in [b[0], b[9]]:
                w = set(j)
        b[6] = set(w)
        for j in data[i][0]:
            lj = len(j)
            if lj == 5 and len(b[3].difference(set(j))) > 0:
                if len(set(j).intersection(b[4])) == 3:
                    w = set(j)
        b[5] = set(w)
        for j in data[i][0]:
            lj = len(j)
            if lj == 5 and set(j) not in [b[3], b[5]]:
                w = set(j)
        b[2] = set(w)

        h = {tuple(sorted(list(b[x]))):x for x in b.keys()}

        r1 = 0
        for idx, j in enumerate(data[i][1]):
            r1 += 10**(3-idx)*h[tuple(sorted(j))]
        print(r1)
        r += r1





        print(b)
        print()
            
    return r


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    # print(part_1(data))
    print(part_2(data))

    