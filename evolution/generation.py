__author__ = 'Troy Squillaci'

import copy
import itertools
import numpy as np


class Generation:

    gid = itertools.count().next

    def __init__(self):

        self.id = Generation.gid()
        self.agents = []
        self.min = []
        self.max = []
        self.mean = []
        self.median = []
        self.std = []

    def __str__(self):

        result = ''

        result += 'GID: ' + str(self.id) + '\n'

        for agent_set, min, max, mean, median, std in zip(self.agents, self.min, self.max, self.mean, self.median, self.std):

            result += '\n'.join(map(str, agent_set))

            result += '\n' + agent_set[0].__class__.__name__ + ' Agents Statistics'
            result += ' Min: ' + str(min)
            result += ' Max: ' + str(max)
            result += ' Mean: ' + str(mean)
            result += ' Median: ' + str(median)
            result += ' Standard Deviation: ' + str(std)

        return result

    def bind_agents(self, agents):

        self.agents = copy.deepcopy(agents)

    def generate_stats(self, agents):

        for agent_set in agents:

            fitness_scores = [agent.fitness for agent in agent_set]

            self.min.append(np.min(fitness_scores))
            self.max.append(np.max(fitness_scores))
            self.mean.append(np.mean(fitness_scores))
            self.median.append(np.median(fitness_scores))
            self.std.append(np.std(fitness_scores))
