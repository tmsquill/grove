import logging
import time

import config
from generation import Generation
import agent
import utils


def exec_fitness(agents, fitness_function):

    agents = fitness_function.__call__(agents)

    return agents


def evolve(population, generations, agent_type, fitness_function, selection_function, crossover_function, mutation_function, log):

    # Initialize Logging
    now = time.strftime("%I:%M-D%dM%mY%Y")
    logging.basicConfig(filename=log + '/' + now + '.log', level=logging.DEBUG)
    logging.info(' Log for py.evolve '.center(180, '='))

    # Log Configurations
    for name in config.global_config:

        logging.info((config.global_config[name]['name'] + ' Configuration ').center(180, '-'))
        logging.info('\n' + config.pretty_config(name))

    # Initialize Generations
    ga_generations = [Generation() for sentinel in xrange(generations)]

    # Initialize Agents
    ga_agents = agent.init_agents(agent_type, population)

    logging.info(' Agent Initialization '.center(180, '='))
    logging.info('\n' + '\n'.join(map(str, ga_agents)))

    logging.info(' Evolution '.center(180, '=') + '\n')

    start_time = time.time()

    for generation in ga_generations:

        logging.info(" Generation %s ".center(180, '*') % str(generation.id))

        print 'Generation ' + str(generation.id)

        ga_agents = exec_fitness(ga_agents, fitness_function)

        generation.bind_agents(ga_agents)
        logging.info('\n' + str(generation))

        ga_agents = selection_function(ga_agents)
        ga_agents = crossover_function(ga_agents, population)
        ga_agents = mutation_function(ga_agents)

    logging.info("Evolution finished in %s seconds " % (time.time() - start_time))
    print "Evolution finished in %s seconds " % (time.time() - start_time)

    utils.generate_csv(ga_generations)
