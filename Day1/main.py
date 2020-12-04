fi = open("input.txt")
fi = fi.readlines()
fi = list(map(int, fi))
fi.sort()
for k, i in enumerate(fi):
    # print(fi)
    fi = [num for num in fi if num < (2020-i*2)]
    # print(fi)
    # break
    for f, a in enumerate(fi[k:]):
        for b in fi[k+f:]:
            if i+a+b == 2020:
                print(i*a*b)
        if i + a*2 > 2020:
            break
            # else:
            #     print(i, a, b)
