from sys import stdin, stdout
import heapq


n, k = map(int, stdin.readline().split())
base = int(stdin.readline())
line, q, res = [[0, [-1, 1]]], [], 0

for i in range(1, n):
    dest = int(stdin.readline())
    dist = dest - base
    line.append([dist, [i - 1, i + 1]])
    heapq.heappush(q, [dist, [i, i + 1]])
    base = dest
line.append([0, [n - 1, n + 1]])
line.append([0, [n, n + 1]])


while k and q:
    v = heapq.heappop(q)
    cl = v[1][0]
    cr = v[1][1]

    if cl >= 1 and cr <= n and cr == line[cl][1][1] and cl == line[cr][1][0]:
        res += v[0]
        nl = line[cl][1][0]
        nr = line[cr][1][1]
        v[1][0] = nl
        v[1][1] = nr
        line[nl][0] = line[nl][0] + line[cr][0] - v[0]
        v[0] = line[nl][0]
        heapq.heappush(q, v)
        line[nl][1][1] = nr
        line[nr][1][0] = nl
        k -= 1

stdout.write(str(res))