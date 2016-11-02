from simulation.entity import Food, Nest, SimAgent
from simulation.environment import Environment

import simulation.behaviors as behaviors


def test_move_north():

    agent = SimAgent(position=(10, 10))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_north(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[1] == 11 and agent.body.bottom_right.position[1] == 10


def test_move_north_with_food():

    agent = SimAgent(position=(10, 10))
    food = Food(position=(10, 10))
    entities = [agent, food]
    environment = Environment()

    agent = behaviors.pickup_food(agent=agent, entities=entities, environment=environment)
    agent = behaviors.move_north(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[1] == 11 and agent.body.bottom_right.position[1] == 10
    assert food.body.top_left.position[1] == 11 and food.body.bottom_right.position[1] == 10


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


def test_move_north_with_food():

    agent = SimAgent(position=(10, 10))
    food = Food(position=(10, 10))
    entities = [agent, food]
    environment = Environment()

    agent = behaviors.pickup_food(agent=agent, entities=entities, environment=environment)
    agent = behaviors.move_east(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[0] == 11 and agent.body.bottom_right.position[0] == 12
    assert food.body.top_left.position[0] == 11 and food.body.bottom_right.position[0] == 12


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


def test_move_south_with_food():

    agent = SimAgent(position=(10, 10))
    food = Food(position=(10, 10))
    entities = [agent, food]
    environment = Environment()

    agent = behaviors.pickup_food(agent=agent, entities=entities, environment=environment)
    agent = behaviors.move_south(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[1] == 9 and agent.body.bottom_right.position[1] == 8
    assert food.body.top_left.position[1] == 9 and food.body.bottom_right.position[1] == 8


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


def test_move_west_with_food():

    agent = SimAgent(position=(10, 10))
    food = Food(position=(10, 10))
    entities = [agent, food]
    environment = Environment()

    agent = behaviors.pickup_food(agent=agent, entities=entities, environment=environment)
    agent = behaviors.move_west(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[0] == 9 and agent.body.bottom_right.position[0] == 10
    assert food.body.top_left.position[0] == 9 and food.body.bottom_right.position[0] == 10


def test_move_west_out_of_bounds():

    agent = SimAgent(position=(0, 10))
    entities = [agent]
    environment = Environment()

    agent = behaviors.move_west(agent=agent, entities=entities, environment=environment)

    assert agent.body.top_left.position[0] == 0 and agent.body.bottom_right.position[0] == 1


def test_pickup_and_drop_food():

    agent1 = SimAgent(position=(12, 8))
    agent2 = SimAgent(position=(12, 8))
    agent3 = SimAgent(position=(5, 5))
    agent4 = SimAgent(position=(5, 5))
    food1 = Food(position=(12, 8))
    food2 = Food(position=(5, 5))
    nest = Nest(position=(10, 10), size=(4, 4))

    entities = [agent1, agent2, agent3, agent4, food1, food2, nest]

    assert all([agent.holding_food is False for agent in [agent1, agent2, agent3, agent4]])
    assert all([food1.interactable for food in [food1, food2]])

    agent1 = behaviors.pickup_food(agent1, entities, None)
    agent2 = behaviors.pickup_food(agent2, entities, None)
    agent3 = behaviors.pickup_food(agent3, entities, None)
    agent4 = behaviors.pickup_food(agent4, entities, None)

    assert agent1.holding_food is True
    assert agent2.holding_food is False
    assert agent3.holding_food is True
    assert agent4.holding_food is False
    assert all([food1.interactable is False for food in [food1, food2]])

    agent1 = behaviors.drop_food(agent1, entities, None)
    agent2 = behaviors.drop_food(agent2, entities, None)
    agent3 = behaviors.drop_food(agent3, entities, None)
    agent4 = behaviors.drop_food(agent4, entities, None)

    assert all([agent.holding_food is False for agent in [agent1, agent2, agent3, agent4]])
    assert food1.interactable is False
    assert food2.interactable is True
    assert nest.food_count == 1


def test_collect_multiple():

    agent = SimAgent(position=(12, 8))

    food1 = Food(position=(12, 8))
    food2 = Food(position=(12, 7))
    nest = Nest(position=(10, 10), size=(4, 4))

    entities = [agent, food1, food2, nest]

    environment = Environment()

    assert agent.holding_food is False
    assert all([food1.interactable for food in [food1, food2]])

    agent = behaviors.pickup_food(agent, entities, environment)

    assert agent.holding_food is True
    assert food1.interactable is False
    assert food2.interactable is True

    agent = behaviors.drop_food(agent, entities, environment)

    assert agent.holding_food is False
    assert food1.interactable is False
    assert food2.interactable is True

    agent = behaviors.move_south(agent=agent, entities=entities, environment=environment)
    agent = behaviors.pickup_food(agent, entities, environment)

    assert agent.holding_food is True
    assert food1.interactable is False
    assert food2.interactable is False

    agent = behaviors.drop_food(agent, entities, environment)

    assert agent.holding_food is False
    assert food1.interactable is False
    assert food2.interactable is False

    assert nest.food_count == 2


def test_random_walk():

    agent = SimAgent(position=(10, 10))

    entities = [agent]
    environment = Environment()

    agent = behaviors.random_walk(agent, entities, environment)

    assert agent.body.top_left.position[0] == 9 or \
        agent.body.top_left.position[1] == 9 or \
        agent.body.top_left.position[0] == 11 or \
        agent.body.top_left.position[1] == 11
