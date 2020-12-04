fi = open("input.txt", "r", newline=None)
fi = fi.read().splitlines()
indexT = 1
lenf = len(fi[0])
for i in range(1,10,2):
    ad = i%8
    x = 0
    index = 0
    for f in fi[::i//8+1]:
        if f[x] == "#":
            index += 1
        x = (x+ad)%lenf
    indexT *= index
print(indexT)