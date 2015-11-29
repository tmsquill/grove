import abc
import itertools
import numpy as np
import random

import config


def init_agents(agent_type, population):
    """
    Initializes a population of agents based on the derived type.
    :param agent_type: A class derived from the base class Agent.
    :param population: The number of agents to produce in the population.
    :return: The population of initialized agents.
    """

    if issubclass(agent_type, GEAgent):

        return [agent_type.factory() for _ in xrange(population)]

    if issubclass(agent_type, ARGoSAgent):

        agents = []

        for i in xrange(population):

            agent = agent_type.factory()
            mean = float(i) / population

            for idx, param in enumerate(agent.genotype):

                param = agent.genotype_ub[idx] * np.random.normal(loc=mean, scale=0.05)

                if param < agent.genotype_lb[idx]:
                    param = agent.genotype_lb[idx]
                elif param > agent.genotype_ub[idx]:
                    param = agent.genotype_ub[idx]

                agent.genotype[idx] = param

            agents.append(agent)

        return agents

    raise TypeError("invalid agent type:", agent_type)


class Agent(object):
    """
    An abstract representation of an agent. All agents have a unique ID, a fitness value, and information regarding
    their genotype. The factory and evaluation methods are abstract and must be implemented in a concrete class.
    """

    __metaclass__ = abc.ABCMeta

    aid = itertools.count().next

    def __init__(self):

        self.id = Agent.aid()
        self.fitness = -1
        self.genotype_lb = config.global_config['agent'][self.__class__.__name__]['genotype_lb']
        self.genotype_ub = config.global_config['agent'][self.__class__.__name__]['genotype_ub']
        self.genotype_mutational_probability = config.global_config['agent'][self.__class__.__name__]['genotype_mp']

    def __str__(self):

        result = ''
        result += self.__class__.__name__ + ' ID: ' + "{:4}".format(self.id)
        result += ' Fitness: ' + "{:8f}".format(self.fitness) + ' '
        result += ' '.join([str(idx) + ': ' + "{:4f}".format(param) for idx, param in enumerate(self.genotype)])

        return result

    @abc.abstractmethod
    def factory(self):
        """ Factory method to instantiate a new Agent object. """

    @staticmethod
    def evaluate(fitness_function, *args):

        result = fitness_function(*args)

        return result


class GEAgent(Agent):
    """ An agent suited for Grammatical Evolution. """

    def __init__(self):
        
        super(GEAgent, self).__init__()

        self.genotype_lb = [self.genotype_lb[0]] * 100
        self.genotype_ub = [self.genotype_ub[0]] * 100
        self.genotype = [random.randint(lower, upper) for lower, upper in zip(self.genotype_lb, self.genotype_ub)]
        self.genotype_len = len(self.genotype)

        self.phenotype = None
        self.used_codons = 0

    @staticmethod
    def factory():

        return GEAgent()


class ARGoSAgent(Agent):
    """ A standard agent suited for CPFA optimization. """
    
    def __init__(self):

        super(ARGoSAgent, self).__init__()

        self.genotype = [random.uniform(lower, upper) for lower, upper in zip(self.genotype_lb, self.genotype_ub)]
        self.genotype_len = len(self.genotype)

    @staticmethod
    def factory():

        return ARGoSAgent()
