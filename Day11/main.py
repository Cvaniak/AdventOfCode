
def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        data = [list(d) for d in data]
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 37
    assert part_2(data) == 26
    data = read_data("input")
    assert part_1(data) == 2273
    assert part_2(data) == 2064

grid = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def check_1(data, i, j):
    su = 0
    for dx, dy in grid:
        if 0 <= i+dx < len(data) and 0 <= j+dy < len(data[i]):
            if data[i+dx][j+dy] == "#":
                su += 1 
    return su

def check_2(data, i, j):
    su = 0
    for x, y in grid:
        dx, dy = (0,0)
        while True:
            dx += x
            dy += y
            if 0 <= i+dx < len(data) and 0 <= j+dy < len(data[i]):
                if data[i+dx][j+dy] == "#":
                    su += 1
                    break
                if data[i+dx][j+dy] == "L":
                    break
            else: break
    return su

def part_1(data):
    d1 = [list(d) for d in data]
    while True:
        g = 0
        for i in range(0, len(data)):
            for k in range(0, len(data[i])):
                if data[i][k] == ".": continue
                re = check_1(data, i, k)
                if data[i][k] == "L" and re == 0:
                    d1[i][k] = "#" 
                    g = 1
                elif data[i][k] == "#" and re >= 4:
                    d1[i][k] = "L"
                    g = 1
        if g:
            data = [list(d) for d in d1]
        else:
            return sum(i.count("#") for i in data)

def part_2(data):
    d1 = [list(d) for d in data]
    while True:
        g = 0
        for i in range(0, len(data)):
            for k in range(0, len(data[i])):
                if data[i][k] == ".": continue
                re = check_2(data, i, k)
                if data[i][k] == "L" and re == 0:
                    d1[i][k] = "#" 
                    g = 1
                elif data[i][k] == "#" and re >= 5:
                    d1[i][k] = "L"
                    g = 1
        if g:
            data = [list(d) for d in d1]
        else:
            return sum(i.count("#") for i in data)

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    