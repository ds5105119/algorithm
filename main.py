from collections import defaultdict
from sys import stdin


def find_cycles(permutation):
    n = len(permutation)
    visited = [False] * n
    cycles = []
    stack = []

    def dfs(i):
        visited[i] = True
        stack.append(i)

        while stack:
            j = permutation[stack[-1]] - 1
            if not visited[j]:
                return dfs(j)
            else:
                if j == i:
                    cycle = stack[:]
                    while cycle:
                        visited[cycle.pop()] = False
                    cycles.append(cycle)
                elif j >= n:
                    break

    for i in range(n):
        if not visited[i]:
            dfs(i)

    return cycles


def reverse_cycle(permutation, cycle, signs):
    for i, j in zip(cycle, cycle[::-1]):
        permutation[i] = j
        signs[i] = not signs[i]


def solve(n, permutation):
    signs = [True] * n
    cycles = find_cycles(permutation)
    answer = len(cycles)

    for cycle in cycles:
        reverse_cycle(permutation, cycle, signs)

    return answer, [(cycle[0] + 1, cycle[-1] + 1) for cycle in cycles]


n = int(stdin.readline())
permutation = list(map(int, stdin.readline().split()))

answer, operations = solve(n, permutation)

print(answer)
for a, b in operations:
    print(a, b)
