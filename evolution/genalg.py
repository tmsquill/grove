from agent import Agent
from generation import Generation

import logging
import random
import stats
import sys
import time
import numpy as np

from argos import ARGoSAgent


class GeneticAlgorithmDescriptor:

    def __init__(self):

        self.general = {
            'generations': 20,
            'population': 40
        }

        self.selection = {
            'truncation': {
                'elite_size': 4,
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
                    5: 0.0,
                    6: 0.10,
                    7: 0.10,
                    8: 0.10,
                    9: 0.10,
                    10: 0.10,
                    11: 0.10
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
            print 'Fitness'
            stats.report(self.agents, generation)
            self.selection('Truncation')()
            print 'Truncation Selection'
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

            print type(self.agents)

            print 'Len' + str(len(self.agents))
            for agent in self.agents:
                print str(agent)

            self.agents.sort()
            self.agents.reverse()

            self.agents = self.agents[:self.ga_descriptor.selection['truncation']['elite_size']]

            print 'Len' + str(len(self.agents))
            for agent in self.agents:
                print str(agent)

        def tournament():
            """
            Tournament selection involves holding several "tournaments" amongst randomly chosen subsets of agents in
            the population. Winners of the tournaments move on for use in the reproduction phase. Changing the
            tournament size effects selection pressure - that is the larger the tournament, the lesser a change weak
            agents will selected.
            :return:
            """

            fittest = None

            for i in xrange(self.ga_descriptor.selection['tournament']['size']):

                agent = self.agents[random(1, self.agent_descriptor.general['population'])]

                if (fittest is None or agent.fitness > fittest.fitness):
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
            Then children are created by combining the first slice of the first parent with the second slice of the
            second parent (or vice versa).
            :return:
            """

            tmp = []

            for x in xrange((self.agent_descriptor.agents - len(self.agents)) / 2):

                parent1 = random.choice(self.agents)
                parent2 = random.choice(self.agents)

                print 'Parent 1: ' + str(parent1)
                print 'Parent 2: ' + str(parent2)

                # TODO Make generic
                child1 = ARGoSAgent(self.agent_descriptor)
                child2 = ARGoSAgent(self.agent_descriptor)

                split = random.randint(0, self.agent_descriptor.params_len - 1)

                print 'Split: ' + str(split)

                child1.params[0:split] = parent1.params[0:split]
                child1.params[split:self.agent_descriptor.params_len] = parent2.params[split:self.agent_descriptor.params_len]

                child2.params[0:split] = parent2.params[0:split]
                child2.params[split:self.agent_descriptor.params_len] = parent1.params[split:self.agent_descriptor.params_len]

                print 'Child 1: ' + str(child1)
                print 'Child 2: ' + str(child2)

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

            for x in xrange((self.ga_descriptor.general['population_size'] - self.ga_descriptor.selection['elite_size']) / 2):

                parent1 = random.choice(self.agents)
                parent2 = random.choice(self.agents)

                child1 = Agent()
                child2 = Agent()

                # TODO - Fix parameters length.
                split1 = random.randint(0, len(self.agents[0].parameters))
                split2 = random.randint(0, len(self.agents[0].parameters))

                child1.parameters[1:split1] = parent1.parameters[1:split1]
                child1.parameters[split1:split2] = parent1.parameters[split1:split2]
                child1.parameters[split2:len(self.agents[0].parameters)] = parent2.parameters[split2:len(self.agents[0].parameters)]

                child2.parameters[1:split1] = parent2.parameters[1:split1]
                child2.parameters[split1:split2] = parent2.parameters[split1:split2]
                child2.parameters[split2:len(self.agents[0].parameters)] = parent1.parameters[split2:len(self.agents[0].parameters)]

                tmp.append(child1)
                tmp.append(child2)

            self.agents.extend(tmp)

        def uniform():

            tmp = []

            for x in xrange((self.ga_descriptor.general['population_size'] - self.ga_descriptor.selection['elite_size']) / 2):

                parent1 = random.choice(self.agents)
                parent2 = random.choice(self.agents)

                child1 = Agent()
                child2 = Agent()

                for parameter in xrange(len(self.agents[0].parameters)):

                    if bool(random.getrandbits(1)):

                        child1.parameters[parameter] = parent1.parameters[parameter]
                        child2.parameters[parameter]= parent2.parameters[parameter]

                    else:

                        child1.parameters[parameter] = parent2.parameters[parameter]
                        child2.parameters[parameter] = parent1.parameters[parameter]

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

            for agent in self.agents:

                for parameter in agent.parameters:

                    if random.uniform(0.0, 1.0) <= self.ga_descriptor.mutate['uniform'][parameter]:

                        val = random.uniform(self.ga_descriptor.mutate['uniform']['lower_bounds'][parameter],
                                             self.ga_descriptor.mutate['uniform']['upper_bounds'][parameter])

                        parameter = val

        def gaussian():

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