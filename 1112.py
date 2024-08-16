from sys import stdin, stdout
x, b = map(int, stdin.readline().split())
s, c = '', ''

if x < 0 < b:
    c += '-'
    x *= -1

while x != 0:
    n = int(x / b)
    m = x - n * b
    if m < 0:
        n += 1
        m -= b
    x = n
    s += str(m)

if s:
    stdout.write(c + s[::-1])
else:
    stdout.write('0')