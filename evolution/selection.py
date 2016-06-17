import random
from operator import attrgetter

import ga
from grove import config


def truncation(elite_proportion=None):

    if not elite_proportion or elite_proportion < 0 or elite_proportion > 1:

        raise ValueError('invalid elite proportion specified for truncation selection closure', elite_proportion)

    def _(agents):

        """
        Truncation selection orders agents of the population by evaluation value then chooses some proportion of the
        highest performing agents for use in the reproduction phase.
        :param agents: The set of agents to perform selection on.
        :return: The updated set of agents after the selection process.
        """

        log = config.grove_config['logging']['selection']

        # Sort the agents from most to least fit.
        agents = sorted(agents, key=lambda agent: agent.value, reverse=True)

        if log:

            ga.log.info(' Truncation Selection '.center(180, '=') + '\n')
            ga.log.info(
                " (Before) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
            ga.log.info('\n' + '\n'.join(map(str, agents)) + '\n')

        # Use slicing to remove the non-elite.
        agents = agents[:int(elite_proportion * len(agents))]

        if log:

            ga.log.info(
            " (After) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
            ga.log.info('\n' + '\n'.join(map(str, agents)) + '\n')

        return agents

    return _


def tournament(agents_ret=None, tournament_size=None):

    if not agents_ret or agents_ret < 1:

        raise ValueError('invalid agent return size specified for tournament selection closure', tournament_size)

    if not tournament_size or tournament_size < 1:

        raise ValueError('invalid tournament size specified for tournament selection closure', tournament_size)

    def _(agents):

        """
        Tournament selection involves holding several "tournaments" amongst randomly chosen subsets of agents in
        the population. Winners of the tournaments move on for use in the reproduction phase. Changing the
        tournament size effects selection pressure - that is the larger the tournament, the lesser a change weak
        agents will selected.
        :param agents: The set of agents to perform selection on.
        :return: The updated set of agents after the selection process.
        """

        log = config.grove_config['logging']['selection']

        if log:

            ga.log.info(' Tournament Selection '.center(180, '=') + '\n')
            ga.log.info(
            " (Before) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
            ga.log.info('\n' + '\n'.join(map(str, agents)) + '\n')

        chosen = []

        for __ in xrange(agents_ret):

            participants = [random.choice(agents) for ___ in xrange(tournament_size)]
            chosen.append(max(participants, key=attrgetter('value')))

        if log:

            ga.log.info(
            " (After) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
            ga.log.info('\n' + '\n'.join(map(str, agents)) + '\n')

        return chosen

    return _


# TODO: Needs looked over, might have issues.
def roulette(sample=None, size=None):

    if not sample or sample < 1:

        raise ValueError('invalid sample specified for roulette selection closure', sample)

    if not size or size < 1:

        raise ValueError('invalid size specified for roulette selection closure', size)

    def _(agents):

        """
        Roulette selection (stochastic acceptance version) involves using the evaluation value to associate a
        probability with each agent. The higher the evaluation value, the more likely it is to be selected for
        reproduction.
        :param agents: The set of agents to perform selection on.
        :return: The updated set of agents after the selection process.
        """

        log = config.grove_config['logging']['selection']

        agents = sorted(agents, key=lambda agent: agent.value, reverse=True)

        if log:

            ga.log.info(' Roulette Selection '.center(180, '=') + '\n')
            ga.log.info(
            " (Before) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
            ga.log.info('\n' + '\n'.join(map(str, agents)) + '\n')

        agents_len = len(agents)
        hits = {_: 0 for _ in xrange(agents_len)}
        max = agents[0].value
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

        if log:

            ga.log.info(
            " (After) {0} Population Size {1} ".center(180, '-').format(agents[0].__class__.__name__, len(agents)))
            ga.log.info('\n' + '\n'.join(map(str, agents)) + '\n')

        return agents

    return _
