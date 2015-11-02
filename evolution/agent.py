__author__ = 'Troy Squillaci'

import abc
import itertools
import numpy as np
import random
import xmltodict

import config


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

        foragers.append(forager)

        for idx, param in enumerate(obstacle.params):

            param = obstacle.params_upper_bounds[idx] * np.random.normal(loc=mean, scale=0.05)

            if param < obstacle.params_lower_bounds[idx]:
                param = obstacle.params_lower_bounds[idx]
            elif param > obstacle.params_upper_bounds[idx]:
                param = obstacle.params_upper_bounds[idx]

            obstacle.params[idx] = param

        obstacles.append(obstacle)

    return [foragers, obstacles]


class Agent(object):

    __metaclass__ = abc.ABCMeta

    aid = itertools.count().next

    def __init__(self):

        self.id = Agent.aid()
        self.fitness = -1
        self.params_lower_bounds = config.global_config['agent'][self.__class__.__name__]['params_lower_bounds']
        self.params_upper_bounds = config.global_config['agent'][self.__class__.__name__]['params_upper_bounds']
        self.params = [random.uniform(lower, upper) for lower, upper in zip(self.params_lower_bounds, self.params_upper_bounds)]
        self.params_len = len(self.params)
        self.params_mutational_probability = config.global_config['agent'][self.__class__.__name__]['params_mutational_probability']

    def __lt__(self, other):

        return self.fitness < other.fitness

    def __gt__(self, other):

        return self.fitness > other.fitness

    def __str__(self):

        result = ''
        result += self.__class__.__name__ + ' ID: ' + "{:4}".format(self.id)
        result += ' Fitness: ' + "{:8f}".format(self.fitness) + ' '
        result += ' '.join([str(idx) + ': ' + "{:4f}".format(param) for idx, param in enumerate(self.params)])

        return result

    @abc.abstractmethod
    def factory(self):
        """Factory method to instantiate a new Agent object."""

    @abc.abstractmethod
    def execute_fitness(self, argos_xml):
        """Executes appropriate code needed to evaluate the fitness of the agent."""


class ForagerAgent(Agent):

    def __init__(self):

        super(ForagerAgent, self).__init__()

    @staticmethod
    def factory():

        return ForagerAgent()

    def execute_fitness(self, argos_xml):

        forager_config = None

        with open(argos_xml, 'r') as xml:

            forager_config = xmltodict.parse(xml)

        # General
        forager_config['argos-configuration']['framework']['experiment']['@random_seed'] = str(random.randint(1, 1000000))

        # iAnt Robots
        forager_config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfSwitchingToSearching'] = str(round(self.params[0], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfReturningToNest'] = str(round(self.params[1], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@UninformedSearchVariation'] = str(round(self.params[2], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfInformedSearchDecay'] = str(round(self.params[3], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfSiteFidelity'] = str(round(self.params[4], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfLayingPheromone'] = str(round(self.params[5], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfPheromoneDecay'] = str(round(self.params[6], 5))

        with open(argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(forager_config, pretty=True))
            xml.truncate()


class ObstacleAgent(Agent):

    def __init__(self):

        super(ObstacleAgent, self).__init__()

        for i in xrange(self.params_len):

            param = random.uniform(-self.params_upper_bounds[i], self.params_upper_bounds[i])

            while abs(param) < self.params_lower_bounds[i]:

                param = random.uniform(-self.params_upper_bounds[i], self.params_upper_bounds[i])

            self.params[i] = param

    @staticmethod
    def factory():

        return ObstacleAgent()

    def execute_fitness(self, argos_xml):

        with open(argos_xml, 'r') as xml:

            obstacle_config = xmltodict.parse(xml)

        # Obstacles
        obstacle_config['argos-configuration']['arena']['box'][0]['body']['@orientation'] = \
            str(round(self.params[0], 3)) + ',0,0'
        obstacle_config['argos-configuration']['arena']['box'][0]['body']['@position'] = \
            str(round(self.params[1], 3)) + ',' + str(round(self.params[2], 3)) + ',0'

        obstacle_config['argos-configuration']['arena']['box'][1]['body']['@orientation'] = \
            str(round(self.params[3], 3)) + ',0,0'
        obstacle_config['argos-configuration']['arena']['box'][1]['body']['@position'] = \
            str(round(self.params[4], 3)) + ',' + str(round(self.params[5], 3)) + ',0'

        obstacle_config['argos-configuration']['arena']['box'][2]['body']['@orientation'] = \
            str(round(self.params[6], 3)) + ',0,0'
        obstacle_config['argos-configuration']['arena']['box'][2]['body']['@position'] = \
            str(round(self.params[7], 3)) + ',' + str(round(self.params[8], 3)) + ',0'

        obstacle_config['argos-configuration']['arena']['box'][3]['body']['@orientation'] = \
            str(round(self.params[9], 3)) + ',0,0'
        obstacle_config['argos-configuration']['arena']['box'][3]['body']['@position'] = \
            str(round(self.params[10], 3)) + ',' + str(round(self.params[11], 3)) + ',0'

        with open(argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(obstacle_config, pretty=True))
            xml.truncate()
