import os
import random

from evolution.agent import Agent
import evolution.config as config
import evolution.ga as ga
import evolution.grammar as grammar
import evolution.selection as selection
import evolution.crossover as crossover
import evolution.mutation as mutation

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


    import thriftpy.transport as tp
    import thriftpy.protocol as pc

    import thriftpy

    module_name = os.path.splitext(os.path.basename('/Users/Zivia/PycharmProjects/py.evolve/examples/grammar_argos/thrift/foraging.thrift'))[0] + '_thrift'
    thrift = thriftpy.load('/Users/Zivia/PycharmProjects/py.evolve/examples/grammar_argos/thrift/foraging.thrift', module_name=module_name)

    transportIn = tp.TMemoryBuffer(agent.phenotype)
    protocolIn = pc.TBinaryProtocol(transportIn)
    root = thrift.Root()
    root.read(protocolIn)

    return 'Agent AID: ' + str(root)


def post_evaluation(agents=None):

    return agents


if __name__ == "__main__":

    import argparse
    import json

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='py.evolve')
    parser.add_argument('-agent_config', action='store', type=str, default='agent.json')
    parser.add_argument('-ga_config', action='store', type=str, default='ga.json')
    parser.add_argument('-p', '--population', action='store', type=int, default=20)
    parser.add_argument('-g', '--generations', action='store', type=int, default=3)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    parser.add_argument('-b', '--grammar', action='store', type=str)
    parser.add_argument('-v', '--verbose', action='store_true', help='show BNF input file')
    args = parser.parse_args()

    # Compile the Thrift file into a python module.
    thrift = grammar.compile_thrift(args.grammar)

    from types import ModuleType
    print dir(thrift)
    print thrift.__thrift_meta__

    thrift_classes = [getattr(thrift, class_name) for class_name in dir(thrift) if not class_name.startswith('_')]
    print thrift_classes

    # Construct a grammar from a BNF file.
    grammar_o = grammar.Grammar(thrift)

    # Toggle verbosity.
    if args.verbose:

        print 'Non-Terminal Symbols: ' + str(grammar_o.non_terminals)
        print 'Terminal Symbols:' + str(grammar_o.terminals)
        print 'Grammar Tree:' + str(json.dumps(grammar_o.rules, sort_keys=True, indent=4))

    # Load the configurations into memory (as dictionaries) by filename.
    config.load_configs([args.agent_config, args.ga_config])

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-GES-ARGoS')

    # Run the genetic algorithm.
    ga.evolve(
        args.population,
        args.generations,
        GESAgent,
        pre_evaluation,
        evaluation,
        post_evaluation,
        selection.tournament(4, 5),
        crossover.one_point(),
        mutation.gaussian(),
        [], #['10.0.0.30', '10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34', '10.0.0.35', '10.0.0.36'],
        [Agent, GESAgent],
        'log'
    )
