import random

from grove import config, logger
import numpy as np


def boundary():

    def _(agents):

        """
        Boundary mutation replaces chosen genes within the genome with either lower or upper bounds for each
        respective gene.
        :param agents: The set of agents to perform mutation on.
        :return: The updated set of agents with mutations.
        """

        log = config.grove_config['logging']['mutation']

        if log:

            logger.log.info(' Boundary Mutation '.center(180, '=') + '\n')

        for agent in agents:

            if log:

                logger.log.info('(Before) ' + str(agent))

            for idx, param in enumerate(agent.genotype):

                if random.uniform(0.0, 1.0) <= agent.genotype_mp[idx]:

                    agent.genotype[idx] = random.choice([agent.genotype_lb[idx], agent.genotype_ub[idx]])

            if log:

                logger.log.info('(After) ' + str(agent) + '\n')

        return agents

    return _


def uniform():

    def _(agents):

        """
        Uniform mutation replaces the value of the chosen gene with a uniform random value within the specified
        bounds of the gene.
        :param agents: The set of agents to perform mutation on.
        :return: The updated set of agents with mutations.
        """

        log = config.grove_config['logging']['mutation']

        if log:

            logger.log.info(' Uniform Mutation '.center(180, '=') + '\n')

        for agent in agents:

            if log:

                logger.log.info('(Before) ' + str(agent))

            for idx, param in enumerate(agent.genotype):

                if random.uniform(0.0, 1.0) <= agent.genotype_mp[idx]:

                    agent.genotype[idx] = random.uniform(agent.genotype_lb[idx], agent.genotype_ub[idx])

                    if isinstance(param, int):

                        agent.genotype[idx] = int(round(agent.genotype[idx]))

            if log:

                logger.log.info('(After) ' + str(agent) + '\n')

        return agents

    return _


def gaussian():

    def _(agents):

        """
        Gaussian mutation adds a unit gaussian distributed value to the chosen gene. Bounds checking ensures
        the mutation does not violate legal ranges for the gene.
        :param agents: The set of agents to perform mutation on.
        :return: The updated set of agents with mutations.
        """

        log = config.grove_config['logging']['mutation']

        if log:

            logger.log.info(' Gaussian Mutation '.center(180, '=') + '\n')

        for agent in agents:

            if log:

                logger.log.info('(Before) ' + str(agent))

            for idx, param in enumerate(agent.genotype):

                if random.uniform(0.0, 1.0) <= agent.genotype_mp[idx]:

                    val = np.random.normal(loc=param, scale=(0.05 * agent.genotype_ub[idx]))

                    if isinstance(param, int):

                        val = int(round(val))

                    while val < agent.genotype_lb[idx] or val > agent.genotype_ub[idx]:

                        val = np.random.normal(loc=param, scale=(0.05 * agent.genotype_ub[idx]))

                        if isinstance(param, int):

                            val = int(round(val))

                    if log:

                        logger.log.info('Mutating Parameter ' + str(idx) + ': ' + str(param) + ' -> ' + str(val))

                    agent.genotype[idx] = val

            if log:

                logger.log.info('(After) ' + str(agent) + '\n')

        return agents

    return _
