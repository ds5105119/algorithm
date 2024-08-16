from sys import stdin, stdout

n, b = map(int, stdin.readline().split())
sol = ''

while n > 0:
    m = n % b
    if m < 10 :
        sol += str(m)
    else:
        sol += chr(m - 10 + ord('A'))
    n = n // b

print(sol[::-1])