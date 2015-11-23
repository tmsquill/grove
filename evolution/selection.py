import logging
import random


def truncation(agents, proportion=0.2):
    """
    Truncation selection orders agents of the population by fitness then chooses some proportion of the fittest
    agents for use in the reproduction phase.
    :return:
    """

    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)

    logging.info(' Truncation Selection '.center(180, '='))

    logging.info(" (Before) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
    logging.info('\n' + '\n'.join(map(str, agents)) + '\n')

    agents = agents[:int(proportion * len(agents))]

    logging.info(" (After) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
    logging.info('\n' + '\n'.join(map(str, agents)) + '\n')

    return agents


# TODO: Default for size variable (consider a proportion of population).
def tournament(agents, size=None):
    """
    Tournament selection involves holding several "tournaments" amongst randomly chosen subsets of agents in
    the population. Winners of the tournaments move on for use in the reproduction phase. Changing the
    tournament size effects selection pressure - that is the larger the tournament, the lesser a change weak
    agents will selected.
    :return:
    """

    fittest = None

    for x in xrange(size):

        agent = agents[random.randint(0, len(agents)) - 1]

        if fittest is None or agent.fitness > fittest.fitness:

            fittest = agent

    return agents
