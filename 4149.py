import sys
import math
import random

PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


def modular_pow(b, p, n):
    """
    :return: b^p mod n
    """
    if n == 1:
        return 0
    c = 1
    for e in range(p):
        c = c * b % n
    return c


def miller_rabin(n):
    """
    :param n: 자연수
    :return: 소수인 경우 True, 합성수인 경우 False를 반환
    """
    if n in PRIME:
        return True
    if n % 2 == 0 or n == 1:
        return False

    for a in PRIME:
        d = n - 1
        while d % 2 == 0:
            if pow(a, d, n) == n - 1:
                break
            d //= 2
        if d % 2 == 1:
            t = pow(a, d, n)
            if t != n - 1 and t != 1:
                return False
    return True


def pollard_rho(n):
    """
    :param n: 자연수
    :return: n의 소수인 약수 하나를 반환
    """
    if n & 1 == 0:
        return 2
    if miller_rabin(n):
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
            pollard_rho(n)

    if miller_rabin(d):
        return d
    else:
        return pollard_rho(n)


def factorization(n):
    """
    :param n: 자연수
    :return: 소인수분해된 리스트를 반환
    """
    factor = []
    if n == 1:
        factor.append(1)
        return factor

    while n != 1:
        d = pollard_rho(n)
        factor.append(d)
        n //= d
    return factor


a = int(sys.stdin.readline())
factor = factorization(a)
factor.sort()

for i in factor:
    print(i)