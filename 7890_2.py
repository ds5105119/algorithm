from sys import stdin, stdout, setrecursionlimit
from collections import deque
from random import sample
setrecursionlimit(10 ** 6)


class QuadNode:
    def __init__(self, x, y, l, r, b, t):
        self.x = x
        self.y = y
        self.l = l
        self.r = r
        self.b = b
        self.t = t
        self.NE = None
        self.NW = None
        self.SW = None
        self.SE = None


def distance(node_a, node_b):
    return (node_a.x - node_b.x) ** 2 + (node_a.y - node_b.y) ** 2


def make_rect_from_distance(dest, r):
    dist = r ** 0.5
    return dest.x - dist, dest.x + dist, dest.y - dist, dest.y + dist


def compare(node, x, y):
    _x, _y = node.x, node.y
    if _x == x and _y == y:
        return 0
    elif _x < x and _y < y:
        return 1
    elif _x >= x and _y <= y:
        return 2
    elif _x >= x and _y >= y:
        return 3
    else:
        return 4


def insert(node, x, y):
    direction = compare(node, x, y)
    if direction == 1:
        if not node.NE:
            node.NE = QuadNode(x, y, node.x, node.r, node.y, node.t)
        else:
            node.NE = insert(node.NE, x, y)
    elif direction == 2:
        if not node.NW:
            node.NW = QuadNode(x, y, node.p, node.x, node.y, node.t)
        else:
            node.NW = insert(node.NW, x, y)
    elif direction == 3:
        if not node.SW:
            node.SW = QuadNode(x, y, node.p, node.x, node.b, node.y)
        else:
            node.SW = insert(node.SW, x, y)
    elif direction == 4:
        if not node.SE:
            node.SE = QuadNode(x, y, node.x, node.r, node.b, node.y)
        else:
            node.SE = insert(node.SE, x, y)
    else:
        return False

    return node


def search(node, x, y):
    direction = compare(node, x, y)
    if direction == 1:
        return search(node.NE, x, y)
    elif direction == 2:
        return search(node.NW, x, y)
    elif direction == 3:
        return search(node.SW, x, y)
    elif direction == 4:
        return search(node.SE, x, y)

    return node


def rectangle_overlaps_region(node, l, r, b, t):
    return (l < node.r) and (r > node.p) and (b < node.t) and (t > node.b)


def search_neighbor_nearest(queue: deque, dest, r, *rect):
    node = queue.pop()
    if node.x == dest.x and node.y == dest.y:
        pass
    elif rectangle_overlaps_region(node, *rect):
        new_r = distance(dest, node)
        if r > new_r:
            r = new_r
            rect = make_rect_from_distance(dest, r)

    if node.NE:
        queue.appendleft(node.NE)
    if node.NW:
        queue.appendleft(node.NW)
    if node.SW:
        queue.appendleft(node.SW)
    if node.SE:
        queue.appendleft(node.SE)

    if not queue:
        return r

    return search_neighbor_nearest(queue, dest, r, *rect)


def nearest_node_search(root, x, y):
    dest = search(root, x, y)
    if dest.NE:
        r = distance(dest, dest.NE)
    elif dest.NW:
        r = distance(dest, dest.NW)
    elif dest.SW:
        r = distance(dest, dest.SW)
    elif dest.SE:
        r = distance(dest, dest.SE)
    else:
        r = distance(dest, root)
    rect = make_rect_from_distance(dest, r)

    return search_neighbor_nearest(deque([root]), dest, r, *rect)


def main():
    test_count = int(stdin.readline())

    for i in range(test_count):
        point_count = int(stdin.readline())
        points = [tuple(map(int, stdin.readline().split())) for _ in range(point_count)]
        sampled_points = sample(points, point_count)
        root = QuadNode(*sampled_points[0], 0, 1e10, 0, 1e10)

        for p in sampled_points[1:]:
            root = insert(root, *p)

        for p in points:
            print(nearest_node_search(root, *p))


main()