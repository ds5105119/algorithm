import random
arr = [random.randint(0, 9) for i in range(100000)]
print(arr[:100])
# 실제로는 데이터의 개수 N에 4를 곱한 크기만큼 미리 세그먼트 트리의 공간을 할당한다.
tree = [0] * (len(arr) * 4)


# <세그먼트 트리를 배열의 각 구간 합으로 채워주기>
# start : 배열의 시작 인덱스, end : 배열의 마지막 인덱스
# index : 세그먼트 트리의 인덱스 (무조건 1부터 시작)
# 세그먼트 트리가 1부터 시작하는 이유는 2를 곱했을 때 왼쪽 자식노드를 가리키고
# 2를 곱하고 1을 더하면 오른쪽 자식노드를 가리키므로 효과적이기 때문에 이렇게 한다!
def init(start, end, index):
    # 가장 끝에 도달했으면 arr 삽입
    if start == end:
        tree[index] = arr[start]
        return tree[index]
    mid = (start + end) // 2
    # 좌측 노드와 우측 노드를 채워주면서 부모 노드의 값도 채워준다.
    tree[index] = init(start, mid, index * 2) + init(mid + 1, end, index * 2 + 1)
    return tree[index]


# <구간 합을 구하는 함수>
# start : 시작 인덱스, end : 마지막 인덱스
# left, right : 구간 합을 구하고자 하는 범위
def interval_sum(start, end, index, left, right):
    # 범위 밖에 있는 경우
    if left > end or right < start:
        return 0
    # 범위 안에 있는 경우
    if left <= start and right >= end:
        return tree[index]
    # 그렇지 않다면 두 부분으로 나누어 합을 구하기
    mid = (start + end) // 2
    # start와 end가 변하면서 구간 합인 부분을 더해준다고 생각하면 된다.
    return interval_sum(start, mid, index * 2, left, right) + interval_sum(mid + 1, end, index * 2 + 1, left, right)


init(0, len(arr) - 1, 1)

sum = 0
for i in range(100000):
    interval_sum(0, len(arr) - 1, 1, 0, i + 1)

print(interval_sum(0, len(arr) - 1, 1, 0, 1))  # 0부터 9까지의 구간 합 (1 + 2 + ... + 9 + 10)
print(interval_sum(0, len(arr) - 1, 1, 0, 2))  # 0부터 2까지의 구간 합 (1 + 2 + 3)
print(interval_sum(0, len(arr) - 1, 1, 0, 3))  # 0부터 2까지의 구간 합 (7 + 8)
print(interval_sum(0, len(arr) - 1, 1, 0, 4))  # 0부터 2까지의 구간 합 (7 + 8)
print(interval_sum(0, len(arr) - 1, 1, 0, 5))  # 0부터 2까지의 구간 합 (7 + 8)
