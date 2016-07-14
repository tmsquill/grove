import dispy
import time
import utils

from generation import Generation
from grove import config, logger


def evolve(population, generations, agent_type, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation, evaluation_type, nodes, depends):

    """
    Performs evolution on a set of agents over a number of generations. The desired evolutionary functions must be
    specified by the caller. Logging is optional.
    :param population: The desired population size.
    :param generations: The number of generation to evolve.
    :param agent_type: The type of agent used to initialize the population.
    :param pre_evaluation: The pre-evaluation function. Intended to prepare agents for evaluation.
    :param evaluation: The evaluation function.
    :param post_evaluation: The post-evaluation function. Intended to gather data or alter agents after evaluation.
    :param selection: The selection function.
    :param crossover: The crossover function.
    :param mutation: The mutation function.
    :param evaluation_type: The type of execution for evaluation. Either serial or distributed.
    :param nodes: The nodes in the cluster used for computing the evaluation function.
    :param depends: The list of dependencies needed by dispynodes to perform computation of the evaluation function.
    """

    with logger.log_handler.applicationbound():

        # Log Configuration
        logger.log.info(config.pretty_config())

        # Validate pre and post evaluation functions.
        if not hasattr(pre_evaluation, '__call__'):

            raise ValueError('pre_evaluation_func is not callable', pre_evaluation)

        if not hasattr(post_evaluation, '__call__'):

            raise ValueError('post_evaluation_func is not callable', post_evaluation)

        # Initialize generations.
        ga_generations = [Generation() for _ in xrange(generations)]

        # Initialize agents.
        ga_agents = agent_type.init_agents(population)

        logger.log.info('\n' + ' Agent Initialization '.center(180, '=') + '\n')
        logger.log.info('\n'.join(map(str, ga_agents)))

        if evaluation_type == 'serial':

            serial(population, ga_generations, ga_agents, pre_evaluation, evaluation, post_evaluation, selection,
                   crossover, mutation)

        elif evaluation_type == 'distributed':

            distributed(population, ga_generations, ga_agents, pre_evaluation, evaluation, post_evaluation, selection,
                        crossover, mutation, nodes, depends)

        else:

            raise ValueError('evaluation_type is invalid', evaluation_type)


def serial(population, generations, agents, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation):

    logger.log.info('\n' + ' Evolution (Serial) '.center(180, '=') + '\n')
    print ' Evolution (Serial) '.center(180, '=') + '\n'

    start_time = time.time()

    for generation in generations:

        logger.log.info(" Generation %s ".center(180, '*') % str(generation.id))
        print 'Generation ' + str(generation.id)

        agents = pre_evaluation(agents)

        for agent in agents:

            agent = evaluation(agent.payload)

        agents = post_evaluation(agents)

        generation.bind_agents(agents)
        logger.log.info('\n' + str(generation))

        agents = selection(agents)
        agents = crossover(agents, population)
        agents = mutation(agents)

    total_time = time.time() - start_time
    logger.log.info("Evolution finished in %s seconds " % total_time)
    print "Evolution finished in %s seconds " % total_time

    if config.grove_config['data']['collection_type']:

        getattr(utils, 'generate_' + config.grove_config['data']['collection_type'])(generations)


def distributed(population, generations, agents, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation, nodes, depends):

    logger.log.info('\n' + ' Evolution (Distributed) '.center(180, '=') + '\n')
    print ' Evolution (Distributed) '.center(180, '=') + '\n'

    # TODO - Remove logging when able.
    import logging

    # Configure the cluster.
    if isinstance(evaluation, basestring) or hasattr(evaluation, '__call__'):

        cluster = dispy.JobCluster(evaluation, nodes=nodes, depends=depends, loglevel=logging.DEBUG)

    else:

        raise TypeError('evaluation is not a string or callable', evaluation)

    start_time = time.time()

    for generation in generations:

        logger.log.info(" Generation %s ".center(180, '*') % str(generation.id))
        print 'Generation ' + str(generation.id)

        agents = pre_evaluation(agents)

        jobs = []

        for agent in agents:

            job = cluster.submit(agent.payload)
            job.id = agent.id
            jobs.append(job)

        cluster.wait()

        for job in jobs:

            job()
            print("Result of program %s with job ID %s starting at %s is %s with stdout %s" % (
                evaluation, job.id, job.start_time, job.result, job.stdout))
            agent = filter(lambda x: x.id == job.id, agents)[0]
            agent.value = job.result

        agents = post_evaluation(agents)

        generation.bind_agents(agents)
        logger.log.info('\n' + str(generation))

        agents = selection(agents)
        agents = crossover(agents, population)
        agents = mutation(agents)

    cluster.stats()

    total_time = time.time() - start_time
    logger.log.info("Evolution finished in %s seconds " % total_time)
    print "Evolution finished in %s seconds " % total_time

    if config.grove_config['data']['collection_type']:

        getattr(utils, 'generate_' + config.grove_config['data']['collection_type'])(generations)
