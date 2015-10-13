__author__ = 'Troy Squillaci'

import evolution.agent as agent
import evolution.ga as ga

import argparse
import json
import os

if __name__ == "__main__":

    # Change the current directory.
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='py.evolve')
    parser.add_argument('-agent_config', action="store", type=str, default='./experiments/agent.json')
    parser.add_argument('-ga_config', action="store", type=str, default='./experiments/ga.json')
    args = parser.parse_args()

    with open(args.agent_config, 'r') as config:
        agent.config = json.load(config)

    with open(args.ga_config, 'r') as config:
        ga.config = json.load(config)

    genetic_algorithm = ga.GeneticAlgorithm()
    genetic_algorithm.evolve()
