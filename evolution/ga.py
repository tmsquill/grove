import config
import dispy
import time
import utils

from generation import Generation

log = None


def evolve(population, generations, agent_type, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation, nodes, depends, logger):

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
    :param nodes: The nodes in the cluster used for computing the evaluation function.
    :param depends: The list of dependencies needed by dispynodes to perform computation of the evaluation function.
    :param logger: The logger object.
    """

    global log
    log = logger

    # Log Configuration
    log.info(config.pretty_config())

    # Validate pre and post evaluation functions.
    if not hasattr(pre_evaluation, '__call__'):

        raise ValueError('pre_evaluation_func is not callable', pre_evaluation)

    if not hasattr(post_evaluation, '__call__'):

        raise ValueError('post_evaluation_func is not callable', post_evaluation)

    # Initialize Generations.
    ga_generations = [Generation() for _ in xrange(generations)]

    # Initialize Agents.
    ga_agents = agent_type.init_agents(population)

    log.info(' Agent Initialization '.center(180, '='))
    log.info('\n' + '\n'.join(map(str, ga_agents)))

    if not nodes and not depends:

        serial(population, ga_generations, ga_agents, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation)

    else:

        distributed(population, ga_generations, ga_agents, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation, nodes, depends)


def serial(population, generations, agents, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation):

    log.info(' Evolution (Serial) '.center(180, '=') + '\n')
    print ' Evolution (Serial) '.center(180, '=') + '\n'

    start_time = time.time()

    for generation in generations:

        log.info(" Generation %s ".center(180, '*') % str(generation.id))
        print 'Generation ' + str(generation.id)

        agents = pre_evaluation(agents)

        for agent in agents:

            agent = evaluation(agent)

        agents = post_evaluation(agents)

        generation.bind_agents(agents)
        log.info('\n' + str(generation))

        agents = selection(agents)
        agents = crossover(agents, population)
        agents = mutation(agents)

    log.info("Evolution finished in %s seconds " % (time.time() - start_time))
    print "Evolution finished in %s seconds " % (time.time() - start_time)

    utils.generate_csv(generations)


def distributed(population, generations, agents, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation, nodes, depends):

    log.info(' Evolution (Distributed) '.center(180, '=') + '\n')
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

        log.info(" Generation %s ".center(180, '*') % str(generation.id))
        print 'Generation ' + str(generation.id)

        agents = pre_evaluation(agents)

        jobs = []

        for agent in agents:

            job = cluster.submit(agent)
            job.id = agent.id
            jobs.append(job)

        cluster.wait()

        for job in jobs:

            job()
            print("Result of program %s with job ID %s starting at %s is %s with stdout %s" % (
            evaluation, job.id, job.start_time, job.result, job.stdout))

        agents = post_evaluation(agents)

        generation.bind_agents(agents)
        log.info('\n' + str(generation))

        agents = selection(agents)
        agents = crossover(agents, population)
        agents = mutation(agents)

    cluster.stats()

    log.info("Evolution finished in %s seconds " % (time.time() - start_time))
    print "Evolution finished in %s seconds " % (time.time() - start_time)

    utils.generate_csv(generations)
