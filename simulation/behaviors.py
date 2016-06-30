import entity
import random

from utils import Direction, Point


def move_north(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to move north one unit.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    if environment.body.contains_point(Point(agent.body.top_left.position[0], agent.body.top_left.position[1] + 1)):

        agent.body.top_left.position[1] += 1
        agent.body.bottom_right.position[1] += 1

    return agent


def move_east(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to move east one unit.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    if environment.body.contains_point(Point(agent.body.bottom_right.position[0] + 1, agent.body.bottom_right.position[1])):

        agent.body.top_left.position[0] += 1
        agent.body.bottom_right.position[0] += 1

    return agent


def move_south(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to move south one unit.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    if environment.body.contains_point(Point(agent.body.bottom_right.position[0], agent.body.bottom_right.position[1] - 1)):

        agent.body.top_left.position[1] -= 1
        agent.body.bottom_right.position[1] -= 1

    return agent


def move_west(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to move west one unit.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    if environment.body.contains_point(Point(agent.body.top_left.position[0] - 1, agent.body.top_left.position[1])):

        agent.body.top_left.position[0] -= 1
        agent.body.bottom_right.position[0] -= 1

    return agent


def pickup_food(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to pickup food.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    foods = filter(lambda x: isinstance(x, entity.Food), entities)

    if not agent.holding_food:

        if any([agent.body.contains_rectangle(food.body) for food in foods]):

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

    nest = filter(lambda x: isinstance(x, entity.Nest), entities)[0]

    if agent.holding_food:

        if nest.body.contains_rectangle(agent.body):

            nest.food_count += 1
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

        return move_north(agent, entities, environment)

    elif random_direction == Direction.East:

        return move_east(agent, entities, environment)

    elif random_direction == Direction.South:

        return move_south(agent, entities, environment)

    elif random_direction == Direction.West:

        return move_west(agent, entities, environment)

    return agent


def return_home(agent=None, entities=None, environment=None):

    """
    Behavior (naive) that causes an agent to return to the nest.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    nest = filter(lambda x: isinstance(x, entity.Nest), entities)

    agent.body.top = (nest[0].body.top + nest[0].body.bottom) / 2
    agent.body.right = (nest[0].body.left + nest[0].body.right) / 2
    agent.body.bottom = (nest[0].body.top + nest[0].body.bottom) / 2
    agent.body.left = (nest[0].body.left + nest[0].body.right) / 2

    return agent
