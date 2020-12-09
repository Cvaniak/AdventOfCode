def read_data(file_name):
    data = open(file_name + ".txt", "r", newline=None)
    data = data.read().splitlines()
    data = [int(d) for d in data]
    return data

def part_test():
    data = read_data("test")
    assert part_1(data, 5) == 127
    assert part_2(data, 127) == 62
    # data = read_data("input")
    # assert part_1(data) == 1451
    # assert part_2(data) == 1160

def part_1(data, n):
    ind = 1
    # print(data, n)
    for k, i in enumerate(data[n:]):
        z= 0
        # print(data[k:5+k], i)
        for g in data[k:n+k]:
            # print(i, g, i-g)
            if i-g in data[k:n+k]:
                z = 1
                break
        if not z:
            return i
            # if g-i in 

    # return boot_code(data)[0]
    
def part_2(data, n):
    co = 1
    while True:
        for i in range(0,len(data)-co):
            k = sum([l for l in data[i:i+co+1]])
            # print(i, k)
            if k == n:
                # print(k, co, i)
                # print(data[i:i+co+1], min(data[i:i+co+1])+max(data[i:i+co+1]))
                return min(data[i:i+co+1])+max(data[i:i+co+1])
        co += 1
    pass

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    # print(part_1(data, 25))
    # print(part_2(data, 15353384))

    
    # print(data)
    # data = data[:15]
    # for k, i in enumerate(data[:]):
    #     print(i, k)
    #     for g in data[k:k+5]:
    #         print()