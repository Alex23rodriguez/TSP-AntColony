# %%
from random import random, randint
from util import all_dists
import json

import util
from importlib import reload
reload(util)


# %%
COUNTRIES = ['Canada', 'Argentina', 'Luxemburgo',
             'Oman', 'Qatar', 'Uruguay', 'Zimbabwe']
# %%

# %%


def make_data(cnt):
    jsn = json.load(open(f'json_data/{cnt}.json', 'r'))
    return {
        "country": cnt,
        "cities": jsn,
        "distances": all_dists(jsn),
        "n": len(jsn)
    }


def make_profile(data, num_ants, num_gen, dst_power, pheromone_power):
    return {
        'data': data,
        'num_ants': num_ants,
        'num_gen': num_gen,
        'dst_power': dst_power,
        'pheromone_power': pheromone_power
    }


# %%
ALL_COUNTRIES = dict(
    (cnt, make_data(cnt)) for cnt in COUNTRIES)


# %%
fake = [
    {'x': 0, 'y': 0},
    {'x': 3, 'y': 4},
    {'x': 9, 'y': 12},
]

# %%
data = make_data("Canada")
# %%
p1 = make_profile(data, 3, 10, 2, 2)
# %%


def one_gen(data, num_ants, pheromone_trails):
    ants = [randint(0, len(data['n'])) for _ in range(num_ants)]

    for _ in range(data['n']):

        pass
