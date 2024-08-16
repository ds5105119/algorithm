from sys import stdin
import math

N = int(stdin.readline())
f = [[0, 0, 0]]
charged = False


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


for i in range(N):
    v = list(map(int, stdin.readline().split()))

    if f[i][1] + v[0] == v[1]:
        v.append(0)
        f.append(v)
    elif v[0] < 0:
        change = v[1] - v[0] - f[i][1]
        if change > 0:
            charged = True
            v.append(change)
            f.append(v)
        else:
            print(-1)
            exit(0)
    else:
        print(-1)
        exit(0)

if charged:
    charge_maximum = min(i[2] for i in f if i[2] != 0)
    charge_minimum = max(i[1] for i in f if i[2] != 0)
else:
    print(1)
    exit(0)

a = math.gcd(*[i[2] for i in f if i[2] != 0])
if charge_minimum < a <= charge_maximum:
    print(a)
else:
    print(-1)

M = charge_maximum

for i in [i for i in f if i[2] != 0]:
    if i[2] % M != 0:
        M = gcd(i[2], M)
        if not charge_minimum < M:
            break

if not charge_minimum < M:
    print(-1)
else:
    print(M)
