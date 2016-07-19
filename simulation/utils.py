import csv
import hashlib
import math
import os

from enum import Enum
from pymongo import MongoClient


class Direction(Enum):

    """
    Cardinal directions used to represent the orientation of entities on a 2D grid.
    """

    North = 0,
    East = 1,
    South = 2,
    West = 3


class Point:

    """
    A point identified by (x, y) coordinates.
    """

    def __init__(self, x=None, y=None):

        self.position = [x, y]

    def __add__(self, point=None):

        return Point(self.position[0] + point.position[0], self.position[1] + point.position[1])

    def __sub__(self, point):

        return Point(self.position[0] - point.position[0], self.position[1] - point.position[1])

    def __mul__(self, scalar):

        return Point(self.position[0] * scalar, self.position[1] * scalar)

    def __div__(self, scalar):

        return Point(self.position[0] / scalar, self.position[1] / scalar)

    def __str__(self):

        return str(self.position)

    def __repr__(self):

        return str(self.position)

    def length(self):

        """
        Calculates the distance from the origin to the current point.
        """

        return math.sqrt(self.position[0] ** 2 + self.position[1] ** 2)

    def distance_to(self, point):

        """
        Calculates the distance from the given point to the current point.
        :param point: The point to compare to.
        """

        return (self - point).length()

    def as_tuple(self):

        """
        Returns a tuple representation of the point.
        """

        return (self.position[0], self.position[1])

    def clone(self):

        """
        Clones the point, creating a new point at the same position.
        """

        return Point(position=[self.position[0], self.position[1]])

    def integerize(self):

        """
        Converts the position to integer values.
        """

        self.position = [int(self.position[0]), int(self.position[1])]

    def floatize(self):

        """
        Converts the position to float values.
        """

        self.position = [float(self.position[0]), float(self.position[1])]

    def move(self, position=None):

        """
        Moves the point to a new position.
        :param position: The new position of the point.
        """

        self.position = position

    def shift(self, delta=None):

        """
        Shifts a point by some delta.
        :param delta: The amount in each direction to shift the point. Must be a list or tuple.
        """

        self.position[0] = self.position[0] + delta[0]
        self.position[1] = self.position[1] + delta[1]


class Rectangle:

    """
    A rectangle identified by two points (top-left and bottom-right).

    Coordinates are based on the Cartesian coordinate system.

    y+                 top        top-left (x, y) +-------------+
    ^                   |                         |             |
    |             left -+- right                  |             |
    + - - - > x+        |                         |             |
    origin            bottom                      +-------------+ bottom-right (x, y)
    """

    def __init__(self, top_left=None, bottom_right=None):

        self.top_left = top_left
        self.bottom_right = bottom_right

    def __str__(self):

        return str(self.top_left) + ' - ' + str(self.bottom_right)

    def __repr__(self):

        return str(self.top_left) + ' - ' + str(self.bottom_right)

    def set_points(self, top_left=None, bottom_right=None):

        """
        Resets the rectangle coordinates.
        :param top_left: The new top-left point to assign to the rectangle.
        :param bottom_right: The new bottom-right point to assign to the rectangle.
        """

        self.top_left = top_left
        self.bottom_right = bottom_right

    def contains_point(self, point):

        """
        Returns a boolean indicating if the given point is contained in the rectangle.
        :param point: The point to compare against the current rectangle.
        """

        return (self.top_left.position[0] <= point.position[0] <= self.bottom_right.position[0] and
                self.top_left.position[1] >= point.position[1] >= self.bottom_right.position[1])

    def contains_rectangle(self, rectangle):

        """
        Returns a boolean indicating if the given rectangle is contained in the current rectangle.
        :param rectangle: The rectangle to compare agianst the current rectangle.
        """

        return self.contains_point(rectangle.top_left) and self.contains_point(rectangle.bottom_right)

    def expand(self, amount=1):

        """
        Expands the bounds of the rectangle in all directions.
        :param amount: The amount of units to expand.
        """

        self.top_left.position[0] -= 1
        self.top_left.position[1] += 1
        self.bottom_right.position[0] += 1
        self.bottom_right.position[1] -= 1

    def contract(self, amount=1):

        """
        Contracts the bounds of the rectangle in all directions.
        :param amount: The amount of units to contract.
        """

        self.top_left.position[0] += 1
        self.top_left.position[1] -= 1
        self.bottom_right.position[0] -= 1
        self.bottom_right.position[1] += 1


def generate_mongo(simulation=None, host='localhost', port=27017):

    """
    Adds a simulation to a MongoDB instance for further data analysis.
    :param simulation: The simulation containing a valid state archive.
    :param host: The host to reach the MongoDB instance.
    :param port: The port to reach the MongoDB instance.
    """

    connection = MongoClient(host, port)
    simulations = connection['grove']['simulations']

    data = [state for state in simulation.state_archive]
    hashed = hashlib.md5(str(data)).hexdigest()

    _id = simulations.insert({hashed: data})
    connection.close()

    print 'Saved simulation data to MongoDB instance at ' + host + ':' + str(port) + \
          ' -> db.grove.simulations with ObjectId ' + str(_id)

    return _id


def generate_csv(simulation=None):

    """
    Generates a CSV file from a simulation for further data analysis.
    :param simulation: The simulation containing a valid state archive.
    """

    header = ['Type', 'Timestamp', 'ID', 'Direction', 'Behavior', 'Left', 'Top', 'Right', 'Bottom']
    data = [state for state in simulation.state_archive]
    hashed = hashlib.md5(str(data)).hexdigest()

    with open(hashed + ".csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)

    print 'Created CSV file at ' + os.getcwd() + '/' + hashed + '.csv'
