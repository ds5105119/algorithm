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
        return abs(a) * int(n ** 0.5), abs(b) * int(n ** 0.5)
    else:
        return False


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