from entity import SimAgent, Food, Nest
from environment import Environment

import random
import simulation.preconditions as pc


class TestPreConditions:

    env = Environment()

    nest = Nest(position=(8, 8), size=(4, 4))
    food = [Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(10)]
    entities = food + [nest, Food(position=(6, 6))]

    def test_on_border(self):

        agent = SimAgent(position=(0, 5))

        assert pc.on_border(agent, self.entities, self.env)

    def test_on_nest(self):

        agent = SimAgent(position=(10, 10))

        assert pc.on_nest(agent, self.entities, self.env)

    def test_on_food(self):

        agent = SimAgent(position=(6, 6))

        assert pc.on_food(agent, self.entities, self.env)

    def test_holding_food(self):

        agent = SimAgent()

        agent.holding_food = True

        assert pc.holding_food(agent, self.entities, self.env)