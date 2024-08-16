# 제곱수의 전 쉬운 버전
import sys
import math
import random
from collections import Counter
sys.setrecursionlimit(10 ** 6)

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
    :return: n의 소인수
    """
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


# 재활용한 함수, 속도가 느려질 것.
def sq2(n):
    """
    :param n: 2개의 제곱수로 분해될 수 있는 자연수
    :return: 2개의 제곱수로 분해된 결과
    """
    factors = factorization(n)
    factors_count = Counter(factors)

    for p, e in factors_count.items():
        if p % 4 == 3 and e % 2 == 1:
            return False
    return True


def solve(n):
    # 1개의 제곱수로 표현될 때
    if int(math.sqrt(n)) ** 2 == n:
        return 1

    # 3개의 제곱수로 표현될 때, n = 4^a * (8k + 7) 꼴이 아니다
    x, k = n, 0
    while x % 4 == 0:
        x //= 4
        k += 1

    if x % 8 != 7:
        # 2개의 제곱수로 표현될 때
        if sq2(n):
            return 2
        else:
            return 3

    # 4개의 제곱수로 표현될 때
    else:
        return 4


n = int(sys.stdin.readline())
print(solve(n))