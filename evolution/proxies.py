__author__ = 'Troy Squillaci'

import abc
import logging

import config
import crossover
import ga
import mutation
import selection
import random


class Proxy(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):

        self.evolution_sequence = []

    def __str__(self):

        result = ''
        result += self.__class__.__name__ + ' ID: ' + "{:4}".format(self.id)
        result += ' Fitness: ' + "{:8f}".format(self.fitness) + ' '
        result += ' '.join([str(idx) + ': ' + "{:4f}".format(param) for idx, param in enumerate(self.params)])

        return result

    @abc.abstractmethod
    def next(self, argos_xml):
        """Executes appropriate code needed to evaluate the fitness of the agent."""


class StandardProxy:

    def __init__(self, fitness=None, selection=None, crossover=None, mutate=None):

        self.evolution_sequence = []

        self.evolution_sequence.append(fitness)

        self.evolution_sequence.append()


class ReflectionProxy:

    def __init__(self):

        self.proxies = generate_ga_proxies(config.global_config['ga']['proxies']['population'])

        logging.info(' Proxy Initialization '.center(180, '='))

        for proxy in self.proxies:

            logging.info(proxy.__name__)
            logging.info(dir(proxy))

