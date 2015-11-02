__author__ = 'Troy Squillaci'

import argparse
import os
import re
import subprocess

import evolution.config as config
import evolution.ga as ga


if __name__ == "__main__":

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='py.evolve')
    parser.add_argument('-agent_config', action="store", type=str, default='./experiments/agent.json')
    parser.add_argument('-ga_config', action="store", type=str, default='./experiments/ga.json')
    args = parser.parse_args()

    # Load the configurations into memory (as dictionaries) by filename.
    config.load_configs([args.agent_config, args.ga_config])

    # Run the genetic algorithm.
    genetic_algorithm = ga.GeneticAlgorithm()
    genetic_algorithm.evolve()


# Domain-specific fitness function.
def fitness(self):

    results = [self.pool.apply_async(argos, args=(agent.config['argos_xml'][:-4] + '_' + str(number) + agent.config['argos_xml'][-4:], forager, obstacle)) for number, forager, obstacle in zip(list(xrange(config['general']['population'])), self.all_agents[0], self.all_agents[1])]

    output = [p.get() for p in results]

    self.all_agents[0] = [agent_out[0] for agent_out in output]
    self.all_agents[1] = [obs_agent_out[1] for obs_agent_out in output]


# Helper function for fitness function.
def argos(argos_xml=None, iant_agent=None, obs_agent=None):

    iant_agent.execute_fitness(argos_xml)
    obs_agent.execute_fitness(argos_xml)

    output = subprocess.check_output(['argos3 -n -c ' + argos_xml], shell=True, stderr=subprocess.STDOUT)
    result = re.search(r'\s(\d+),\s(\d+),\s(\d+)', output)
    iant_agent.fitness = float(float(result.group(1)) / 256)
    obs_agent.fitness = 1 - iant_agent.fitness

    return iant_agent, obs_agent