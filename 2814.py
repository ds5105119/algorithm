from sys import stdin, stdout, setrecursionlimit
from math import trunc
from collections import deque
from functools import reduce
setrecursionlimit(10 ** 6)


def sundaram_sieve(n):
    """
    :param n: 자연수
    :return: n 이하 소수의 deque
    """
    if n == 1:
        return deque()
    elif n == 2 or n == 3:
        return deque([n])

    k = (n - 3) // 2 + 1
    checksum = [True] * k

    for i in range((int(n ** 0.5) - 3) // 2 + 1):
        if checksum[i]:
            p = 2 * i + 3
            for j in range((p * p - 3) // 2, k, p):
                checksum[j] = False

    primes = deque(filter(lambda i: checksum[(i - 3) // 2], range(3, n + 1, 2)))

    if n % 2 == 0:
        primes.appendleft(2)

    return primes


def pim(a, primes):
    open, close = deque(), deque()

    for i in primes:
        open.append(a / i)
        for j in range(len(open) - 1):
            u = open.popleft()
            if u * u >= i * i:
                open.append(u)
                open.append(-u / i)
            else:
                close.append(u)

    s = reduce(lambda acc, mul: acc + trunc(mul), list(open), 0)
    return reduce(lambda acc, mul: acc + trunc(mul), list(close), s)


def solve(n, p, primes):
    start, end = 1, 10 ** 9 // p
    while start != end:
        m = (start + end) // 2
        y = m - pim(m, primes)
        if y > n:
            end = m - 1
        elif y < n:
            start = m + 1
        else:
            end = m

    if start - pim(start, primes) == n:
        return p * (start + end) // 2
    else:
        return 0


def main():
    n, p = map(int, stdin.readline().split())

    if p > 10 ** 4.5:
        if p <= 10 ** 9 and n == 1:
            stdout.write(str(p))
        else:
            stdout.write('0')
        exit(0)

    primes = sundaram_sieve(p - 1)
    stdout.write(str(solve(n, p, primes)))


main()
