import logging
import time

import dispy

import config
import utils
from generation import Generation


def evolve(population, generations, agent_type, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation, nodes, depends, log):
    """
    Performs evolution on a set of agents over a number of generations. The desired evolutionary functions must be
    specified by the caller. Logging is optional.
    :param population: The desired population size.
    :param generations: The number of generation to evolve.
    :param agent_type: The type of agent used to initialize the population.
    :param evaluation: The evaluation function.
    :param selection: The selection function.
    :param crossover: The crossover function.
    :param mutation: The mutation function.
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

    # Validate pre and post evaluation functions.
    if not hasattr(pre_evaluation, '__call__'):

        raise ValueError('pre_evaluation_func is not callable', pre_evaluation)

    if not hasattr(post_evaluation, '__call__'):

        raise ValueError('post_evaluation_func is not callable', post_evaluation)

    # Configure the cluster.
    cluster = dispy.JobCluster(evaluation, nodes=nodes, depends=depends, loglevel=logging.DEBUG)

    # Initialize Generations.
    ga_generations = [Generation() for _ in xrange(generations)]

    # Initialize Agents.
    ga_agents = agent_type.init_agents(population)

    logging.info(' Agent Initialization '.center(180, '='))
    logging.info('\n' + '\n'.join(map(str, ga_agents)))

    # Perform Evolution.
    logging.info(' Evolution '.center(180, '=') + '\n')

    start_time = time.time()

    for generation in ga_generations:

        logging.info(" Generation %s ".center(180, '*') % str(generation.id))

        print 'Generation ' + str(generation.id)

        ga_agents = pre_evaluation(ga_agents)

        jobs = []

        for agent in ga_agents:

            job = cluster.submit(agent)
            job.id = agent.id
            jobs.append(job)

        cluster.wait()

        for job in jobs:

            job()
            print("Result of program %s with job ID %s starting at %s is %s with stdout %s" % (evaluation, job.id, job.start_time, job.result, job.stdout))

        ga_agents = post_evaluation(ga_agents)

        generation.bind_agents(ga_agents)
        logging.info('\n' + str(generation))

        ga_agents = selection(ga_agents)
        ga_agents = crossover(ga_agents, population)
        ga_agents = mutation(ga_agents)

    cluster.stats()

    logging.info("Evolution finished in %s seconds " % (time.time() - start_time))
    print "Evolution finished in %s seconds " % (time.time() - start_time)

    utils.generate_csv(ga_generations)
