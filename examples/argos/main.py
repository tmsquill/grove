import numpy as np
import os
import random

from evolution.agent import Agent
import evolution.config as config
import evolution.ga as ga
import evolution.selection as selection
import evolution.crossover as crossover
import evolution.mutation as mutation


class CPFAAgent(Agent):

    def __init__(self):

        super(CPFAAgent, self).__init__()
        self.genotype = [random.uniform(lower, upper) for lower, upper in zip(self.genotype_lb, self.genotype_ub)]
        self.genotype_len = len(self.genotype)

    @staticmethod
    def factory():

        return CPFAAgent()

    @staticmethod
    def init_agents(population):

        agents = []

        for i in xrange(population):

            agent = CPFAAgent.factory()
            mean = float(i) / population

            for idx, param in enumerate(agent.genotype):

                param = agent.genotype_ub[idx] * 1 # np.random.normal(loc=mean, scale=0.05)

                if param < agent.genotype_lb[idx]:
                    param = agent.genotype_lb[idx]
                elif param > agent.genotype_ub[idx]:
                    param = agent.genotype_ub[idx]

                agent.genotype[idx] = param

            agents.append(agent)

        return agents


def evaluation(agent=None):
    """
    Evaluation function that executes ARGoS with the specified agent.
    :param agent: The agent to evaluate in the ARGoS simulation.
    :return: The agent with updated evaluation value.
    """

    import random
    print agent
    return random.randint(1, 100)


if __name__ == "__main__":

    import argparse

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='py.evolve')
    parser.add_argument('-agent_config', action='store', type=str, default='agent.json')
    parser.add_argument('-ga_config', action='store', type=str, default='ga.json')
    parser.add_argument('-p', '--population', action='store', type=int, default=28)
    parser.add_argument('-g', '--generations', action='store', type=int, default=1000)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    args = parser.parse_args()

    # Load the configurations into memory (as dictionaries) by filename.
    config.load_configs([args.agent_config, args.ga_config])

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    # Run the genetic algorithm.
    ga.evolve(
        args.population,
        args.generations,
        CPFAAgent,
        evaluation,
        selection.tournament(4, 5),
        crossover.one_point(),
        mutation.gaussian(),
        ['10.0.0.30', '10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34', '10.0.0.35', '10.0.0.36'],
        'log'
    )
