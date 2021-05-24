from simulator import Simulator
import json
import numpy as np

COUNTRIES = ['Canada', 'Argentina', 'Luxemburgo',
             'Oman', 'Qatar', 'Uruguay', 'Zimbabwe']


# TODO: change to inline argument
COUNTRY = COUNTRIES[4]  # Qatar

data = json.load(open(f'data/{COUNTRY}.json', 'r'))

# default parameters
params = {
    'num_ants': 20,
    'dst_power': 4,
    'phero_power': 1,
    'init_phero': 1,
    'phero_intensity': 10,
    'phero_resilience': 0.7,
    'max_phero': 200
}

test_param = 'dst_power'
repeat = 5

# Simulation
for val in np.linspace(3, 6, 10):
    params['dst_power'] = val
    for _ in range(repeat):
        s = Simulator(data, params)
        s.run_k_gens(30, verbose=False)
        print(f'dst_power: {val}, best: {s.best_eval}')

        s.save(f'states/{s.country}_{round(s.best_eval, 2)}.json')
