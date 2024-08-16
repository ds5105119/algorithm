# SPDX-License-Identifier: MIT
# IGI IIH
from sys import stdin
from collections import deque
import math
import random
import time
from array import array


def mod_catalan(queries, m, sorting=False):
    """
    :param queries: queue, x in q {x|x ∈ N}
    :param m: modular
    :param sorting: if sorting is True, queries will be sorted
    :return: [catalan(x) % m: x ∈ queries]
    """
    idx = deque(sorted(queries)) if sorting else deque(queries)
    idx_min, idx_max = idx[0], idx[-1]
    c_k = idx.popleft()
    c_i = math.comb(2 * idx_min, idx_min) // (idx_min + 1) % m
    catalans = []

    for i in range(idx_min, idx_max + 1):
        while i == c_k:
            catalans.append(c_i)
            if idx:
                c_k = idx.popleft()
            else:
                break
        # Optimize it if necessary
        c_i = (c_i * (4 * i + 2) // (i + 2)) % m

    return catalans


def get_a(queries: list, m):
    """
    :param queries: queue, x in q {x|x ∈ N}
    :param m: modular
    :return: non correct strings counts list
    """
    val = sorted(queries)
    idx = sorted(range(len(queries)), key=lambda k: queries[k])

    even_check = False
    for i in val:
        if i & 1 == 0:
            even_check = True
            break

    if even_check:
        even_val = filter(lambda x: x & 1 == 0, val)
        even_val = map(lambda x: x // 2, even_val)
        catalans = deque(mod_catalan(even_val, m))
        for i in range(len(val)):
            a = 2 ** val[i] % m
            if val[i] & 1 == 0:
                a -= catalans.popleft()
                a %= m
            val[i] = a
    else:
        for i in range(len(val)):
            val[i] = 2 ** val[i] % m

    val = sorted(enumerate(val), key=lambda k: idx[k[0]])
    val = list(map(lambda x: x[1], val))

    return val


# print(get_a([1], 17))
# print(get_a([4, 8], 17))
# print(get_a([random.randint(1, 100000) for i in range(10000)], 17))

def get_b(queries: list, m, sorting=False):
    """
    :param queries: queue, x in q {x|x ∈ N}
    :param m: modular
    :param sorting: if sorting is True, queries will be sorted
    :return: non-periodic strings counts list
    """
    val, idx = None, None
    if sorting:
        val = deque(sorted(queries))
        idx = deque(sorted(range(len(queries)), key=lambda k: queries[k]))
    else:
        val = deque(queries)

    mid = val[-1] // 2 + 1
    b_i = 2
    b_q = deque([2])
    b_k = val.popleft()
    b_l = []

    if b_k == 1:
        b_l.append(b_i)
        if val:
            b_k = val.popleft()

    for i in range(2, val[-1] + 1):
        if i & 1:
            b_i = 2 * b_i % m
        else:
            b_i = (2 * b_i - b_q.popleft()) % m
        if i < mid:
            b_q.append(b_i)

        while i == b_k:
            b_l.append(b_i)
            if val:
                b_k = val.popleft()
            else:
                break

    if sorting:
        b_l = sorted(enumerate(b_l), key=lambda k: idx[k[0]])
        b_l = list(map(lambda x: x[1], b_l))

    return b_l


# print(get_b([1], 17))
# print(get_b([4, 4, 4, 4, 7, 7, 8, 9, 8], 100, True))
print(get_b(list(range(1, 1000)), 1000000))


def get_c(queries: list, m, sorting=False):
    """
    :param queries: queue, x in q {x|x ∈ N}
    :param m: modular
    :param sorting: if sorting is True, queries will be sorted
    :return:
    """
    val, idx = None, None
    if sorting:
        val = sorted(queries)
        idx = sorted(range(len(queries)), key=lambda k: queries[k])
    else:
        val = queries
    even = list(filter(lambda x: x & 1 == 0, val))

    if even:
        catalans = mod_catalan(range(even[-1] // 2 + 1), m)
        a_l = []

        for i in range(even[-1] // 2 + 1):
            a = catalans[i]
            a -= sum(map(lambda x: catalans[i - 2 * x] * a_l[x] % m, range(1, i // 2 + 1))) % m
            a %= m
            a_l.append(a)

        return a_l
    else:
        val = get_b(val, m)

    val = sorted(enumerate(val), key=lambda k: idx[k[0]])
    val = list(map(lambda x: x[1], val))

    return val


t = time.time()
print(get_c(range(1, 1001), 1000000))
print(time.time() - t)


def main():
    p, q, m, Q = map(int, stdin.readline().split())
    queries = []
    for i in range(Q):
        queries.append(int(stdin.readline()))

    if p == 1 and q == 0:
        print('\n'.join(map(str, get_a(queries, m))))
    elif p == 0 and q == 1:
        print('\n'.join(map(str, get_b(queries, m, sorting=True))))
    else:
        mode = 2


