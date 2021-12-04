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
    assert part_1(data) == 4512
    assert part_2(data) == None

def part_1(data):
    print(data)
    nums = list(map(int, data[0].split(",")))
    data = data[1:]
    print(nums)
    
    boards = []
    for i, j in enumerate(data):
        if not i%6:
            boards.append([])
            continue
        boards[-1].append(list(map(int, j.split())))
        
    print(boards)
    boardssets = []
    for i in boards:
        boardssets.append(list())
        for j in i:
            boardssets[-1].append((set(j), sum(j)))
        for j in list(list(x) for x in zip(*i))[::-1]:
            boardssets[-1].append((set(j), sum(j)))
    print(boardssets)
    print()
    al = set(range(len(boardssets)))
    def find():
        for i in nums:
            for k, x in enumerate(boardssets):
                for y in x:
                    if i in y[0]:
                        y[0].remove(i)
                        if len(y[0]) == 0:
                            al.remove(k)
                            if len(al) == 0:
                                print("Hyc")
                                return k, i, y[1]
                        
    w, z, sz = find()


    # Lel
    print(w,z, sz, boardssets)
 
    final = boards[w]
    f = set()
    for x in final:
        for y in x:
            f.add(y)

    r = sum(f)
    print(r, sz, r-sz)
    # Lel

    final = boardssets[w]
    r = 0
    for x, y in final[:5]:
        print(x)
        r += sum(x)
    print(r, z)


    return z*r



 
def part_2(data):
    ...

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    # print(part_2(data))

    