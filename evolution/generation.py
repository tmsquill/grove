import copy
import itertools


class Generation:
    """
    Represents a generation from the evolutionary process. Maintains a snapshot of the populations during that time.
    Particularly useful for logging and saving data for future data analysis.
    """

    gid = itertools.count().next

    def __init__(self):

        self.id = Generation.gid()
        self.agents = []

    def __str__(self):

        result = ''

        result += 'GID: ' + str(self.id) + '\n'

        result += '\n'.join(map(str, self.agents)) + '\n'

        return result

    def bind_agents(self, agents):

        self.agents = copy.deepcopy(agents)

    def csv(self):

        return [[[self.id] + [agent.id] + [agent.fitness] + agent.genotype].pop(0) for agent in self.agents]
