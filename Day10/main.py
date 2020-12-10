import itertools
from collections import defaultdict

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = [int(d) for d in data.read().splitlines()]
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == (7*5, 22)
    assert part_2(data, 22) == 8
    data = read_data("test2")
    assert part_1(data) == (22*10, 52)
    assert part_2(data, 52) == 19208
    # data = read_data("input")
    # assert part_1(data, 25) == 15353384
    # assert part_2(data, 15353384) == 2466556

def part_1(data):
    data.sort()
    a = {"1":0, "2":0, "3":0}
    i = 1
    a[str(data[0])] += 1
    while i<len(data):
        print(data[i], data[i-1], a)
        a[str(data[i]-data[i-1])] += 1# a[str(data[0]-data[i-1])] 
        i += 1
    a["3"] += 1

    # print(a["1"]+2*a["2"]+3*a["3"])
    return (a["1"]*a["3"], a["1"]+2*a["2"]+3*a["3"])
        
def vali(data, n, m):
    i = 1
    if data[-1] != m or  data[0] != n:
        # print(data[-1], n)
        return 0
    while i < len(data):
        # print(data[i-1]+3,data[i])
        if data[i-1]+3 < data[i]:
            return 0
        i += 1
    print(data)
    return 1

v = defaultdict(int)

def abc(data, n, end):
    if data[n] == end:
        v[str(data[n])] = 1
        return 1
    # if v[str(data[n])]>0:
    #     print("rce")
    #     v[str(data[n])] += 1
    #     return v[data[n]]
    i = 1
    while n+i < len(data) and data[n+i] - data[n] <= 3:
        v[str(data[n])] += v[str(data[n+i])]
        i += 1
    # for i in range(3):
    #     acb()
    
    # print(n)
    # if n>=len(data):
    #     return 0
    # if(data[n]==22):
    #     return 1
    # # for i in range(3):
    # return( sum([acb(data, n+i+1) for i in range(3)] ))

def part_2(data, n):
    a = 0
    global v
    n -=3
    v = defaultdict(int)
    data.append(0)
    data.sort()
    print(data)
    for i in range(0,len(data))[::-1]:
        abc(data, i, n), i, data[i]
    print(v, v["0"])
    return v["0"]
    # for i in range(len(data)):
    #     j = 1
    #     if(i+j>=len(data)):
    #         break
    #     while data[i+j]-data[i] <= 3:
    #         print(i , j)
    #         b[str(data[i])] += 1
    #         j += 1
    #         if(i+j>=len(data)):
    #             break

    # print(b.items())

    # while data[i]-data[i-1] >= 0:

    # for i in range(3):
    # a = 0
    # n -= 3
    # for i in range(int(n/3), len(data)+1):
    #     # n -= 3
    #     # print()
    #     for k in itertools.combinations(data, i):
    #         if vali(k, data[0], data[-1]):
    #             a+=1
    # # print(vali(data, n))
    # print(a)
    # return a
    #     print(acb(data, i+1))
    # for i in range(len(data)):
    #     for k in range(len(data)):
    #         for i in range()

    
    

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    res_1 = part_1(data)
    print(res_1)
    print(part_2(data, res_1[1]))

    