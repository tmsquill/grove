import entity as entity
import environment as environment
import simulation as simulation
import utils as utils

import random

# Entity Creation
agents = [entity.SimAgent(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(5)]
nest = entity.Nest(position=(8, 8), size=(4, 4))
food = [entity.Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(10)]

entities = agents + [nest] + food

# Environment Creation
env = environment.Environment()

# Simulation Creation
sim = simulation.Simulation(duration=10, environment=env, entities=entities)

# Execute simulation.
sim.execute()
utils.generate_csv(sim)
