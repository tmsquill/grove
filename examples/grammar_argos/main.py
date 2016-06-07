import os
import random

from evolution import config, ga, grammar, selection, crossover, mutation
from evolution.agent import Agent

import thriftpy.transport as tp
import thriftpy.protocol as pc

grammar_o = None


class GESAgent(Agent):

    """ An agent targeted towards GES. """

    def __init__(self):

        super(GESAgent, self).__init__()

        self.genotype = [random.randint(lower, upper) for lower, upper in zip(self.genotype_lb, self.genotype_ub)]

        self.phenotype = None
        self.used_in_seq = 0

    @staticmethod
    def factory():

        return GESAgent()

    @staticmethod
    def init_agents(population):

        """
        Initialized a set of agents based on a population size.
        :param population: The population (number of agents) to initialize.
        :return: The initialized population.
        """
        return [GESAgent.factory() for _ in xrange(population)]


def pre_evaluation(agents=None):

    for agent in agents:

        phenotype, used_in_seq = grammar_o.generate(agent.genotype)

        transOut = tp.TMemoryBuffer()
        protocolOut = pc.TBinaryProtocol(transOut)
        phenotype.write(protocolOut)
        agent.phenotype = transOut.getvalue()

    return agents


def evaluation(agent=None):

    """
    Evaluation function that executes ARGoS with the specified agent.
    :param agent: The agent to evaluate in the ARGoS simulation.
    :return: The agent with updated evaluation value.
    """

    from simulation.entity import Food, Nest, SimAgent
    from simulation.environment import Environment
    from simulation.simulation import Simulation

    import thriftpy.transport as tp
    import thriftpy.protocol as pc
    import thriftpy

    # Path to Thrift
    thrift_path = '/Users/Zivia/PycharmProjects/py.evolve/examples/grammar_argos/thrift/foraging.thrift'

    # Compile the Thrift and read the grammar.
    module_name = os.path.splitext(os.path.basename(thrift_path))[0] + '_thrift'
    thrift = thriftpy.load(thrift_path, module_name=module_name)

    transportIn = tp.TMemoryBuffer(agent.phenotype)
    protocolIn = pc.TBinaryProtocol(transportIn)
    root = thrift.Root()
    root.read(protocolIn)

    # Create the entities for the simulation.
    agents = [SimAgent(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(5)]
    nest = Nest(position=(8, 8), size=(4, 4))
    food = [Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(10)]

    entities = agents + [nest] + food

    # Create the environment for the simulation.
    env = Environment()

    # Create and execute the simulation.
    sim = Simulation(environment=env, entities=entities, parse_tree=root)
    sim.execute()

    # Get the food tags collected, and return as the evaluation score.
    nest = filter(lambda x: isinstance(x, Nest), sim.entities)

    return nest[0].food_count


def post_evaluation(agents=None):

    return agents


if __name__ == "__main__":

    import argparse

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='grove')
    parser.add_argument('-config', action='store', type=str, default='grove-config.json')
    parser.add_argument('-p', '--population', action='store', type=int)
    parser.add_argument('-g', '--generations', action='store', type=int)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    parser.add_argument('-b', '--grammar', action='store', type=str)
    args = parser.parse_args()

    # Compile the Thrift file into a python module.
    thrift = grammar.compile_thrift(args.grammar)

    # Construct the grammar object.
    grammar_o = grammar.Grammar(thrift)

    # Load the grove configuration.
    config.load_config(args.config)

    # Initialize logging handler.
    from logbook import FileHandler, Logger
    import time

    log_handler = FileHandler('grove-' + time.strftime("%I:%M-M%mD%dY%Y" + '.log'))
    log = Logger('Grove Logger')

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-GES-ARGoS')

    # Run the genetic algorithm.
    with log_handler.applicationbound():

        ga.evolve(
            args.population or config.grove_config['ga']['parameters']['population'],
            args.generations or config.grove_config['ga']['parameters']['generations'],
            GESAgent,
            pre_evaluation,
            evaluation,
            post_evaluation,
            selection.tournament(4, 5),
            crossover.one_point(),
            mutation.gaussian(),
            [], #['10.0.0.30', '10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34', '10.0.0.35', '10.0.0.36'],
            [], #[Agent, GESAgent],
            log
        )
