from sys import stdin, stdout, setrecursionlimit
from math import trunc
from collections import deque
from functools import reduce
setrecursionlimit(10 ** 6)


def solve(n, item, rows):
    odds = reduce(lambda acc, mul: acc + mul[1] % 2, item, 0)
    if n - odds < 0:
        return False

    array = [[None] * n for i in range(len(rows))]
    left_eye = n

    for i in item:
        if i[1] % 2:
            if left_eye > odds:
                pass

        else:
            pass



def main():
    n, k = map(int, stdin.readline().split())
    item = [stdin.readline().split() for _ in range(k)]
    item = [[i[0], int(i[1])] for i in item]
    p = int(stdin.readline())
    rows = list(map(int, stdin.readline().split()))

    print(n, k, item)


main()