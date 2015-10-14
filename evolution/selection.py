__author__ = 'Troy Squillaci'

import logging
import random


def truncation(ga=None, proportion=0.2):
    """
    Truncation selection orders agents of the population by fitness then chooses some proportion of the fittest
    agents for use in the reproduction phase.
    :return:
    """

    logging.info(' Truncation Selection '.center(180, '='))

    for agent_set in ga.agents:

        logging.info(" (Before) {0} Population Size {1} ".center(180, '-').format(agent_set[0].__class__.__name__, len(agent_set)))
        logging.info('\n' + '\n'.join(map(str, agent_set)) + '\n')

    ga.agents = [agent_set[:int(proportion * len(agent_set))] for agent_set in ga.agents]

    for agent_set in ga.agents:

        logging.info(" (After) {0} Population Size {1} ".center(180, '-').format(agent_set[0].__class__.__name__, len(agent_set)))
        logging.info('\n' + '\n'.join(map(str, agent_set)) + '\n')


def tournament(ga=None):
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