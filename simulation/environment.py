from utils import Point, Rectangle


class Environment:

    def __init__(self, size=(20, 20)):

        self.body = Rectangle(Point(0, 0), Point(size[0], size[1]))

    def __str__(self):

        return self.__class__.__name__ + ' ' + str(self.body)

    def expand(self, amount=1):
        """
        Expands the bounds of the environment in all directions.
        :param amount: The amount of units to expand.
        """

        tl = self.body.top_left()
        br = self.body.bottom_right()

        self.body.set_points(Point(tl.x - amount, tl.y - amount), Point(br.x + amount, br.y + amount))

    def contract(self, amount=1):
        """
        Contracts the bounds of the environment in all directions.
        :param amount: The amount of units to contract.
        """
        tl = self.body.top_left()
        br = self.body.bottom_right()

        self.body.set_points(Point(tl.x + amount, tl.y + amount), Point(br.x - amount, br.y - amount))
