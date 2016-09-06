import csv
import hashlib
import itertools
import os

from pymongo import MongoClient


def generate_mongo(generations=None, host='localhost', port=27017):

    """
    Adds an evolutionary run to a MongoDB instance for further data analysis.
    :param generations: The generations containing archives of the agents at each generation.
    :param host: The host to reach the MongoDB instance.
    :param port: The port to reach the MongoDB instance.
    """

    connection = MongoClient(host, port)
    evolutions = connection['grove']['evolutions']

    data = [[(generation.id, agent.genotype, agent.value, agent.random_seed) for agent in generation.agents] for generation in generations]
    checksum = hashlib.md5(str(data)).hexdigest()

    _id = evolutions.insert({checksum: data})
    connection.close()

    print 'Saved evolution data to MongoDB instance at ' + host + ':' + str(port) + \
          ' -> db.grove.evolutions with ObjectId: ' + str(_id)


def generate_csv(generations=None):

    """
    Adds an evolutionary run to a CSV file for further data analysis.
    :param generations: The generations containing archives of the agents at each generation.
    """

    header = ['GID', 'Genotype', 'Value']
    data = [[(generation.id, agent.genotype, agent.value) for agent in generation.agents] for generation in generations]
    checksum = hashlib.md5(str(data)).hexdigest()

    with open(checksum + ".csv", "w") as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(itertools.chain.from_iterable(data))

    print 'Saved evolution data to CSV at ' + os.getcwd() + '/' + checksum + '.csv'
