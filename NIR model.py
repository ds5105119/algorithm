from collections import defaultdict


def solve(n, arr):
    # 순환 리스트 생성
    cycle = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        cycle[abs(arr[i - 1])].append(i)

    # 강한 연결 요소 분할
    visited = [False] * (n + 1)
    scc_id = [0] * (n + 1)
    scc_cnt = 0
    for i in range(1, n + 1):
        if not visited[i]:
            scc_cnt += 1
            dfs(i, cycle, visited, scc_id, scc_cnt)

    # 순열 사이클 분할 및 최소 연산 길이 계산
    cycle_info = defaultdict(list)
    for i in range(1, n + 1):
        if scc_id[i] == scc_id[abs(arr[i - 1])]:
            cycle_info[scc_id[i]].append((min(i, abs(arr[i - 1])), max(i, abs(arr[i - 1]))))

    # 최소 연산 길이 계산
    min_op = 0
    for scc, cycle in cycle_info.items():
        if len(cycle) == 1:
            min_op += 1
        else:
            # 사이클 내 이동 거리 계산
            cycle_dist = abs(cycle[-1][1] - cycle[0][0])
            for i in range(len(cycle) - 1):
                cycle_dist += abs(cycle[i + 1][0] - cycle[i][1])
            min_op += min(cycle_dist, cycle_dist - abs(cycle[0][0] - cycle[-1][1]))

    # 회전 연산 정보 정렬 및 최소 연산 길이에 맞는 정보 추출
    for scc in cycle_info:
        cycle_info[scc].sort()
        if len(cycle_info[scc]) > 1:
            cycle_info[scc] = cycle_info[scc][:-1]
            min_op -= 1

    # 출력
    print(min_op)
    for scc in cycle_info:
        for a, b in cycle_info[scc]:
            print(a, b)


def dfs(v, cycle, visited, scc_id, scc_cnt):
    """
  순환 리스트에서 강한 연결 요소를 찾는 함수

  Args:
    v: 현재 탐색하는 정점
    cycle: 순환 리스트
    visited: 방문 여부 리스트
    scc_id: 강한 연결 요소 ID 리스트
    scc_cnt: 강한 연결 요소 카운터
  """
    visited[v] = True
    scc_id[v] = scc_cnt

    for next in cycle[v]:
        if not visited[next]:
            dfs(next, cycle, visited, scc_id, scc_cnt)


# 입력 처리
n = int(input())
arr = list(map(int, input().split()))

# 문제 해결
solve(n, arr)
