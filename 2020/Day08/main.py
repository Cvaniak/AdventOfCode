def read_data(file_name):
    data = open(file_name + ".txt", "r", newline=None)
    data = data.read().splitlines()
    data = [(d.split(" ")[0], d.split(" ")[1]) for d in data]
    return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 5
    assert part_2(data) == 8
    data = read_data("input")
    assert part_1(data) == 1451
    assert part_2(data) == 1160

def boot_code(data):
    ind = 0
    acc = 0 
    been = set()
    while True:
        if(ind in been): return (acc, False)
        elif ind == len(data): return (acc, True)
        been.add(ind)
        
        if data[ind][0] == "jmp": ind += int(data[ind][1])-1
        elif data[ind][0] == "acc": acc += int(data[ind][1])
        ind += 1

def part_1(data):
    return boot_code(data)[0]
    
def part_2(data):
    for g, i in enumerate(data):
        temp = data[g]
        
        if i[0] == "acc": continue
        elif int(i[1]) != 0 and i[0] == "nop":
            data[g] = ("jmp", i[1])
        else:
            data[g] = ("nop", i[1])

        result = boot_code(data)
        data[g] = temp
        if result[1]: return result[0]

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))