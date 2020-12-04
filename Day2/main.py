import re
types = (int, int, str, str)
index = 0
fi = open("input.txt")
for f in fi:
    f = [type(value) for type, value in zip(types, re.findall(r"[\w']+", f))] 
    try:
        if (f[3][f[0]-1]+f[3][f[1]-1]).count(f[2]) == 1:
            index += 1
            print(f)
    except:
        pass
print(index)