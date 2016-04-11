from simulation.entity import Agent, Food, Nest
from simulation.environment import Environment

import random
import simulation.preconditions as pc


class TestPreConditions:

    env = Environment()

    nest = Nest(position=(8, 8), size=(4, 4))
    food = [Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(10)]
    entities = food + [nest, Food(position=(6, 6))]

    def test_on_border(self):

        agent = Agent(position=(0, 5))

        assert pc.on_border(agent, self.entities, self.env)

    def test_on_nest(self):

        agent = Agent(position=(10, 10))

        assert pc.on_nest(agent, self.entities, self.env)

    def test_on_food(self):

        agent = Agent(position=(6, 6))

        assert pc.on_food(agent, self.entities, self.env)

    def test_holding_food(self):

        agent = Agent()

        agent.holding_food = True

        assert pc.holding_food(agent, self.entities, self.env)