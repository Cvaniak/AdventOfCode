def read_data():
    data = open("input.txt")
    data = data.readlines()
    data = list(map(int, data))
    data.sort()
    return data

def part_1(data):
    for i in data:
        if (2020-int(i)) in data:
            return(i*(2020-i))

def part_2(data):
    for k, i in enumerate(data):
        data = [num for num in data if num < (2020-i*2)]
        for f, a in enumerate(data[k:]):
            for b in data[k+f:]:
                if i+a+b == 2020:
                    return (i*a*b)
            if i + a*2 > 2020:
                break

if __name__ == "__main__":
    data = read_data()
    print(part_1(data))
    print(part_2(data))