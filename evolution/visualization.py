__author__ = 'Troy Squillaci'

import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
from agent import Agent, AgentDescriptor
import random


class Visualization:

    def __init__(self, agent_descriptor, generations, elite_size):

        self.agent_descriptor = agent_descriptor
        self.generations = generations
        self.elite_size = elite_size

    def normalize(self, current_data):

        for idx, data in enumerate(current_data):
            data /= self.agent_descriptor.config['params_upper_bounds'][idx]
            current_data[idx] = data

        return current_data

    def obs_normalize(self, current_data):

        for idx, data in enumerate(current_data):
            data /= self.agent_descriptor.config['obs_params_upper_bounds'][idx]
            current_data[idx] = data

        return current_data

    def plot_elite(self, analysis_type, parameter_toggle):

        # Holds the raw data to be plotted.
        data = []

        # Gather / Calculate data.
        for generation in self.generations:

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

    def plot_obs_elite(self, analysis_type, parameter_toggle):

        # Holds the raw data to be plotted.
        data = []

        # Gather / Calculate data.
        for generation in self.generations:

            current = np.empty(0)

            # Minimum
            if analysis_type == 'Min':

                current = generation.obs_agents[self.elite_size - 1].params
                current = self.obs_normalize(current)

            # Maximum
            elif analysis_type == 'Max':

                current = generation.obs_agents[0].params
                current = self.obs_normalize(current)

            # Mean
            elif analysis_type == 'Mean':

                current = np.asarray(generation.obs_agents[0].params)

                for elite in xrange(1, self.elite_size):
                    current += np.asarray(generation.obs_agents[elite].params)

                current /= self.elite_size
                current = self.obs_normalize(current)

            # Median
            elif analysis_type == 'Median':

                current = np.asarray(generation.obs_agents[0].params)

                for elite in xrange(1, self.elite_size):
                    current = np.vstack((current, np.asarray(generation.obs_agents[elite].params)))

                current = np.median(current, axis=0)
                current = self.obs_normalize(current)

            # Variance
            elif analysis_type == 'Variance':

                current = np.asarray(generation.obs_agents[0].params)

                for elite in xrange(1, self.elite_size):
                    current = np.vstack((current, np.asarray(generation.obs_agents[elite].params)))

                current = np.var(current, axis=0)
                current = self.obs_normalize(current)

            # Standard Deviation
            elif analysis_type == 'Standard Deviation':

                current = np.asarray(generation.obs_agents[0].params)

                for elite in xrange(1, self.elite_size):
                    current = np.vstack((current, np.asarray(generation.obs_agents[elite].params)))

                current = np.std(current, axis=0)
                current = self.obs_normalize(current)

            data.append(current)

        data = np.asarray(data)
        data = np.transpose(data)

        x_axis_len = np.arange(len(self.generations))

        p_scatters = []

        if parameter_toggle[0]:
            p_scatters.append(Scatter(name='(Obstacle 1) Orientation', x=x_axis_len, y=data[0]))

        if parameter_toggle[1]:
            p_scatters.append(Scatter(name='(Obstacle 1) Position X', x=x_axis_len, y=data[1]))

        if parameter_toggle[2]:
            p_scatters.append(Scatter(name='(Obstacle 1) Position Y', x=x_axis_len, y=data[2]))

        if parameter_toggle[3]:
            p_scatters.append(Scatter(name='(Obstacle 2) Orientation', x=x_axis_len, y=data[3]))

        if parameter_toggle[4]:
            p_scatters.append(Scatter(name='(Obstacle 2) Position X', x=x_axis_len, y=data[4]))

        if parameter_toggle[5]:
            p_scatters.append(Scatter(name='(Obstacle 2) Position Y', x=x_axis_len, y=data[5]))

        if parameter_toggle[6]:
            p_scatters.append(Scatter(name='(Obstacle 3) Orientation', x=x_axis_len, y=data[6]))

        if parameter_toggle[7]:
            p_scatters.append(Scatter(name='(Obstacle 3) Position X', x=x_axis_len, y=data[7]))

        if parameter_toggle[8]:
            p_scatters.append(Scatter(name='(Obstacle 3) Position Y', x=x_axis_len, y=data[8]))

        if parameter_toggle[9]:
            p_scatters.append(Scatter(name='(Obstacle 4) Orientation', x=x_axis_len, y=data[9]))

        if parameter_toggle[10]:
            p_scatters.append(Scatter(name='(Obstacle 4) Position X', x=x_axis_len, y=data[10]))

        if parameter_toggle[11]:
            p_scatters.append(Scatter(name='(Obstacle 4) Position Y', x=x_axis_len, y=data[11]))

        # Plot the data.
        p_data = Data(p_scatters)

        p_layout = Layout(
            title='(Obstacles) Elite ' + analysis_type,
            xaxis=XAxis(title='Generation'),
            yaxis=YAxis(title='Normalized Value')
        )

        p_figure = Figure(data=p_data, layout=p_layout)

        py.plot(p_figure, filename='(Obstacles) Elite ' + analysis_type)

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

    def plot_obs_fitness(self):

        min_fitness_data = [generation.obs_min for generation in self.generations]
        max_fitness_data = [generation.obs_max for generation in self.generations]
        mean_fitness_data = [generation.obs_mean for generation in self.generations]

        x_axis_len = np.arange(len(self.generations))

        p_data = Data([
            Scatter(name='Minimum Fitness', x=x_axis_len, y=min_fitness_data),
            Scatter(name='Maximum Fitness', x=x_axis_len, y=max_fitness_data),
            Scatter(name='Mean Fitness', x=x_axis_len, y=mean_fitness_data)
        ])

        p_layout = Layout(
            title='(Obstacles) Elite Fitness Values',
            xaxis=XAxis(title='Generation'),
            yaxis=YAxis(title='Normalized Value')
        )

        p_figure = Figure(data=p_data, layout=p_layout)

        py.plot(p_figure, filename='(Obstacles) Elite Fitness Scores')
