from sys import stdin, stdout
from decimal import Decimal, getcontext
from functools import reduce
getcontext().prec = 50


def hm(n: Decimal):
    if n < Decimal(1000):
        return reduce(lambda m, i: m + Decimal(1) / Decimal(i + 1), range(int(n)), Decimal(0))
    else:
        h = n.ln()
        h += Decimal("0.57721566490153286060")
        h += Decimal(1) / (Decimal(2) * n)
        h -= Decimal(1) / (Decimal(12) * n ** 2)
        h += Decimal(1) / (Decimal(120) * n ** 4)
        return h


n, k = stdin.readline().split()
n, k = Decimal(n), Decimal(k)
if n == k:
    stdout.write(str(n * hm(n)))
else:
    stdout.write(str(n * (hm(n) - hm(n - k))))
