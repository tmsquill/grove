from simulation.entity import Agent
from simulation.environment import Environment

import simulation.behaviors as behaviors


class TestBehaviors:

    def test_move_north_out_of_bounds(self):

        agent = Agent(position=(10, 0))
        environment = Environment()

        agent = behaviors.move_north(agent, environment=environment)

        assert agent.body.top_left().y == 0

    def test_move_east_out_of_bounds(self):

        agent = Agent(position=(19, 10))
        environment = Environment()

        agent = behaviors.move_east(agent, environment=environment)

        assert agent.body.bottom_right().x == 20

    def test_move_south_out_of_bounds(self):

        agent = Agent(position=(10, 19))
        environment = Environment()

        agent = behaviors.move_south(agent, environment=environment)

        assert agent.body.bottom_right().y == 20

    def test_move_west_out_of_bounds(self):

        agent = Agent(position=(0, 10))
        environment = Environment()

        agent = behaviors.move_west(agent, environment=environment)

        assert agent.body.top_left().x == 0

    def test_pickup_food(self):

        agent = Agent()
        agent.holding_food = False

        agent = behaviors.pickup_food(agent)

        assert agent.holding_food

    def test_drop_food(self):

        agent = Agent()
        agent.holding_food = True

        agent = behaviors.drop_food(agent)

        assert not agent.holding_food

    def test_random_walk(self):

        agent = Agent(position=(10, 10))
        environment = Environment()

        agent = behaviors.random_walk(agent, environment)

        assert True
