import atexit
import dispy
import dispy.httpd
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

        dispynode.kill()
        dispynode.wait()

        print 'Closed all dispynode.py workers.'

atexit.register(exit_handler)


def evolve(population_size, generations, repeats, depends, dest_path, setup, agent_func, pre_evaluation, evaluation, post_evaluation, selection, crossover, mutation, nodes, debug):

    """
    Performs evolution on a set of agents over a number of generations. The desired evolutionary functions must be
    specified by the caller. Logging is optional.
    :param population_size: The desired population size.
    :param generations: The number of generation to evolve.
    :param repeats: The number of evaluations to perform on an individual agent.
    :param depends: The dependencies needed by nodes for computation.
    :param dest_path: The path to the directory that will contain files needed for the computation on nodes.
    :param setup: The setup function that is executed on the nodes prior to evolution.
    :param agent_func: Function used to initialize a population of agents.
    :param pre_evaluation: The pre-evaluation function. Intended to prepare agents for evaluation.
    :param evaluation: The evaluation function.
    :param post_evaluation: The post-evaluation function. Intended to gather data or alter agents after evaluation.
    :param selection: The selection function.
    :param crossover: The crossover function.
    :param mutation: The mutation function.
    :param nodes: The nodes in the cluster used for computing the evaluation function.
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

        logger.log.info('\n' + ' Agent Initialization '.center(120, '=') + '\n')
        logger.log.info('\n'.join(map(str, agents)))

        # Start Distributed Evolution
        logger.log.info('\n' + ' Evolution '.center(120, '=') + '\n')
        print ' Evolution '.center(120, '=') + '\n'

        # Start the dispynode.py workers.
        if not nodes or '127.0.0.1' in nodes:

            FNULL = open(os.devnull, 'w')
            global dispynode
            dispynode = subprocess.Popen('dispynode.py', stdout=FNULL, stderr=subprocess.STDOUT)

        # Configure the cluster.
        if isinstance(evaluation, basestring) or hasattr(evaluation, '__call__'):

            if debug:

                cluster = dispy.JobCluster(evaluation, nodes=nodes, depends=depends, dest_path=dest_path, loglevel=10, setup=setup)

            else:

                cluster = dispy.JobCluster(evaluation, nodes=nodes, depends=depends, dest_path=dest_path, setup=setup)

        else:

            raise TypeError('evaluation is not a callable or a string to an executable', evaluation)

        # Start the HTTP server for cluster monitoring.
        http_server = dispy.httpd.DispyHTTPServer(cluster)

        start_time = time.time()

        # Begin evolution.
        for generation in generations:

            logger.log.info(" Generation %s ".center(120, '*') % str(generation.id))
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

                        print ' Traceback in Evaluation Function '.center(120, '=')
                        print job.exception
                        exit()

                    agent.random_seed = job.result['random_seed']
                    agent.value = numpy.mean([job.result['value'] for job in agent.jobs])

            headers = ['Job ID', 'Job Time', 'IP Address', 'Job Result', 'Job Stderr', 'Job Stdout']
            table = [[job.id, job.end_time - job.start_time, job.ip_addr, job.result, job.stderr, job.stdout] for agent in agents for job in agent.jobs]

            print tabulate(table, headers, tablefmt="orgtbl")

            agents = post_evaluation(agents)

            generation.bind_agents(agents)
            logger.log.info('\n' + str(generation))

            agents = selection(agents)
            agents = crossover(agents, population_size)
            agents = mutation(agents)

        # Report information about the cluster.
        cluster.stats()

        # Close the HTTP server and cluster.
        http_server.shutdown()
        cluster.close()

        collection_type = config.grove_config['data']['collection_type']

        # Save the data generated by the evolutionary run.
        if collection_type == 'mongo':

            if 'uri' in config.grove_config['data']['mongo']:

                utils.generate_mongo(generations=generations, uri=config.grove_config['data']['mongo']['uri'])

            elif 'host' in config.grove_config['data']['mongo'] and 'port' in config.grove_config['data']['mongo']:

                host = config.grove_config['data']['mongo']['host']
                port = config.grove_config['data']['mongo']['port']

                utils.generate_mongo(generations=generations, host=host, port=port)

            else:

                utils.generate_mongo(generations)

        elif collection_type is 'csv':

            utils.generate_csv(generations)

        # Report evolution time.
        total_time = time.time() - start_time
        logger.log.info("Evolution finished in %s seconds " % total_time)
        print "Evolution finished in %s seconds " % total_time
