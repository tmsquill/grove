import abc
import itertools

import config


class Agent(object):
    """
    An abstract representation of an agent. All agents have a unique ID, an evaluation value, and information regarding
    their genotype. The factory and init_agents methods are abstract and must be implemented as static methods in the
    concrete class.
    """

    __metaclass__ = abc.ABCMeta

    aid = itertools.count().next

    def __init__(self):

        self.id = Agent.aid()
        self.value = -1

        self.genotype_lb = config.global_config['agent'][self.__class__.__name__]['genotype_lb']
        self.genotype_ub = config.global_config['agent'][self.__class__.__name__]['genotype_ub']
        self.genotype_mp = config.global_config['agent'][self.__class__.__name__]['genotype_mp']
        self.genotype = []

    def __str__(self):

        result = ''
        result += self.__class__.__name__ + ' ID: ' + "{:4}".format(self.id)
        result += ' Evaluation Value: ' + "{:8f}".format(self.value) + ' '
        result += ' '.join([str(idx) + ': ' + "{:4f}".format(param) for idx, param in enumerate(self.genotype)])

        return result

    @abc.abstractmethod
    def factory(self):
        """
        Factory method to instantiate a new Agent object.
        :return: Returns a newly created Agent object.
        """

    @abc.abstractmethod
    def init_agents(self, population):
        """
        Initializes a set of agents based on the population size.
        :return: Returns a set of newly created agents.
        """
