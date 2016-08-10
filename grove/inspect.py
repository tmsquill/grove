import random

from grammar.grammar import Grammar
from grammar.parse_tree import ParseTree
# TODO - Determine proper import for ObjectId
from pymongo import MongoClient


def inspect_parse_tree(genotype=None, grammar_file=None):

    if not isinstance(genotype, list):

        genotype = [raw_input('Enter a genotype (i.e. 34, 1, 93, ...): ').replace(",", "").split()]

    grammar = Grammar(grammar_file)
    parse_tree = ParseTree(grammar, genotype)
    parse_tree.generate()
    print parse_tree


def inspect_simulation(genotype=None, grammar_file=None, host='localhost', port=27017):

    from simulation.entity import SimAgent, Food, Nest
    from simulation.environment import Environment
    from simulation.simulation import Simulation
    from simulation.utils import generate_mongo

    if isinstance(genotype, ObjectId)

        connection = MongoClient(host, port)
        simulations = connection['grove']['simulations']

        # TODO - Determine how to access record. Its probably...
        simulation = simulations[genotype]

    elif not isinstance(genotype, list):

        genotype = [raw_input('Enter a genotype (i.e. 34, 1, 93, ...): ').replace(",", "").split()]

    grammar = Grammar(grammar_file)
    parse_tree = ParseTree(grammar, genotype)
    parse_tree.generate()

    # Create the entities for the simulation.
    agents = [SimAgent(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(5)]
    nest = Nest(position=(8, 8), size=(4, 4))
    food = [Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(10)]

    entities = agents + [nest] + food

    # Create the environment for the simulation.
    env = Environment()

    # Create and execute the simulation.
    sim = Simulation(environment=env, entities=entities, parse_tree=parse_tree.root.obj)
    sim.execute()

    generate_mongo(sim)

    # Get the food tags collected, and return as the evaluation score.
    nest = filter(lambda x: isinstance(x, Nest), sim.entities)

    return nest[0].food_count
