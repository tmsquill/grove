__author__ = 'Troy Squillaci'

from genalg import GeneticAlgorithm, GeneticAlgorithmDescriptor
from argos import ARGoSAgentDescriptor

if __name__ == "__main__":

    agent_descriptor = ARGoSAgentDescriptor('./experiments/iAnt_mac.argos')

    ga = GeneticAlgorithm(
        ga_descriptor=GeneticAlgorithmDescriptor(),
        agent_descriptor=agent_descriptor
    )

    ga.evolve()
