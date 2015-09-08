__author__ = 'Troy Squillaci'

import itertools

class Generation:

    gid = itertools.count().next

    def __init__(self):

        self.id = Generation.gid()
        self.mean = -1
        self.median = -1
        self.std = -1
        self.min = -1
        self.max = -1

    def __str__(self):

        return str(self.id)
