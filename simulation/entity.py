import abc
import itertools

from utils import Direction, Point, Rectangle


class Entity:

    """
    Abstract representation of an entity.
    """

    __metaclass__ = abc.ABCMeta

    eid = itertools.count().next

    def __init__(self, position=(0, 0), size=(1, 1), direction=Direction.North):

        self.id = SimAgent.eid()
        self.body = Rectangle(Point(position[0], position[1]), Point(position[0] + size[0], position[1] - size[1]))
        self.direction = direction
        self.behavior = None

    def __str__(self):

        return self.__class__.__name__ + str(self.id)

    def to_csv(self):

        return [self.__class__.__name__,
                self.id,
                str(self.direction),
                str(self.behavior),
                self.body.top_left.position[0],
                self.body.top_left.position[1],
                self.body.bottom_right.position[0],
                self.body.bottom_right.position[1]]


class SimAgent(Entity):

    def __init__(self, holding_food=False, *args, **kwargs):

        super(SimAgent, self).__init__(*args, **kwargs)

        # State machine variables.
        self.holding_food = holding_food

    def __str__(self):

        return self.__class__.__name__ + str(self.id) + ' ' + str(self.behavior) + str(self.body)


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
