from argos import ARGoSAgent
from agent import Agent
from generation import Generation

import logging
import random
import numpy as np
import stats
import sys
import time


class GeneticAlgorithmDescriptor:

    def __init__(self):

        self.general = {
            'generations': 30,
        }

        self.selection = {
            'truncation': {
                'elite_size': 8,
            },
            'tournament': {
                'size': 10,
                'probability': 0.9
            }
        }

        self.mutate = {
            'uniform': {
                'probability': [],
                'lower_bounds': [],
                'upper_bounds': []
            },
            'gaussian': {
                'probability': {
                    0: 0.10,
                    1: 0.10,
                    2: 0.10,
                    3: 0.10,
                    4: 0.10,
                    5: 0.10,
                    6: 0.10,
                }
            }
        }


class GeneticAlgorithm:

    def __init__(self, ga_descriptor=None, agent_descriptor=None):

        now = time.strftime("%I:%M-D%dM%mY%Y")
        logging.basicConfig(filename=now + '.log', level=logging.DEBUG)
        logging.info(' GW2 Evolution Log '.center(120, '='))

        self.ga_descriptor = ga_descriptor
        self.agent_descriptor = agent_descriptor

        logging.info(' GA Descriptor '.center(120, '-'))
        logging.info('Generation Count: ' + str(self.ga_descriptor.general['generations']))

        logging.info(' Agent Descriptor '.center(120, '-'))

        self.generations = [Generation() for x in xrange(self.ga_descriptor.general['generations'])]
        self.agents = agent_descriptor.init_agents()

    def evolve(self):

        logging.info(' Evolution '.center(120, '-'))

        start_time = time.time()

        for generation in self.generations:

            logging.info(" Generation %s ".center(120, '-') % str(generation))

            self.fitness(generation)
            stats.report(self.agents, generation)
            self.selection('Truncation')()
            stats.report(self.agents, generation)
            self.crossover('One-Point')()
            self.mutate('Gaussian')()

        logging.info(" Finished in %s seconds ".center(120, '-') % (time.time() - start_time))

    def fitness(self, generation):
        # TODO Clean up
        progress = 0
        for agent in self.agents:

            agent.run()
            progress += 1
            percent = float(progress) / len(self.agents)
            hashes = '#' * int(round(percent * 120))
            spaces = ' ' * (120 - len(hashes))
            sys.stdout.write(("\rGeneration " + str(generation) + ": [{0}] {1}%").format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()

        print '\n'

    def selection(self, selection_type):

        def truncation():
            """
            Truncation selection orders agents of the population by fitness then chooses some proportion of the fittest
            agents for use in the reproduction phase.
            :return:
            """

            logging.info(' Truncation Selection '.center(120, '-'))
            logging.info('(Before) Length: ' + str(len(self.agents)))

            for agent in self.agents:
                logging.info(str(agent))

            self.agents.sort()
            self.agents.reverse()
            self.agents = self.agents[:self.ga_descriptor.selection['truncation']['elite_size']]

            logging.info('(After) Length: ' + str(len(self.agents)))

            for agent in self.agents:
                logging.info(str(agent))

        def tournament():
            """
            Tournament selection involves holding several "tournaments" amongst randomly chosen subsets of agents in
            the population. Winners of the tournaments move on for use in the reproduction phase. Changing the
            tournament size effects selection pressure - that is the larger the tournament, the lesser a change weak
            agents will selected.
            :return:
            """

            fittest = None

            for x in xrange(self.ga_descriptor.selection['tournament']['size']):

                agent = self.agents[random.randint(0, self.agent_descriptor.general['population']) - 1]

                if fittest is None or agent.fitness > fittest.fitness:

                    fittest = agent

            return fittest

        return {
            'Truncation': truncation,
            'Tournament': tournament
        }[selection_type]

    def crossover(self, crossover_type):

        def one_point():
            """
            One-point crossover involves generating a random index in the each of the parents' genome sequences.
            Then offspring are created by combining the first slice of the first parent with the second slice of the
            second parent (or vice versa).
            :return:
            """

            logging.info(' One-Point Crossover '.center(120, '-'))

            tmp = []

            for x in xrange((self.agent_descriptor.agents - len(self.agents)) / 2):

                parent1 = random.choice(self.agents)
                parent2 = random.choice(self.agents)

                logging.info('Parent 1: ' + str(parent1))
                logging.info('Parent 2: ' + str(parent2))

                child1 = self.agent_descriptor.factory()
                child2 = self.agent_descriptor.factory()

                split = random.randint(0, self.agent_descriptor.params_len - 1)

                logging.info('Split: ' + str(split))

                child1.params[0:split] = parent1.params[0:split]
                child1.params[split:self.agent_descriptor.params_len] = parent2.params[split:self.agent_descriptor.params_len]

                child2.params[0:split] = parent2.params[0:split]
                child2.params[split:self.agent_descriptor.params_len] = parent1.params[split:self.agent_descriptor.params_len]

                logging.info('Child 1: ' + str(child1))
                logging.info('Child 2: ' + str(child2) + '\n')

                tmp.append(child1)
                tmp.append(child2)

            self.agents.extend(tmp)

        def two_point():
            """
            Two-point crossover is essentially the same as one-point crossover, but with two slicings of the parent
            genome sequences.
            :return:
            """

            tmp = []

            for x in xrange((self.agent_descriptor.agents - len(self.agents)) / 2):

                parent1 = random.choice(self.agents)
                parent2 = random.choice(self.agents)

                logging.info('Parent 1: ' + str(parent1))
                logging.info('Parent 2: ' + str(parent2))

                child1 = self.agent_descriptor.factory()
                child2 = self.agent_descriptor.factory()

                split1 = random.randint(0, self.agent_descriptor.params_len - 1)
                split2 = random.randint(0, self.agent_descriptor.params_len - 1)

                logging.info('(1) Split: ' + str(split1))
                logging.info('(2) Split: ' + str(split2))

                child1.params[1:split1] = parent1.params[1:split1]
                child1.params[split1:split2] = parent2.params[split1:split2]
                child1.params[split2:len(self.agents[0].params)] = parent1.params[split2:self.agent_descriptor.params_len - 1]

                child2.params[1:split1] = parent2.params[1:split1]
                child2.params[split1:split2] = parent1.params[split1:split2]
                child2.params[split2:len(self.agents[0].params)] = parent2.params[split2:self.agent_descriptor.params_len - 1]

                logging.info('Child 1: ' + str(child1))
                logging.info('Child 2: ' + str(child2) + '\n')

                tmp.append(child1)
                tmp.append(child2)

            self.agents.extend(tmp)

        def uniform():
            """
            Uniform crossover uses a fixed mixing ratio between two parents to form offspring.
            """

            tmp = []

            for x in xrange((self.agent_descriptor.agents - len(self.agents)) / 2):

                parent1 = random.choice(self.agents)
                parent2 = random.choice(self.agents)

                logging.info('Parent 1: ' + str(parent1))
                logging.info('Parent 2: ' + str(parent2))

                child1 = self.agent_descriptor.factory()
                child2 = self.agent_descriptor.factory()

                for param in xrange(self.agent_descriptor.params_len):

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

            self.agents.extend(tmp)

        return {
            'One-Point': one_point,
            'Two-Point': two_point,
            'Uniform': uniform
        }[crossover_type]

    def mutate(self, mutation_type):

        def uniform():
            """
            Uniform mutation replaces the value of the chosen gene with a uniform random value within the specified
            bounds of the gene.
            """

            for agent in self.agents:

                for idx, param in enumerate(agent.params):

                    if random.uniform(0.0, 1.0) <= self.ga_descriptor.mutate['uniform'][param]:

                        val = random.uniform(
                            self.ga_descriptor.mutate['uniform']['lower_bounds'][param],
                            self.ga_descriptor.mutate['uniform']['upper_bounds'][param]
                        )

                        agent.params[idx] = val

        def gaussian():
            """
            Gaussian mutation adds a unit gaussian distributed value to the chosen gene. Bounds checking ensures
            the mutation does not violate legal ranges for the gene.
            """

            for agent in self.agents:

                for idx, param in enumerate(agent.params):

                    if random.uniform(0.0, 1.0) <= self.ga_descriptor.mutate['gaussian']['probability'][idx]:

                        val = np.random.normal(
                            loc=param,
                            scale=(0.05 * self.agent_descriptor.params_upper_bounds[idx])
                        )

                        while self.agent_descriptor.params_lower_bounds[idx] < 0 or val > self.agent_descriptor.params_upper_bounds[idx]:

                            val = np.random.normal(
                                loc=param,
                                scale=(0.05 * self.agent_descriptor.params_upper_bounds[idx])
                            )

                        agent.params[idx] = val

        return {
            'Uniform': uniform,
            'Gaussian': gaussian
        }[mutation_type]
