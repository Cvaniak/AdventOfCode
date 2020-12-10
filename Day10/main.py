from collections import defaultdict

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = [int(d) for d in data.read().splitlines()]
        data.append(0)
        data.sort()
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 7*5
    assert part_2(data) == 8
    data = read_data("test2")
    assert part_1(data) == 22*10
    assert part_2(data) == 19208
    data = read_data("input")
    assert part_1(data) == 2232
    assert part_2(data) == 173625106649344

def part_1(data):
    a = defaultdict(int)
    a[3] += 1
    for i in range(1, len(data)):
        a[data[i]-data[i-1]] += 1
    return a[1]*a[3]

def part_2(data):
    v = defaultdict(int)
    v[data[-1]] = 1
    for n in range(len(data)-1)[::-1]:
        k = 1
        while n+k < len(data) and data[n+k] - data[n] <= 3:
            v[data[n]] += v[data[n+k]]
            k += 1
    return v[0]

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    