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


def fitness(argos_xml=None, agent=None):
    """
    Helper function for iAnt forager fitness function.
    :param argos_xml: ARGoS XML Configuration.
    :param agent: Forager agent to evaluate in simulation.
    :return: The agent with updated fitness value.
    """

    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    agent.evaluate(argos_xml)

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


class ForagerAgent(ARGoSAgent):

    def __init__(self):

        super(ForagerAgent, self).__init__()

    @staticmethod
    def factory():

        return ForagerAgent()

    def evaluate(self, argos_xml):

        forager_config = None

        with open(argos_xml, 'r') as xml:

            forager_config = xmltodict.parse(xml)

        # General
        forager_config['argos-configuration']['framework']['experiment']['@random_seed'] = str(random.randint(1, 1000000))

        # iAnt Robots
        forager_config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfSwitchingToSearching'] = str(round(self.genotype[0], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfReturningToNest'] = str(round(self.genotype[1], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@UninformedSearchVariation'] = str(round(self.genotype[2], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfInformedSearchDecay'] = str(round(self.genotype[3], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfSiteFidelity'] = str(round(self.genotype[4], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfLayingPheromone'] = str(round(self.genotype[5], 5))
        forager_config['argos-configuration']['loop_functions']['CPFA']['@RateOfPheromoneDecay'] = str(round(self.genotype[6], 5))

        with open(argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(forager_config, pretty=True))
            xml.truncate()


class ObstacleAgent(ARGoSAgent):

    def __init__(self):

        super(ObstacleAgent, self).__init__()

        for i in xrange(self.genotype_len):

            param = random.uniform(-self.genotype_ub[i], self.genotype_ub[i])

            while abs(param) < self.genotype_lb[i]:

                param = random.uniform(-self.genotype_ub[i], self.genotype_ub[i])

            self.genotype[i] = param

    @staticmethod
    def factory():

        return ObstacleAgent()

    def evaluate(self, argos_xml):

        with open(argos_xml, 'r') as xml:

            obstacle_config = xmltodict.parse(xml)

        # Obstacles
        obstacle_config['argos-configuration']['arena']['box'][0]['body']['@orientation'] = \
            str(round(self.genotype[0], 3)) + ',0,0'
        obstacle_config['argos-configuration']['arena']['box'][0]['body']['@position'] = \
            str(round(self.genotype[1], 3)) + ',' + str(round(self.genotype[2], 3)) + ',0'

        obstacle_config['argos-configuration']['arena']['box'][1]['body']['@orientation'] = \
            str(round(self.genotype[3], 3)) + ',0,0'
        obstacle_config['argos-configuration']['arena']['box'][1]['body']['@position'] = \
            str(round(self.genotype[4], 3)) + ',' + str(round(self.genotype[5], 3)) + ',0'

        obstacle_config['argos-configuration']['arena']['box'][2]['body']['@orientation'] = \
            str(round(self.genotype[6], 3)) + ',0,0'
        obstacle_config['argos-configuration']['arena']['box'][2]['body']['@position'] = \
            str(round(self.genotype[7], 3)) + ',' + str(round(self.genotype[8], 3)) + ',0'

        obstacle_config['argos-configuration']['arena']['box'][3]['body']['@orientation'] = \
            str(round(self.genotype[9], 3)) + ',0,0'
        obstacle_config['argos-configuration']['arena']['box'][3]['body']['@position'] = \
            str(round(self.genotype[10], 3)) + ',' + str(round(self.genotype[11], 3)) + ',0'

        with open(argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(obstacle_config, pretty=True))
            xml.truncate()


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
        selection.truncation,
        crossover.one_point,
        mutation.gaussian,
        'log'
    )
