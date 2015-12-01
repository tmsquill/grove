import os
import random
import re
import subprocess
import xmltodict

from evolution.agent import ARGoSAgent
import evolution.config as config
import evolution.ga as ga
import evolution.selection as selection
import evolution.crossover as crossover
import evolution.mutation as mutation


class ForagerAgent(ARGoSAgent):

    def __init__(self):

        super(ForagerAgent, self).__init__()
        self.xml_argos = None

    @staticmethod
    def factory():

        return ForagerAgent()

    # TODO: Maybe remove this.
    def evaluate(self, argos_xml):

        pass


def fitness(argos_xml=None, agent=None):
    """
    Helper function for iAnt forager fitness function.
    :param argos_xml: ARGoS XML Configuration.
    :param agent: Forager agent to evaluate in simulation.
    :return: The agent with updated fitness value.
    """

    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    forager_config = None

    with open(argos_xml, 'r') as xml:

        forager_config = xmltodict.parse(xml)

    # General
    forager_config['argos-configuration']['framework']['experiment']['@random_seed'] = str(random.randint(1, 1000000))

    # iAnt Robots
    forager_config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfSwitchingToSearching'] = str(round(agent.genotype[0], 5))
    forager_config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfReturningToNest'] = str(round(agent.genotype[1], 5))
    forager_config['argos-configuration']['loop_functions']['CPFA']['@UninformedSearchVariation'] = str(round(agent.genotype[2], 5))
    forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfInformedSearchDecay'] = str(round(agent.genotype[3], 5))
    forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfSiteFidelity'] = str(round(agent.genotype[4], 5))
    forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfLayingPheromone'] = str(round(agent.genotype[5], 5))
    forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfPheromoneDecay'] = str(round(agent.genotype[6], 5))

    with open(argos_xml, 'w') as xml:

        xml.write(xmltodict.unparse(forager_config, pretty=True))
        xml.truncate()

    output = subprocess.check_output(['argos3 -n -c ' + argos_xml], shell=True, stderr=subprocess.STDOUT)
    result = re.search(r'\s(\d+),\s(\d+),\s(\d+)', output)
    agent.fitness = float(float(result.group(1)) / 256)

    return agent


class ForagerFitness:
    """
    Fitness function for iAnt forager agents using grammatical evolution.
    """

    import multiprocessing
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    def __call__(self, agents):

        results = [
            self.pool.apply_async(
                fitness,
                args=('./experiments/iAnt_Obstacles_' + str(number) + '.xml', agent)
            ) for number, agent in zip(list(xrange(len(agents))), agents)
        ]
        output = [result.get() for result in results]
        agents = [agent_out for agent_out in output]

        return agents


if __name__ == "__main__":

    import argparse

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='py.evolve')
    parser.add_argument('-agent_config', action='store', type=str, default='./experiments/agent.json')
    parser.add_argument('-ga_config', action='store', type=str, default='./experiments/ga.json')
    parser.add_argument('-p', '--population', action='store', type=int, default=20)
    parser.add_argument('-g', '--generations', action='store', type=int, default=3)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    args = parser.parse_args()

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    # Load the configurations into memory (as dictionaries) by filename.
    config.load_configs([args.agent_config, args.ga_config])

    # Run the genetic algorithm.
    ga.evolve(
        args.population,
        args.generations,
        ForagerAgent,
        ForagerFitness(),
        selection.tournament(4, 5),
        crossover.one_point,
        mutation.gaussian,
        'log'
    )
