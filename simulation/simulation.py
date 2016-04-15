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

            for entity in self.entities:

                # New behavior needs selected.
                if entity.behavior[1] == 0:

                    self.process_rules(entity)

                # Continue with current behavior.
                else:

                    entity = entity.behavior[0](entity, self.entities, self.environment)

                entity.behavior[1] -= 1

            # # ---
            # import entity
            # import random
            #
            # agents = [entity.Agent(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(5)]
            # nest = entity.Nest(position=(8, 8), size=(4, 4))
            # food = [entity.Food(position=(random.randint(0, 20), random.randint(0, 20))) for _ in xrange(10)]
            #
            # self.entities = agents + [nest] + food
            # # ---
            #
            # self.save_state(timestamp)
            #
            # self.pre_step()
            # self.step()
            # self.post_step()

    def process_rules(self, entity):

        """
        Processes the ruleset on a given entity.
        :param entity: The entity to evaluate with the ruleset.
        :return: The entity, with possible updates.
        """

        for rule in self.ast.rules:

            # Gather all preconditions functions contained in the current rule.
            # TODO - Consider using thrift services to avoid lookup tables.
            preconditions = [lu_precondition[precondition] for precondition in rule.preconditions]

            # Evaluate the current entity.
            if all([precondition(entity, self.entities, self.environment) for precondition in preconditions]):

                pass


# TODO - Replace this with thrift services.
import preconditions as pc

lu_precondition = {
    0: pc.holding_food,
    1: pc.on_border,
    2: pc.on_nest
}