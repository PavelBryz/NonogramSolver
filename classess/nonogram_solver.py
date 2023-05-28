from typing import Union

import numpy as np
from numpy import ndarray


def get_all_possible_combinations_for_line(figs: list[int], line: np.ndarray, n: int, trys: list):
    tmp_line = line.copy()
    if not figs:
        trys.append(tmp_line)
        return

    fig = figs.pop(0)
    for i in range(len(line) - fig - n - sum(figs) - len(figs) + 1):
        tmp_line[n:] = 0
        tmp_line[n + i:n + i + fig] += 1
        n = n + i + fig + 1
        get_all_possible_combinations_for_line(figs, tmp_line, n, trys)
        n = n - i - fig - 1

    figs.insert(0, fig)


def solver(vert: list[list[int]], hor: list[list[int]], board: Union[list[list[bool]], None]) -> ndarray:
    if board:
        solution = np.array(board)
    else:
        solution = np.zeros((len(hor), len(vert)))

    tr_v = []
    tr_h = [] * len(hor)

    for i in range(len(vert)):
        tr_v.append([])
        get_all_possible_combinations_for_line(vert[i], solution[:, i], 0, tr_v[i])

    for i in range(len(hor)):
        tr_h.append([])
        get_all_possible_combinations_for_line(hor[i], solution[i], 0, tr_h[i])

    while any([len(el) != 1 for el in tr_v]) and any([len(el) != 1 for el in tr_h]):

        for i in range(len(vert)):
            tr_v[i] = [el for el in tr_v[i] if
                       np.array_equal(np.logical_and(solution[:, i] == 1, el == 1), solution[:, i] == 1) and \
                       np.array_equal(np.logical_and(solution[:, i] == -1, el == 0), solution[:, i] == -1)]

        prob_v = np.zeros(solution.shape, dtype='f')
        for i in range(len(vert)):
            for t in tr_v[i]:
                prob_v[:, i] += t
            prob_v[:, i] = prob_v[:, i] / len(tr_v[i])

        solution[prob_v == 1] = 1
        solution[prob_v == 0] = -1

        for i in range(len(hor)):
            tr_h[i] = [el for el in tr_h[i] if
                       np.array_equal(np.logical_and(solution[i] == 1, el == 1), solution[i] == 1) and \
                       np.array_equal(np.logical_and(solution[i] == -1, el == 0), solution[i] == -1)]

        prob_h = np.zeros(solution.shape, dtype='f')
        for i in range(len(vert)):
            for t in tr_h[i]:
                prob_h[i] += t
            prob_h[i] = prob_h[i] / len(tr_h[i])

        solution[prob_h == 1] = 1
        solution[prob_h == 0] = -1
        # print(f"{'Prob V':-^30}")
        # print(prob_v)
        # print(f"{'Prob H':-^30}")
        # print(prob_h)

        print(f"{'Solution':-^30}")
        print(solution)

    return solution


if __name__ == '__main__':
    # vt = [[3], [2, 5], [5], [3, 3], [2, 2], [4, 5], [4, 4], [3, 2], [2, 1, 3], [2, 2, 6], [6, 3], [5, 2], [2, 2, 4],
    #       [7], [4]]
    # hr = [[2], [1, 6], [2, 8], [1, 3, 3], [2, 3, 3], [3, 5], [3, 4], [2, 1, 2], [3, 3, 2], [8, 2], [4, 1, 3], [2, 2, 3],
    #       [5], [3, 1], [2]]

    vt = [[2], [2,1], [2,1], [2,1], [2]]
    hr = [[1],[3],[2,2],[1,1],[3]]

    sol = solver(vt, hr, None)

    print(f"{'Solution':-^30}")
    sol[sol == 1] = 88
    print(sol)
