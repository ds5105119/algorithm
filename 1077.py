from sys import stdin


def outer_product(a, b):
    return a[0] * b[1] - a[1] * b[0]


def ccw(base, a, b):
    ab = [a[0] - base[0], a[1] - base[1]]
    ac = [b[0] - base[0], b[1] - base[1]]
    return outer_product(ab, ac)


def sort_by_ccw(p: list):
    base = min(p)

    def sort_function(i):
        norm = abs(i[0] - base[0]) + abs(i[1] - base[1])
        if i[0] - base[0] == 0:
            return [1, 0, -norm]
        else:
            return [0, (i[1] - base[1]) / (i[0] - base[0]), -norm]

    p.sort(key=sort_function)

    return p


def graham_scan(p: list):
    convex = []

    for i in p:
        while len(convex) > 1:
            _ = ccw(convex[-2], convex[-1], i)
            if _ > 0:
                break
            convex.pop()
        convex.append(i)
    if ccw(convex[-2], convex[-1], convex[0]) == 0:
        convex = convex[:-1]

    return convex


def in_convex(a, p):
    base, start, end = p[0], 1, len(p) - 1

    if ccw(base, p[1], a) < 0:
        return False, 0
    if ccw(base, p[-1], a) > 0:
        return False, 0

    while end > start + 1:
        mid = (start + end) // 2
        if ccw(base, p[mid], a) < 0:
            end = mid
        else:
            start = mid

    return ccw(a, p[start], p[end]) > 0, [start, end]


def is_intersect(a1, a2, b1, b2):
    r = [a2[0] - a1[0], a2[1] - a1[1]]
    s = [b2[0] - b1[0], b2[1] - b1[1]]
    det = outer_product(r, s)

    if det == 0:
        # TODO: 선분이 겹쳐지는지 확인하고, 점 반환 결정
        pass
    else:
        _ = outer_product([b1[0] - a1[0], b1[1] - a1[1]], s)
        x = a1[0] + r[0] * _ / det
        y = a1[1] + r[1] * _ / det

        if (min(a1[0], a2[0]) <= x <= max(a1[0], a2[0]) and
            min(a1[1], a2[1]) <= y <= max(a1[1], a2[1]) and
            min(b1[0], b2[0]) <= x <= max(b1[0], b2[0]) and
            min(b1[1], b2[1]) <= y <= max(b1[1], b2[1])):
            return [x, y]
        else:
            return False


n = list(map(int, stdin.readline().split()))
points = [[], []]
inner_points_index = [[False] * n[0], [False] * n[1]]
polygon = []

for i in range(n[0]):
    points[0].append(list(map(int, stdin.readline().split())))
for i in range(n[1]):
    points[1].append(list(map(int, stdin.readline().split())))

points[0] = graham_scan(points[0])
points[1] = graham_scan(points[1])

convex_0_min = [min(points[0])[0], min([i[::-1] for i in points[0]])[0]]
convex_0_max = [max(points[0])[0], max([i[::-1] for i in points[0]])[0]]
convex_1_min = [min(points[1])[0], min([i[::-1] for i in points[1]])[0]]
convex_1_max = [max(points[1])[0], max([i[::-1] for i in points[1]])[0]]

for i, p in enumerate(points[0]):
    if convex_1_min[0] < p[0] < convex_1_max[0] and convex_1_min[1] < p[1] < convex_1_max[1]:
        value, edge_points = in_convex(p, points[1])
        if value:
            polygon.append(p)
            inner_points_index[0][i] = True

for i, p in enumerate(points[1]):
    if convex_0_min[0] < p[0] < convex_0_max[0] and convex_0_min[1] < p[1] < convex_0_max[1]:
        value, edge_points = in_convex(p, points[0])
        if value:
            polygon.append(p)
            inner_points_index[1][i] = True

if sum(inner_points_index[0]) < sum(inner_points_index[1]):
    points.reverse()
    inner_points_index.reverse()

for i, p in enumerate(points[0]):
    # 둘 다 안쪽에 있는 경우
    if inner_points_index[0][i] and inner_points_index[0][i - 1]:
        pass
    # 둘 다 바깥에 있는 경우
    elif not(inner_points_index[0][i] or inner_points_index[0][i - 1]):
        checksum_find = 0
        for j in range(len(points[1])):
            intersect_point = is_intersect(points[0][i - 1], p, points[1][j], points[1][(j + 1) % len(points[1])])
            if intersect_point:
                checksum_find += 1
                polygon.append(intersect_point)
                if checksum_find == 2:
                    break
    else:
        for j in range(len(points[1])):
            intersect_point = is_intersect(points[0][i - 1], p, points[1][j], points[1][(j + 1) % len(points[1])])
            if intersect_point:
                polygon.append(intersect_point)
                break


if polygon:
    polygon = sort_by_ccw(polygon)
    s = 0

    for i in range(1, len(polygon) - 1):
        s += abs(ccw(polygon[0], polygon[i], polygon[i + 1])) / 2

    print(s)
else:
    print(0)