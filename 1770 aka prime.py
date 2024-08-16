from sys import stdin, stdout, setrecursionlimit
import math
import random
setrecursionlimit(10 ** 6)

PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23]


def miller_rabin(n, p):
    d = n - 1
    while d % 2 == 0:
        if pow(p, d, n) == n - 1:
            return 1
        d >>= 1
    d = pow(p, d, n)
    return d == n - 1 or d == 1


def is_prime(n):
    if n in PRIME:
        return True
    if n % 2 == 0 or n == 1:
        return False

    for a in PRIME:
        if not miller_rabin(n, a):
            return False
    return True


def pollard_rho(n):
    if n & 1 == 0:
        return 2
    if is_prime(n):
        return n

    x = y = random.randint(2, 10)
    c = random.randint(1, 10)
    d = 1

    while d == 1:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = math.gcd(x - y, n)
        if d == n:
            return pollard_rho(n)

    return pollard_rho(d)


def main():
    t = int(stdin.readline())
    for i in range(t):
        n = int(stdin.readline())
        factor = []

        if n == 1 or n == 4:
            stdout.write("1\n")
            continue

        while n != 1:
            d = pollard_rho(n)
            if d in factor:
                break
            factor.append(d)
            n //= d

        if n != 1:
            stdout.write("-1\n")
        else:
            stdout.write(str(math.factorial(len(factor))))
            stdout.write("\n")


main()