__author__ = 'Troy Squillaci'

import logging
import multiprocessing
import random
import time

import config
from generation import Generation
import agent
import utils


class GeneticAlgorithm:

    def __init__(self, evolution_sequence=None):

        # Initialize Logging
        now = time.strftime("%I:%M-D%dM%mY%Y")
        logging.basicConfig(filename=config.global_config['ga']['log'] + '/' + now + '.log', level=logging.DEBUG)
        logging.info(' Log for py.evolve '.center(180, '='))

        # Log Configurations
        for configuration in config.global_config:

            logging.info((configuration['name'] + ' Configuration ').center(180, '-'))
            logging.info('\n' + config.pretty_config(configuration))

        # Initialize Generations
        self.generations = [Generation() for sentinel in xrange(config.global_config['ga']['general']['generations'])]

        # Initialize Agents
        self.all_agents = agent.init_agents(config.global_config['ga']['general']['population'])
        self.active_agents = None

        logging.info(' Agent Initialization '.center(180, '='))

        for agent_set in self.all_agents:
            logging.info('\n' + '\n'.join(map(str, agent_set)))

        # Proxy defines functions that drive the evolutionary process.
        self.evolution_sequence = evolution_sequence

        # Multi-processing
        self.pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    def evolve(self):

        logging.info(' Evolution '.center(180, '=') + '\n')

        start_time = time.time()

        for generation in self.generations:

            logging.info(" Generation %s ".center(180, '*') % str(generation.id))
            print 'Generation ' + str(generation.id)

            for function in self.evolution_sequence:

                function()

            generation.bind_agents(self.all_agents)
            logging.info('\n' + str(generation))

            for idx, agent_set in enumerate(self.all_agents):

                self.active_agents = agent_set
                random.choice(self.proxies).selection(self)
                random.choice(self.proxies).crossover(self)
                random.choice(self.proxies).mutation(self)

        logging.info("Evolution finished in %s seconds " % (time.time() - start_time))
        print "Evolution finished in %s seconds " % (time.time() - start_time)

        utils.generate_csv(self.generations)


