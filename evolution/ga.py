import atexit
import dispy
import numpy
import os
import subprocess
import time
import utils

from generation import Generation
from grove import config, logger
from tabulate import tabulate


dispynode = None


def exit_handler():

    if dispynode:

        global dispynode
        dispynode.kill()
        dispynode.wait()

        print 'Closed all dispynode.py workers.'

atexit.register(exit_handler)


def evolve(population_size, generations, repeats, agent_func, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation, nodes, depends, debug):

    """
    Performs evolution on a set of agents over a number of generations. The desired evolutionary functions must be
    specified by the caller. Logging is optional.
    :param population_size: The desired population size.
    :param generations: The number of generation to evolve.
    :param repeats: The number of evaluations to perform on an individual agent.
    :param agent_func: Function used to initialize a population of agents.
    :param pre_evaluation: The pre-evaluation function. Intended to prepare agents for evaluation.
    :param evaluation: The evaluation function.
    :param post_evaluation: The post-evaluation function. Intended to gather data or alter agents after evaluation.
    :param selection: The selection function.
    :param crossover: The crossover function.
    :param mutation: The mutation function.
    :param nodes: The nodes in the cluster used for computing the evaluation function.
    :param depends: The list of dependencies needed by dispynodes to perform computation of the evaluation function.
    :param debug: Boolean for toggling debugging for distributed computation.
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
        generations = [Generation() for _ in xrange(generations)]

        # Initialize agents.
        agents = agent_func(population_size)

        logger.log.info('\n' + ' Agent Initialization '.center(180, '=') + '\n')
        logger.log.info('\n'.join(map(str, agents)))

        # Start Distributed Evolution
        logger.log.info('\n' + ' Evolution '.center(180, '=') + '\n')
        print ' Evolution '.center(180, '=') + '\n'

        # Start the dispynode.py workers.
        if not nodes or '127.0.0.1' in nodes:

            FNULL = open(os.devnull, 'w')
            global dispynode
            dispynode = subprocess.Popen('dispynode.py', stdout=FNULL, stderr=subprocess.STDOUT)

        # Configure the cluster.
        if isinstance(evaluation, basestring) or hasattr(evaluation, '__call__'):

            if debug:

                cluster = dispy.JobCluster(evaluation, nodes=nodes, depends=depends, loglevel=10)

            else:

                cluster = dispy.JobCluster(evaluation, nodes=nodes, depends=depends)

        else:

            raise TypeError('evaluation is not a callable or a string to an executable', evaluation)

        start_time = time.time()

        # Begin evolution.
        for generation in generations:

            logger.log.info(" Generation %s ".center(180, '*') % str(generation.id))
            print 'Generation ' + str(generation.id)

            agents = pre_evaluation(agents)

            for agent in agents:

                agent.jobs = []

                for repeat in xrange(repeats):

                    job = cluster.submit(agent.payload)
                    job.id = str(agent.id) + '-' + str(repeat)
                    agent.jobs.append(job)

            cluster.wait()

            for agent in agents:

                for job in agent.jobs:

                    job()

                    if job.exception:

                        print job.exception
                        exit()

                    agent.random_seed = job.result['random_seed']
                    agent.value = numpy.mean([job.result['value'] for job in agent.jobs])

            headers = ['Job ID', 'Job Time', 'IP Address', 'Job Result', 'Job Exception', 'Job Stderr', 'Job Stdout']
            table = [[job.id, job.end_time - job.start_time, job.ip_addr, job.result, job.exception, job.stderr, job.stdout] for agent in agents for job in agent.jobs]

            print tabulate(table, headers, tablefmt="orgtbl")

            agents = post_evaluation(agents)

            generation.bind_agents(agents)
            logger.log.info('\n' + str(generation))

            agents = selection(agents)
            agents = crossover(agents, population_size)
            agents = mutation(agents)

        # Report information about the cluster.
        cluster.stats()

        # Save the data generated by the evolutionary run.
        if config.grove_config['data']['collection_type']:

            getattr(utils, 'generate_' + config.grove_config['data']['collection_type'])(generations)

        # Report evolution time.
        total_time = time.time() - start_time
        logger.log.info("Evolution finished in %s seconds " % total_time)
        print "Evolution finished in %s seconds " % total_time
