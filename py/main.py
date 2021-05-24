from simulator import Simulator
import json
import numpy as np
from stats import save_state_if_best, add_stat

COUNTRIES = ['Canada', 'Argentina', 'Luxemburgo',
             'Oman', 'Qatar', 'Uruguay', 'Zimbabwe']


# TODO: change to inline argument
COUNTRY = COUNTRIES[4]  # Qatar

data = json.load(open(f'data/{COUNTRY}.json', 'r'))

# default parameters
params = {
    'num_ants': 25,
    'dst_power': 4,
    'phero_power': 1,
    'init_phero': 1,
    'phero_intensity': 10,
    'phero_resilience': 0.7,
    'max_phero': 200
}

test_param = 'phero_resilience'
repeat = 5

# Simulation
for val in np.linspace(0.5, 0.95, 10):
    params[test_param] = val
    for _ in range(repeat):
        s = Simulator(data, params)
        s.run_k_gens(30, updates=100, verbose=False)
        print(f'{test_param}: {val}, best: {s.best_eval}')

        state = s.save()
        save_state_if_best(
            state, f'states/{s.country}_{round(s.best_eval, 2)}.json')
        add_stat(state)
