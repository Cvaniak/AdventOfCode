import re

def read_data(file_name):
    data = open(file_name + ".txt", "r", newline=None)
    data = data.read().splitlines()
    return data

def replacer(data):
    for i in data:
        i = re.sub(r'[BR]', '1', i)
        i = re.sub(r'[FL]', '0', i)
        yield int(i, base=2)

def part_test():
    data = read_data("test")
    assert part_1(data) == 820
    data = read_data("input")
    assert part_1(data) == 871
    assert part_2(data) == 640

def part_1(data):
    return max(replacer(data))

def part_2(data):
    l = list(replacer(data))
    l.sort()
    for i in range(min(l), max(l)):
        if i not in l:
            if i-1 in l and i+1 in l:
                return i

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))