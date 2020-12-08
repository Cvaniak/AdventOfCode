import re

index = 0

def read_data(file_name):
    data = open(file_name + ".txt", "r", newline=None)
    data = data.read().splitlines()
    return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 5
    # assert part_2(data) == 32
    # data = read_data("test2")
    # assert part_2(data) == 126
    # assert part_2(data) == 6
    # data = read_data("input")
    # assert part_1(data) == 27
    # assert part_2(data) == 158730


def part_1(data):
    print(data)
    b= []
    for d in data:
        b.append({d.split(" ")[0]: d.split(" ")[1]})
    print(b)
    ind = 0
    acc =0 
    byl = set()
    while True:
        if(ind in byl):
            break
        byl.add(ind)
        for i in b[ind]:
            print(b[ind][i])
            if i == "nop":
                ind += 1
            elif i == "jmp":
                ind += int(b[ind][i])
            else:
                acc += int(b[ind][i])
                ind += 1
    print(acc)
    return acc
    # print(sum ([find_bag()])

        

            # if d[10:].find("shiny gold"):
            #     print("ok")
            #     d = d.split(" ")
            #     b = " ".join(d[:2])
            #     c = " ".join(d[5:7])
            #     # if(d.find("shiny"))
            #     print(b, c)
        # a1 = -1
        # while True:
        #     a = d.find("shiny gold", a)
        #     print(" a   ", a, d, a1)
        #     try:
        #         if a1 != a:
        #             print(a)
        #             index += int(d[a-2])
        #             print(d[a-2:a], index)
        #             a1 = a
        #         else:
        #             break
        #     except:
        #         break
    
def part_2(data):
        


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    # print(part_2(data))