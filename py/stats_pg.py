# %%
import json
import operator as op
from matplotlib import pyplot as plt
# %%
op_dict = {
    '==': op.eq,
    '<=': op.le,
    '>=': op.ge,
    '<': op.lt,
    '>': op.gt
}
# %%


def load_stats(raw_stats):
    stats = raw_stats['stats']
    stat_vals = [v for k, v in raw_stats.items() if k != 'stats']
    return stats, stat_vals


def index_all_stats(stat_vals):
    index = {}
    for dct in stat_vals:
        for p, val in dct['params'].items():
            if p not in index:
                index[p] = {}
            if val not in index[p]:
                index[p][val] = []
            index[p][val].append(dct)
    return index


def aggregate(stat_vals, key, operator, val):
    assert operator in op_dict, 'invalid operator'
    return [s for s in stat_vals if op_dict[operator](s['params'][key], val)]


def flatten(agg):
    # inverts dict structure. instead of a['results'] being a list,
    # flat['results'] is a dict with keys 'all_best' and 'avg'
    flat = {
        'all_best': [],
        'avg': []
    }
    for a in agg:
        flat['all_best'] += [x['all_best'] for x in a['results']]
        flat['avg'] += [x['avg'] for x in a['results']]
    return flat


def summarize_param(index, param):
    xy1 = []
    xy2 = []
    for val, sims in index[param].items():
        print(f"value: {val}")
        print(f"total: {len(sims)}")
        flat = flatten(sims)
        best_intg = avg_integral(flat["all_best"])
        avg_intg = avg_integral(flat["avg"])
        print(f'avg integral of best: {best_intg}')
        print(f'avg integral of avg: {avg_intg}')
        print('\n')
        xy1.append([val, best_intg])
        xy2.append([val, avg_intg])

    print(list(zip(sorted(xy1))))
    plt.plot(*zip(*sorted(xy1)))
    plt.plot(*zip(*sorted(xy2)))


def avg_integral(lists):
    return sum([sum(l) for l in lists]) / len(lists)


def plot_many(lists):
    for v in lists:
        plt.plot(*zip(*enumerate(v)))
    plt.ylim(10000, 12000)


def plot_one(lists):
    n = len(lists)
    l = []

    l = [sum([l[i] for l in lists])/n
         for i in range(len(lists[0]))]
    plt.plot(*zip(*enumerate(l)))
    plt.ylim(11000, 12000)


def draw_path(cities, path, nums=False):
    x, y = zip(*(cities[i] for i in path))
    x = list(x) + [x[0]]
    y = list(y) + [y[0]]
    fig, ax = plt.subplots()
    ax.plot(x, y, 'b-')

    if nums:
        for X, Y, Z in zip(x, y, path):
            # Annotate the points 5 _points_ above and to the left of the vertex
            ax.annotate('{}'.format(Z), xy=(X, Y), xytext=(-5, 5), ha='right',
                        textcoords='offset points')
    plt.show()


# %%
cities = json.load(open('data/Qatar.json'))['cities']
stats, stat_vals = load_stats(json.load(open('stats.json', 'r'))['Qatar'])
# %%
len(stat_vals)
# %%

# %%
# agg = aggregate(stat_vals, 'num_ants', '>=', 30)
agg = aggregate(stat_vals, 'dst_power', '>=', 4)
agg = aggregate(agg, 'dst_power', '>=', 6)
flat = flatten(agg)
# %%
plot_one(flat['all_best'])
# %%
plot_many(flat['all_best'])

# %%
len(agg)
# %%
# %%
len(flat['all_best'])
# %%
# %%
plot_many(flat['avg'])

# %%
[len(l) for l in flat['all_best']]
# %%
draw_path(cities, stats['best_path'])
# %%
stats['best_params']
# %%
index = index_all_stats(stat_vals)
# %%
index.keys()
# %%
len(index['num_ants'][20])
# %%
summarize_param(index, 'phero_supply')
# %%

{
    'num_ants': [20, 25, 30],
    # 'dst_power': list(np.linspace(2, 6, 11)),
    'dst_power': [4.5, 5, 6, 7, 8],
    # 'phero_power': [0.8, 1, 1.5, 2],
    'phero_power': [1.3, 1.5, 1.7],
    'init_phero': [5, 10, 15, 20],
    'phero_resilience': [0.65, 0.7, 0.75, 0.8],
    'vote_power': [0.6, 0.7, 0.8, 1, 2, 2.5],
    'phero_supply': [0.3, 0.4, 0.5, 0.7, 1]

}
