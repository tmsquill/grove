import random

from grove import config, logger


def one_point():

    def _(agents=None, population=None):

        """
        One-point crossover involves generating a random index in the each of the parents' genome sequences.
        Then offspring are created by combining the first slice of the first parent with the second slice of the
        second parent (or vice versa).
        :param agents: The set of agents to perform crossover on.
        :param population: The population size.
        :return: The updated set of agents with new offspring.
        """

        log = config.grove_config['logging']['crossover']

        if log:

            logger.log.info(' One-Point Crossover '.center(120, '=') + '\n')

        offspring = []

        for _ in xrange((population - len(agents)) / 2):

            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            if log:

                logger.log.info('Parent 1: ' + str(parent1))
                logger.log.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__()
            child2 = parent2.__class__()

            split = random.randint(0, parent1.genome_len - 1)

            if log:

                logger.log.info('Split: ' + str(split))

            child1.genome[0:split] = parent1.genome[0:split]
            child1.genome[split:parent1.genome_len] = parent2.genome[split:parent1.genome_len]

            child2.genome[0:split] = parent2.genome[0:split]
            child2.genome[split:parent1.genome_len] = parent1.genome[split:parent1.genome_len]

            if log:

                logger.log.info('Child 1: ' + str(child1))
                logger.log.info('Child 2: ' + str(child2) + '\n')

            offspring.append(child1)
            offspring.append(child2)

        agents.extend(offspring)

        return agents

    return _


def two_point():

    def _(agents=None, population=None):

        """
        Two-point crossover is essentially the same as one-point crossover, but with two slices of the parent
        genome sequences.
        :param agents: The set of agents to perform crossover on.
        :param population: The population size.
        :return: The updated set of agents with new offspring.
        """

        log = config.grove_config['logging']['crossover']

        if log:

            logger.log.info(' Two-Point Crossover '.center(120, '=') + '\n')

        offspring = []

        for _ in xrange((population - len(agents)) / 2):

            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            if log:

                logger.log.info('Parent 1: ' + str(parent1))
                logger.log.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__()
            child2 = parent2.__class__()

            split1 = random.randint(0, parent1.genome_len - 1)
            split2 = random.randint(0, parent1.genome_len - 1)

            if log:

                logger.log.info('(1) Split: ' + str(split1))
                logger.log.info('(2) Split: ' + str(split2))

            child1.genome[1:split1] = parent1.genome[1:split1]
            child1.genome[split1:split2] = parent2.genome[split1:split2]
            child1.genome[split2:len(agents[0].genome)] = parent1.genome[split2:parent1.genome_len - 1]

            child2.genome[1:split1] = parent2.genome[1:split1]
            child2.genome[split1:split2] = parent1.genome[split1:split2]
            child2.genome[split2:len(agents[0].genome)] = parent2.genome[split2:parent1.genome_len - 1]

            if log:

                logger.log.info('Child 1: ' + str(child1))
                logger.log.info('Child 2: ' + str(child2) + '\n')

            offspring.append(child1)
            offspring.append(child2)

        agents.extend(offspring)

        return agents

    return _


def uniform():

    def _(agents=None, population=None):

        """
        Uniform crossover uses a fixed mixing ratio between two parents to form offspring.
        :param agents: The set of agents to perform crossover on.
        :param population: The population size.
        :return: The updated set of agents with new offspring.
        """

        log = config.grove_config['logging']['crossover']

        if log:

            logger.log.info(' Uniform Crossover '.center(120, '=') + '\n')

        offspring = []

        for _ in xrange((population - len(agents)) / 2):

            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            if log:

                logger.log.info('Parent 1: ' + str(parent1))
                logger.log.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__()
            child2 = parent1.__class__()

            for i in xrange(parent1.genome_len):

                if bool(random.getrandbits(1)):

                    child1.genome[i] = parent1.genome[i]
                    child2.genome[i] = parent2.genome[i]

                else:

                    child1.genome[i] = parent2.genome[i]
                    child2.genome[i] = parent1.genome[i]

            if log:

                logger.log.info('Child 1: ' + str(child1))
                logger.log.info('Child 2: ' + str(child2) + '\n')

            offspring.append(child1)
            offspring.append(child2)

        agents.extend(offspring)

        return agents

    return _
