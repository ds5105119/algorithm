from sys import stdin, stdout


class ListTree:
    def __init__(self):
        self.tree = list()

    def append(self):
        pass



def one_sweep(w):
    stack, s = [w[-2], w[-1]], []

    for w_c in w[:-2][::-1]:
        while len(stack) >= 2 and stack[-1] > w_c:
            stack.pop()
            s.append([stack[-1], w_c])
        stack.append(w_c)

    while len(stack) > 3:
        stack.pop()
        s.append([stack[-1], stack[0]])

    return s


def one_sweep2(w):
    stack, s = [], []

    for w_c in w:
        while len(stack) >= 2 and stack[-1] > w_c:
            stack.pop()
            s.append([stack[-1], w_c])
        stack.append(w_c)

    while len(stack) > 3:
        stack.pop()
        s.append([stack[-1], stack[0]])

    return s


print(one_sweep([1, 16, 34, 259, 77, 29, 44]))
print(one_sweep2([1, 16, 34, 259, 77, 29, 44]))


