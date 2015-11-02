__author__ = 'Troy Squillaci'

import logging
import random

import config


# TODO Alternative access to config.
def one_point(self, ga=None):
    """
    One-point crossover involves generating a random index in the each of the parents' genome sequences.
    Then offspring are created by combining the first slice of the first parent with the second slice of the
    second parent (or vice versa).
    :return:
    """

    logging.info(' One-Point Crossover '.center(180, '='))

    for idx, agent_set in enumerate(ga.agents):

        logging.info(" {0} ".center(180, '-').format(agent_set[0].__class__.__name__))

        offspring = []

        for sentinel in xrange((config.global_config['ga']['general']['population'] - len(agent_set)) / 2):

            parent1 = random.choice(agent_set)
            parent2 = random.choice(agent_set)

            logging.info('Parent 1: ' + str(parent1))
            logging.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__.factory()
            child2 = parent2.__class__.factory()

            split = random.randint(0, parent1.params_len - 1)

            logging.info('Split: ' + str(split))

            child1.params[0:split] = parent1.params[0:split]
            child1.params[split:parent1.params_len] = parent2.params[split:parent1.params_len]

            child2.params[0:split] = parent2.params[0:split]
            child2.params[split:parent1.params_len] = parent1.params[split:parent1.params_len]

            logging.info('Child 1: ' + str(child1))
            logging.info('Child 2: ' + str(child2) + '\n')

            offspring.append(child1)
            offspring.append(child2)

        ga.agents[idx].extend(offspring)


# TODO Alternative access to config.
def two_point(self, ga=None):
    """
    Two-point crossover is essentially the same as one-point crossover, but with two slices of the parent
    genome sequences.
    :return:
    """

    logging.info(' Two-Point Crossover '.center(180, '='))

    for idx, agent_set in enumerate(ga.agents):

        logging.info(" {0} ".center(180, '-').format(agent_set[0].__class__.__name__))

        offspring = []

        for sentinel in xrange((config.global_config['ga']['general']['population'] - len(agent_set)) / 2):

            parent1 = random.choice(agent_set)
            parent2 = random.choice(agent_set)

            logging.info('Parent 1: ' + str(parent1))
            logging.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__.factory()
            child2 = parent2.__class__.factory()

            split1 = random.randint(0, parent1.params_len - 1)
            split2 = random.randint(0, parent1.params_len - 1)

            logging.info('(1) Split: ' + str(split1))
            logging.info('(2) Split: ' + str(split2))

            child1.params[1:split1] = parent1.params[1:split1]
            child1.params[split1:split2] = parent2.params[split1:split2]
            child1.params[split2:len(ga.agents[0].params)] = parent1.params[split2:parent1.params_len - 1]

            child2.params[1:split1] = parent2.params[1:split1]
            child2.params[split1:split2] = parent1.params[split1:split2]
            child2.params[split2:len(ga.agents[0].params)] = parent2.params[split2:parent1.params_len - 1]

            logging.info('Child 1: ' + str(child1))
            logging.info('Child 2: ' + str(child2) + '\n')

            offspring.append(child1)
            offspring.append(child2)

        ga.agents[idx].extend(offspring)


# TODO Alternative access to config.
def uniform(self, ga=None):
    """
    Uniform crossover uses a fixed mixing ratio between two parents to form offspring.
    """

    logging.info(' Uniform Crossover '.center(180, '='))

    for idx, agent_set in enumerate(ga.agents):

        logging.info(" {0} ".center(180, '-').format(agent_set[0].__class__.__name__))

        offspring = []

        for sentinel in xrange((config.global_config['ga']['general']['population'] - len(agent_set)) / 2):

            parent1 = random.choice(agent_set)
            parent2 = random.choice(agent_set)

            logging.info('Parent 1: ' + str(parent1))
            logging.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__.factory()
            child2 = parent1.__class__.factory()

            for i in xrange(parent1.params_len):

                if bool(random.getrandbits(1)):

                    child1.params[i] = parent1.params[i]
                    child2.params[i] = parent2.params[i]

                else:

                    child1.params[i] = parent2.params[i]
                    child2.params[i] = parent1.params[i]

            logging.info('Child 1: ' + str(child1))
            logging.info('Child 2: ' + str(child2) + '\n')

            offspring.append(child1)
            offspring.append(child2)

        ga.agents[idx].extend(offspring)
