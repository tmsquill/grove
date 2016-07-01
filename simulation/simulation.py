import lookup
import random

import entity as e


class Simulation:

    def __init__(self, duration=1000, environment=None, entities=None, parse_tree=None, produce_output=True):

        self.duration = duration
        self.environment = environment
        self.entities = entities
        self.parse_tree = parse_tree
        self.produce_output = produce_output
        self.state_archive = []

    def save_state(self, entity=None):

        """
        Saves the current state of all entities to the state archive.
        :param timestamp: The time step (current time step).
        """

        self.state_archive.append(entity.to_csv())

    def execute(self):

        """
        Executes the simulation, updating entities and saving their states at each
        time step.
        """

        agents = filter(lambda x: isinstance(x, e.SimAgent), self.entities)

        # Initial behavioral state for each entity.
        for agent in agents:

            agent.behavior = lookup.b[self.parse_tree.default_behavior.id_behavior]

        while not all([agent.done for agent in agents]):

            for agent in agents:

                if agent.time > self.duration:

                    agent.done = True
                    continue

                agent = self.process_rules(agent)

                agent.time += 1


        # for timestamp in xrange(self.duration):
        #
        #     for entity in self.entities:
        #
        #         # TODO - May include all entities in the future.
        #         if not isinstance(entity, e.SimAgent):
        #
        #             continue
        #
        #         # New behavior needs selected.
        #         if entity.behavior[1] == 0:
        #
        #             entity = self.process_rules(entity)
        #
        #         # Execute the current behavior.
        #         else:
        #
        #             # entity = entity.behavior[0](entity, self.entities, self.environment)
        #             entity.behavior[1] -= 1
        #
        #     if self.produce_output:
        #
        #         self.save_state(timestamp)

    def process_rules(self, entity):

        """
        Processes the ruleset on a given entity.
        :param entity: The entity to evaluate with the ruleset.
        :return: The entity, with possible updates.
        """

        for rule in self.parse_tree.rules:

            # TODO - Consider using thrift services to avoid lookup tables.
            # Gather all precondition functions contained in the current rule.
            preconditions = [lookup.pc[precondition.id_precondition] for precondition in rule.preconditions if precondition]
            behaviors = [lookup.b[behavior.id_behavior] for behavior in rule.behaviors if behavior]

            # Evaluate the current entity.
            pc_check = all([precondition(entity, self.entities, self.environment) for precondition in preconditions])
            b_check = any([entity.behavior is behavior for behavior in behaviors])

            if pc_check and b_check:

                for action in rule.actions:

                    if random.uniform(0.0, 1.0) <= action.prob:

                        entity = lookup.b[action.id_action](entity, self.entities, self.environment, self)
                        entity.behavior = lookup.b[action.id_action]

        return entity
