import dispy
import logging
import time
from tqdm import tqdm

import config
from generation import Generation
import utils
import proto.agent_pb2 as pb


def evolve(population, generations, agent_type, evaluation_func, selection_func, crossover_func, mutation_func, nodes, log):
    """
    Performs evolution on a set of agents over a number of generations. The desired evolutionary functions must be
    specified by the caller. Logging is optional.
    :param population: The desired population size.
    :param generations: The number of generation to evolve.
    :param agent_type: The type of agent used to initialize the population.
    :param evaluation_func: The evaluation function.
    :param selection_func: The selection function.
    :param crossover_func: The crossover function.
    :param mutation_func: The mutation function.
    :param nodes: The nodes in the cluster used for computing the evaluation function.
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

    # Configure the cluster.
    cluster = dispy.JobCluster(evaluation_func, nodes=nodes, depends=[pb], loglevel=logging.DEBUG)

    # Initialize Generations.
    ga_generations = [Generation() for _ in xrange(generations)]

    # Initialize Agents.
    ga_agents = agent_type.init_agents(population)

    logging.info(' Agent Initialization '.center(180, '='))
    logging.info('\n' + '\n'.join(map(str, ga_agents)))

    # Perform Evolution.
    logging.info(' Evolution '.center(180, '=') + '\n')

    start_time = time.time()

    for generation in tqdm(ga_generations):

        logging.info(" Generation %s ".center(180, '*') % str(generation.id))

        print 'Generation ' + str(generation.id)

        jobs = []

        for agent in ga_agents:

            pb_agent = pb.Agent()
            pb_agent.genotype.probabilityOfSwitchingToSearching = agent.genotype[0]
            pb_agent.genotype.probabilityOfReturningToNest = agent.genotype[1]
            pb_agent.genotype.uninformedSearchVariation = agent.genotype[2]
            pb_agent.genotype.rateOfInformedSearchDecay = agent.genotype[3]
            pb_agent.genotype.rateOfSiteFidelity = agent.genotype[4]
            pb_agent.fitness = -1.0

            job = cluster.submit(str(pb_agent.SerializeToString()))
            job.id = agent.id
            jobs.append(job)

        cluster.wait()

        for job in jobs:

            job()
            print("Result of program %s with job ID %s starting at %s is %s with stdout %s" % (evaluation_func, job.id, job.start_time, job.result, job.stdout))

        cluster.stats()

        generation.bind_agents(ga_agents)
        logging.info('\n' + str(generation))

        ga_agents = selection_func(ga_agents)
        ga_agents = crossover_func(ga_agents, population)
        ga_agents = mutation_func(ga_agents)

    logging.info("Evolution finished in %s seconds " % (time.time() - start_time))
    print "Evolution finished in %s seconds " % (time.time() - start_time)

    utils.generate_csv(ga_generations)
