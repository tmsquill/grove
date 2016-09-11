import itertools
import random

from grove import config


class Agent(object):

    """
    A standard representation of an agent. All agents have the following attributes; a unique ID, an evaluation value,
    a genome (along with other genome-specific attributes used by the GA), a list of jobs used for evaluating the agent
    with distributed computation, a random seed that can be used by the evaluation functionm, and a payload that can be
    used to transport arbitrary data to the evaluation function.
    """

    aid = itertools.count().next

    def __init__(self, genome=None):

        self.id = Agent.aid()

        self.genome_len = config.grove_config['agent'][self.__class__.__name__]['genome_len']

        lb = config.grove_config['agent'][self.__class__.__name__]['genome_lb']

        if isinstance(lb, float) or isinstance(lb, int):

            self.genome_lb = [lb] * self.genome_len

        elif isinstance(lb, list):

            self.genome_lb = lb

        else:

            raise ValueError('invalid lower bound defined in grove-config.json')

        ub = config.grove_config['agent'][self.__class__.__name__]['genome_ub']

        if isinstance(ub, float) or isinstance(ub, int):

            self.genome_ub = [ub] * self.genome_len

        elif isinstance(ub, list):

            self.genome_ub = ub

        else:

            raise ValueError('invalid upper bound defined in grove-config.json')

        mp = config.grove_config['agent'][self.__class__.__name__]['genome_mp']

        if isinstance(mp, float):

            self.genome_mp = [mp] * self.genome_len

        elif isinstance(mp, list):

            self.genome_mp = mp

        else:

            raise ValueError('invalid mutational probability defined in grove-config.json')

        self.genome_type = config.grove_config['agent'][self.__class__.__name__]['genome_type']

        if genome:

            self.genome = genome

        else:

            if self.genome_type == 'int':

                self.genome = [random.randint(lower, upper) for lower, upper in zip(self.genome_lb, self.genome_ub)]

            elif self.genome_type == 'float':

                self.genome = [random.uniform(lower, upper) for lower, upper in zip(self.genome_lb, self.genome_ub)]

            else:

                self.genome = []

        self.jobs = None
        self.payload = None
        self.random_seed = None
        self.value = -1

    def __str__(self):

        result = ''
        result += self.__class__.__name__ + ' ID: ' + "{:4}".format(self.id)
        result += ' Evaluation Value: ' + "{:8f}".format(float(self.value)) + ' '
        result += '| ' + ' | '.join('{0}: {1:>8.3f}'.format(idx, param) for idx, param in enumerate(self.genome))

        return result
