import sys
import math
import random
from collections import Counter
sys.setrecursionlimit(10 ** 6)
import time

PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def miller_rabin(n, p):
    d = n - 1
    while d % 2 == 0:
        if pow(p, d, n) == n - 1:
            return 1
        d >>= 1
    d = pow(p, d, n)
    return d == n - 1 or d == 1


def is_prime(n):
    """
    Miller Rabin Algorithm을 사용하여 소수를 판별한다.
    :param n: 자연수
    :return: 소수인 경우 True, 합성수인 경우 False를 반환
    """
    if n in PRIME:
        return True
    if n % 2 == 0 or n == 1:
        return False

    for a in PRIME:
        if not miller_rabin(n, a):
            return False
    return True


def pollard_rho(n):
    """
    :param n: 자연수
    :return: n의 소수인 약수 하나를 반환
    """
    if n & 1 == 0:
        return 2
    if is_prime(n):
        return n

    x = y = random.randint(2, n)
    c = random.randint(1, n - 2)
    d = 1

    while d == 1:
        x = (x ** 2 + c) % n
        y = (y ** 2 + c) % n
        y = (y ** 2 + c) % n
        d = math.gcd(x - y, n)
        if d == n:
            return pollard_rho(n)

    if is_prime(d):
        return d
    else:
        return pollard_rho(d)


def factorization(n):
    """
    :param n: 자연수
    :return: 소인수분해된 리스트를 반환
    """
    if n == 1:
        return [1]
    factor = []
    while n != 1:
        d = pollard_rho(n)
        factor.append(d)
        n //= d
    return factor


def div_prime(p):
    """
    :param p: 4k + 1 꼴로 나타내지는 소수와 2
    :return: p = a^2 + b^2 일 때, [a, b]
    """
    if p == 2:
        return 1, 1

    n, x, k, sq_value = p, 0, (p - 1) // 4, []

    for j in range(2, int(math.sqrt(p)) + 1):
        x = pow(j, k, p)
        if pow(x, 2, p) == p - 1:
            break

    while True:
        n, x = x, n % x
        if n * n < p:
            sq_value.append(n)
        if len(sq_value) == 2:
            break

    return sq_value


def sq2(n):
    """
    :param n: 2개로 소인수 분해될 수 있는 자연수
    :return:
    """
    factors = factorization(n)
    factors_count = Counter(factors)
    a, b = 1, 0

    for p, e in factors_count.items():
        if p % 4 == 3 and e % 2 == 1:
            return False
        elif (p % 4 == 1 or p == 2) and e % 2 == 1:
            n //= p
            c, d = div_prime(p)
            a, b = a * c - b * d, a * d + b * c

    if b != 0:
        return abs(a) * int(math.sqrt(n)), abs(b) * int(math.sqrt(n))
    else:
        return False


def solve(n):
    # 1개의 제곱수로 표현될 때
    if int(math.sqrt(n)) ** 2 == n:
        return [int(math.sqrt(n))]

    # 3개 이하의 제곱수로 표현될 때, n = 4^a * (8k + 7) 꼴이 아니다
    x, k = n, 0
    while x % 4 == 0:
        x //= 4
        k += 1

    if x % 8 != 7:
        # 2개의 제곱수로 표현될 때
        is_divided_by_2_sums = sq2(n)
        if is_divided_by_2_sums:
            return is_divided_by_2_sums

        # 같은 3개의 제곱수로 표현될 때
        if n % 3 == 0 and int(math.sqrt(n // 3)) ** 2 == n // 3:
            return [int(math.sqrt(n // 3)) for _ in range(3)]

        # 이외 3개의 제곱수로 표현될
        for i in range(1, int(math.sqrt(x))):
            p = sq2(x - (i ** 2))
            if p:
                return (2 ** k) * i, *[(2 ** k) * _ for _ in p]

    # 4개의 제곱수로 표현될 때
    else:
        return 2 ** k, *solve(n - 4 ** k)


def main():
    n = int(sys.stdin.readline())

    a = solve(n)
    a = [i for i in a if i]
    a.sort()

    print(len(a))
    for i in a:
        print(i)


if __name__ == '__main__':
    main()

