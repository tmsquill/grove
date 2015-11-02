__author__ = 'Troy Squillaci'

import logging

import config
import crossover
import ga
import mutation
import selection
import random


def generate_ga_proxies(population_size=0):

    selection_funcs = [getattr(selection, func) for func in config.global_config['ga']['proxies']['selection']]
    crossover_funcs = [getattr(crossover, func) for func in config.global_config['ga']['proxies']['crossover']]
    mutation_funcs = [getattr(mutation, func) for func in config.global_config['ga']['proxies']['mutation']]

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


class StandardProxy:

    def __init__(self, fitness=None, selection=None, crossover=None, mutate=None):

        self.fitness = fitness
        self.selection = selection
        self.crossover = crossover
        self.mutate = mutate


class ReflectionProxy:

    def __init__(self):

        self.proxies = generate_ga_proxies(config.global_config['ga']['proxies']['population'])

        logging.info(' Proxy Initialization '.center(180, '='))

        for proxy in self.proxies:

            logging.info(proxy.__name__)
            logging.info(dir(proxy))