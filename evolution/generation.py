__author__ = 'Troy Squillaci'

import copy
import itertools
import numpy as np


class Generation:

    gid = itertools.count().next

    def __init__(self):

        self.id = Generation.gid()
        self.agents = []

    def __str__(self):

        result = ''

        result += 'GID: ' + str(self.id) + '\n'

        for agent_set in self.agents:

            result += '\n'.join(map(str, agent_set)) + '\n'

        return result

    def bind_agents(self, agents):

        self.agents = copy.deepcopy(agents)
