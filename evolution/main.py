__author__ = 'Troy Squillaci'

from genalg import GeneticAlgorithm, GeneticAlgorithmDescriptor
from argos import ARGoSAgentDescriptor

import os


if __name__ == "__main__":

    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')
    agent_descriptor = ARGoSAgentDescriptor('./experiments/iAnt.xml')

    ga = GeneticAlgorithm(ga_descriptor=GeneticAlgorithmDescriptor(), agent_descriptor=agent_descriptor)

    ga.evolve()
