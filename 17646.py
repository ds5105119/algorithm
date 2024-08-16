import sys
import math
import random
from collections import Counter
sys.setrecursionlimit(10 ** 6)
import time

PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


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

    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for p in PRIME:
        x = pow(p, d, n)
        for _ in range(s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y
        if x != 1:
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
        return pollard_rho(n)


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


def _sq4(n):
    _n = n
    while True:
        r1 = random.randint(1, int(math.sqrt(_n)))
        _n -= r1 ** 2
        r2 = random.randint(1, int(math.sqrt(_n)))
        _n -= r2 ** 2
        if int(math.sqrt(_n)) ** 2 == _n:
            return [r1, r2, int(math.sqrt(_n)), 0]
        if _n % 4 == 1 and is_prime(_n):
            return [r1, r2, *div_prime(_n)]
        _n = n


def sq4(n):
    if n % 4 == 0:
        return [2 * _ for _ in sq4(n // 4)]

    if n % 4 != 2:
        _ = _sq4(2 * n)
        o = list(filter(lambda i: i % 2 == 1, _))
        e = list(filter(lambda i: i % 2 == 0, _))

        o = sum(o) // 2, abs(o[0] - o[1]) // 2
        e = sum(e) // 2, abs(e[0] - e[1]) // 2

        return [_ for _ in o + e if _]

    else:
        return _sq4(n)


def solve3(n):
    # 1개의 제곱수로 표현될 때
    if int(math.sqrt(n)) ** 2 == n:
        return [int(math.sqrt(n))]

    # 2개의 제곱수로 표현될 때
    is_divided_by_2_sums = sq2(n)
    if is_divided_by_2_sums:
        return is_divided_by_2_sums

    # 3개의 제곱수로 표현될 때, n = 4^a * (8k + 7) 꼴이 아니다
    x, k = n, 0
    while x % 4 == 0:
        x //= 4
        k += 1

    if x % 8 != 7:
        print(n, n % 8)
        if is_prime(n):
            z = int(math.sqrt(n))
            z = z if z % 2 else z - 1
            for i in range(0, int(math.sqrt(n)), 2):
                m = sq2(n - (z - i) ** 2)
                if m:
                    return z - i, *m
        else:
            if n % 3 == 0 and int(math.sqrt(n // 3)) ** 2 == n // 3:
                return [int(math.sqrt(n // 3)) for _ in range(3)]
            # n ≡ 1, 2, 5, 6 mod 8일 때
            elif x % 4 == 1 or x % 4 == 2:
                for i in range(int(math.sqrt(n)) + 1):
                    x = n - i ** 2
                    y = sq2(x)
                    if y:
                        return i, *y
                    elif int(math.sqrt(x)) ** 2 == x:
                        return i, int(math.sqrt(x))
            # n ≡ 8 mod 3일 때
            else:
                z = int(math.sqrt(n))
                z = z if z % 2 else z - 1
                for i in range(0, int(math.sqrt(n)), 2):
                    x = n - (z - i) ** 2
                    if x // 2 == 1:
                        return i, 1, 1
                    elif is_prime(x // 2):
                        x = div_prime(x // 2)
                        return i, x[0] + x[1], abs(x[0] - x[1])

    # 4개의 제곱수로 표현될 때
    else:
        print("trigged 4")
        if n % 4 == 0 and int(math.sqrt(n // 4)) ** 2 == n // 4:
            return [int(math.sqrt(n // 4)) for _ in range(4)]
        else:
            return 4 ** k, *solve3(n - 4 ** k)


def solve4(n):
    # 1개의 제곱수로 표현될 때
    if int(math.sqrt(n)) ** 2 == n:
        return [int(math.sqrt(n))]

    # 2개의 제곱수로 표현될 때
    is_divided_by_2_sums = sq2(n)
    if is_divided_by_2_sums:
        return is_divided_by_2_sums

    # 3개의 제곱수로 표현될 때, n = 4^a * (8k + 7) 꼴이 아니다
    x, k = n, 0
    while x % 4 == 0:
        x //= 4
        k += 1

    if x % 8 != 7:
        if n % 3 == 0 and int(math.sqrt(n // 3)) ** 2 == n // 3:
            return [int(math.sqrt(n // 3)) for _ in range(3)]
        # p = x^2 + 2y^2
        elif is_prime(n):
            return ["이건홀수고 운지다."]
            pass
        # n = x^2 + p^2
        elif x % 4 == 1 or x % 4 == 2:
            print("triggered 1")
            for i in range(1, int(math.sqrt(n))):
                q = sq2(n - i ** 2)
                if q:
                    return i, *q
        # n = x^2 + 2p
        elif x % 8 == 3:
            print("triggered 2")
            for i in range(int(math.sqrt(n))):
                p = n - i ** 2
                print( p // 2)
                if (p // 2) % 4 == 1:
                    print(p)
                if (p // 2) % 4 == 1 and is_prime(p // 2):
                    p = div_prime(p // 2)
                    return int(math.sqrt(n)) - i, p[0] + p[1], abs(p[0] - p[1])
        # n != 4^a(8k + 7) and n ≡ 0 mod 4
        else:
            print("triggered 3", n, Counter(factorization(n)))
            d = int(math.sqrt(n))
            d = d if d % 2 == 0 else d - 1
            for i in range(0, d, 2):
                q = sq2(n - (d - i) ** 2)
                if q:
                    return d - i, *q

    # 4개의 제곱수로 표현될 때
    else:
        return sq4(n)


def solve5(n):
    # 1개의 제곱수로 표현될 때
    if int(math.sqrt(n)) ** 2 == n:
        return [int(math.sqrt(n))]

    # 3개의 제곱수로 표현될 때, n = 4^a * (8k + 7) 꼴이 아니다
    x, k = n, 0
    while x % 4 == 0:
        x //= 4
        k += 1

    if x % 8 != 7:
        # 2개의 제곱수로 표현될 때
        is_divided_by_2_sums = sq2(n)
        if is_divided_by_2_sums:
            return is_divided_by_2_sums

        if n % 3 == 0 and int(math.sqrt(n // 3)) ** 2 == n // 3:
            return [int(math.sqrt(n // 3)) for _ in range(3)]
        for i in range(1, int(math.sqrt(x))):
            p = sq2(x - (i ** 2))
            if p:
                return (2 ** k) * i, *[(2 ** k) * _ for _ in p]

    # 4개의 제곱수로 표현될 때
    else:
        return 2 ** k, *solve5(n - 4 ** k)


n = int(sys.stdin.readline())
a = solve5(n)
a = [i for i in a if i]
a.sort()

print(len(a))
for i in a:
    print(i)