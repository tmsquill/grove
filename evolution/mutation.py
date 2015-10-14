__author__ = 'Troy Squillaci'

import logging
import numpy as np
import random


def uniform(ga=None):
    """
    Uniform mutation replaces the value of the chosen gene with a uniform random value within the specified
    bounds of the gene.
    """

    for agent in ga.agents:

        for idx, param in enumerate(agent.params):

            if random.uniform(0.0, 1.0) <= ga.ga_descriptor.config['mutate']['uniform'][param]:

                val = random.uniform(
                    ga.ga_descriptor.config['mutate']['uniform']['lower_bounds'][param],
                    ga.ga_descriptor.config['mutate']['uniform']['upper_bounds'][param]
                )

                agent.params[idx] = val


def gaussian(ga=None):
    """
    Gaussian mutation adds a unit gaussian distributed value to the chosen gene. Bounds checking ensures
    the mutation does not violate legal ranges for the gene.
    """

    logging.info(' Gaussian Mutation '.center(180, '='))

    for a_idx, agent_set in enumerate(ga.agents):

        for agent in agent_set:

            logging.info('(Before) ' + str(agent))

            for idx, param in enumerate(agent.params):

                if random.uniform(0.0, 1.0) <= agent.params_mutational_probability[idx]:

                    val = np.random.normal(
                        loc=param,
                        scale=(0.05 * agent.params_upper_bounds[idx])
                    )

                    while val < agent.params_lower_bounds[idx] or val > agent.params_upper_bounds[idx]:

                        val = np.random.normal(
                            loc=param,
                            scale=(0.05 * agent.params_upper_bounds[idx])
                        )

                    logging.info('Mutating Parameter ' + str(idx) + ': ' + str(param) + ' -> ' + str(val))

                    agent.params[idx] = val

            logging.info('(After) ' + str(agent))

        ga.agents[a_idx] = agent_set
