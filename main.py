__author__ = 'Troy Squillaci'

from evolution.ga import GeneticAlgorithm, GeneticAlgorithmDescriptor
from evolution.agent import AgentDescriptor
import argparse
import json
import os

if __name__ == "__main__":

    # Change directory to ARGoS.
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='py.evolve')
    parser.add_argument('-log', action="store", type=str, default='../log')
    parser.add_argument('-agent_config', action="store", type=str, default='./experiments/agentdescriptor.json')
    parser.add_argument('-ga_config', action="store", type=str, default='./experiments/gadescriptor.json')
    args = parser.parse_args()

    agent_descriptor = None
    ga_descriptor = None

    with open(args.agent_config, 'r') as config:
        agent_descriptor = AgentDescriptor(json.load(config))

    with open(args.ga_config, 'r') as config:
        ga_descriptor = GeneticAlgorithmDescriptor(json.load(config))

    ga = GeneticAlgorithm(ga_descriptor=ga_descriptor, agent_descriptor=agent_descriptor)
    ga.evolve()
