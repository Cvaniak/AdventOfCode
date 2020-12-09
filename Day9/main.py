def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = [int(d) for d in data.read().splitlines()]
        return data

def part_test():
    data = read_data("test")
    assert part_1(data, 5) == 127
    assert part_2(data, 127) == 62
    data = read_data("input")
    assert part_1(data, 25) == 15353384
    assert part_2(data, 15353384) == 2466556

def part_1(data, n):
    for k, i in enumerate(data[n:]):
        if not any(i-g in data[k:n+k] for g in data[k:n+k]):
            return i
    
def part_2(data, n):
    for sp in range(2, len(data)):
        for i in range(0,len(data)-sp):
            if n == sum([l for l in data[i:i+sp+1]]):
                return min(data[i:i+sp+1])+max(data[i:i+sp+1])

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    res_1 = part_1(data, 25)
    print(res_1)
    print(part_2(data, res_1))

    