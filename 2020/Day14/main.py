import collections
import math
import itertools

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 165
    data = read_data("test2")
    assert part_2(data) == 208 
    data = read_data("input")
    assert part_1(data) == 11179633149677
    assert part_2(data) == 4822600194774

def all_sums(data):
    for i in range(len(data)+1):
        for k in itertools.combinations(data, i):
            yield sum(k)

def part_1(data):
    res = collections.defaultdict(int)
    for d in data:
        if d[1] == "a":
            a = d[7:]
        else:
            z = d.find("]")
            b = int(d[z+3:])
            for k, i in enumerate(a):
                if i == "1":
                    b |= (1<<35-k)
                elif i == "0":
                    b &= ~(1<<35-k)
            res[int(d[4:z])] = b
    return sum(res.values())

def part_2(data):
    res = collections.defaultdict(int)
    for d in data:
        if d[1] == "a":
            a = d[7:]
        else:
            z = d.find("]")
            b = list(format(int(d[4:z]),'036b'))
            b1 = []
            for k, i in enumerate(a):
                if i == "1":
                    b[k] = "1"
                if i == "X":
                    b[k] = "0"
                    b1.extend([2**(35-k)])
            for i in all_sums(b1):
                res[int("".join(b), base=2)+i] = int(d[z+3:])
    return sum(res.values())

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    