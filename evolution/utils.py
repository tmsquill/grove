import csv
import itertools
import logging
import os

import config


def generate_csv(generations=None):
    """
    Generates a CSV file from a set of generations for further data analysis.
    :param generations: The generations containing snapshots of the agents at each generation.
    """

    agent_type = str(type(generations[0].agents[0]).__name__)
    header = ['GID'] + ['AID'] + ['Evaluation Value'] + config.grove_config['agent'][agent_type]['genotype_abbr_names']
    data = itertools.chain.from_iterable([generation.csv() for generation in generations])

    with open(agent_type + ".csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)

    print 'Created CSV file at ' + os.getcwd()
    logging.info('Created CSV file at ' + os.getcwd())
