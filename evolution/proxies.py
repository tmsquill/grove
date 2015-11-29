import abc


class Proxy(object):
    """
    A proxy is essentially a subset of a genetic algorithm that uses reflection and dynamic typing the alter its
    behavior at runtime. This is currently a bare-bones shell, but takes ideas from genetic programming and the
    middleware stack in Express (Node.js).
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):

        self.evolution_sequence = []

    @abc.abstractmethod
    def next(self):
        """Executes next segment in the middleware stack needed to advance the evolutionary process."""
