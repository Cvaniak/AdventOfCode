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

def part_1(data):
    return sum([len(set(d.replace(" ", ""))) for d in data])

def part_2(data):
    return sum(len(set.intersection(*[set(d) for d in group.split(" ")])) for group in data)

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))