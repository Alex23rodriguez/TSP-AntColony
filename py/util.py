from random import random


def distSq(p1, p2):
    dx = p1['x'] - p2['x']
    dy = p1['y'] - p2['y']
    return dx*dx + dy*dy


def getDist(p1, p2):
    dx = p1['x'] - p2['x']
    dy = p1['y'] - p2['y']
    return (dx*dx + dy*dy)**0.5


def normalizedArray(arr):
    s = sum(arr)
    return [x/s for x in arr]


def pick(desirability):
    r = random()
    s = 0
    for i, d in enumerate(desirability):
        s += d
        if r < s:
            return i


def all_dists(cities):
    ans = [[0 for _ in range(len(cities))] for _ in range(len(cities))]
    for i in range(len(cities)):
        for j in range(len(cities)):
            ans[i][j] = ans[j][i] = getDist(cities[i], cities[j])
    return ans
