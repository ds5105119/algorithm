import sys


node_count, weight_count = map(int, sys.stdin.readline().split(' '))
weights = [list(map(int, sys.stdin.readline().split(' '))) for _ in range(weight_count)]
search_list_count = int(sys.stdin.readline())
search_list = [list(map(int, sys.stdin.readline().split(' '))) for _ in range(search_list_count)]

weights = [[i[0] - 1, i[1] - 1, i[2]] for i in weights]
weights.sort(key=lambda i: i[2])
search_list = [[i[0] - 1, i[1] - 1] for i in search_list]
nodes = list(range(node_count))
tree, p = [[0, [], {i}] for i in nodes], nodes.copy()

for s in search_list:
    for i in range(len(weights)):
        if p[s[0]] == p[s[1]]:
            break
        w = weights.pop(0)
        if p[w[0]] == p[w[1]]:
            continue
        a, b = tree[p[w[0]]], tree[p[w[1]]]
        tree.append([w[2], [p[w[0]], p[w[1]]], {*a[2], *b[2]}])
        for c in tree[-1][2]:
            p[c] = len(tree) - 1

    if p[s[0]] == p[s[1]]:
        parent_node = tree[p[s[0]]]
        while True:
            test_a = set(s).issubset(tree[parent_node[1][0]][2])
            test_b = set(s).issubset(tree[parent_node[1][1]][2])
            if test_a:
                parent_node = tree[parent_node[1][0]]
            elif test_b:
                parent_node = tree[parent_node[1][1]]
            else:
                break
        sys.stdout.write(' '.join([str(parent_node[0]), str(len(parent_node[2]))]))
        sys.stdout.write('\n')
    else:
        sys.stdout.write('-1\n')

exit()

tree = [[0, {i}] for i in nodes]
p = nodes.copy()


for s in search_list:
    while p[s[0]] != p[s[1]]:
        w = weights.pop(0)
        tree.append([[p[w[0]], p[w[1]]], w[2], {*tree[p[w[0]]][2], *tree[p[w[1]]][2]}])
        for i in tree[-1][2]:
            p[i] = len(tree) - 1
    sys.stdout.write(' '.join([str(tree[p[s[0]]][1]), str(len(tree[p[s[0]]][2]))]))
    sys.stdout.write('\n')

exit()




nodes = list(range(node_count))

tree = dict(zip(nodes, [{'v': [i], 't': 0, 'c': [i]} for i in nodes]))
p = nodes.copy()

for w in weights:
    pa, pb = p[w[0]], p[w[1]]
    if pa != pb:
        new_node = len(tree)
        tree[new_node] = {'v': [pa, pb], 't': w[2], 'c': tree[pa]['c'] + tree[pb]['c']}
        for i in tree[new_node]['c']:
            p[i] = new_node

for s in search_list:
    local_end_node = tree[p[s[0]]]
    while True:
        test_1 = set(s).issubset(tree[local_end_node['v'][0]]['c'])
        test_2 = set(s).issubset(tree[local_end_node['v'][1]]['c'])

        if test_1:
            local_end_node = tree[local_end_node['v'][0]]
        elif test_2:
            local_end_node = tree[local_end_node['v'][1]]
        else:
            sys.stdout.write(' '.join([str(local_end_node['t']), str(len(local_end_node['c']))]))
            sys.stdout.write('\n')
            break
