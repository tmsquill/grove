import os
import random

from evolution import agent, ga, selection, crossover, mutation
from grammar.parse_tree import ParseTree
from grove import config, logger


class GESAgent(agent.Agent):

    """
    An agent targeted for GES.
    """

    grammar = None

    def __init__(self):

        super(GESAgent, self).__init__()

        self.genotype = [random.randint(lower, upper) for lower, upper in zip(self.genotype_lb, self.genotype_ub)]
        self.parse_tree = ParseTree(GESAgent.grammar, self.genotype)

    @staticmethod
    def init_agents(population):

        """
        Initialized a set of agents based on a population size.
        :param population: The population (number of agents) to initialize.
        :return: The initialized population.
        """

        return [GESAgent() for _ in xrange(population)]


def pre_evaluation(agents=None):

    """
    Pre-evaluation function prepares agents for evaluation. In this case, a genome is used to generate a parse tree,
    which is used during evaluation.
    :param agents: The population of agents to map the generation of parse trees over.
    :return: The updated agents with generated parse trees.
    """

    for agent in agents:

        agent.parse_tree.generate()

        # print agent.parse_tree
        # print agent.parse_tree.root.obj
        #
        # from ete3 import TreeStyle
        #
        # ts = TreeStyle()
        # ts.show_leaf_name = True
        # ts.mode = "c"
        # ts.arc_start = -180 # 0 degrees = 3 o'clock
        # ts.arc_span = 180
        # # agent.parse_tree.root.show(tree_style=ts)
        # exit()

        agent.payload = agent.parse_tree.serialize()

    return agents


def evaluation(payload=None):

    """
    Evaluation function that executes a simulation with the specified payload. In this case the payload is a serialized
    parse tree that defines the legal transformation that can take place in the dynamic state machine.
    :param payload: The payload (serialized parse tree) to evaluate.
    :return: The evaluation value determined by executing the evaluation function with the payload.
    """

    import os
    import traceback

    os.chdir(os.path.expanduser('~') + '/lyssa/simulations')

    try:

        import sys
        sys.path.append('/Users/Zivia/PycharmProjects/grove')

        from simulation.entity import SimAgent, Food, Nest
        from simulation.environment import Environment
        from simulation.simulation import Simulation
        from simulation.utils import generate_mongo

        import thriftpy.transport as tp
        import thriftpy.protocol as pc
        import thriftpy

        # Path to Thrift
        thrift_path = '/Users/Zivia/PycharmProjects/grove/examples/ges_lyssa/thrift/foraging.thrift'

        # Compile the Thrift and read the grammar.
        module_name = os.path.splitext(os.path.basename(thrift_path))[0] + '_thrift'
        thrift = thriftpy.load(thrift_path, module_name=module_name)

        transportIn = tp.TMemoryBuffer(payload)
        protocolIn = pc.TBinaryProtocol(transportIn)
        root = thrift.Root()
        root.read(protocolIn)

        # Create the entities for the simulation.
        agents = [SimAgent(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(5)]
        nest = Nest(position=(8, 8), size=(4, 4))
        food = [Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(80)]

        entities = agents + [nest] + food

        # Create the environment for the simulation.
        env = Environment()

        # Create and execute the simulation.
        sim = Simulation(environment=env, entities=entities, parse_tree=root)
        sim.execute()

        _id = generate_mongo(sim)

        # Get the food tags collected, and return as the evaluation score.
        nest = filter(lambda x: isinstance(x, Nest), sim.entities)

        return (nest[0].food_count, _id)

    except Exception:

        print traceback.format_exc()
        return traceback.format_exc()


def post_evaluation(agents=None):

    """
    Post-evaluation function performs data collection and/or alters agents after evaluation. In this case, no action
    is needed, so the agents are simply returned.
    :param agents: The population of agents.
    :return: The population of agents.
    """

    return agents


if __name__ == "__main__":

    # Parser for command line arguments.
    import argparse

    parser = argparse.ArgumentParser(description='grove')
    parser.add_argument('-config', action='store', type=str, default='examples/ges_lyssa/grove-config.json')
    parser.add_argument('-p', '--population', action='store', type=int)
    parser.add_argument('-g', '--generations', action='store', type=int)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    parser.add_argument('-b', '--grammar', action='store', type=str)
    parser.add_argument('-l', '--log_path', action='store', type=str)
    args = parser.parse_args()

    # Load the grammar file.
    from grammar.grammar import Grammar

    GESAgent.grammar = Grammar(args.grammar)

    # Load the grove configuration.
    config.load_config(args.config)

    # Initialize the grove logger.
    logger.init_logger(args.log_path)

    # Change the current directory, for logging purposes.
    os.chdir(os.path.expanduser('~') + '/lyssa')

    # Run the genetic algorithm.
    ga.evolve(
        population=args.population or config.grove_config['ga']['parameters']['population'],
        generations=args.generations or config.grove_config['ga']['parameters']['generations'],
        repeats=config.grove_config['ga']['parameters']['repeats'],
        agent_type=GESAgent,
        pre_evaluation=pre_evaluation,
        evaluation=evaluation,
        post_evaluation=post_evaluation,
        selection=selection.tournament(4, 5),
        crossover=crossover.one_point(),
        mutation=mutation.gaussian(),
        evaluation_type='distributed',
        nodes=[],
        depends=[],
        debug=config.grove_config['debug']
    )
