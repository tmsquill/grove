import logging
import random


def one_point(agents=None, population=None):
    """
    One-point crossover involves generating a random index in the each of the parents' genome sequences.
    Then offspring are created by combining the first slice of the first parent with the second slice of the
    second parent (or vice versa).
    :param agents: The set of agents to perform crossover on.
    :param population: The population size.
    :return: The updated set of agents with new offspring.
    """

    logging.info(' One-Point Crossover '.center(180, '='))

    offspring = []

    for _ in xrange((population - len(agents)) / 2):

        parent1 = random.choice(agents)
        parent2 = random.choice(agents)

        logging.info('Parent 1: ' + str(parent1))
        logging.info('Parent 2: ' + str(parent2))

        child1 = parent1.__class__.factory()
        child2 = parent2.__class__.factory()

        split = random.randint(0, parent1.genotype_len - 1)

        logging.info('Split: ' + str(split))

        child1.genotype[0:split] = parent1.genotype[0:split]
        child1.genotype[split:parent1.genotype_len] = parent2.genotype[split:parent1.genotype_len]

        child2.genotype[0:split] = parent2.genotype[0:split]
        child2.genotype[split:parent1.genotype_len] = parent1.genotype[split:parent1.genotype_len]

        logging.info('Child 1: ' + str(child1))
        logging.info('Child 2: ' + str(child2) + '\n')

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)

    return agents


def two_point(agents=None, population=None):
    """
    Two-point crossover is essentially the same as one-point crossover, but with two slices of the parent
    genome sequences.
    :param agents: The set of agents to perform crossover on.
    :param population: The population size.
    :return: The updated set of agents with new offspring.
    """

    logging.info(' Two-Point Crossover '.center(180, '='))

    offspring = []

    for _ in xrange((population - len(agents)) / 2):

        parent1 = random.choice(agents)
        parent2 = random.choice(agents)

        logging.info('Parent 1: ' + str(parent1))
        logging.info('Parent 2: ' + str(parent2))

        child1 = parent1.__class__.factory()
        child2 = parent2.__class__.factory()

        split1 = random.randint(0, parent1.genotype_len - 1)
        split2 = random.randint(0, parent1.genotype_len - 1)

        logging.info('(1) Split: ' + str(split1))
        logging.info('(2) Split: ' + str(split2))

        child1.genotype[1:split1] = parent1.genotype[1:split1]
        child1.genotype[split1:split2] = parent2.genotype[split1:split2]
        child1.genotype[split2:len(agents[0].genotype)] = parent1.genotype[split2:parent1.genotype_len - 1]

        child2.genotype[1:split1] = parent2.genotype[1:split1]
        child2.genotype[split1:split2] = parent1.genotype[split1:split2]
        child2.genotype[split2:len(agents[0].genotype)] = parent2.genotype[split2:parent1.genotype_len - 1]

        logging.info('Child 1: ' + str(child1))
        logging.info('Child 2: ' + str(child2) + '\n')

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)

    return agents


def uniform(agents=None, population=None):
    """
    Uniform crossover uses a fixed mixing ratio between two parents to form offspring.
    :param agents: The set of agents to perform crossover on.
    :param population: The population size.
    :return: The updated set of agents with new offspring.
    """

    logging.info(' Uniform Crossover '.center(180, '='))

    offspring = []

    for _ in xrange((population - len(agents)) / 2):

        parent1 = random.choice(agents)
        parent2 = random.choice(agents)

        logging.info('Parent 1: ' + str(parent1))
        logging.info('Parent 2: ' + str(parent2))

        child1 = parent1.__class__.factory()
        child2 = parent1.__class__.factory()

        for i in xrange(parent1.genotype_len):

            if bool(random.getrandbits(1)):

                child1.genotype[i] = parent1.genotype[i]
                child2.genotype[i] = parent2.genotype[i]

            else:

                child1.genotype[i] = parent2.genotype[i]
                child2.genotype[i] = parent1.genotype[i]

        logging.info('Child 1: ' + str(child1))
        logging.info('Child 2: ' + str(child2) + '\n')

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)

    return agents
