from sys import stdin, stdout, setrecursionlimit
import math
import random
setrecursionlimit(10 ** 6)

PRIME = [2, 3, 5, 7, 11, 13, 17, 23]


def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True


def is_prime(n):
    if n in PRIME:
        return True
    if any((n % p) == 0 for p in PRIME) or n in (0, 1):
        return False

    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1

    if n < 1373653:
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467:
        if n == 3215031751:
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    return not any(_try_composite(a, d, n, s) for a in PRIME)


def pollard_rho(n):
    if n & 1 == 0:
        return 2
    if is_prime(n):
        return n

    x = y = random.randint(2, 10)
    c = random.randint(1, 20)
    d = 1

    while d == 1:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = math.gcd(x - y, n)
        if d == n:
            pollard_rho(n)

    if is_prime(n):
        return d
    else:
        return pollard_rho(d)


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