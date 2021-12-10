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
    assert part_1(data) == 26397
    assert part_2(data) ==288957

def part_1(data):
    a = []
    w = {"[":"]", "<":">", "{":"}", "(":")"}
    w1 = {w[x]:x for x in w}
    z = {"]":57, ">":25137, "}":1197, ")":3}
    r = 0
    for i in data:
        for idx, j in enumerate(i):
            if j in w:
                a.append(w[j])
            else:
                k = a.pop()
                if j != k:
                    r +=z[j]
                    break
                # if w1[j] != k:
                    # print("oj")
        
    return r

def part_2(data):
    a = []
    w = {"[":"]", "<":">", "{":"}", "(":")"}
    w1 = {w[x]:x for x in w}
    z = {"]":2, ">":4, "}":3, ")":1}
    r = []
    for i in data:
        a = []
        flag = 0
        for idx, j in enumerate(i):
            if j in w:
                a.append(w[j])
            else:
                k = a.pop()
                if j != k:
                    flag = 1
                    break
        if flag == 0:
            r.append(0)
            a = "".join(a)
            print(a)
            for v in reversed(a):
                r[-1] *= 5
                r[-1] += z[v]
    print(r)
    r.sort()
    print(r)
    r1 = r[(len(r)//2)]
    print(r1)
    return r1
                # if w1[j] != k:    ...


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    