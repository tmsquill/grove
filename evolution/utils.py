import csv
import itertools
import logging
import os

import config


# TODO: Make generic.
def generate_csv(generations=None):
    """
    Generates a CSV file from a set of generations for separate data analysis.
    :param generations: The generations containing snapshots of the agents at each generation.
    """

    header = ['GID'] + ['AID'] + ['Fitness'] + config.global_config['agent']['ForagerAgent']['genotype_abbr_names']
    data = itertools.chain.from_iterable([generation.csv() for generation in generations])

    with open('ForagerAgent' + ".csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)

    print 'Created CSV file at ' + os.getcwd()
    logging.info('Created CSV file at ' + os.getcwd())
