import numpy as np
import random

SHAPE = np.array([8, 14])


def find(a: str, array, candidate=None, path=None):
    if not a:
        return path

    if candidate is None:
        score = []
        for i in np.transpose(np.nonzero(array == int(a[0]))):
            path = find(a[1:], array, i, i)
            if path is not False:
                score.append(path)
        return np.array(score)

    else:
        k, l = np.fmax(0, candidate - 1), np.fmin(candidate + 2, SHAPE)
        c = np.full_like(array, -1)
        c[k[0]:l[0], k[1]:l[1]] = array[k[0]:l[0], k[1]:l[1]]
        c[*candidate] = -1
        c = np.transpose(np.nonzero(c == int(a[0])))

        if c.any():
            for i in c:
                return find(a[1:], array, i, np.vstack([path, i]))
        else:
            return False


def model(array):
    score = 0

    for i in range(10000):
        if not find(str(i), array).size:
            break
        score += 1

    return score


def model_score(array):
    s = np.zeros(SHAPE)

    for i in range(10000):
        path = find(str(i), array)
        if not path.size:
            break
        s[np.vstack(path).T[0], np.vstack(path).T[1]] += (len(str(i)) - 1) / path.shape[0] ** 2

    return s


def score(array):
    parameter_score, score = np.zeros(SHAPE), 0

    for i in range(10000):
        path = find(str(i), array)
        if not path.size:
            break
        np.add.at(parameter_score, tuple(path.reshape(2, -1)), (len(str(i)) - 1) / path.shape[1] ** 2)
        score += 1

    return parameter_score


def model(array):
    s = 0

    for i in range(10000):
        path = find(str(i), array)
        if not path.size:
            break
        s += 1

    return s


mask_2 = mask_2.reshape(path.shape[1], 8, 14)
facecolors = np.where(mask_2, '#FFD65DC0', '#7A88CC05')
edgecolors = np.where(mask_2, '#BFAB6EC0', '#7D84A605')
filled = np.ones(mask_2.shape)

filled_2 = explode(filled)
fcolors_2 = explode(facecolors)
ecolors_2 = explode(edgecolors)

x, y, z = np.indices(np.array(filled_2.shape) + 1).astype(float) // 2
x[0::2, :, :] += 0.05
y[:, 0::2, :] += 0.05
z[:, :, 0::2] += 0.05
x[1::2, :, :] += 0.95
y[:, 1::2, :] += 0.95
z[:, :, 1::2] += 0.95

ax = plt.figure().add_subplot(projection='3d')
ax.voxels(x, y, z, filled_2, facecolors=fcolors_2, edgecolors=ecolors_2)
ax.set_aspect('equal')

plt.show()
