__author__ = 'Troy Squillaci'

import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
import visualization


def plot_params(generations=None, proportion=0.2, analysis_type=None, param_idx=None):

    agent_sets_by_generations = visualization.extract_by_agent(generations)

    scatters = []

    for agent_sets_by_generation in agent_sets_by_generations:

        agent_subsets_by_generation = [agent_set[:int(proportion * len(agent_set))] for agent_set in agent_sets_by_generation]

        current = analysis_type([agent_subset.params[param_idx] for agent_subset in agent_subsets_by_generation])

        x_axis_len = np.arange(len(generations))

        scatters.append(Scatter(name=agent_set, x=x_axis_len, y=data[0]))

    # Plot the data.
    p_data = Data(p_scatters)

    p_layout = Layout(
        title='(iAnts) Elite ' + analysis_type,
        xaxis=XAxis(title='Generation'),
        yaxis=YAxis(title='Normalized Value')
    )

    p_figure = Figure(data=p_data, layout=p_layout)

    py.plot(p_figure, filename=analysis_type)


def plot_fitness(generations=None, proportion=0.2):

    sorted_generations = visualization.extract_by_agent(generations)
    x_axis_len = np.arange(len(generations))
    data = []

    for agent_set in sorted_generations:

        min_fitnesses = [agents[len(agent_set) - 1].fitness for agents in agent_set]
        max_fitnesses = [agents[0].fitness for agents in agent_set]
        mean_fitnesses = np.mean([agents.fitness for agents in agent_set])

        data.append(Scatter(name='Minimum Fitness', x=x_axis_len, y=min_fitnesses))
        data.append(Scatter(name='Maximum Fitness', x=x_axis_len, y=max_fitnesses))
        data.append(Scatter(name='Mean Fitness', x=x_axis_len, y=mean_fitnesses))

        layout = Layout(
            title=agent_set[0].__class__.__name__ + ' Elite Fitness Values',
            xaxis=XAxis(title='Generation'),
            yaxis=YAxis(title='Normalized Value')
        )

        figure = Figure(data=data, layout=layout)
        py.plot(figure, filename='(' + agent_set[0].__class__.__name__ + ') Fitness Scores')
