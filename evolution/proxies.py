__author__ = 'Troy Squillaci'

import crossover
import ga
import mutation
import selection
import random


def generate_ga_proxies(population_size=0):

    selection_funcs = [getattr(selection, func) for func in ga.config['proxies']['selection']]
    crossover_funcs = [getattr(crossover, func) for func in ga.config['proxies']['crossover']]
    mutation_funcs = [getattr(mutation, func) for func in ga.config['proxies']['mutation']]

    proxies = []

    for sentinel in xrange(population_size):

        selection_func = random.choice(selection_funcs)
        crossover_func = random.choice(crossover_funcs)
        mutation_func = random.choice(mutation_funcs)

        proxies.append(type(selection_func.__name__ + crossover_func.__name__ + mutation_func.__name__, (object,), {
            'selection': selection_func,
            'crossover': crossover_func,
            'mutation': mutation_func
        }))

    return proxies
