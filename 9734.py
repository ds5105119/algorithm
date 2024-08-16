a = input().split('(')
b = a[0].split('.')

x, y, z = int(b[0]), float(b[1]), int(a[1][:-1])

b, c = len(a[0]), len(a[1]) - 1
d, e = float(a[0]), int(a[1][:-1])

print(a, b, c)