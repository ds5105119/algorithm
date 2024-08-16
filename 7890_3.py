from sys import stdin, setrecursionlimit
from collections import deque
from random import sample
setrecursionlimit(10 ** 6)


def quad_node(x, y, l, r, b, t):
    return {'x': x, 'y': y,
            'l': l, 'r': r, 'b': b, 't': t,
            'NE': -1, 'NW': -1, 'SW': -1, 'SE': -1}


def distance(node_a, node_b):
    return (node_a['x'] - node_b['x']) ** 2 + (node_a['y'] - node_b['y']) ** 2


def make_rect_from_distance(dest, r):
    dist = r ** 0.5
    return dest['x'] - dist, dest['x'] + dist, dest['y'] - dist, dest['y'] + dist


def rectangle_overlaps_region(node, l, r, b, t):
    return (l < node['r']) and (r > node['l']) and (b < node['t']) and (t > node['b'])


class QuadTree:
    def __init__(self, x, y, *rect):
        self.tree = [quad_node(x, y, *rect)]

    def compare(self, p, x, y):
        _x, _y = self.tree[p]['x'], self.tree[p]['y']
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

    def search(self, x, y, p=0):
        direction = self.compare(p, x, y)
        if direction == 1:
            return self.search(x, y, self.tree[p]['NE'])
        elif direction == 2:
            return self.search(x, y, self.tree[p]['NW'])
        elif direction == 3:
            return self.search(x, y, self.tree[p]['SW'])
        elif direction == 4:
            return self.search(x, y, self.tree[p]['SE'])
        return p

    def insert(self, x, y, n=0):
        node = self.tree[n]
        direction = self.compare(n, x, y)
        if direction == 1:
            if node['NE'] == -1:
                self.tree[n]['NE'] = len(self.tree)
                self.tree.append(quad_node(x, y, node['x'], node['r'], node['y'], node['t']))
            else:
                return self.insert(x, y, node['NE'])
        elif direction == 2:
            if node['NW'] == -1:
                self.tree[n]['NW'] = len(self.tree)
                self.tree.append(quad_node(x, y, node['l'], node['x'], node['y'], node['t']))
            else:
                return self.insert(x, y, node['NW'])
        elif direction == 3:
            if node['SW'] == -1:
                self.tree[n]['SW'] = len(self.tree)
                self.tree.append(quad_node(x, y, node['l'], node['x'], node['b'], node['y']))
            else:
                return self.insert(x, y, node['SW'])
        elif direction == 4:
            if node['SE'] == -1:
                self.tree[n]['SE'] = len(self.tree)
                self.tree.append(quad_node(x, y, node['x'], node['r'], node['b'], node['y']))
            else:
                return self.insert(x, y, node['SE'])
        else:
            return False
        return True

    def _search_neighbor_nearest(self, dest, queue, r, *rect):
        p = queue.pop()
        node = self.tree[p]
        if node['x'] == dest['x'] and node['y'] == dest['y']:
            pass
        elif rectangle_overlaps_region(node, *rect):
            new_r = distance(dest, node)
            if r > new_r:
                r = new_r
                rect = make_rect_from_distance(dest, r)

        if node['NE'] != -1:
            queue.appendleft(node['NE'])
        if node['NW'] != -1:
            queue.appendleft(node['NW'])
        if node['SW'] != -1:
            queue.appendleft(node['SW'])
        if node['SE'] != -1:
            queue.appendleft(node['SE'])

        if not queue:
            return r

        return self._search_neighbor_nearest(dest, queue, r, *rect)

    def search_neighbor_nearest(self, x, y):
        dest = self.tree[self.search(x, y)]
        if dest['NE'] != -1:
            r = distance(dest, self.tree[dest['NE']])
        elif dest['NW'] != -1:
            r = distance(dest, self.tree[dest['NW']])
        elif dest['SW'] != -1:
            r = distance(dest, self.tree[dest['SW']])
        elif dest['SE'] != -1:
            r = distance(dest, self.tree[dest['SE']])
        else:
            r = distance(dest, self.tree[0])
        rect = make_rect_from_distance(dest, r)

        return self._search_neighbor_nearest(dest, deque([0]), r, *rect)


def main():
    test_count = int(stdin.readline())

    for i in range(test_count):
        point_count = int(stdin.readline())
        points = [tuple(map(int, stdin.readline().split())) for _ in range(point_count)]
        sampled_points = sample(points, point_count)
        quadtree = QuadTree(*sampled_points[0], 0, 1e10, 0, 1e10)

        for p in sampled_points[1:]:
            quadtree.insert(*p)

        for p in points:
            print(quadtree.search_neighbor_nearest(*p))


main()


def main():
    test_count = int(stdin.readline())

    for i in range(test_count):
        point_count = int(stdin.readline())
        points = [tuple(map(int, stdin.readline().split())) for _ in range(point_count)]

        for j in range(len(points)):
            x = map(lambda p: (points[j][0] - points[p][0]) ** 2 + (points[j][1] - points[p][1]) ** 2, points[:j] + points[j + 1:])
            print(min(x))


main()
