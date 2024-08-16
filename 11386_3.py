MOD = 10 ** 9 + 7


def catalan_numbers(limit, mod):
    catalans = [1] * (limit + 1)
    for n in range(1, limit + 1):
        catalans[n] = (catalans[n - 1] * (4 * n - 2) * pow(n + 1, mod - 2, mod)) % mod
    return catalans


def count_non_periodic_strings(limit, mod):
    B = [0] * (limit + 1)
    B[0] = 1  # Base case

    for L in range(1, limit + 1):
        B[L] = pow(2, L, mod)
        for i in range(1, L // 2 + 1):
            B[L] -= B[i] * pow(2, L - 2 * i, mod)
            B[L] %= mod

    return B


def solve(p, q, m, queries):
    max_length = max(queries)
    mod = m

    # Precompute Catalan numbers and other required values
    catalans = catalan_numbers(max_length // 2, mod)
    non_periodic = count_non_periodic_strings(max_length, mod)

    results = []
    for L in queries:
        if p == 1 and q == 0:
            total_strings = pow(2, L, mod)
            correct_strings = catalans[L // 2] if L % 2 == 0 else 0
            result = (total_strings - correct_strings) % mod
        elif p == 0 and q == 1:
            result = non_periodic[L] % mod
        elif p == 1 and q == 1:
            correct = catalans[L // 2] if L % 2 == 0 else 0
            result = (non_periodic[L] - correct) % mod
        else:
            result = 0
        results.append(result)

    return results


# Example input
p, q, m, Q = 1, 1, 17, 2
queries = [4, 8]

# Calculate results
results = solve(p, q, m, queries)

# Print results
for result in results:
    print(result)