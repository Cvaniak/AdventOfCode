import re
types = (int, int, str, str)

def read_data():
    data = open("input.txt")
    data = data.read().splitlines()
    return data

def part_1(data):
    index = 0
    for f in data:
        f = [type(value) for type, value in zip(types, re.findall(r"[\w']+", f))] 
        if  f[0] <= f[3].count(f[2]) <= f[1]:
            index += 1
    return index

def part_2(data):
    index = 0
    for f in data:
        f = [type(value) for type, value in zip(types, re.findall(r"[\w']+", f))] 
        try:
            if (f[3][f[0]-1]+f[3][f[1]-1]).count(f[2]) == 1:
                index += 1
        except:
            pass
    return index

if __name__ == "__main__":
    data = read_data()
    print(part_1(data))
    print(part_2(data))