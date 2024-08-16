MOD = 10 ** 9 + 7


def catalan_numbers_up_to(n):
    catalan = [0] * (n + 1)
    catalan[0] = 1
    for i in range(1, n + 1):
        for j in range(i):
            catalan[i] = (catalan[i] + catalan[j] * catalan[i - 1 - j]) % MOD
    return catalan


def count_periodic_strings(L, periodic_counts):
    if periodic_counts[L] != -1:
        return periodic_counts[L]
    if L == 1:
        periodic_counts[L] = 0  # Single character strings are not periodic
        return 0
    count = 0
    for i in range(1, L):
        if L % i == 0:
            count += pow(2, i, MOD)
            count %= MOD
    periodic_counts[L] = count
    return count


def calculate_BL_A_L(max_L, catalan):
    BL = [0] * (max_L + 1)
    AL = [0] * ((max_L // 2) + 1)
    periodic_counts = [-1] * (max_L + 1)

    for L in range(1, max_L + 1):
        if L % 2 == 1:
            BL[L] = pow(2, L, MOD)
        else:
            valid_count = catalan[L // 2]
            periodic_string_count = count_periodic_strings(L, periodic_counts)
            BL[L] = (pow(2, L, MOD) - valid_count + MOD) % MOD

    for L in range(1, (max_L // 2) + 1):
        sum_ = 0
        for i in range(1, L + 1):
            if i % 2 == 0:
                sum_ = (sum_ + catalan[L - (i // 2)] - AL[i // 2] + MOD) % MOD
        AL[L] = (catalan[L] - sum_ + MOD) % MOD

    return BL, AL


def main():
    import sys
    input = sys.stdin.readline
    data = input().split()

    p = int(data[0])
    q = int(data[1])
    m = int(data[2])
    Q = int(data[3])
    L_values = list()
    for i in range(Q):
        L_values.append(int(input()))
    print(L_values)

    max_L = max(L_values)

    catalan = catalan_numbers_up_to(max_L // 2)
    BL, AL = calculate_BL_A_L(max_L, catalan)

    results = []

    for L in L_values:
        if p == 0 and q == 0:
            P_intersect_Q = pow(2, L, MOD)
        elif p == 0 and q == 1:
            P_intersect_Q = (pow(2, L, MOD) - count_periodic_strings(L, [-1] * (max_L + 1))) % MOD
        elif p == 1 and q == 0:
            P_intersect_Q = BL[L]
        elif p == 1 and q == 1:
            if L % 2 == 0:
                P_intersect_Q = (BL[L] - AL[L // 2]) % MOD
            else:
                P_intersect_Q = BL[L]  # if L is odd, AL[L // 2] is 0

        result = P_intersect_Q % m
        results.append(result)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
