p=sorted([list(set(map(int, input().split())))for _ in range(int(input()))])
l,r=p[0]
s=0
for i in p[1:]:
    if i[0]<=r<i[1]:
        r=i[1]
    elif r<i[0]:
        s+=r-l
        l,r=i
print(s+r-l)