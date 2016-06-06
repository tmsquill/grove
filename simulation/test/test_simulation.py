import environment as environment
import entity as entity
import simulation as simulation
import random

# Create the entities for the simulation.
agents = [entity.SimAgent(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(5)]
nest = entity.Nest(position=(8, 8), size=(4, 4))
food = [entity.Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(10)]

entities = agents + [nest] + food

# Create the environment for the simulation.
env = environment.Environment()

# Create and execute the simulation.
sim = simulation.Simulation(environment=env, entities=entities)
sim.execute()
