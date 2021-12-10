import collections
from collections import defaultdict, Counter
import functools 
import itertools
from itertools import product, permutations, combinations
import math 
import operator
def prod(factors):
    return functools.reduce(operator.mul, factors, 1)

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    # assert part_1(data) == 15
    assert part_2(data) == 1134

def part_1(data):
    r = 0
    m, n = len(data), len(data[0])
    for i in range(len(data)):
        data[i] = [int(x) for x in data[i]]
    for idxi, i in enumerate(data):
        for idxj, j in enumerate(i):
            
            j = int(j)
            if idxj > 0 and j >= data[idxi][idxj-1]:
                continue
            if idxj < n-1 and j >= data[idxi][idxj+1]:
                continue
            if idxi > 0 and j >= data[idxi-1][idxj]:
                continue
            if idxi < m-1 and j >= data[idxi+1][idxj]:
                continue
            r += j + 1
    return r



 
def part_2(data):
    r1 = []
    r = 0
    m, n = len(data), len(data[0])
    been = set()
    def isstart(idxi, idxj):
        j = data[idxi][idxj]
        if idxj > 0 and j >= data[idxi][idxj-1]:
            return False
        if idxj < n-1 and j >= data[idxi][idxj+1]:
            return False
        if idxi > 0 and j >= data[idxi-1][idxj]:
            return False
        if idxi < m-1 and j >= data[idxi+1][idxj]:
            return False
        return True


    def foo(idxi, idxj):
        if (idxi, idxj) in been:
            return 0
        been.add((idxi, idxj))
        j = data[idxi][idxj]
        if j == 9:
            return 0
        a = []

        if idxj > 0: #and j+1 >= data[idxi][idxj-1]:
            a.append(foo(idxi, idxj-1))
        if idxj < n-1:# and j+1 >= data[idxi][idxj+1]:
            a.append(foo(idxi, idxj+1))
        if idxi > 0:# and j+1 >= data[idxi-1][idxj]:
            a.append(foo(idxi-1, idxj))
        if idxi < m-1: # and j +1 >= data[idxi+1][idxj]:
            a.append(foo(idxi+1, idxj))
        return sum(a)+1

    for i in range(len(data)):
        data[i] = [int(x) for x in data[i]]
    
    for idxi, i in enumerate(data):
        for idxj, j in enumerate(i):
            if isstart(idxi, idxj):
                k = foo(idxi, idxj)
                r1.append(k)

    r1.sort()
    print(prod(r1[-3:]))
    return prod(r1[-3:])
 
if __name__ == "__main__":
    part_test()
    data = read_data("input")
    # print(part_1(data))
    print(part_2(data))

    