__author__ = 'Troy Squillaci'

import copy
import itertools


class Generation:

    gid = itertools.count().next

    def __init__(self):

        self.id = Generation.gid()
        self.agents = []
        self.agents_map = {}

    def __str__(self):

        result = ''

        result += 'GID: ' + str(self.id) + '\n'

        for agent_set in self.agents:

            result += '\n'.join(map(str, agent_set)) + '\n'

        return result

    def bind_agents(self, agents):

        self.agents = copy.deepcopy(agents)

        for idx, agent_set in enumerate(self.agents):

            self.agents_map[agent_set[0].__class__.__name__] = idx

    def csv(self, agent_idx):

        return [[[self.id] + [agent.id] + [agent.fitness] + agent.params].pop(0) for agent in self.agents[agent_idx]]
