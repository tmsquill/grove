__author__ = 'Troy Squillaci'

import agent
import ga

import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np


def normalize(self, current_data):

    for idx, data in enumerate(current_data):
        data /= self.agent_descriptor.config['params_upper_bounds'][idx]
        current_data[idx] = data

    return current_data

def plot_all(generations=None, proportion=0.2):

    pass

def plot_min(generations=None, proportion=0.2):

    for generation in generations:

        for agent_set in generation.agents:

            current = agent_set[ga.config['general']['population'] * proportion - 1].params

def plot_elite(analysis_type, parameter_toggle):

    # Holds the raw data to be plotted.
    data = []

    # Gather / Calculate data.
    for generation in self.generations:

        for agent_set in generation.agents:

            current = np.empty(0)

            # Minimum
            if analysis_type == 'Min':

                current = generation.agents[self.elite_size - 1].params
                current = self.normalize(current)

            # Maximum
            elif analysis_type == 'Max':

                current = generation.agents[0].params
                current = self.normalize(current)

            # Mean
            elif analysis_type == 'Mean':

                current = np.asarray(generation.agents[0].params)

                for elite in xrange(1, self.elite_size):
                    current += np.asarray(generation.agents[elite].params)

                current /= self.elite_size
                current = self.normalize(current)

            # Median
            elif analysis_type == 'Median':

                current = np.asarray(generation.agents[0].params)

                for elite in xrange(1, self.elite_size):
                    current = np.vstack((current, np.asarray(generation.agents[elite].params)))

                current = np.median(current, axis=0)
                current = self.normalize(current)

            # Variance
            elif analysis_type == 'Variance':

                current = np.asarray(generation.agents[0].params)

                for elite in xrange(1, self.elite_size):
                    current = np.vstack((current, np.asarray(generation.agents[elite].params)))

                current = np.var(current, axis=0)
                current = self.normalize(current)

            # Standard Deviation
            elif analysis_type == 'Standard Deviation':

                current = np.asarray(generation.agents[0].params)

                for elite in xrange(1, self.elite_size):
                    current = np.vstack((current, np.asarray(generation.agents[elite].params)))

                current = np.std(current, axis=0)
                current = self.normalize(current)

            data.append(current)

    data = np.asarray(data)
    data = np.transpose(data)

    x_axis_len = np.arange(len(self.generations))

    p_scatters = []

    if parameter_toggle[0]:
        p_scatters.append(Scatter(name='Probability Of Switching To Searching', x=x_axis_len, y=data[0]))

    if parameter_toggle[1]:
        p_scatters.append(Scatter(name='Probability Of Returning To Nest', x=x_axis_len, y=data[1]))

    if parameter_toggle[2]:
        p_scatters.append(Scatter(name='Uninformed Search Variation', x=x_axis_len, y=data[2]))

    if parameter_toggle[3]:
        p_scatters.append(Scatter(name='Rate Of Informed Search Decay', x=x_axis_len, y=data[3]))

    if parameter_toggle[4]:
        p_scatters.append(Scatter(name='Rate Of Site Fidelity', x=x_axis_len, y=data[4]))

    if parameter_toggle[5]:
        p_scatters.append(Scatter(name='Rate Of Laying Pheromone', x=x_axis_len, y=data[5]))

    if parameter_toggle[6]:
        p_scatters.append(Scatter(name='Rate Of Pheromone Decay', x=x_axis_len, y=data[6]))

    # Plot the data.
    p_data = Data(p_scatters)

    p_layout = Layout(
        title='(iAnts) Elite ' + analysis_type,
        xaxis=XAxis(title='Generation'),
        yaxis=YAxis(title='Normalized Value')
    )

    p_figure = Figure(data=p_data, layout=p_layout)

    py.plot(p_figure, filename=analysis_type)

def plot_fitness(self):

    min_fitness_data = [generation.min for generation in self.generations]
    max_fitness_data = [generation.max for generation in self.generations]
    mean_fitness_data = [generation.mean for generation in self.generations]

    x_axis_len = np.arange(len(self.generations))

    p_data = Data([
        Scatter(name='Minimum Fitness', x=x_axis_len, y=min_fitness_data),
        Scatter(name='Maximum Fitness', x=x_axis_len, y=max_fitness_data),
        Scatter(name='Mean Fitness', x=x_axis_len, y=mean_fitness_data)
    ])

    p_layout = Layout(
        title='(iAnts) Elite Fitness Values',
        xaxis=XAxis(title='Generation'),
        yaxis=YAxis(title='Normalized Value')
    )

    p_figure = Figure(data=p_data, layout=p_layout)

    py.plot(p_figure, filename='(iAnts) Elite Fitness Scores')
