import numpy as np
import random
import matplotlib.pyplot as plt

SHAPE = np.array([8, 14])
ENTITY = 10
SEARCH_DEPTH = 20
SEARCH_COUNT = 20


def explode(data):
    size = np.array(data.shape)*2
    data_e = np.zeros(size - 1, dtype=data.dtype)
    data_e[::2, ::2, ::2] = data
    return data_e


def find(a: str, array, path=None):
    if path is None:
        candidates = np.array(np.nonzero(array == int(a[0]))).reshape(3, -1, 1)

        if candidates.size == 0:
            return np.array([])
        if len(a) == 1:
            return candidates
        return find(a[1:], array, candidates)
    else:
        # 다음 후보를 찾기 위한 3차원 마스크 생성
        start, end = np.fmax(0, path[..., -1] - 1), np.fmin(SHAPE.reshape(2, 1), path[..., -1] + 1)
        r_1 = np.tile(np.arange(8), (14, 1))
        r_2 = np.tile(np.arange(14), (8, 1))
        mask_1 = (start[0].reshape(-1, 1, 1) <= r_1) & (end[0].reshape(-1, 1, 1) >= r_1)
        mask_2 = (start[1].reshape(-1, 1, 1) <= r_2) & (end[1].reshape(-1, 1, 1) >= r_2)
        mask_2 &= mask_1.swapaxes(1, 2)
        mask_2[np.arange(path.shape[1]), *path[..., -1]] = False

        # 후보별 갈 수 있는 위치를 저장
        c = np.array(np.nonzero((array + 1) * mask_2 - 1 == int(a[0])))
        new_path = np.full((2, c.shape[1], path.shape[2] + 1), 0)
        new_path[..., :-1] = path[:, c[0]]
        new_path[..., -1] = c[1:]

        if c.size == 0:
            return np.array([])
        if len(a) == 1:
            return new_path
        return find(a[1:], array, new_path)


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
        # 다음 후보를 찾기 위한 3차원 마스크 생성
        start, end = np.fmax(0, path[1:, :, -1] - 1), np.fmin(SHAPE.reshape(2, 1), path[1:, :, -1] + 1)
        r_1 = np.tile(np.arange(SHAPE[0]), (SHAPE[1], 1))
        r_2 = np.tile(np.arange(SHAPE[1]), (SHAPE[0], 1))
        mask_1 = (start[0].reshape(-1, 1, 1) <= r_1) & (end[0].reshape(-1, 1, 1) >= r_1)
        mask_2 = (start[1].reshape(-1, 1, 1) <= r_2) & (end[1].reshape(-1, 1, 1) >= r_2)
        mask_2 &= mask_1.swapaxes(1, 2)
        mask_2[np.arange(path.shape[1]), *path[1:, :, -1]] = False

        # 후보별 갈 수 있는 위치를 확인
        value, count = np.unique(path[0, :, -1], return_counts=True)
        search_array_mask = np.repeat((array[value] == int(a[0])), count, axis=0)
        found_path = np.array(np.nonzero(mask_2 & search_array_mask))

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


def score_3d(array, start=1, end=10000, parameter_score=None):
    score = np.full(len(array), start - 1, dtype=int)
    found_path = np.empty(10 ** (len(str(end - 1)) - 1), dtype=object)
    if parameter_score is None:
        parameter_score = np.zeros_like(array, dtype=float)

    for i in range(start, end):
        progress_chk = score == i - 1
        progress_idx = np.where(progress_chk)[0]
        progress_array = array[progress_chk]

        if i < 10:
            path = find3d(str(i), progress_array)
        else:
            pre_path = found_path[int(str(i)[:-1]) - 1]
            condition = np.isin(pre_path[0, :, 0], progress_idx)
            pre_path = np.compress(condition, pre_path, axis=1)

            pre_path_value, pre_path_count = np.unique(pre_path[0, :, 0], return_counts=True)
            pre_path[0] = np.repeat(np.arange(np.count_nonzero(progress_chk)), pre_path_count).reshape(-1, 1)

            path = find3d(str(i)[-1], progress_array, pre_path)
            path_value, path_count = np.unique(path[0, :, 0], return_counts=True)
            path[0] = np.repeat(pre_path_value[path_value], path_count).reshape(-1, 1)

        if path.size == 0:
            break

        if i < len(found_path):
            found_path[i - 1] = path

        value, count = np.unique(path[0], return_counts=True)
        temp_score = np.zeros_like(parameter_score[progress_idx])
        p = np.repeat((len(str(i)) / count) ** 2, count)

        print(i, progress_idx, value, progress_idx[value])

        score[progress_idx[value]] += 1
        np.add.at(temp_score, tuple(path.reshape(3, -1)), p)
        parameter_score[progress_idx] += temp_score

    return parameter_score, score


def find3d(i, a, arr):
    return np.pad(find(str(a), arr).reshape(2, -1), ((1, 0), (0, 0)), 'constant', constant_values=i)


def score_3d(array, start=1, end=10000, parameter_score=None):
    if parameter_score is None:
        parameter_score = np.zeros_like(array, dtype=float)
    score = np.full(len(array), start - 1, dtype=int)

    for i in range(start, end):
        path = [find3d(_, str(i), array[_]) for _ in np.nonzero(np.array(score == i - 1))[0]]
        found_path = np.array(list(map(lambda x: x.shape[1] // len(str(i)), path)))

        if found_path.sum() == 0:
            break

        score[score == i - 1] += (found_path != 0)
        path = [path[_] for _ in range(len(path)) if path[_].size]
        found_path = found_path[found_path != 0]
        p = np.repeat(1 / (found_path * len(str(i))) ** 2, found_path * len(str(i)))
        np.add.at(parameter_score, tuple(np.hstack(path)), p)

    return parameter_score, score


def score_3d2(array, min_score, parameter_score):
    score = np.full(len(array), min_score, dtype=int)

    for i in range(min_score + 1, 10000):
        path = [find3d(_, str(i), array[_]) for _ in np.nonzero(np.array(score == i - 1))[0]]
        found_path = np.array(list(map(lambda x: x.shape[1] // len(str(i)), path)))

        if found_path.sum() == 0:
            break

        score[score == i - 1] += (found_path != 0)
        path = [path[_] for _ in range(len(path)) if path[_].size]
        found_path = found_path[found_path != 0]
        p = np.repeat(1 / (found_path * len(str(i))) ** 2, found_path * len(str(i)))
        np.add.at(parameter_score, tuple(np.hstack(path)), p)

    return parameter_score, score


def shuffle(array):
    for i in range(len(array)):
        seed = np.random.choice(np.arange(10), size=10, replace=False)
        temp_array = np.zeros(SHAPE)
        for j in range(10):
            temp_array[array[i] == j] = seed[j]
        array[i] = temp_array
    return array


def shuffle2(array):
    for i in range(len(array)):
        seed, temp = np.arange(10), np.random.choice(np.arange(10), size=2, replace=False)
        temp.sort()
        seed[temp[0]:temp[1] + 1] = np.random.choice(np.arange(temp[0], temp[1] + 1), size=temp[1] - temp[0] + 1, replace=False)
        temp_array = np.zeros(SHAPE)
        for j in range(10):
            temp_array[array[i] == j] = seed[j]
        array[i] = temp_array
    return array


def main():
    parameters = np.zeros((ENTITY, 8, 14))
    parameters[:] = np.loadtxt('./bestmodel.txt', dtype=int)
    parameters[1:] = shuffle2(parameters[1:])

    parameter_score, score = score_3d(parameters)
    best_score = score[0]
    stopped = np.zeros_like(score)

    for i in range(50000):
        weights = np.cumsum(parameter_score.reshape(-1, 8 * 14), axis=1).tolist()
        checksum = np.full(ENTITY, True)

        for j in range(SEARCH_DEPTH):
            change_idx = np.array(
                [random.choices(range(8 * 14), cum_weights=weights[_], k=1) for _ in np.nonzero(checksum)[0]])
            change_idx = change_idx.reshape(-1) // 14, change_idx.reshape(-1) % 14
            new_parameter = parameters[checksum].copy()
            new_parameter[np.arange(checksum.sum()), *change_idx] = np.random.randint(1, 10, checksum.sum())
            new_score = score_3d(new_parameter)[1]

            update_drop = np.full(ENTITY, False)
            update_drop[checksum] = new_score > score[checksum]
            parameters[update_drop] = new_parameter[update_drop[checksum]]
            score[update_drop] = new_score[update_drop[checksum]]
            checksum *= ~update_drop

            if ~checksum.any():
                break

        stopped += checksum
        stopped[~checksum] = 0

        for j in range(SEARCH_COUNT):
            change_idx = np.array(
                [random.choices(range(8 * 14), cum_weights=weights[_], k=1) for _ in np.nonzero(checksum)[0]])
            change_idx = change_idx.reshape(-1) // 14, change_idx.reshape(-1) % 14
            new_parameter = parameters[checksum].copy()
            new_parameter[np.arange(checksum.sum()), *change_idx] = np.random.randint(1, 10, checksum.sum())
            new_score = score_3d(new_parameter)[1]

            update_drop = np.full(ENTITY, False)
            update_drop[checksum] = new_score >= score[checksum]
            parameters[update_drop] = new_parameter[update_drop[checksum]]
            score[update_drop] = new_score[update_drop[checksum]]
            checksum *= ~update_drop

            if ~checksum.any():
                break

        parameters[stopped >= 40] = shuffle2(parameters[stopped >= 40])
        stopped[stopped >= 40] = 0

        if i % 201 == 200:
            parameters[0] = parameters[np.where(score == score.max())]
            parameters[1:] = shuffle2(parameters[1:])
        parameter_score, score = score_3d(parameters)

        if i % 10 == 0:
            np.save('./parameters.npy', parameters)

        if score.max() > best_score:
            best_score = score.max()
            np.savetxt('./bestmodel.txt', parameters[np.where(score == best_score)[0][0]].reshape(8, 14), fmt='%d')
        print(score)
        print(stopped)


def main():
    parameters = np.zeros((ENTITY, *SHAPE))
    parameters[:] = np.loadtxt('./bestmodel.txt', dtype=int)
    parameters[1:] = shuffle(parameters[1:], 3, 5)

    parameter_score, score, path = score_3d(parameters)
    best_score = score[0]
    stopped = np.zeros(ENTITY)
    temp = None

    for epoch in range(50000):
        parameter_score, score, path = score_3d(parameters)
        is_visited_depth = np.zeros((ENTITY, *SHAPE, 10), dtype=bool)
        is_visited_count = np.zeros((ENTITY, *SHAPE, 10), dtype=bool)
        is_passed = np.zeros(ENTITY, dtype=bool)

        if temp is not None:
            is_visited_depth[~temp[2]] = temp[0][~temp[2]]
            is_visited_count[~temp[2]] = temp[1][~temp[2]]
            temp = None

        for _ in range(SEARCH_DEPTH + SEARCH_COUNT):
            if _ == SEARCH_DEPTH:
                stopped += ~is_passed
            if is_passed.all():
                break

            new_parameter = parameters[~is_passed]
            change_idx = np.zeros((2, (~is_passed).sum()), dtype=int)
            change_val = np.zeros((~is_passed).sum(), dtype=int)

            # 변경할 인덱스 선택
            for sub_n, n in enumerate(np.where(~is_passed)[0]):
                while True:
                    idx = choice_idx(parameter_score[n])
                    val = np.random.randint(1, 10)
                    if _ < SEARCH_DEPTH:
                        if ~is_visited_depth[n, idx[0], idx[1], val]:
                            change_idx[:, sub_n] = np.array([idx[0], idx[1]])
                            change_val[sub_n] = val
                            is_visited_depth[n, idx[0], idx[1], val] = True
                            break
                    else:
                        if ~is_visited_count[n, idx[0], idx[1], val]:
                            change_idx[:, sub_n] = np.array([idx[0], idx[1]])
                            change_val[sub_n] = val
                            is_visited_count[n, idx[0], idx[1], val] = True
                            break

            new_parameter[np.arange((~is_passed).sum()), *change_idx] = change_val
            new_parameter_score, new_score, new_path = score_3d(new_parameter, start=score)
            succeed = new_score > score[~is_passed] if _ < SEARCH_DEPTH else new_score >= score[~is_passed]
            parameters[np.where(~is_passed)[0][succeed]] = new_parameter[succeed]
            score[np.where(~is_passed)[0][succeed]] = new_score[succeed]
            is_passed[~is_passed] += succeed

            print(f'{epoch}: {_:3d}\n{score}\n{is_passed}')

        temp = (is_visited_depth, is_visited_count, is_passed) if (~is_passed).any() else None
        parameters[stopped >= 20] = random_change(parameters[stopped >= 20])
        stopped[stopped >= 20] = 0

        if epoch % 200 == 0:
            score_rank = np.argsort(score)[[0, 1, 2]]
            parameters[score_rank] = shuffle(parameters[score_rank])
            parameter_score, score, path = score_3d(parameters)

        if score.max() > best_score:
            best_score = score.max()
            np.savetxt('./bestmodel.txt', parameters[np.where(score == best_score)[0][0]].reshape(8, 14), fmt='%d')


main()
