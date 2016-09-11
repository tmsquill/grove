from utils import Point, Rectangle


class Environment:

    """
    An environment is simply a large two-dimensional body that is used by the simulator to determine the boundries
    where agents can reside.
    """

    def __init__(self, position=(0, 20), size=(20, 20)):

        self.body = Rectangle(Point(position[0], position[1]), Point(position[0] + size[0], position[1] - size[1]))

    def __str__(self):

        return self.__class__.__name__ + ' ' + str(self.body)
