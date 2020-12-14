import collections
import math

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

def part_2(data):
    res = collections.defaultdict(int)
    a = 0
    b1 = []
    for d in data:
        if d[:4] == "mask":
            a = d[7:]
        else:
            z = d.find("]")
            b1 = []
            b = list(format(int(d[4:z]),'036b'))
            for k, i in enumerate(a):
                if i == "1":
                    b[k] = "1"
            for k, i in enumerate(a):
                if i == "X":
                    if len(b1) > 0:
                        y = []
                        for g in range(len(b1)):
                            x = b1[g].copy()
                            x[k] = "1"
                            y.append(x.copy())
                            x[k] = "0"
                            y.append(x.copy())
                        b1 = y
                    else:
                        x = b.copy()
                        x[k] = "1"
                        b1.append(x.copy())
                        x[k] = "0"
                        b1.append(x.copy())
            for i in b1:
                res[int("".join(i), base=2)] = int(d[z+3:])
    return sum([res[k] for k in res])



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
    return sum([res[k] for k in res])


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    