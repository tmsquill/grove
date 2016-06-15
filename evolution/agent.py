import abc
import config
import itertools


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

        self.genotype_len = config.grove_config['agent'][self.__class__.__name__]['genotype_len']

        lb = config.grove_config['agent'][self.__class__.__name__]['genotype_lb']

        if isinstance(lb, float) or isinstance(lb, int):

            self.genotype_lb = [lb] * self.genotype_len

        else:

            self.genotype_lb = lb

        ub = config.grove_config['agent'][self.__class__.__name__]['genotype_ub']

        if isinstance(ub, float) or isinstance(ub, int):

            self.genotype_ub = [ub] * self.genotype_len

        else:

            self.genotype_ub = ub

        mp = config.grove_config['agent'][self.__class__.__name__]['genotype_mp']

        if isinstance(mp, float):

            self.genotype_mp = [mp] * 200

        else:

            self.genotype_mp = mp

        self.genotype = []
        self.payload = None

    def __str__(self):

        result = ''
        result += self.__class__.__name__ + ' ID: ' + "{:4}".format(self.id)
        result += ' Evaluation Value: ' + "{:8f}".format(self.value) + ' '
        result += '| ' + ' | '.join('{0}: {1:>8.3f}'.format(idx, param) for idx, param in enumerate(self.genotype))

        return result

    @abc.abstractmethod
    def init_agents(self, population):

        """
        Initializes a set of agents based on the population size.
        :return: Returns a set of newly created agents.
        """