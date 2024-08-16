from collections import Counter
x = Counter(input().upper())
if len(x) == 1:
    print(max(x))
elif x:
    y = x.most_common()
    print(y[0][0]) if y[0][1] > y[1][1] else print('?')