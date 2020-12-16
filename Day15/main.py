import collections
import math
import itertools

def part_test():
    assert part_0([0,3,6], 10) == 0 
    assert part_0([1,3,2], 2020) == 1
    assert part_0([2,1,3], 2020) == 10
    assert part_0([1,2,3], 2020) == 27
    assert part_0([2,3,1], 2020) == 78
    # assert part_0([1,3,2], 30000000) == 2578
    # assert part_0([2,1,3], 30000000) == 3544142
    
def part_0(data, n):
    b = collections.defaultdict(int)
    for k, i in enumerate(data):
        b[i] = k + 1
    last = 0
    for i in range(len(data)+1,n):
        c = b[last] 
        b[last] = i  
        if c == 0:
            last = 0
        else:
            last = i - c
    print(last)
    return last

def part_1(data):
    return part_0(data, 2020)
    
def part_2(data):
    return part_0(data, 30000000)

if __name__ == "__main__":
    part_test()
    data = [5,1,9,18,13,8,0]
    print(part_1(data))
    print(part_2(data))

    