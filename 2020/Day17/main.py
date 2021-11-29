import collections
import math
import itertools

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 112 
    assert part_2(data) == 848

def part_1(data):
    a = []
    for yi, y in enumerate(data):
        for xi, x in enumerate(y):
            if x == "#":
                a.append((xi, yi, 0))

    arround_t = [(x, y, z) for x in range(-1,2) for y in range(-1,2) for z in range(-1,2)]
    arround_t.remove((0,0,0))
    for _ in range(6):
        a_new = []
        arround = list([(ax+tx, ay+ty, az+tz) for ax, ay, az in a for tx, ty, tz in arround_t])
        arround_s = set(arround)
        for d in arround_s:
            if d in a:
                if arround.count(d) <= 3 and arround.count(d) >=2:
                    a_new.append(d)
            elif arround.count(d) == 3:
                a_new.append(d)
        a = a_new[:]
    return len(a)

def part_2(data):
    a = []
    for yi, y in enumerate(data):
        for xi, x in enumerate(y):
            if x == "#":
                a.append((xi, yi, 0, 0))
    arround_t = [(x, y, z, w) for x in range(-1,2) for y in range(-1,2) for z in range(-1,2) for w in range(-1,2)]
    arround_t.remove((0,0,0,0))
    for _ in range(6):
        a_new = []
        arround = list([(ax+tx, ay+ty, az+tz, aw+tw) for ax, ay, az, aw in a for tx, ty, tz, tw in arround_t])
        arround_s = set(arround)
        for d in arround_s:
            if d in a:
                if arround.count(d) <= 3 and arround.count(d) >=2:
                    a_new.append(d)
            elif arround.count(d) == 3:
                a_new.append(d)
        a = a_new[:]
    return len(a)

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    