fi = open("input.txt")
fi = fi.readlines()
fi = list(map(int, fi))
fi.sort()
for i in fi:
    if (2020-int(i)) in fi:
        print(i*(2020-i))
        break
