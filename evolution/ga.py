__author__ = 'Troy Squillaci'

from generation import Generation

import agent
import crossover
import mutation
import selection
import visualization

import json
import logging
import multiprocessing
import re
import subprocess
import time


# TODO Move this.
def argos(argos_xml=None, agent=None, obs_agent=None):
    agent.execute_fitness(argos_xml)
    obs_agent.execute_fitness(argos_xml)

    output = subprocess.check_output(['argos3 -n -c ' + argos_xml], shell=True, stderr=subprocess.STDOUT)
    result = re.search(r'\s(\d+),\s(\d+),\s(\d+)', output)
    agent.fitness = float(float(result.group(1)) / 256)
    obs_agent.fitness = 1 - agent.fitness

    return agent, obs_agent


config = None


def pretty_config():

    return json.dumps(config, sort_keys=True, indent=4)


class GeneticAlgorithm:

    def __init__(self):

        # Logging
        now = time.strftime("%I:%M-D%dM%mY%Y")
        logging.basicConfig(filename=config['log'] + '/' + now + '.log', level=logging.DEBUG)
        logging.info(' Log for py.evolve '.center(180, '='))

        # Multi-processing
        self.pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        logging.info(' Agent Configuration '.center(180, '-'))
        logging.info('\n' + agent.pretty_config())
        logging.info(' GA Configuration '.center(180, '-'))
        logging.info('\n' + pretty_config())

        self.generations = [Generation() for sentinel in xrange(config['general']['generations'])]
        # TODO Consider Dynamic Injection
        self.agents = agent.init_agents(config['general']['population'])

        logging.info(' Agent Initialization '.center(180, '='))

        for agent_set in self.agents:
            logging.info('\n' + '\n'.join(map(str, agent_set)))

    def evolve(self):
        logging.info(' Evolution '.center(180, '=') + '\n')

        start_time = time.time()

        for generation in self.generations:
            logging.info(" Generation %s ".center(180, '*') % str(generation.id))
            print 'Generation ' + str(generation.id)

            self.fitness()

            for idx, agent_set in enumerate(self.agents):

                self.agents[idx].sort()
                self.agents[idx].reverse()

            generation.bind_agents(self.agents)
            logging.info('\n' + str(generation))
            selection.truncation(self)
            crossover.one_point(self, config)
            mutation.gaussian(self)

        logging.info("Evolution finished in %s seconds " % (time.time() - start_time))
        print "Evolution finished in %s seconds " % (time.time() - start_time)

        visualization.plot_fitness()

    def fitness(self):

        results = [self.pool.apply_async(
            argos,
            args=(agent.config['argos_xml'][:-4] + '_' + str(number) + agent.config['argos_xml'][-4:], forager, obstacle))
                   for number, forager, obstacle in zip(list(xrange(40)), self.agents[0], self.agents[1])]

        output = [p.get() for p in results]

        self.agents[0] = [agent_out[0] for agent_out in output]
        self.agents[1] = [obs_agent_out[1] for obs_agent_out in output]
