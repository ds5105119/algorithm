import numpy as np
import pandas as pd
import time
import sys

# USER CONFIG
rng = np.random.default_rng()
SHAPE = (8, 14)
ENTITY = 42
SEARCH_DEPTH = 4  # 최대 문자열의 길이
SEARCH_RANGE = 100  # Below SHAPE[0] * SHAPE[1] * 10
SEARCH_COUNT = 20  # Below SHAPE[0] * SHAPE[1] * 10

# COMPUTE NUMBER OF CASES
ROUTE_GROUP = np.indices((2 * SEARCH_DEPTH - 1,) * 2)
ARRAY_ROUTE = [ROUTE_GROUP[:, SEARCH_DEPTH - 1, SEARCH_DEPTH - 1].reshape(1, 2)]
PATH_SIEVE = []
SEARCH_LIST = []

for i in range(SEARCH_DEPTH - 1):
    route = np.empty((8 ** i, 8, 2), dtype=int)
    for j in range(8 ** i):
        pre_idx = ARRAY_ROUTE[-1][j]
        now_idx = ROUTE_GROUP[:, pre_idx[0] - 1:pre_idx[0] + 2, pre_idx[1] - 1:pre_idx[1] + 2]
        route[j] = now_idx.reshape(2, -1).T[[0, 1, 2, 3, 5, 6, 7, 8]]
    ARRAY_ROUTE.append(route.reshape(-1, 2))

_padded_array = np.pad(np.zeros(SHAPE), SEARCH_DEPTH - 1, 'constant', constant_values=1)
_routed_array = np.lib.stride_tricks.sliding_window_view(_padded_array, SHAPE)
_path = np.empty((8, ) * (SEARCH_DEPTH - 1) + (*SHAPE, SEARCH_DEPTH), dtype=int)
for i in range(SEARCH_DEPTH):
    _path[..., i] = _routed_array[*ARRAY_ROUTE[i].T].reshape((8,) * i + SHAPE)
    PATH_SIEVE.append(np.all(_path[*(0, ) * (SEARCH_DEPTH - i - 1), ..., :i + 1].reshape(-1, i + 1) == 0, axis=1))
    SEARCH_LIST.append(np.array(np.unravel_index(np.arange(10 ** (i + 1)), (10, ) * (i + 1))).T)
del _padded_array, _routed_array, _path


def find(array):
    padded_array = np.pad(array, SEARCH_DEPTH - 1, 'constant', constant_values=-1)
    routed_array = np.lib.stride_tricks.sliding_window_view(padded_array, SHAPE)
    raw_path = np.empty((8, ) * (SEARCH_DEPTH - 1) + (*SHAPE, SEARCH_DEPTH), dtype=int)
    path = []
    for i in range(SEARCH_DEPTH):
        raw_path[..., i] = routed_array[*ARRAY_ROUTE[i].T].reshape((8,) * i + SHAPE)
        path.append(raw_path[*(0, ) * (SEARCH_DEPTH - i - 1), ..., :i + 1].reshape(-1, i + 1)[PATH_SIEVE[i]])

    score = []
    for i in range(SEARCH_DEPTH):
        #score.append(np.unique(path[i]))
        #score.append(np.isin(SEARCH_LIST[i], path[i], assume_unique=True))
        #score.append(pd.Series(path[i].view(("S", path[i][0].nbytes))[:, 0]).duplicated())
        print(np.unique(np.sort(path[i], axis=0), axis=0))
    return path, score


t = time.time()
for i in range(1):
    a = find(np.arange(8 * 14).reshape(8, 14) % 10)
    a = find(np.loadtxt('./bestmodel.txt', dtype=int))
print(time.time() - t)


def find3d(a: str, array, path=None):
    """
    :param a: 찾을 문자
    :param array: a를 찾을 배열들
    :param path: 내부 재귀 과정에 사용됨
    :return: 좌표 행렬 [3, 찾은 개수, len(a)]의 모습
    """
    if path is None:
        path = np.array(np.nonzero(array == int(a[0])), dtype=int).reshape(3, -1, 1)

        if path.size == 0:
            return path
        if len(a) == 1:
            return path
        return find3d(a[1:], array, path)
    else:
        # 다음 후보를 찾기 위한 마스크 생성
        start = np.fmax(0, path[1:, :, -1] - 1)
        end = np.fmin(np.array([[array.shape[1]], [array.shape[2]]]), path[1:, :, -1] + 1)
        idx_1, idx_2 = np.arange(SHAPE[0]), np.arange(SHAPE[1])
        mask_1 = (start[0].reshape(-1, 1) <= idx_1) & (end[0].reshape(-1, 1) >= idx_1)
        mask_2 = (start[1].reshape(-1, 1) <= idx_2) & (end[1].reshape(-1, 1) >= idx_2)

        # 후보별 갈 수 있는 위치를 확인
        value, count = np.unique(path[0, :, -1], return_counts=True)
        search_array = np.repeat((array[value] == int(a[0])), count, axis=0)
        search_array *= np.expand_dims(mask_1, axis=2)
        search_array *= np.expand_dims(mask_2, axis=1)
        search_array[np.arange(path.shape[1]), *path[1:, :, -1]] = False
        found_path = np.array(np.nonzero(search_array))

        # 확보한 길을 저장
        new_path = np.empty((3, found_path.shape[1], path.shape[2] + 1), dtype=int)
        new_path[..., -1] = found_path
        new_path[..., :-1] = path[:, found_path[0]]
        new_path[0, :, -1] = new_path[0, :, -2]

        if found_path.size == 0:
            return np.array([])
        if len(a) == 1:
            return new_path
        return find3d(a[1:], array, new_path)


def score_3d(array, start, end=10000, parameter_score=None, paths=None):
    start = np.full(len(array), 1) if type(start) is int else start
    parameter_score = np.zeros_like(array, dtype=float) if parameter_score is None else parameter_score
    paths = []
    score = np.full(len(array), start - 1, dtype=int)

    for i in range(start.min(), end):
        progress_chk = (score == i - 1) & (start <= i)
        progress_idx = np.where(progress_chk)[0]
        progress_array = array[progress_chk]

        if i < 10:
            path = find3d(str(i), progress_array)
        else:
            pre_path = paths[int(str(i)[:-1]) - 1]
            condition = np.isin(pre_path[0, :, 0], progress_idx)
            pre_path = np.compress(condition, pre_path, axis=1)
            pre_path_value, pre_path_count = np.unique(pre_path[0, :, 0], return_counts=True)
            pre_path[0] = np.repeat(np.arange(np.count_nonzero(progress_chk)), pre_path_count).reshape(-1, 1)
            path = find3d(str(i)[-1], progress_array, pre_path)

            if path.size == 0:
                break
            path_value, path_count = np.unique(path[0, :, 0], return_counts=True)
            path[0] = np.repeat(pre_path_value[path_value], path_count).reshape(-1, 1)

        paths.append(path)
        value, count = np.unique(path[0], return_counts=True)
        p = np.repeat(np.log(len(str(i)) + 1) / count, count)
        score[value] += 1
        np.add.at(parameter_score, tuple(path.reshape(3, -1)), p)

    return parameter_score, score, paths


def chunk_check(idx, score, paths):
    is_passed = np.full(len(idx), True, dtype=bool)
    for i, path in enumerate(paths):
        validate = (path == np.expand_dims(idx[score > i], [2, 3])).all(1).any(2).sum(1)
        value, count = np.unique(path[0, :, 0], return_counts=True)
        is_passed[score > i] &= (count - validate) > 0
    return is_passed


def chunk_check2(array, idx, score, paths):
    is_passed = np.full(len(array), True, dtype=bool)
    for i, path in enumerate(paths):
        value, count = np.unique(path[0, :, 0], return_counts=True)
        path = np.split(path, np.cumsum(count)[:-1], axis=1)
        validate = [(path[n][1:] == np.expand_dims(idx[n][1:], [1, 2])).all(0).any(1).sum() for n in range(len(path))]
        is_passed[score > i] &= (count - validate) > 0
    return is_passed


def shuffle(array, low: int = 2, high: int = 10):
    for i in range(len(array)):
        temp_arr = array[i].copy()
        n = rng.integers(low, high)
        seed_idx = rng.choice(np.arange(10), n, replace=False)
        seed_val = rng.permutation(seed_idx)
        for k in range(n):
            temp_arr[array[i] == seed_idx[k]] = seed_val[k]
        array[i] = temp_arr
    return array


def random_change(array):
    for i in range(len(array)):
        idx = np.random.choice(np.arange(SHAPE[0] * SHAPE[1]), 2, replace=False)
        val = array[i][idx // SHAPE[1], idx % SHAPE[1]]
        array[i, idx[0] // SHAPE[1], idx[0] % SHAPE[1]] = val[1]
        array[i, idx[1] // SHAPE[1], idx[1] % SHAPE[1]] = val[0]
    return array


def choice_idx(parameter_score):
    p = abs(parameter_score.flatten() - parameter_score.max()) ** 2
    p = p / p.sum()
    temp = rng.choice(np.arange(SHAPE[0] * SHAPE[1]), p=p)
    return temp // SHAPE[1], temp % SHAPE[1]


def main():
    parameters = np.zeros((ENTITY, *SHAPE))
    parameters[:] = np.loadtxt('./bestmodel.txt', dtype=int)
    parameters[1:] = shuffle(parameters[1:], 3, 5)

    parameter_score, score, path = score_3d(parameters, 1)
    best_score = score[0]
    stopped = np.zeros(ENTITY)
    temp = None
    print(score)

    for epoch in range(50000):
        parameter_score, score, path = score_3d(parameters, 1)
        change_idx = np.full((SEARCH_RANGE, ENTITY, 4), -1)
        change_score = np.zeros((SEARCH_RANGE, ENTITY), dtype=int)

        for i in range(SEARCH_RANGE):
            for n in range(ENTITY):
                while True:
                    idx = np.array([n, *choice_idx(parameter_score[n]), np.random.randint(1, 10)])
                    if ~(change_idx[:, n] == idx).all(1).any() and parameters[*idx[:3]] != idx[3]:
                        change_idx[i, n] = idx
                        break
            new_parameter = parameters
            new_parameter[*change_idx[i, :, :3].T] = change_idx[i, :, 3]

            t = time.time()
            chunk_checksum = chunk_check(change_idx[i, :, :3], score, path)
            new_parameter_score, new_score, new_path = score_3d(new_parameter[chunk_checksum], 0)
            change_score[i, np.where(chunk_checksum)] = new_score
            print(time.time() - t)

        print(change_score.max(axis=0), '\n', change_score)

        temp = change_idx if (~is_passed).any() else None
        parameters[stopped >= 20] = random_change(parameters[stopped >= 20])
        stopped[stopped >= 20] = 0

        if epoch % 200 == 0:
            score_rank = np.argsort(score)[[0, 1, 2]]
            parameters[score_rank] = shuffle(parameters[score_rank])
            parameter_score, score, path = score_3d(parameters)

        if score.max() > best_score:
            best_score = score.max()
            np.savetxt('./bestmodel.txt', parameters[np.where(score == best_score)[0][0]].reshape(8, 14), fmt='%d')


if __name__ == '__main__':
    main()
