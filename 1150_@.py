from sys import stdin, stdout
import heapq


n, k = map(int, stdin.readline().split())
base = int(stdin.readline())
line, res = [], 0

for i in range(n - 1):
    dest = int(stdin.readline())
    line.append([dest - base, i])
    base = dest

while k and len(line) > 2:
    val = min(line[1:-1])
    idx = line.index(val)
    res += line[idx][0]
    if idx == 0:
        line[idx][0] = line[idx + 1][0] - line[idx][0]
        line.pop(idx + 1)
    elif idx == len(line) - 1:
        line[idx][0] = line[idx - 1][0] - line[idx][0]
        line.pop(idx - 1)
    else:
        line[idx][0] = line[idx + 1][0] + line[idx - 1][0] - line[idx][0]
        line.pop(idx + 1)
        line.pop(idx - 1)
    k -= 1

if k > 0:
    res += min(line)[0]



stdout.write(str(res))