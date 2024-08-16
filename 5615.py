import sys
PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


def miller_rabin(n):
    if n % 2 == 0 or n == 1:
        return False
    if n in PRIME:
        return True

    s, d = 1, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for a in PRIME:
        x, y = pow(a, d, n), 0
        for r in range(s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y
        if y != 1:
            return False
    return True


n, s = int(sys.stdin.readline()), []
count = 0

for i in range(n):
    s.append(int(sys.stdin.readline()))
for i in s:
    if miller_rabin(2 * i + 1):
        count += 1

print(count)
