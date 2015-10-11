__author__ = 'Troy Squillaci'

from generation import Generation
from visualization import Visualization

import crossover
import mutation
import selection

import json
import logging
import multiprocessing
import re
import subprocess
import time


def argos(argos_xml=None, agent=None, obs_agent=None):
    agent.update_xml(argos_xml)
    obs_agent.update_xml(argos_xml)

    output = subprocess.check_output(['argos3 -n -c ' + argos_xml], shell=True, stderr=subprocess.STDOUT)
    result = re.search(r'\s(\d+),\s(\d+),\s(\d+)', output)
    agent.fitness = float(float(result.group(1)) / 256)
    obs_agent.fitness = 1 - agent.fitness

    return agent, obs_agent


class GeneticAlgorithmDescriptor:
    def __init__(self, config=None):
        if config is None:
            raise Exception

        self.config = config

    def __str__(self):
        return json.dumps(self.config, sort_keys=True, indent=4)


class GeneticAlgorithm:
    def __init__(self, agent_descriptor=None, ga_descriptor=None):
        # Logging
        now = time.strftime("%I:%M-D%dM%mY%Y")
        logging.basicConfig(filename=now + '.log', level=logging.DEBUG)
        logging.info(' GW2 Evolution Log '.center(180, '='))

        # Multi-processing
        self.pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        # GA Initialization
        self.agent_descriptor = agent_descriptor
        self.ga_descriptor = ga_descriptor

        logging.info(' Agent Descriptor '.center(180, '-'))
        logging.info('\n' + str(self.agent_descriptor))
        logging.info(' GA Descriptor '.center(180, '-'))
        logging.info('\n' + str(self.ga_descriptor))

        self.generations = [Generation() for x in xrange(self.ga_descriptor.config['general']['generations'])]
        self.agents, self.obs_agents = agent_descriptor.init_agents(self.ga_descriptor.config['general']['population'])

        logging.info(' Agent Initialization '.center(180, '-'))
        logging.info('\n' + '\n'.join(map(str, self.agents)))

    def evolve(self):
        logging.info(' Evolution '.center(180, '-') + '\n')

        start_time = time.time()

        for generation in self.generations:
            logging.info(" Generation %s ".center(180, '-') % str(generation.id))

            self.fitness(generation)
            self.agents.sort()
            self.agents.reverse()
            self.obs_agents.sort()
            self.obs_agents.reverse()
            generation.generate_stats(self.agents, self.obs_agents)
            generation.bind_agents(self.agents, self.obs_agents)
            logging.info('\n' + str(generation))
            selection.truncation(self)
            crossover.one_point(self)
            mutation.gaussian(self)

        logging.info("Evolution finished in %s seconds " % (time.time() - start_time))
        print "Evolution finished in %s seconds " % (time.time() - start_time)

        # Apply Visualization
        show = [True] * 12
        show_obs = [True] * 12

        visual = Visualization(self.agent_descriptor, self.generations,
                               self.ga_descriptor.config['selection']['truncation']['elite_size'])
        visual.plot_elite('Min', show)
        visual.plot_elite('Max', show)
        visual.plot_elite('Mean', show)
        visual.plot_elite('Median', show)
        visual.plot_fitness()
        visual.plot_obs_elite('Min', show_obs)
        visual.plot_obs_elite('Max', show_obs)
        visual.plot_obs_elite('Mean', show_obs)
        visual.plot_obs_elite('Median', show_obs)
        visual.plot_obs_fitness()

    def fitness(self, generation):
        print (" Generation %s ".center(180, '-') % str(generation.id))

        results = [self.pool.apply_async(argos, args=(
            self.agent_descriptor.config['argos_xml'][:-4] + '_' + str(number) +
            self.agent_descriptor.config['argos_xml'][-4:], agent, obs_agent))
                   for number, agent, obs_agent in zip(list(xrange(40)), self.agents, self.obs_agents)]

        output = [p.get() for p in results]

        self.agents = [agent_out[0] for agent_out in output]
        self.obs_agents = [obs_agent_out[1] for obs_agent_out in output]
