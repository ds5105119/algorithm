def f(a, b, arr):
    _ = arr[:a]
    _.append([-i for i in arr[a:b+1]])
    _.append(arr[b+1:])
    return _


def solve(n, arr):
    visited = [False] * n
    stack = []

    def dfs(i):
        visited[i] = True
        stack.append(arr)

        while stack:
            j = arr[stack[-1]]
            if visited[j]:
                pass
            else:
                return dfs(i)
