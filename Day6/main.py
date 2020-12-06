import re

def read_data(file_name):
    data = open(file_name + ".txt", "r", newline=None)
    data = data.read().splitlines()
    data = " ".join(data).split("  ")
    return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 11
    assert part_2(data) == 6
    data = read_data("input")
    assert part_1(data) == 6930
    assert part_2(data) == 3585

def counter2(data):
    for d in data:
        num = d.count(" ")
        d.replace(" ", "")
        for i in set(d):
            if d.count(i) > num:
                yield 1

def counter(data):
    for d in data:
        yield len(set(d))

def part_1(data):
    data = [w.replace(" ", "") for w in data]
    return sum(counter(data))

def part_2(data):
    return sum(counter2(data))

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))