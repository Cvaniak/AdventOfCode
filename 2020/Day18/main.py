import collections
import math
import itertools

def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data

def part_test():
    data = read_data("test")
    assert part_1(data) == 71+51+26+437+12240+13632 
    assert part_2(data) == 231+51+46+1445+669060+23340

def part_1(data):
    sum_all = 0
    for i in data:
        i = i.replace("(", "( ")
        i = i.replace(")", " )")
        i = i.split(" ") 
        sum1 = []
        sum2 = []
        last = "+"
        ind = 0
        sum1.append(0)
        for j in i:
            if j == "(":
                ind += 1
                sum1.append(0)
                sum2.append(last)
                last = "+"
            elif j == ")":
                ind -= 1
                t_s = sum2.pop()
                t_d = int(sum1.pop())
                if t_s == "+":
                    sum1[ind] += t_d
                else:
                    sum1[ind] *= t_d
            elif j.isdigit():
                j = int(j)
                if last == "+":
                    sum1[ind] += j
                else:
                    sum1[ind] *= j
            else:
                last = j
        sum_all += sum1.pop()
    return sum_all



def part_2(data):
    
    sum_all = 0
    for i in data:
        i = i.replace("(", "( ")
        i = i.replace(")", " )")
        i = i.split(" ") 
        sum1 = []
        sum2 = []
        sum3 = []
        ind = 0
        sum1.append(0)
        sum3.append(list())
        for j in i:
            if j == "(":
                ind += 1
                sum1.append(0)
                sum3.append(list())
            elif j == "*":
                sum3[ind].append(sum1[ind])
                sum1[ind] = 0
            elif j == ")":
                sum3[ind].append(int(sum1.pop()))
                t_d = math.prod(sum3.pop()) 
                ind -= 1
                sum1[ind] += t_d
            elif j.isdigit():
                sum1[ind] += int(j)
        sum3.append(sum1)
        sum3 =  list(itertools.chain.from_iterable(sum3))
        sum_all += math.prod(sum3)
    return sum_all

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))

    