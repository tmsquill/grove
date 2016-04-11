import entity
import random

from utils import Direction, Point


def move_north(agent=None, entities=None, environment=None):

    if environment.body.contains(Point(agent.body.top_left().x, agent.body.top_left().y - 1)):

        agent.body.set_points(Point(agent.body.top_left().x, agent.body.top_left().y - 1),
                              Point(agent.body.bottom_right().x, agent.body.bottom_right().y - 1))

    return agent


def move_east(agent=None, entities=None, environment=None):

    if environment.body.contains(Point(agent.body.bottom_right().x + 1, agent.body.bottom_right().y)):

        agent.body.set_points(Point(agent.body.top_left().x + 1, agent.body.top_left().y),
                              Point(agent.body.bottom_right().x + 1, agent.body.bottom_right().y))

    return agent


def move_south(agent=None, entities=None, environment=None):

    if environment.body.contains(Point(agent.body.bottom_right().x, agent.body.bottom_right().y + 1)):

        agent.body.set_points(Point(agent.body.top_left().x, agent.body.top_left().y + 1),
                              Point(agent.body.bottom_right().x, agent.body.bottom_right().y + 1))

    return agent


def move_west(agent=None, entities=None, environment=None):

    if environment.body.contains(Point(agent.body.top_left().x - 1, agent.body.top_left().y)):

        agent.body.set_points(Point(agent.body.top_left().x - 1, agent.body.top_left().y),
                              Point(agent.body.bottom_right().x - 1, agent.body.bottom_right().y))

    return agent


def pickup_food(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to pickup food.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    if not agent.holding_food:

        agent.holding_food = True

    return agent


def drop_food(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to drop food.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    if agent.holding_food:

        agent.holding_food = False

    return agent


def random_walk(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to walk in a random direction for one time step.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    random_direction = random.choice(list(Direction))

    if random_direction == Direction.North:

        return move_north(agent, environment)

    elif random_direction == Direction.East:

        return move_east(agent, environment)

    elif random_direction == Direction.South:

        return move_south(agent, environment)

    elif random_direction == Direction.West:

        return move_west(agent, environment)


def return_home(agent=None, entities=None, environment=None):

    """
    Behavior (naive) that causes an agent to return to the nest.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    nest = filter(lambda x: isinstance(x, entity.Nest), entities)

    agent.body.top = (nest.body.top + nest.body.bottom) / 2
    agent.body.right = (nest.body.left + nest.body.right) / 2
    agent.body.bottom = (nest.body.top + nest.body.bottom) / 2
    agent.body.left = (nest.body.left + nest.body.right) / 2

    return agent
