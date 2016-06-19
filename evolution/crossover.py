import ga
import random

from grove import config


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

            ga.log.info(' One-Point Crossover '.center(180, '=') + '\n')

        offspring = []

        for _ in xrange((population - len(agents)) / 2):

            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            if log:

                ga.log.info('Parent 1: ' + str(parent1))
                ga.log.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__()
            child2 = parent2.__class__()

            split = random.randint(0, parent1.genotype_len - 1)

            if log:

                ga.log.info('Split: ' + str(split))

            child1.genotype[0:split] = parent1.genotype[0:split]
            child1.genotype[split:parent1.genotype_len] = parent2.genotype[split:parent1.genotype_len]

            child2.genotype[0:split] = parent2.genotype[0:split]
            child2.genotype[split:parent1.genotype_len] = parent1.genotype[split:parent1.genotype_len]

            if log:

                ga.log.info('Child 1: ' + str(child1))
                ga.log.info('Child 2: ' + str(child2) + '\n')

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

            ga.log.info(' Two-Point Crossover '.center(180, '=') + '\n')

        offspring = []

        for _ in xrange((population - len(agents)) / 2):

            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            if log:

                ga.log.info('Parent 1: ' + str(parent1))
                ga.log.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__()
            child2 = parent2.__class__()

            split1 = random.randint(0, parent1.genotype_len - 1)
            split2 = random.randint(0, parent1.genotype_len - 1)

            if log:

                ga.log.info('(1) Split: ' + str(split1))
                ga.log.info('(2) Split: ' + str(split2))

            child1.genotype[1:split1] = parent1.genotype[1:split1]
            child1.genotype[split1:split2] = parent2.genotype[split1:split2]
            child1.genotype[split2:len(agents[0].genotype)] = parent1.genotype[split2:parent1.genotype_len - 1]

            child2.genotype[1:split1] = parent2.genotype[1:split1]
            child2.genotype[split1:split2] = parent1.genotype[split1:split2]
            child2.genotype[split2:len(agents[0].genotype)] = parent2.genotype[split2:parent1.genotype_len - 1]

            if log:

                ga.log.info('Child 1: ' + str(child1))
                ga.log.info('Child 2: ' + str(child2) + '\n')

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

            ga.log.info(' Uniform Crossover '.center(180, '=') + '\n')

        offspring = []

        for _ in xrange((population - len(agents)) / 2):

            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            if log:

                ga.log.info('Parent 1: ' + str(parent1))
                ga.log.info('Parent 2: ' + str(parent2))

            child1 = parent1.__class__()
            child2 = parent1.__class__()

            for i in xrange(parent1.genotype_len):

                if bool(random.getrandbits(1)):

                    child1.genotype[i] = parent1.genotype[i]
                    child2.genotype[i] = parent2.genotype[i]

                else:

                    child1.genotype[i] = parent2.genotype[i]
                    child2.genotype[i] = parent1.genotype[i]

            if log:

                ga.log.info('Child 1: ' + str(child1))
                ga.log.info('Child 2: ' + str(child2) + '\n')

            offspring.append(child1)
            offspring.append(child2)

        agents.extend(offspring)

        return agents

    return _
