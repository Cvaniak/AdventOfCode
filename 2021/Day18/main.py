import collections
from collections import defaultdict, Counter
import functools
import itertools
from itertools import product, permutations, combinations
import bisect
import math
from rich import print
import parse
import operator
from heapq import heappop, heappush


def read_data(file_name):
    with open(file_name + ".txt", "r", newline=None) as data:
        data = data.read().splitlines()
        return data


def part_test():
    ...
    data = read_data("test2")
    assert part_1(data) == 3488
    data = read_data("test")
    assert part_1(data) == 4140
    assert part_2(data) == 3993


class N:
    def __init__(self, val=None, par=None):
        self.left = None
        self.right = None
        self.parent = par
        self.val = val
        ...

    # This is so great, I like this so much
    def __str__(self):
        if self.val is not None:
            return str(self.val)
        return f"[{str(self.left)},{str(self.right)}]"


def find_left(n):
    if n.parent == None:
        return None
    if n == n.parent.left:
        return find_left(n.parent)
    n_left = n.parent.left
    while n_left.right != None:
        n_left = n_left.right
    return n_left


def find_right(n):
    if n.parent == None:
        return None
    if n == n.parent.right:
        return find_right(n.parent)
    n_right = n.parent.right
    while n_right.left != None:
        n_right = n_right.left
    return n_right


change = [0]


def explode(n):
    # print("explode", n)
    vl = n.left.val
    vr = n.right.val
    n.left = None
    n.right = None
    n.val = 0

    if l := find_left(n):
        l.val += vl
    if r := find_right(n):
        r.val += vr


def find_explode(n, d):
    if n is None or change[0]:
        return
    if d > 4:
        if n.left is not None and n.left.val is not None:
            explode(n)
            change[0] = 1
            return 1
    find_explode(n.left, d + 1)
    find_explode(n.right, d + 1)


def split(n):
    # print("split", n)
    n.left = N(val=n.val // 2, par=n)
    n.right = N(val=(n.val + 1) // 2, par=n)
    n.val = None


def find_split(n):
    if n is None or change[0]:
        return
    if n.val is not None and n.val >= 10:
        split(n)
        change[0] = 1
        return
    find_split(n.left)
    find_split(n.right)


def reduce(n, d):
    find_explode(n, d)
    if change[0]:
        change[0] = 0
        reduce(n, d)

    find_split(n)
    if change[0]:
        change[0] = 0
        reduce(n, d)


def create_root(li):
    if isinstance(li, int):
        return N(val=li)

    node = N()
    node.left = create_root(li[0])
    node.right = create_root(li[1])
    node.left.parent = node
    node.right.parent = node

    return node


def add_nodes(a, b):
    n = N()
    n.left = a
    n.right = b
    n.left.parent = n
    n.right.parent = n
    return n


def magnitude(root):
    if root.val is not None:
        return root.val

    return 3 * magnitude(root.left) + 2 * magnitude(root.right)


def part_1(datat):
    data = datat[:]

    root = data[0]
    root = eval(root)
    root = create_root(root)
    print(root)
    reduce(root, 1)

    for li in data[1:]:
        li = eval(li)
        li = create_root(li)
        reduce(li, 1)
        root = add_nodes(root, li)
        reduce(root, 1)

    mag = magnitude(root)
    print(mag)
    return mag


def part_2(datat):
    data = datat[:]
    mx = 0
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                continue
            root = eval(data[i])
            root = create_root(root)
            reduce(root, 1)
            r = eval(data[j])
            r = create_root(r)
            reduce(r, 1)
            r = add_nodes(root, r)
            reduce(r, 1)
            mag = magnitude(r)
            mx = max(mx, mag)
    return mx


if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))
