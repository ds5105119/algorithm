from sys import stdin, stdout

n = int(stdin.readline())
m = [[0] * (n + 2) for i in range(n + 2)]
k = []

for i in range(n):
    mine = stdin.readline().rstrip()
    for j, cell in enumerate(mine):
        if cell == '.':
            continue
        else:
            k.append([i, j])
            cell = int(cell)
            m[i][j] += cell
            m[i][j + 1] += cell
            m[i][j + 2] += cell
            m[i + 1][j] += cell

            m[i + 1][j + 2] += cell
            m[i + 2][j] += cell
            m[i + 2][j + 1] += cell
            m[i + 2][j + 2] += cell

for i, l in enumerate(m[1:-1]):
    for j, c in enumerate(l[1:-1]):
        if [i, j] in k:
            stdout.write('*')
        else:
            if c > 9:
                stdout.write('M')
            else:
                stdout.write(str(c))
    stdout.write('\n')
