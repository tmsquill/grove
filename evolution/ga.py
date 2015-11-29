import logging
import time

import agent
import config
from generation import Generation
import utils


def exec_fitness(agents, fitness_function):
    """
    Evaluates the population of agents and updates their fitness values.
    :param agents: The set of agents to evaluate.
    :param fitness_function: The fitness function used to evaulate the agents.
    :return: The same set of agents with updated fitness values.
    """

    agents = fitness_function.__call__(agents)

    return agents


def evolve(population, generations, agent_type, fitness_func, selection_func, crossover_func, mutation_func, log):
    """
    Performs evolution on a set of agents over a number of generations. The desired evolutionary functions must be
    specified by the caller. Logging is optional.
    :param population: The desired population size.
    :param generations: The number of generation to evolve.
    :param agent_type: The type of agent used to initialize the population.
    :param fitness_func: The fitness function.
    :param selection_func: The selection function.
    :param crossover_func: The crossover function.
    :param mutation_func: The mutation function.
    :param log: The path to output the log file, if not specified does not log.
    """

    # TODO: If logging not specified, must disable.
    # Initialize Logging
    if log:
        now = time.strftime("%I:%M-D%dM%mY%Y")
        logging.basicConfig(filename=log + '/' + now + '.log', level=logging.DEBUG)
        logging.info(' Log for py.evolve '.center(180, '='))

    # Log Configurations
    for name in config.global_config:

        logging.info((config.global_config[name]['name'] + ' Configuration ').center(180, '-'))
        logging.info('\n' + config.pretty_config(name))

    # Initialize Generations
    ga_generations = [Generation() for _ in xrange(generations)]

    # Initialize Agents
    ga_agents = agent.init_agents(agent_type, population)

    logging.info(' Agent Initialization '.center(180, '='))
    logging.info('\n' + '\n'.join(map(str, ga_agents)))

    logging.info(' Evolution '.center(180, '=') + '\n')

    start_time = time.time()

    for generation in ga_generations:

        logging.info(" Generation %s ".center(180, '*') % str(generation.id))

        print 'Generation ' + str(generation.id)

        ga_agents = exec_fitness(ga_agents, fitness_func)

        generation.bind_agents(ga_agents)
        logging.info('\n' + str(generation))

        ga_agents = selection_func(ga_agents)
        ga_agents = crossover_func(ga_agents, population)
        ga_agents = mutation_func(ga_agents)

    logging.info("Evolution finished in %s seconds " % (time.time() - start_time))
    print "Evolution finished in %s seconds " % (time.time() - start_time)

    utils.generate_csv(ga_generations)
