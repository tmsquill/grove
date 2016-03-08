class Simulation:

    def __init__(self, duration=10, environment=None, entities=None, ast=None, produce_output=True):

        self.duration = duration
        self.environment = environment
        self.entities = entities
        self.ast = ast
        self.produce_output = produce_output
        self.state_archive = []

    def save_state(self, timestamp=None):

        for entity in self.entities:

            self.state_archive.append([timestamp] + entity.to_csv())

    def execute(self):

        for timestamp in xrange(self.duration):

            # ---
            import entity
            import random

            agents = [entity.Agent(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(5)]
            nest = entity.Nest(position=(8, 8), size=(4, 4))
            food = [entity.Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(10)]

            self.entities = agents + [nest] + food
            # ---

            self.save_state(timestamp)

            self.pre_step()
            self.step()
            self.post_step()

    def pre_step(self):

        pass

    def step(self):

        for entity in self.entities:

            pass

    def post_step(self):

        pass
