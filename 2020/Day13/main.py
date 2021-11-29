import math
def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 295
    assert part_2(data[1]) == 1068781
    data = read_data("test2")
    assert part_2(data[0]) == 3417
    assert part_2(data[1]) == 754018
    assert part_2(data[2]) == 779210
    assert part_2(data[3]) == 1261476
    assert part_2(data[4]) ==  1202161486
    data = read_data("input")
    assert part_1(data) == 3789
    assert part_2(data[1]) == 667437230788118

def part_1(data):
    n = int(data[0])
    data = [int(i) for i in data[1].split(",") if i != "x"]
    z = min([((abs(n-((n//i)+1)*i), i)) for i in data], key = lambda k: k[0])
    return z[0]*z[1]

# Based on https://shainer.github.io/crypto/math/2017/10/22/chinese-remainder-theorem.html
def extended_euclid(x, y):
    m = y
    x0, x1 = 1, 0
    while y > 0:
        a, x, y = x//y, y, x % y
        x0, x1 = x1, x0 - a * x1
    return x0 % m
    
def part_2(data):
    data  = [(int(i), int(i)-k) for k, i in enumerate(data.split(",")) if i != "x"]
    prod = math.prod([i[0] for i in data])
    a = sum([i[1]*extended_euclid(prod//i[0], i[0])*prod//i[0] for i in data])
    return a%prod
    
if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data[1]))

    