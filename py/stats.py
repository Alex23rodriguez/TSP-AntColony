import json


def add_stat(sim_state):
    stats = json.load(open('stats.json', 'r'))
    country = sim_state['country']
    if country not in stats:
        stats[country] = {}
    h = hash(str(sim_state['params']))
    if h not in stats[country]:
        stats[country][h] = {
            'params': sim_state['params'],
            'results': []
        }
    stats[country][h]['results'].append({
        'avg': sim_state['avg'],
        'all_best': sim_state['all_best'],
        'best_eval': sim_state['best_eval'],
        'best_path': sim_state['best_path'],
        'gens': sim_state['gen']
    })
    json.dump(stats, open('stats.json', 'w'))
    del stats


def save_state_if_best(sim_state, filename):
    stats = json.load(open('stats.json', 'r'))
    for d in stats[sim_state['country']].values():
        evals = [x['best_eval'] for x in d['results']]
        if sim_state.best_eval <= min(evals):
            json.dump(sim_state, open(filename, 'w'))
