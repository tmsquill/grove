import entity


def on_border(agent=None, entities=None, environment=None):

    """
    Precondition testing if an agent is along the border of the environment.
    :param agent: The agent to test.
    :param entities: The entities associated with the simulation.
    :param environment: The environment to test against.
    :return: Boolean value indicating the result of the test.
    """

    return agent.body.left == environment.body.left or \
           agent.body.top == environment.body.top or \
           agent.body.right == environment.body.right or \
           agent.body.bottom == environment.body.bottom


def on_nest(agent=None, entities=None, environment=None):

    """
    Precondition testing if an agent is on top of the nest.
    :param agent: The agent to test.
    :param entities: The entities associated with the simulation.
    :param environment: The environment to test against.
    :return: Boolean value indicating the result of the test.
    """

    nest = filter(lambda x: isinstance(x, entity.Entity), entities)

    return nest[0].body.contains(agent.body)


def on_food(agent=None, entities=None, environment=None):

    """
    Precondition testing if an agent is on top of food.
    :param agent: The agent to test.
    :param entities: The entities associated with the simulation.
    :param environment: The environment to test against.
    :return: Boolean value indicating the result of the test.
    """

    foods = filter(lambda x: isinstance(x, entity.Food), entities)

    return any([food.body.contains(agent.body) for food in foods])


def holding_food(agent=None, entities=None, environment=None):

    """
    Precondition testing if an agent is holding food.
    :param agent: The agent to test.
    :param entities: The entities associated with the simulation.
    :param environment: The environment to test against.
    :return: Boolean value indicating the result of the test.
    """

    return agent.holding_food
