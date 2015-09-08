__author__ = 'Troy Squillaci'

from abc import ABCMeta, abstractmethod

import itertools


class AgentDescriptor(object):

    __metaclass__ = ABCMeta

    def __init__(self):

        self.agents = 10
        self.params_len = 12
        self.params_lower_bounds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0]
        self.params_upper_bounds = [20.0, 1.0, 1.0, 20.0, 1.0, 5.0, 5.0, 0.75, 1.0, 180.0, 100.0, 360.0]


class Agent(object):

    __metaclass__ = ABCMeta

    aid = itertools.count().next

    def __init__(self):

        self.id = Agent.aid()
        self.fitness = -1
        self.params = []

    def __lt__(self, other):

        return self.fitness < other.fitness

    def __gt__(self, other):

        return self.fitness > other.fitness

    def __str__(self):

        result = ''

        result += 'Fitness: ' + str(self.fitness)

        for idx, param in enumerate(self.params):

            result += ' ' + str(idx) + ': ' + str(param)

        return result

    @abstractmethod
    def run(self):
        pass
