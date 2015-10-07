__author__ = 'Troy Squillaci'

import random


def truncation(ga=None):
    """
    Truncation selection orders agents of the population by fitness then chooses some proportion of the fittest
    agents for use in the reproduction phase.
    :return:
    """

    ga.agents = ga.agents[:ga.ga_descriptor.config['selection']['truncation']['elite_size']]
    ga.obs_agents = ga.obs_agents[:ga.ga_descriptor.config['selection']['truncation']['elite_size']]


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