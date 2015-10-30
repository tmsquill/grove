__author__ = 'Troy Squillaci'

import logging
import random


def truncation(self, ga=None, proportion=0.2):
    """
    Truncation selection orders agents of the population by fitness then chooses some proportion of the fittest
    agents for use in the reproduction phase.
    :return:
    """

    logging.info(' Truncation Selection '.center(180, '='))

    logging.info(" (Before) {0} Population Size {1} ".center(180, '-').format(ga.active_agents[0].__class__.__name__, len(ga.active_agents)))
    logging.info('\n' + '\n'.join(map(str, ga.active_agents)) + '\n')

    ga.active_agents = ga.active_agents[:int(proportion * len(ga.active_agents))]

    logging.info(" (After) {0} Population Size {1} ".center(180, '-').format(ga.active_agents[0].__class__.__name__, len(ga.active_agents)))
    logging.info('\n' + '\n'.join(map(str, ga.active_agents)) + '\n')


def tournament(self, ga=None):
    """
    Tournament selection involves holding several "tournaments" amongst randomly chosen subsets of agents in
    the population. Winners of the tournaments move on for use in the reproduction phase. Changing the
    tournament size effects selection pressure - that is the larger the tournament, the lesser a change weak
    agents will selected.
    :return:
    """

    fittest = None

    for x in xrange(ga.ga_descriptor['selection']['tournament']['size']):

        agent = ga.agents[random.randint(0, ga.agent_descriptor.general['population']) - 1]

        if fittest is None or agent.fitness > fittest.fitness:

            fittest = agent