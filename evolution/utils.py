__author__ = 'Troy Squillaci'

import agent
import csv
import itertools


def generate_csv(generations=None):

    for agent_type in agent.config['agent_types']:

        header = ['GID'] + ['AID'] + ['Fitness'] + agent.config[agent_type]['params_abbr_names']
        data = itertools.chain.from_iterable([generation.csv(generation.agents_map[agent_type]) for generation in generations])

        with open(agent_type + ".csv", "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(data)
