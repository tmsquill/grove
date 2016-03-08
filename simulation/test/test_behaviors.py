from simulation.entity import Agent
from simulation.environment import Environment

import simulation.behaviors as behaviors


class TestBehaviors:

    def test_move_north_out_of_bounds(self):

        agent = Agent(position=(10, 0))
        environment = Environment()

        agent = behaviors.move_north(agent, environment)

        assert agent.body.top_left().y == 0

    def test_move_east_out_of_bounds(self):

        agent = Agent(position=(19, 10))
        environment = Environment()

        agent = behaviors.move_east(agent, environment)

        assert agent.body.bottom_right().x == 20

    def test_move_south_out_of_bounds(self):

        agent = Agent(position=(10, 19))
        environment = Environment()

        agent = behaviors.move_south(agent, environment)

        assert agent.body.bottom_right().y == 20

    def test_move_west_out_of_bounds(self):

        agent = Agent(position=(0, 10))
        environment = Environment()

        agent = behaviors.move_west(agent, environment)

        assert agent.body.top_left().x == 0

    def test_pickup_food(self):

        pass

    def test_drop_food(self):

        pass
