import csv
import itertools

import config


# TODO: Make generic.
def generate_csv(generations=None):
    """
    Generates a CSV file from a set of generations for seperate data analysis.
    :param generations: The generations containing snapshots of the agents at each generation.
    """

    header = ['GID'] + ['AID'] + ['Fitness'] + config.global_config['agent']['ForagerAgent']['params_abbr_names']
    data = itertools.chain.from_iterable([generation.csv() for generation in generations])

    with open('ForagerAgent' + ".csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)
