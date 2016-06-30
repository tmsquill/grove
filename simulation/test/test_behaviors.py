from simulation.entity import Food, Nest, SimAgent
from simulation.environment import Environment

import simulation.behaviors as behaviors


def test_move_north():

    agent = SimAgent(position=(10, 10))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_north(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[1] == 11 and agent.body.bottom_right.position[1] == 10


def test_move_north_out_of_bounds():

    agent = SimAgent(position=(10, 20))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_north(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[1] == 20 and agent.body.bottom_right.position[1] == 19


def test_move_east():

    agent = SimAgent(position=(10, 10))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_east(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[0] == 11 and agent.body.bottom_right.position[0] == 12


def test_move_east_out_of_bounds():

    agent = SimAgent(position=(20, 10))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_east(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[0] == 20 and agent.body.bottom_right.position[0] == 21


def test_move_south():

    agent = SimAgent(position=(10, 10))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_south(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[1] == 9 and agent.body.bottom_right.position[1] == 8


def test_move_south_out_of_bounds():

    agent = SimAgent(position=(10, 0))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_south(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[1] == 0 and agent.body.bottom_right.position[1] == -1


def test_move_west():

    agent = SimAgent(position=(10, 10))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_west(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[0] == 9 and agent.body.bottom_right.position[0] == 10


def test_move_west_out_of_bounds():

    agent = SimAgent(position=(0, 10))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_west(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[0] == 0 and agent.body.bottom_right.position[0] == 1


def test_pickup_food():

    agent1 = SimAgent(position=(7, 7))
    agent2 = SimAgent(position=(8, 8))
    food = Food(position=(7, 7))

    entities = [agent1, agent2, food]

    agent1 = behaviors.pickup_food(agent1, entities, None)
    agent2 = behaviors.pickup_food(agent2, entities, None)

    assert agent1.holding_food is True
    assert agent2.holding_food is False


def test_drop_food():

    agent1 = SimAgent(holding_food=True, position=(12, 8))
    agent2 = SimAgent(holding_food=True, position=(5, 5))
    nest = Nest(position=(10, 10), size=(4, 4))

    entities = [agent1, agent2, nest]

    agent1 = behaviors.drop_food(agent1, entities, None)
    agent2 = behaviors.drop_food(agent2, entities, None)

    assert agent1.holding_food is False
    assert agent2.holding_food is True


def test_random_walk():

    agent = SimAgent(position=(10, 10))

    entities = [agent]
    environment = Environment()

    agent = behaviors.random_walk(agent, entities, environment)

    assert agent.body.top_left.position[0] == 9 or agent.body.top_left.position[1] == 9 or agent.body.top_left.position[0] == 11 or agent.body.top_left.position[1] == 11
