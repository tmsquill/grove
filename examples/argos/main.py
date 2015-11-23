import os
import re
import subprocess

import evolution.agent as agent
import evolution.config as config
import evolution.ga as ga
import evolution.selection as selection
import evolution.crossover as crossover
import evolution.mutation as mutation


def argos(argos_xml=None, agent=None):
    """
    Helper function for iAnt forager fitness function.
    :param argos_xml: ARGoS XML Configuration.
    :param agent: Forager agent to evaluate in simulation.
    :return: The agent with updated fitness value.
    """

    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    agent.execute_fitness(argos_xml)

    output = subprocess.check_output(['argos3 -n -c ' + argos_xml], shell=True, stderr=subprocess.STDOUT)
    result = re.search(r'\s(\d+),\s(\d+),\s(\d+)', output)
    agent.fitness = float(float(result.group(1)) / 256)

    return agent


class Forager:
    """
    Fitness function for iAnt forager agents using grammatical evolution.
    """

    import multiprocessing
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    def __call__(self, agents):

        results = [self.pool.apply_async(argos, args=('./experiments/iAnt_Obstacles_' + str(number) + '.xml', agent)) for number, agent in zip(list(xrange(len(agents))), agents)]
        output = [result.get() for result in results]
        agents = [agent_out for agent_out in output]

        return agents


if __name__ == "__main__":

    import argparse

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='py.evolve')
    parser.add_argument('-agent_config', action='store', type=str, default='./experiments/agent.json')
    parser.add_argument('-ga_config', action='store', type=str, default='./experiments/ga.json')
    parser.add_argument('-p', '--population', action='store', type=int, default=20)
    parser.add_argument('-g', '--generations', action='store', type=int, default=3)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    parser.add_argument('-b', '--bnf_grammar', action='store', type=int, default=40)
    parser.add_argument('-v', '--verbose', help='show BNF input file', action='store_true')
    args = parser.parse_args()

    # Load the configurations into memory (as dictionaries) by filename.
    config.load_configs([args.agent_config, args.ga_config])

    # Run the genetic algorithm.
    ga.evolve(args.population, args.generations, agent.ForagerAgent, Forager(), selection.truncation, crossover.one_point, mutation.gaussian, 'log')