import lookup

class Simulation:

    def __init__(self, duration=10, environment=None, entities=None, ast=None, produce_output=True):

        self.duration = duration
        self.environment = environment
        self.entities = entities
        self.ast = ast
        self.produce_output = produce_output
        self.state_archive = []

    def save_state(self, timestamp=None):

        """
        Saves the current state of all entities to the state archive.
        :param timestamp: The time step (current time step).
        """

        for entity in self.entities:

            self.state_archive.append([timestamp] + entity.to_csv())

    def execute(self):

        """
        Executes the simulation, updating entities and saving their states at each
        time step.
        """

        for timestamp in xrange(self.duration):

            for entity in self.entities:

                # New behavior needs selected.
                if entity.behavior[1] == 0:

                    entity = self.process_rules(entity)

                # Continue with current behavior.
                else:

                    entity = entity.behavior[0](entity, self.entities, self.environment)

                entity.behavior[1] -= 1

            self.save_state(timestamp)

    def process_rules(self, entity):

        """
        Processes the ruleset on a given entity.
        :param entity: The entity to evaluate with the ruleset.
        :return: The entity, with possible updates.
        """

        for rule in self.ast.rules:

            # Gather all precondition functions contained in the current rule.
            # TODO - Consider using thrift services to avoid lookup tables.
            preconditions = [lookup.pc[precondition] for precondition in rule.preconditions]

            # Evaluate the current entity.
            pc_check = all([precondition(entity, self.entities, self.environment) for precondition in preconditions])
            b_check = [entity.behavior[0] in lookup.b[behavior] for behavior in rule.behaviors]

            if pc_check and b_check:

                actions = [lookup.a[action] for action in rule.actions]

                for action in actions:

                    entity = action(entity, self.entities, self.environment)

        return entity
