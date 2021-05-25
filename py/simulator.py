# from tsp_util import eval_path
from util import normalizedArray, pick
from random import randint
from matplotlib import pyplot
import json
from copy import deepcopy
from time import time

'''
params example:
{
    'num_ants': 10,
    'dst_power': 2,
    'phero_power': 1,
    'init_phero': 1,
    'phero_intensity': 10,
    'phero_resilience': 0.7,
    'max_phero': 50
}
'''


class Simulator:
    def __init__(self, data, params):
        self.country = data['country']
        self.cities = data['cities']
        self.dists = data['distances']
        self.n = data['n']
        self.set_params(params)
        self.reset()
        self.update_pow_dists()

        # self.best_state = {}

    def run_k_gens(self, k, updates=10, verbose=True):
        start_time = time()
        for _ in range(k):
            if(self.gen % updates == 0):
                print(f'gen {self.gen}')

            trails = [self.simulate_ant()
                      for _ in range(self.params['num_ants'])]

            # update pheromone trails
            self.update_trails(trails)
            # update best and avg
            gen_evals = [self.eval_path(t) for t in trails]
            gen_best = min(gen_evals)
            self.all_best.append(gen_best)
            self.avg.append(sum(gen_evals)/len(gen_evals))
            # update global best
            if gen_best < self.best_eval:
                self.best_eval = gen_best
                self.best_path = trails[gen_evals.index(gen_best)]
                if verbose:
                    print(f'new best! gen{self.gen}, val: {self.best_eval}')
                # self.best_state = self.save()
            # keep best path pheromones high
            self.add_phero(self.best_path)

            self.gen += 1
        rt = time() - start_time
        self.run_time += rt
        if verbose:
            print(f'Run time: {round(rt, 2)}')
            if self.run_time != rt:
                print(f'Total run time: {round(self.run_time, 2)}')

    def update_trails(self, new_trails):
        # add new trails
        for tr in new_trails:
            self.add_phero(tr)

        # evaporate previous trails
        self.phero_trails = [
            [x*self.params['phero_resilience'] for x in tr] for tr in self.phero_trails
        ]

        # cap at max_phero
        self.phero_trails = [
            [min(x, self.params['max_phero']) for x in tr]
            for tr in self.phero_trails
        ]

    def add_phero(self, trail):
        for i, j in zip(trail, trail[1:] + [trail[0]]):
            self.phero_trails[i][j] += self.params['phero_intensity']
            self.phero_trails[j][i] += self.params['phero_intensity']

    def simulate_ant(self):
        city = randint(0, self.n-1)
        path = [city]
        visited = set([city])

        for _ in range(self.n-1):

            desir = [
                # desirability based on distance
                (self.pow_dists[city][i] if i not in visited else 0)
                # desirability based on pheromones
                * (self.phero_trails[city][i] ** self.params['phero_power'])
                # for each city
                for i in range(self.n)
            ]

            city = pick(normalizedArray(desir))
            path.append(city)
            visited.add(city)
        return path

    def eval_path(self, path, closed=True):
        s = self.dists[path[0]][path[-1]] if closed else 0
        s += sum(self.dists[a][b] for a, b in zip(path, path[1:]))
        return s

    def set_params(self, params, update_pow_dists=True):
        self.params = params
        if update_pow_dists:
            self.update_pow_dists()

    def summary(self):
        print('params:')
        print(self.params)
        print('\nvalue of best path found:')
        print(self.best_eval)
        pyplot.plot(*zip(*enumerate(self.all_best)))
        pyplot.plot(*zip(*enumerate(self.avg)))
        pyplot.legend(('best', 'average'),
                      loc='upper right')
        # pyplot.ylim(0, None)
        self.draw_path()

    def draw_path(self, path=None, nums=False):
        if path is None:
            path = self.best_path
        x, y = zip(*(self.cities[i] for i in path))
        x = list(x) + [x[0]]
        y = list(y) + [y[0]]
        fig, ax = pyplot.subplots()
        ax.plot(x, y, 'b-')

        if nums:
            for X, Y, Z in zip(x, y, path):
                # Annotate the points 5 _points_ above and to the left of the vertex
                ax.annotate('{}'.format(Z), xy=(X, Y), xytext=(-5, 5), ha='right',
                            textcoords='offset points')
        pyplot.show()

    def reset(self):
        self.gen = 0
        self.run_time = 0
        self.phero_trails = [[self.params['init_phero']
                              for _ in range(self.n)] for _ in range(self.n)]
        self.all_best = []
        self.avg = []
        self.best_eval = float('inf')
        self.best_path = list(range(self.n))

    def load(self, sim_state):
        assert sim_state['country'] == self.country, "Countries must match to load state"
        self.phero_trails = sim_state['phero_trails']
        self.all_best = sim_state['all_best']
        self.avg = sim_state['avg']
        self.best_eval = sim_state['best_eval']
        self.best_path = sim_state['best_path']
        self.gen = sim_state['gen']
        self.set_params(sim_state['params'])

    def save(self, filename=None):
        state = {
            'phero_trails': deepcopy(self.phero_trails),
            'all_best': self.all_best.copy(),
            'avg': self.avg.copy(),
            'best_eval': self.best_eval,
            'best_path': self.best_path.copy(),
            'gen': self.gen,
            'params': deepcopy(self.params),
            'country': self.country
        }

        if filename is None:
            return state

        json.dump(state, open(filename, 'w'))

    def restore_pheromones(self):
        self.phero_trails = [[self.params['init_phero']
                              for _ in range(self.n)] for _ in range(self.n)]

        self.add_phero(self.best_path)

    def update_pow_dists(self):
        self.pow_dists = [[d**-self.params['dst_power'] if d != 0 else 0
                           for d in row] for row in self.dists]
