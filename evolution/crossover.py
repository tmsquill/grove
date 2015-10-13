__author__ = 'Troy Squillaci'

import logging
import random


def one_point(ga=None):
    """
    One-point crossover involves generating a random index in the each of the parents' genome sequences.
    Then offspring are created by combining the first slice of the first parent with the second slice of the
    second parent (or vice versa).
    :return:
    """

    logging.info(' One-Point Crossover '.center(180, '='))

    for agent_set in ga.agents:

        offspring = []

        for sentinel in xrange((ga.config['general']['population'] - len(agent_set)) / 2):

            parent1 = random.choice(ga.agents)
            parent2 = random.choice(ga.agents)

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

        agent_set.extend(offspring)


def two_point(ga=None):
    """
    Two-point crossover is essentially the same as one-point crossover, but with two slicings of the parent
    genome sequences.
    :return:
    """

    tmp = []
    params_len = ga.agent_descriptor.config['params_len']

    for x in xrange((ga.ga_descriptor.config['general']['population'] - len(ga.agents)) / 2):

        parent1 = random.choice(ga.agents)
        parent2 = random.choice(ga.agents)

        logging.info('Parent 1: ' + str(parent1))
        logging.info('Parent 2: ' + str(parent2))

        child1 = ga.agent_descriptor.factory()
        child2 = ga.agent_descriptor.factory()

        split1 = random.randint(0, params_len - 1)
        split2 = random.randint(0, params_len - 1)

        logging.info('(1) Split: ' + str(split1))
        logging.info('(2) Split: ' + str(split2))

        child1.params[1:split1] = parent1.params[1:split1]
        child1.params[split1:split2] = parent2.params[split1:split2]
        child1.params[split2:len(ga.agents[0].params)] = parent1.params[split2:params_len - 1]

        child2.params[1:split1] = parent2.params[1:split1]
        child2.params[split1:split2] = parent1.params[split1:split2]
        child2.params[split2:len(ga.agents[0].params)] = parent2.params[split2:params_len - 1]

        logging.info('Child 1: ' + str(child1))
        logging.info('Child 2: ' + str(child2) + '\n')

        tmp.append(child1)
        tmp.append(child2)

    ga.agents.extend(tmp)


def uniform(ga=None):
    """
    Uniform crossover uses a fixed mixing ratio between two parents to form offspring.
    """

    tmp = []

    for x in xrange((ga.ga_descriptor.config['general']['population'] - len(ga.agents)) / 2):

        parent1 = random.choice(ga.agents)
        parent2 = random.choice(ga.agents)

        logging.info('Parent 1: ' + str(parent1))
        logging.info('Parent 2: ' + str(parent2))

        child1 = ga.agent_descriptor.factory()
        child2 = ga.agent_descriptor.factory()

        for param in xrange(ga.agent_descriptor.params_len):

            if bool(random.getrandbits(1)):

                child1.params[param] = parent1.params[param]
                child2.params[param] = parent2.params[param]

            else:

                child1.params[param] = parent2.params[param]
                child2.params[param] = parent1.params[param]

        logging.info('Child 1: ' + str(child1))
        logging.info('Child 2: ' + str(child2) + '\n')

        tmp.append(child1)
        tmp.append(child2)

    ga.agents.extend(tmp)
