import os
import random

from evolution.agent import Agent
import evolution.config as config
import evolution.ga as ga
import evolution.grammar as grammar
import evolution.selection as selection
import evolution.crossover as crossover
import evolution.mutation as mutation


bnf_grammar = None


class GESAgent(Agent):
    """ An agent targeted towards GES. """

    def __init__(self):

        super(GESAgent, self).__init__()

        self.genotype_lb = [self.genotype_lb[0]] * 100
        self.genotype_ub = [self.genotype_ub[0]] * 100
        self.genotype = [random.randint(lower, upper) for lower, upper in zip(self.genotype_lb, self.genotype_ub)]
        self.genotype_len = len(self.genotype)

        self.phenotype = None
        self.used_codons = 0

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



def evaluation(agent=None):
    """
    Evaluation function that executes ARGoS with the specified agent.
    :param agent: The agent to evaluate in the ARGoS simulation.
    :return: The agent with updated evaluation value.
    """

    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-GES-ARGoS')

    agent.phenotype, agent.used_codons = bnf_grammar.generate(agent.genotype)

    # TODO: Execute ARGoS with the phenotype, update the value of agent, then return it.

    return agent


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
    parser.add_argument('-b', '--bnf_grammar', action='store', type=str)
    parser.add_argument('-v', '--verbose', action='store_true', help='show BNF input file')
    args = parser.parse_args()

    # Construct a grammar from a BNF file.
    bnf_grammar = grammar.Grammar(args.bnf_grammar)

    # Toggle verbosity.
    if args.verbose:

        print 'Non-Terminal Symbols: ' + str(bnf_grammar.non_terminals)
        print 'Terminal Symbols:' + str(bnf_grammar.terminals)
        print 'Grammar Tree:' + str(json.dumps(bnf_grammar.rules, sort_keys=True, indent=4))

    # TODO: For grammar testing purposes, will be removed for actual runs.
    exit()

    # Load the configurations into memory (as dictionaries) by filename.
    config.load_configs([args.agent_config, args.ga_config])

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-GES-ARGoS')

    # Run the genetic algorithm.
    ga.evolve(
        args.population,
        args.generations,
        GESAgent,
        evaluation,
        selection.truncation,
        crossover.one_point,
        mutation.gaussian,
        'log'
    )
