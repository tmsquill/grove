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

    for agent in ga.agents:

        for idx, param in enumerate(agent.params):

            if random.uniform(0.0, 1.0) <= ga.ga_descriptor.config['mutate']['gaussian']['probability'][idx]:

                val = np.random.normal(
                    loc=param,
                    scale=(0.05 * ga.agent_descriptor.config['params_upper_bounds'][idx])
                )

                while ga.agent_descriptor.config['params_lower_bounds'][idx] < 0 or val > ga.agent_descriptor.config['params_upper_bounds'][idx]:

                    val = np.random.normal(
                        loc=param,
                        scale=(0.05 * ga.agent_descriptor.config['params_upper_bounds'][idx])
                    )

                agent.params[idx] = val

    for obs_agent in ga.obs_agents:

        for idx, param in enumerate(obs_agent.params):

            if random.uniform(0.0, 1.0) <= 0.10:

                val = np.random.normal(
                    loc=param,
                    scale=(0.05 * ga.agent_descriptor.config['obs_params_upper_bounds'][idx])
                )

                while abs(val) < ga.agent_descriptor.config['obs_params_lower_bounds'][idx] < 0 or abs(val) > ga.agent_descriptor.config['obs_params_upper_bounds'][idx]:

                    val = np.random.normal(
                        loc=param,
                        scale=(0.05 * ga.agent_descriptor.config['obs_params_upper_bounds'][idx])
                    )

                obs_agent.params[idx] = val
