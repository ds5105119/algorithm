from sys import stdin


def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])


def sort_by_ccw(p: list):
    base = min(p)

    def sort_function(i):
        norm = abs(i[0] - base[0]) + abs(i[1] - base[1])
        if i[0] - base[0] == 0:
            return [1, 0, norm]
        else:
            return [0, (i[1] - base[1]) / (i[0] - base[0]), norm]

    p.sort(key=sort_function)

    return p


def ressol(n, p):
    """
    :param n: 리턴 설명을 참조
    :param p: 홀수인 소수, 특히 4k + 1인 꼴의 소수
    :return: x^2 = n mod p일 때, x
    """
    q, m, z = p - 1, 0, 2

    while q % 2 == 0:
        q //= 2
        m += 1

    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)

    if t == 0:
        return 0

    while t != 1:
        if t == 1:
            return r
        i = 1
        while pow(t, 2 ** i, p) == 1:
            i += 1
        b = c ** (2 ** (m - i - 1))
        m = i
        c = b ** 2
        t = t * b ** 2
        r = r * b

    return r


def graham_scan(p: list):
    base = min(p)
    p.remove(base)

    def sort_function(i):
        norm = abs(i[0] - base[0]) + abs(i[1] - base[1])
        if i[0] - base[0] == 0:
            return [1, 0, norm]
        else:
            return [0, (i[1] - base[1]) / (i[0] - base[0]), norm]
    p.sort(key=sort_function)
    convex = [base]

    for i in p:
        while len(convex) > 1:
            _ = ccw(convex[-2], convex[-1], i)
            if _ > 0:
                break
            convex.pop()
        convex.append(i)

    return convex


n = int(stdin.readline())
points = []

for i in range(n):
    points.append(list(map(int, stdin.readline().split())))

print(len(graham_scan(points)))
