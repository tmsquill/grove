__author__ = 'Troy Squillaci'

import copy
import itertools
import numpy as np


class Generation:

    gid = itertools.count().next

    def __init__(self):

        self.id = Generation.gid()
        self.agents = []
        self.obs_agents = []
        self.min = -1
        self.max = -1
        self.mean = -1
        self.median = -1
        self.std = -1
        self.obs_min = -1
        self.obs_max = -1
        self.obs_mean = -1
        self.obs_median = -1
        self.obs_std = -1

    def __str__(self):

        result = ''

        result += 'GID: ' + str(self.id) + '\n'

        result += '\n'.join(map(str, self.agents))

        result += '\niAnt Agents Statistics'
        result += ' Min: ' + str(self.min)
        result += ' Max: ' + str(self.max)
        result += ' Mean: ' + str(self.mean)
        result += ' Median: ' + str(self.median)
        result += ' Standard Deviation: ' + str(self.std)

        result += '\n'.join(map(str, self.agents))

        result += '\nObstacle Agents Statistics'
        result += ' Min: ' + str(self.obs_min)
        result += ' Max: ' + str(self.obs_max)
        result += ' Mean: ' + str(self.obs_mean)
        result += ' Median: ' + str(self.obs_median)
        result += ' Standard Deviation: ' + str(self.obs_std)

        return result

    def bind_agents(self, agents, obs_agents):

        self.agents = copy.deepcopy(agents)
        self.obs_agents = copy.deepcopy(obs_agents)

    def generate_stats(self, agents, obs_agents):

        fitness_scores = [agent.fitness for agent in agents]
        obs_fitness_scores = [obs_agent.fitness for obs_agent in obs_agents]

        self.min = np.min(fitness_scores)
        self.max = np.max(fitness_scores)
        self.mean = np.mean(fitness_scores)
        self.median = np.median(fitness_scores)
        self.std = np.std(fitness_scores)

        self.obs_min = np.min(obs_fitness_scores)
        self.obs_max = np.max(obs_fitness_scores)
        self.obs_mean = np.mean(obs_fitness_scores)
        self.obs_median = np.median(obs_fitness_scores)
        self.obs_std = np.std(obs_fitness_scores)
