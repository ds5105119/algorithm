def linear_sieve(n):
    primes, ca = [], [True] * (n + 1)
    for i in range(2, n + 1):
        if ca[i]:
            primes.append(i)
        for p in primes:
            if i * p > n:
                break
            ca[i * p] = False
            if i % p == 0:
                break
    return primes


def get(x, primes):
    cnt, sq = 0, 0
    q = [(1, -1, 1)]
    while q:
        p, i, s = q.pop()
        for j in range(i + 1, len(primes)):
            n_p = p * primes[j] ** 2
            if n_p > x:
                break
            cnt += x // n_p * s
            sq |= int(not x % n_p)
            q.append((n_p, j, -s))
    return x-cnt, sq


def main():
    k = int(input())
    primes = linear_sieve(50000)
    x, c = 1 << 31, 30
    while 1:
        d_k, sq = get(x, primes)
        if d_k < k:
            x += 1 << c
        elif d_k > k or d_k == k and sq:
            x -= 1 << c
        else:
            break
        c -= 1
    print(x)


main()