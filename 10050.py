# reference by https://keet.wordpress.com/2014/06/28/acm-icpc-2014-solution-to-problem-a-baggage/


def get(n):
    # particular solution
    if n == 3:
        print('2 to -1\n5 to 2\n3 to -3')
    elif n == 4:
        print('6 to -1\n3 to 6\n0 to 3\n7 to 0')
    elif n == 5:
        print('8 to -1\n3 to 8\n6 to 3\n0 to 6\n9 to 0')
    elif n == 6:
        print('10 to -1\n7 to 10\n2 to 7\n6 to 2\n0 to 6\n11 to 0')
    elif n == 7:
        print('12 to -1\n5 to 12\n8 to 5\n3 to 8\n9 to 3\n0 to 9\n13 to 0')

    # general solution
    else:
        pos = -1
        pre, cur = 2 * n - 2, -1
        mid = n // 2
        p = ([' ', ' '])
        p.extend(['B', 'A'] * n)

        def idx(a):
            return a + 1

        for i in range(mid):
            if pos ** i == 1:
                print(f'{pre} to {cur}')
                p[idx(cur)] = p[idx(pre)]
                p[idx(cur) + 1] = p[idx(pre) + 1]
                p[idx(pre)] = ' '
                p[idx(pre) + 1] = ' '
                cur += 4
            else:
                print(f'{cur} to {pre}')
                p[idx(pre)] = p[idx(cur)]
                p[idx(pre) + 1] = p[idx(cur) + 1]
                p[idx(cur)] = ' '
                p[idx(cur) + 1] = ' '
                pre -= 4
            print(p)

        print("안될거뭐있노?")

        if n % 2:
            pre += 2
            print(f'{pre} to {cur}')
            p[idx(cur)] = p[idx(pre)]
            p[idx(cur) + 1] = p[idx(pre) + 1]
            p[idx(pre)] = ' '
            p[idx(pre) + 1] = ' '

        print(p)
        print(pre, cur)
        pre, cur = pre, 0
        print("순전파 끝")

        for i in range(mid):
            if pos ** i == 1:
                print(f'{cur} to {pre}')
                p[idx(pre)] = p[idx(cur)]
                p[idx(pre) + 1] = p[idx(cur) + 1]
                p[idx(cur)] = ' '
                p[idx(cur) + 1] = ' '
                pre += 4
            else:
                print(f'{pre} to {cur}')
                p[idx(cur)] = p[idx(pre)]
                p[idx(cur) + 1] = p[idx(pre) + 1]
                p[idx(pre)] = ' '
                p[idx(pre) + 1] = ' '
                cur += 4
            print(p)


def main():
    n = int(input())
    get(n)

main()