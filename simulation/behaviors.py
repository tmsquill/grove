import entity

from utils import Direction, Point, rand


def move_north(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to move north one unit.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    if environment.body.contains_point(Point(agent.body.top_left.position[0], agent.body.top_left.position[1] + 1)):

        for item in agent.inventory:

            item.body.top_left.position[1] += 1
            item.body.bottom_right.position[1] += 1

        agent.body.top_left.position[1] += 1
        agent.body.bottom_right.position[1] += 1

    agent.time += 1

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

        for item in agent.inventory:

            item.body.top_left.position[0] += 1
            item.body.bottom_right.position[0] += 1

        agent.body.top_left.position[0] += 1
        agent.body.bottom_right.position[0] += 1

    agent.time += 1

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

        for item in agent.inventory:

            item.body.top_left.position[1] -= 1
            item.body.bottom_right.position[1] -= 1

        agent.body.top_left.position[1] -= 1
        agent.body.bottom_right.position[1] -= 1

    agent.time += 1

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

        for item in agent.inventory:

            item.body.top_left.position[0] -= 1
            item.body.bottom_right.position[0] -= 1

        agent.body.top_left.position[0] -= 1
        agent.body.bottom_right.position[0] -= 1

    agent.time += 1

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

        for food in foods:

            if agent.body.contains_rectangle(food.body) and food.interactable:

                agent.inventory.append(food)
                food.interactable = False
                agent.holding_food = True
                break

    agent.time += 1

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

        for item in agent.inventory:

            agent.inventory.remove(item)

            if nest.body.contains_rectangle(agent.body):

                nest.food_count += 1

            else:

                item.interactable = True

        agent.holding_food = False

    agent.time += 1

    return agent


def random_walk(agent=None, entities=None, environment=None):

    """
    Behavior that causes an agent to walk in a random direction for one time step.
    :param agent: The agent to perform the behavior.
    :param entities: A list of entities in the simulation.
    :param environment: The environment containing the agent.
    :return: The updated agent.
    """

    random_direction = rand.choice(list(Direction))

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

    nest = filter(lambda x: isinstance(x, entity.Nest), entities)[0]

    agent.time += int(agent.body.top_left.distance_to(nest.body.top_left))

    agent.body.top_left.position[1] = (nest.body.top_left.position[1] + nest.body.bottom_right.position[1]) / 2
    agent.body.bottom_right.position[0] = (nest.body.top_left.position[0] + nest.body.bottom_right.position[0]) / 2
    agent.body.bottom_right.position[1] = (nest.body.top_left.position[1] + nest.body.bottom_right.position[1]) / 2
    agent.body.top_left.position[0] = (nest.body.top_left.position[0] + nest.body.bottom_right.position[0]) / 2

    return agent
