import logging
import random


def truncation(elite_proportion=None):

    if not elite_proportion or elite_proportion < 0 or elite_proportion > 1:

        raise ValueError('invalid elite proportion specified for truncation selection closure')

    def _(agents):
        """
        Truncation selection orders agents of the population by fitness then chooses some proportion of the fittest
        agents for use in the reproduction phase.
        :param agents: The set of agents to perform selection on.
        :return: The updated set of agents after the selection process.
        """

        agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)

        logging.info(' Truncation Selection '.center(180, '='))

        logging.info(
            " (Before) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
        logging.info('\n' + '\n'.join(map(str, agents)) + '\n')

        agents = agents[:int(elite_proportion * len(agents))]

        logging.info(
            " (After) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
        logging.info('\n' + '\n'.join(map(str, agents)) + '\n')

        return agents

    return _


# TODO: Needs looked over, might have issues.
def tournament(size=None):

    if not size or size < 1:

        raise ValueError('invalid size specified for tournament selection closure')

    def _(agents):
        """
        Tournament selection involves holding several "tournaments" amongst randomly chosen subsets of agents in
        the population. Winners of the tournaments move on for use in the reproduction phase. Changing the
        tournament size effects selection pressure - that is the larger the tournament, the lesser a change weak
        agents will selected.
        :param agents: The set of agents to perform selection on.
        :return: The updated set of agents after the selection process.
        """

        fittest = None

        for x in xrange(size):

            agent = agents[random.randint(0, len(agents)) - 1]

            if fittest is None or agent.fitness > fittest.fitness:
                fittest = agent

        return agents

    return _


# TODO: Needs looked over, might have issues.
def roulette(sample=None, size=None):

    if not sample or sample < 1:

        raise ValueError('invalid sample specified for roulette selection closure')

    if not size or size < 1:

        raise ValueError('invalid size specified for roulette selection closure')

    def _(agents):
        """
        Roulette selection (stochastic acceptance version) involves using the fitness value to associate a probability
        with each agent. The higher the fitness value, the more likely it is to be selected for reproduction.
        :param agents: The set of agents to perform selection on.
        :return: The updated set of agents after the selection process.
        """

        agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)

        logging.info(' Roulette Selection '.center(180, '='))

        logging.info(
            " (Before) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents))
        )
        logging.info('\n' + '\n'.join(map(str, agents)) + '\n')

        agents_len = len(agents)
        hits = {_: 0 for _ in xrange(agents_len)}
        max = agents[0].fitness
        index = -1

        for i in xrange(sample):

            not_accepted = True

            while not_accepted:

                index = random.randint(0, agents_len)

                if random.uniform(0, 1) < agents[index] / max:

                    not_accepted = False

            hits[index] += 1

        hits = sorted(hits, key=lambda count: hits[idx], reverse=True)
        agents = [agent for (idx, agent) in sorted(zip(hits, agents))]

        logging.info(
            " (After) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents))
        )
        logging.info('\n' + '\n'.join(map(str, agents)) + '\n')

        return agents

    return _
