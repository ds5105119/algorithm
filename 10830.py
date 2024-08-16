from sys import stdin, stdout


def dot(x, y):
    d = list(map(lambda _: [0] * len(x), range(len(x))))
    for i in range(len(x)):
        for j in range(len(x)):
            for k in range(len(x)):
                d[i][j] += x[i][k] * y[k][j]
            d[i][j] %= 1000
    return d


n, b = stdin.readline().split()
n, b = int(n), format(int(b), 'b')
m = []

for i in range(n):
    m.append(list(map(int, stdin.readline().split())))

m_c = list(map(lambda _: [0] * n, range(n)))
for i in range(n):
    m_c[i][i] = 1

if b[-1] == '1':
    m_c = dot(m_c, m)

for i in b[:-1][::-1]:
    m = dot(m, m)
    if i == '1':
        m_c = dot(m_c, m)

for i in m_c:
    for j in i:
        stdout.write(str(j) + ' ')
    stdout.write('\n')