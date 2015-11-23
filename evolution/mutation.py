import logging
import numpy as np
import random


def boundary(agents):
    """
    Boundary mutation replaces chosen genes within the genome with either lower or upper bounds for each respective
    gene.
    """

    logging.info(' Boundary Mutation '.center(180, '='))

    for agent in agents:

        logging.info('(Before) ' + str(agent))

        for idx, param in enumerate(agent.params):

            if random.uniform(0.0, 1.0) <= agent.params_mutational_probability[idx]:

                agent.params[idx] = random.choice([agent.params_lower_bounds[idx], agent.params_upper_bounds[idx]])

        logging.info('(After) ' + str(agent))

    return agents


def uniform(agents):
    """
    Uniform mutation replaces the value of the chosen gene with a uniform random value within the specified
    bounds of the gene.
    """

    logging.info(' Uniform Mutation '.center(180, '='))

    for agent in agents:

        logging.info('(Before) ' + str(agent))

        for idx, param in enumerate(agent.params):

            if random.uniform(0.0, 1.0) <= agent.params_mutational_probability[idx]:

                agent.params[idx] = random.uniform(agent.params_lower_bounds[idx], agent.params_upper_bounds[idx])

        logging.info('(After) ' + str(agent))

    return agents


def gaussian(agents):
    """
    Gaussian mutation adds a unit gaussian distributed value to the chosen gene. Bounds checking ensures
    the mutation does not violate legal ranges for the gene.
    """

    logging.info(' Gaussian Mutation '.center(180, '='))

    for agent in agents:

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

    return agents
