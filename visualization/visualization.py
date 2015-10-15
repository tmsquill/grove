__author__ = 'Troy Squillaci'

import agent
import ga

import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np


def extract(all=None):

    all_stats = []

    for i in xrange(len(all[0])):

        all_stats.append([stat[i] for stat in all])


def plot_scatter(generations=None, proportion=0.2, analysis_type=None):

    all= []

    for generation in generations:

        data = []

        agent_subsets = [agent_set[:int(proportion * len(agent_set))] for agent_set in generation]

        for agent_set in agent_subsets:

            current = analysis_type(agent_set)
            current = np.max(np.abs(current), axis=0)

            data.append(current)

        all.append(data)

    print str(all)

    prepared_data = extract(all)

    x_axis_len = np.arange(len(generations))

    p_scatters = []

    if parameter_toggle[0]:
        p_scatters.append(Scatter(name='Probability Of Switching To Searching', x=x_axis_len, y=data[0]))

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
