import json


def name_from_params(params):
    lst = sorted(list(params.keys()))
    return ':'.join([f'{k}{round(params[k], 2)}' for k in lst])


def add_stat(sim_state):
    stats = json.load(open('stats.json', 'r'))
    country = sim_state['country']
    if country not in stats:
        stats[country] = {}
    h = name_from_params(sim_state['params'])

    if h not in stats[country]:
        print('new hash')
        stats[country][h] = {
            'params': sim_state['params'],
            'results': []
        }
    else:
        print('old hash')
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
    all_time_best = float('inf')
    for d in stats[sim_state['country']].values():
        evals = [x['best_eval'] for x in d['results']]
        all_time_best = min(min(evals), all_time_best)
    if sim_state['best_eval'] < all_time_best:
        print('saving state...')
        json.dump(sim_state, open(filename, 'w'))


def best_with_params(stats, country, params):
    best = {}
    for d in stats[country][hash(str(params))]:
        pass


def stats_summary(coutry):
    stats = json.load(open('stats.json', 'r'))
    ans = []
    for d in stats[coutry].values():
        evals = [x['best_eval'] for x in d['results']]
        ans.append({
            'params': d['params'],
            'len': len(d['results']),
            'best': min(evals),
            'avg_of_best': sum(evals)/len(evals)
        })
    del stats
    return ans
