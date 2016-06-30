from utils import Point, Rectangle


class Environment:

    def __init__(self, position=(0, 20), size=(20, 20)):

        self.body = Rectangle(Point(position[0], position[1]), Point(position[0] + size[0], position[1] - size[1]))

    def __str__(self):

        return self.__class__.__name__ + ' ' + str(self.body)
