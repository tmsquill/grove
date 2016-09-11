from pymongo import MongoClient


def load_mongo(object_id=None, host='localhost', port=27017):

    """
    Loads an evolutionary run from a MongoDB instance for further data analysis.
    :param object_id: The ObjectId of the entry in the MongoDB.
    :param host: The host to reach the MongoDB instance.
    :param port: The port to reach the MongoDB instance.
    """

    from bson.objectid import ObjectId

    connection = MongoClient(host, port)
    evolutions = connection['grove']['evolutions']

    data = evolutions.find_one({'_id': ObjectId(object_id)})

    return data


def generate_mongo(generations=None, host='localhost', port=27017):

    """
    Adds an evolutionary run to a MongoDB instance for further data analysis.
    :param generations: The generations containing archives of the agents at each generation.
    :param host: The host to reach the MongoDB instance.
    :param port: The port to reach the MongoDB instance.
    """

    connection = MongoClient(host, port)
    evolutions = connection['grove']['evolutions']

    data = [[(generation.id, agent.genome, agent.value, agent.random_seed) for agent in generation.agents] for generation in generations]

    _id = evolutions.insert({'generations': data})
    connection.close()

    print 'Saved evolution data to MongoDB instance at ' + host + ':' + str(port) + \
          ' -> db.grove.evolutions with ObjectId: ' + str(_id)


def generate_csv(generations=None):

    """
    Adds an evolutionary run to a CSV file for further data analysis.
    :param generations: The generations containing archives of the agents at each generation.
    """

    import csv
    import itertools
    import hashlib
    import os

    header = ['GID', 'genome', 'Value']
    data = [[(generation.id, agent.genome, agent.value) for agent in generation.agents] for generation in generations]
    checksum = hashlib.md5(str(data)).hexdigest()

    with open(checksum + ".csv", "w") as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(itertools.chain.from_iterable(data))

    print 'Saved evolution data to CSV at ' + os.getcwd() + '/' + checksum + '.csv'
