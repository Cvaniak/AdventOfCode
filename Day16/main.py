import collections
import math
import itertools

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 71 
    data = read_data("test2")
    assert part_2(data) == 11*12*13
    data = read_data("input")
    assert part_1(data) == 24980
    assert part_2(data) == 809376774329


def part_1(data):
    i = 0
    ranges = []
    while True:
        print(data[i].find("or"))
        if -1 == data[i].find("or"):
            break
        a = data[i].split(":")[1].split(" ")
        for k in range(1,4,2):
            ranges.append(tuple(map(int, a[k].split("-"))))
        i += 1
    i += 5
    su = 0
    for k in range(i, len(data)):
        for g in map(int, data[k].split(",")):
            if not any( (f[0]<=g<=f[1]) for f in ranges):
                # print(g)
                su += g
        #     print(g)
        # print(data[k])
    print(ranges)
    return su

def part_2(data):
    i = 0
    ranges = []
    while True:
        # print(data[i].find("or"))
        if -1 == data[i].find("or"):
            break
        a = data[i].split(":")[1].split(" ")
        for k in range(1,4,2):
            ranges.append(tuple(map(int, a[k].split("-"))))
        i += 1
    i += 2
    my = list(map(int, data[i].split(",")))
    print(my)
    i += 3
    valid = []
    for k in range(i, len(data)):
        t = 0
        for g in map(int, data[k].split(",")):
            if not any( (f[0]<=g<=f[1]) for f in ranges):
                t = 1
        if not t:
            valid.append(list(map(int, data[k].split(","))))
    print(len(valid), len(data))

    z = [[] for i in range(len(my))]
    print(z)
    for r in range(0, len(ranges), 2):
        for l in range(len(my)):
            va = 0
            for v in valid:
                if ranges[r][0] <= v[l] <= ranges[r][1] or ranges[r+1][0] <= v[l] <= ranges[r+1][1]: 
                    pass
                else:
                    va = 1
            if va != 1:
                # print("valid")
                z[l].append(1)
            else:
                # print("Not valid")
                z[l].append(0)
    # print(z)
    # z = list(map(list, zip(*reversed(z[::-1]))))
    for i in z:
        print(i)
    index = [i for i in range(len(my))]
    index1 = [i for i in range(len(my))]
    mul = 1
    mul1 = 1
    while True:
        if len(z) == 0:
            break
        for k,i in enumerate(z):
            if sum(i) == 1:
                # print(k, i)
                y = i.index(1)
                e = index1.pop(k)
                z.pop(k)
                
                for x in z:
                    x.pop(y)
                d = index.pop(y)
                if d < 6:
                    print(d, my[y], e, my[e])
                    mul *= my[d]
                    mul1 *= my[e]
    for i in z:
        print(i)
    return mul1


    # print(valid)

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    