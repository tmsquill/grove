import abc
import itertools

from utils import Direction, Point, Rectangle


class Entity:
    """
    Abstract representation of an entity. An entity is a component present in a
    spatial environment.
    """

    __metaclass__ = abc.ABCMeta

    eid = itertools.count().next

    def __init__(self, position=(0, 0), size=(1, 1), direction=Direction.North):

        self.id = SimAgent.eid()
        self.body = Rectangle(Point(position[0], position[1]), Point(position[0] + size[0], position[1] + size[1]))
        self.direction = direction
        self.behavior = [None, 0]

    def __str__(self):

        return self.__class__.__name__ + str(self.id)

    def to_csv(self):

        return [self.__class__.__name__] + \
               [self.id] + \
               [self.direction] + \
               [self.behavior] + \
               [self.body.left] + \
               [self.body.top] + \
               [self.body.right] + \
               [self.body.bottom]


class SimAgent(Entity):

    def __init__(self, speed=5, holding_food=False, *args, **kwargs):

        super(SimAgent, self).__init__(*args, **kwargs)

        self.speed = speed

        # State machine variables.
        self.holding_food = holding_food

    def __str__(self):

        return self.__class__.__name__ + str(self.id)


class Food(Entity):

    def __init__(self, *args, **kwargs):

        super(Food, self).__init__(*args, **kwargs)

    def __str__(self):

        return self.__class__.__name__ + str(self.id)


class Nest(Entity):

    def __init__(self, *args, **kwargs):

        super(Nest, self).__init__(*args, **kwargs)

        # State machine variables.
        self.food_count = 0

    def __str__(self):

        return self.__class__.__name__ + str(self.id)
