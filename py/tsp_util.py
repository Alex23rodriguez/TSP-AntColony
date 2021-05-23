from py.util import normalizedArray
from itertools import permutations


def get_desirability_of_dist(dst, dstPower):
    return 1/dst ** (-dstPower)


def get_desirability_from_city(data, city_index, visited=[]):
    desirability = [0 if i in visited else get_desirability_of_dist(
        data['distances'][i][city_index], data['dstPower']) for i in range(len(data['cities']))]
    return normalizedArray(desirability)


def eval_path(data, path):
    dsts = data['distances']
    s = dsts[path[0]][path[-1]]
    s += sum(dsts[a][b] for a, b in zip(path, path[1:]))
    return s


def find_best_path(data):
    best_path = []
    best = float('inf')
    for p in permutations(range(1, len(data['cities']))):
        val = eval_path([0] + p)
        if val < best:
            best = val
            best_path = [0] + p

    return best_path
