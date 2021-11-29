def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return preprocess(data)

def preprocess(data):
    sl = {}
    for d in data:
        d = d.split(" ")
        sl[" ".join(d[:2])] = {" ".join(d[1+a:3+a]):int(d[a]) for a in range(4, len(d)-3, 4)}
    return sl

def part_test():
    data = read_data("test")
    assert part_1(data) == 4
    assert part_2(data) == 32
    data = read_data("test2")
    assert part_2(data) == 126
    data = read_data("input")
    assert part_1(data) == 274
    assert part_2(data) == 158730

def nested_bags(data, st):
    if len(data[st]):
        return sum([data[st][k]*nested_bags(data, k) + data[st][k] for k in data[st]])
    else: return 0

def is_shiny_gold(data, st):
    if st == "shiny gold":
        return 1
    else:
        return sum([is_shiny_gold(data, k) for k in data[st]])

def part_1(data):
    return sum([1 for d in data if is_shiny_gold(data, d)])-1
    
def part_2(data):
    return nested_bags(data,"shiny gold")

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    data1 = preprocess(data)
    print(part_1(data))
    print(part_2(data))
