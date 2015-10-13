__author__ = 'Troy Squillaci'

import abc
import itertools
import json
import numpy as np
import random
import xmltodict


config = None


def init_agents(population):

    foragers = []
    obstacles = []

    for i in xrange(population):

        forager = ForagerAgent.factory()
        obstacle = ObstacleAgent.factory()
        mean = float(i) / population

        for idx, param in enumerate(forager.params):

            param = forager.params_upper_bounds[idx] * np.random.normal(loc=mean, scale=0.05)

            if param < forager.params_lower_bounds[idx]:
                param = forager.params_lower_bounds[idx]
            elif param > forager.params_upper_bounds[idx]:
                param = forager.params_upper_bounds[idx]

            forager.params[idx] = param

        print 'Forager ' + str(i) + ' ' + str(forager)
        foragers.append(forager)

        for idx, param in enumerate(obstacle.params):

            param = obstacle.params_upper_bounds[idx] * np.random.normal(loc=mean, scale=0.05)

            if param < obstacle.params_lower_bounds[idx]:
                param = obstacle.params_lower_bounds[idx]
            elif param > obstacle.params_upper_bounds[idx]:
                param = obstacle.params_upper_bounds[idx]

            obstacle.params[idx] = param

        print 'Obstacle ' + str(i) + ' ' + str(obstacle)
        obstacles.append(obstacle)

    return [foragers, obstacles]


def pretty_config():

    return json.dumps(config, sort_keys=True, indent=4)


class Agent(object):

    __metaclass__ = abc.ABCMeta

    aid = itertools.count().next

    def __init__(self):

        self.id = Agent.aid()
        self.fitness = -1
        self.params_lower_bounds = config[self.__class__.__name__]['params_lower_bounds']
        self.params_upper_bounds = config[self.__class__.__name__]['params_upper_bounds']
        self.params = [random.uniform(lower, upper) for lower, upper in zip(self.params_lower_bounds, self.params_upper_bounds)]
        self.params_len = len(self.params)

    def __lt__(self, other):

        return self.fitness < other.fitness

    def __gt__(self, other):

        return self.fitness > other.fitness

    def __str__(self):

        result = ''
        result += __name__ + 'ID: ' + str(self.id)
        result += ' Fitness: ' + str(self.fitness) + ' '
        result += ' '.join([str(idx) + ': ' + "{:4f}".format(param) for idx, param in enumerate(self.params)])

        return result

    @abc.abstractmethod
    def factory(self):
        """Factory method to instantiate a new Agent object."""

    @abc.abstractmethod
    def execute(self, argos_xml):
        """Executes appropriate code needed to evaluate the fitness of the agent."""


class ForagerAgent(Agent):

    def __init__(self):

        super(ForagerAgent, self).__init__()

        self.config = []

    @staticmethod
    def factory():

        return ForagerAgent()

    def execute(self, argos_xml):

        with open(argos_xml, 'r') as xml:

            self.config = xmltodict.parse(xml)

        # General
        self.config['argos-configuration']['framework']['experiment']['@random_seed'] = str(random.randint(1, 1000000))

        # iAnt Robots
        self.config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfSwitchingToSearching'] = str(round(self.params[0], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfReturningToNest'] = str(round(self.params[1], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@UninformedSearchVariation'] = str(round(self.params[2], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfInformedSearchDecay'] = str(round(self.params[3], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfSiteFidelity'] = str(round(self.params[4], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfLayingPheromone'] = str(round(self.params[5], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfPheromoneDecay'] = str(round(self.params[6], 5))

        with open(argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(self.config, pretty=True))
            xml.truncate()


class ObstacleAgent(Agent):

    def __init__(self):

        super(ObstacleAgent, self).__init__()

        self.config = []

        for i in xrange(self.params_len):

            param = random.uniform(-self.params_upper_bounds[i], self.params_upper_bounds[i])

            while abs(param) < self.params_lower_bounds[i]:

                param = random.uniform(-self.params_upper_bounds[i], self.params_upper_bounds[i])

            self.params[i] = param

    @staticmethod
    def factory():

        return ForagerAgent()

    def execute(self, argos_xml):

        with open(argos_xml, 'r') as xml:

            self.config = xmltodict.parse(xml)

        # Obstacles
        self.config['argos-configuration']['arena']['box'][0]['body']['@orientation'] = \
            str(round(self.params[0], 3)) + ',0,0'
        self.config['argos-configuration']['arena']['box'][0]['body']['@position'] = \
            str(round(self.params[1], 3)) + ',' + str(round(self.params[2], 3)) + ',0'

        self.config['argos-configuration']['arena']['box'][1]['body']['@orientation'] = \
            str(round(self.params[3], 3)) + ',0,0'
        self.config['argos-configuration']['arena']['box'][1]['body']['@position'] = \
            str(round(self.params[4], 3)) + ',' + str(round(self.params[5], 3)) + ',0'

        self.config['argos-configuration']['arena']['box'][2]['body']['@orientation'] = \
            str(round(self.params[6], 3)) + ',0,0'
        self.config['argos-configuration']['arena']['box'][2]['body']['@position'] = \
            str(round(self.params[7], 3)) + ',' + str(round(self.params[8], 3)) + ',0'

        self.config['argos-configuration']['arena']['box'][3]['body']['@orientation'] = \
            str(round(self.params[9], 3)) + ',0,0'
        self.config['argos-configuration']['arena']['box'][3]['body']['@position'] = \
            str(round(self.params[10], 3)) + ',' + str(round(self.params[11], 3)) + ',0'

        with open(argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(self.config, pretty=True))
            xml.truncate()
