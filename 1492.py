MODULUS = 1000000007  # 소수
N, K = map(int, input().split())
COMB = [[1] for i in range(K + 2)]
SUMS = [N % MODULUS]

for n in range(K + 1):
    for r in range(n):
        COMB[n + 1].append((COMB[n][r] + COMB[n][r + 1]) % MODULUS)
    COMB[n + 1].append(1)

for i in range(K):
    tmp = pow(N + 1, i + 2, MODULUS) - 1
    tmp -= sum(map(lambda k: (COMB[i + 2][k] * SUMS[k]) % MODULUS, range(i + 1))) % MODULUS
    tmp *= pow(COMB[i + 2][i + 1], (MODULUS - 2), MODULUS)
    tmp %= MODULUS
    SUMS.append(tmp)

print(SUMS[-1])
