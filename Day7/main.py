import re

index = 0

def read_data(file_name):
    data = open(file_name + ".txt", "r", newline=None)
    data = data.read().splitlines()
    return data

def part_test():
    data = read_data("test")
    # assert part_1(data) == 4
    assert part_2(data) == 32
    data = read_data("test2")
    assert part_2(data) == 126
    # assert part_2(data) == 6
    data = read_data("input")
    # assert part_1(data) == 27
    assert part_2(data) == 158730

def find_bag(data, st, data1):
    print(st)
    # for d in data:
        # if st == "shiny gold":
        #     return data1[st]
        # else:
    try:
        print("------- in", st, data[st])
        if len(data[st]):
            w = 0
            # for k in data[st]:
            #     print(k)
            for k in data[st]:
                # print(k)
                a = find_bag(data, k, data1)
                print("---", k, data[st][k], a)
                w += data[st][k]*a + data[st][k]
                print("-", k, w)
            print("return ", st, w)
            return w 
        else:
            print("return ", st, 0)
            return 0
    except:
        print("except1")
        return 0

def find_bag1(data, st):
    print(st)
    for d in data:
        if st == "shiny gold":
            return 1
        else:
            try:
                if len(data[st]):
                    return sum([find_bag1(data, k) for k in data[st]])
                else:
                    return 0
            except:
                return 0



def part_1(data):
    print(data)
    index= 0
    sl = {}
    for d in data:
        d = d.split(" ")
        b = " ".join(d[:2])
        c = []
        a = 0
        # print(d)
        while True:
            try:
                if(len(d)>a+7):
                    c.append(" ".join(d[5+a:7+a]))
                    # print(c)
                    a += 4
                else:
                    break
            except:
                break
        sl[b] = c
    print(sl)
    print("----------------")
    
    index = 0
    for d in sl:
       if find_bag(sl, d):
           index += 1

    return index-1
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
    print(data)
    index= 0
    sl1 = {}
    for d in data:
        d = d.split(" ")
        b = " ".join(d[:2])
        c = 0
        a = 0
        print(d)
        while True:
            try:
                if(len(d)>a+7):
                    c += int(d[4+a])
                    a += 4
                else:
                    break
            except:
                break
        sl1[b] = c
    
    
    print(sl1)
    index= 0
    sl = {}
    for d in data:
        d = d.split(" ")
        b = " ".join(d[:2])
        c = {}
        a = 0
        # print(d)
        # if b == "shiny gold":
        #     continue
        while True:
            try:
                if(len(d)>a+7):
                    c[" ".join(d[5+a:7+a])] =int(d[4+a])
                    # print(c)
                    a += 4
                else:
                    break
            except:
                break
        sl[b] = c
        print(b, c)
    print(sl)
    print("----------------")
    
    index = 0
    # for d in sl:
    #     print("----")
    #     if find_bag1(sl, d):
    #         index += find_bag(sl, d, sl1)
    print(find_bag(sl,"shiny gold",sl1))
    return find_bag(sl,"shiny gold",sl1)


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    # print(part_1(data))
    print(part_2(data))