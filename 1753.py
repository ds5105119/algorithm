from sys import stdin


def update(tree, idx, val):
    while idx < len(tree) - 1:
        tree[i][idx] += val
        idx += idx & -idx


def update_range(tree, start, end, val):
    if start <= end:
        update(tree, start, val)
        update(tree, end + 1, -val)
    else:
        update(tree, 1, val)
        update(tree, start + 1, -val)
        update(tree, end, val)


def get_sum(tree, idx):
    ret = 0

    while idx > 0:
        ret += tree[idx]
        idx -= idx & -idx

    return ret


n, m = map(int, stdin.readline().split())
o = map(int, stdin.readline().split())
g = [list() * (n + 1)]
p = map(int, stdin.readline().split())
q = int(stdin.readline())
a = []
chk = True
l, r = [1] * (n + 1), list(range(n + 1))

for i in range(len(o)):
    g[o[i]].append(i)
del o

for i in range(1, q + 1):
    a.append(list(map(int, stdin.readline().split())))

while chk:
    chk = False
    tree = [[0] * (m + 1)]
    for i in range(1, n + 1):
        if l[i] < r[i]:
            g.append(l[i] + r[i])
        if lo[i] < hi[i]:
        vt[(lo[i] + hi[i]) >> 1].push_back(i)

