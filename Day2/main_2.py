import re
types = (int, int, str, str)
index = 0
fi = open("input.txt")
for f in fi:
    f = [type(value) for type, value in zip(types, re.findall(r"[\w']+", f))] 
    if  f[0] <= f[3].count(f[2]) <= f[1]:
        index += 1
    # print(f)
print(index)