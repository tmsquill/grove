__author__ = 'Zivia'

import numpy as np


def report(agents, generation):

    fitnesses = [agent.fitness for agent in agents]

    generation.mean = np.mean(fitnesses)
    generation.median = np.median(fitnesses)
    generation.std = np.std(fitnesses)
    generation.min = np.min(fitnesses)
    generation.max = np.max(fitnesses)

    print 'Mean: ' + str(generation.mean) + ' Median: ' + str(generation.median) + ' STD: ' + str(generation.std) \
          + ' Min: ' + str(generation.min) + ' Max: ' + str(generation.max)