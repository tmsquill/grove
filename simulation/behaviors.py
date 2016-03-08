from utils import Point


def move_north(entity=None, environment=None):

    if environment.body.contains(Point(entity.body.top_left().x, entity.body.top_left().y - 1)):

        entity.body.set_points(Point(entity.body.top_left().x, entity.body.top_left().y - 1),
                               Point(entity.body.bottom_right().x, entity.body.bottom_right().y - 1))

    return entity


def move_east(entity=None, environment=None):

    if environment.body.contains(Point(entity.body.bottom_right().x + 1, entity.body.bottom_right().y)):

        entity.body.set_points(Point(entity.body.top_left().x + 1, entity.body.top_left().y),
                               Point(entity.body.bottom_right().x + 1, entity.body.bottom_right().y))

    return entity


def move_south(entity=None, environment=None):

    if environment.body.contains(Point(entity.body.bottom_right().x, entity.body.bottom_right().y + 1)):

        entity.body.set_points(Point(entity.body.top_left().x, entity.body.top_left().y + 1),
                               Point(entity.body.bottom_right().x, entity.body.bottom_right().y + 1))

    return entity


def move_west(entity=None, environment=None):

    if environment.body.contains(Point(entity.body.top_left().x - 1, entity.body.top_left().y)):

        entity.body.set_points(Point(entity.body.top_left().x - 1, entity.body.top_left().y),
                               Point(entity.body.bottom_right().x - 1, entity.body.bottom_right().y))

    return entity


def pickup_food(agent=None, environment=None):

    if not agent.holding_food:

        agent.holding_food = True


def drop_food(agent=None, environment=None):

    if agent.holding_food:

        agent.holding_food = False
