def read_data():
    data = open("input.txt", "r", newline=None)
    data = data.read().splitlines()
    lenf = len(data[0])
    return data, lenf

def count_trees(step_x, step_y, lenf):
    x = 0
    index = 0
    for f in data[::step_y]:
        if f[x] == "#":
            index += 1
        x = (x+step_x)%lenf
    return index

def part_1(data, lenf):
    return count_trees(3, 1, lenf)

def part_2(data, lenf):
    index = 1
    for i in range(1,10,2):
        index *= count_trees(i%8, i//8+1, lenf)
    return index

if __name__ == "__main__":
    data, lenf = read_data()
    print(part_1(data, lenf))
    print(part_2(data, lenf))