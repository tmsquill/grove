import entity


def on_border(agent=None, entities=None, environment=None):

    """
    Precondition testing if an agent is along the border of the environment.
    :param agent: The agent to test.
    :param entities: The entities associated with the simulation.
    :param environment: The environment to test against.
    :return: Boolean value indicating the result of the test.
    """

    return agent.body.top_left.position[0] == environment.body.top_left.position[0] or \
        agent.body.top_left.position[1] == environment.body.top_left.position[1] or \
        agent.body.bottom_right.position[0] == environment.body.bottom_right.position[0] or \
        agent.body.bottom_right.position[1] == environment.body.bottom_right.position[1]


def on_nest(agent=None, entities=None, environment=None):

    """
    Precondition testing if an agent is on top of the nest.
    :param agent: The agent to test.
    :param entities: The entities associated with the simulation.
    :param environment: The environment to test against.
    :return: Boolean value indicating the result of the test.
    """

    nest = filter(lambda x: isinstance(x, entity.Nest), entities)[0]

    return nest.body.contains_rectangle(agent.body)


def on_food(agent=None, entities=None, environment=None):

    """
    Precondition testing if an agent is on top of food.
    :param agent: The agent to test.
    :param entities: The entities associated with the simulation.
    :param environment: The environment to test against.
    :return: Boolean value indicating the result of the test.
    """

    foods = filter(lambda x: isinstance(x, entity.Food), entities)

    return any([food.body.contains_rectangle(agent.body) for food in foods])


def holding_food(agent=None, entities=None, environment=None):

    """
    Precondition testing if an agent is holding food.
    :param agent: The agent to test.
    :param entities: The entities associated with the simulation.
    :param environment: The environment to test against.
    :return: Boolean value indicating the result of the test.
    """

    if isinstance(agent, entity.SimAgent):

        return agent.holding_food
