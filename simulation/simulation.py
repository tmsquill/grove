import lookup
import random

import entity as e


class Simulation:

    """
    A simple simulator designed to be used with GESwarm (Grammatical Evolution Swarm). Parse trees containing a set of
    rules dictate the control flow of the simulation. Rules contain a list of preconditions, behaviors, and actions.
    Together these rules may lead to interesting behaviors.

    For more information about GESwarm, see the article (http://dl.acm.org/citation.cfm?id=2463385).
    """

    def __init__(self, duration=500, environment=None, entities=None, parse_tree=None, produce_output=True):

        self.duration = duration
        self.environment = environment
        self.entities = entities
        self.parse_tree = parse_tree
        self.produce_output = produce_output
        self.state_archive = []

    def save_state(self, entity=None):

        """
        Saves the current state of all entities to the state archive.
        :param entity: The entity to add to the state archive
        """

        self.state_archive.append(entity.to_csv())

    def execute(self):

        """
        Executes the simulation, updating entities and saving their states at each
        time step.
        """

        agents = filter(lambda x: isinstance(x, e.SimAgent), self.entities)
        other = filter(lambda x: not isinstance(x, e.SimAgent), self.entities)

        for timestamp in xrange(self.duration):

            for entity in other:

                entity.time = timestamp
                self.save_state(entity)

        # Initial behavioral state for each entity.
        for agent in agents:

            agent.behavior = lookup.b[self.parse_tree.default_behavior.id_behavior]

        while all([agent.time < self.duration for agent in agents]):

            for agent in agents:

                if agent.time >= self.duration:

                    agent.done = True
                    continue

                agent = self.process_rules(agent)

    def process_rules(self, agent):

        """
        Processes the rule set on a given entity.
        :param agent: The agent to evaluate with the rule set.
        :return: The entity, with possible updates.
        """

        hit = False

        for rule in self.parse_tree.rules:

            # Gather all precondition functions contained in the current rule.
            preconditions = [lookup.pc[pc.id_precondition] for pc in rule.preconditions if pc]
            behaviors = [lookup.b[b.id_behavior] for b in rule.behaviors if b]

            # Evaluate the current entity.
            pc_check = all([precondition(agent, self.entities, self.environment) for precondition in preconditions])
            b_check = any([agent.behavior is behavior for behavior in behaviors])

            if pc_check and b_check:

                for action in rule.actions:

                    if random.uniform(0.0, 1.0) <= action.prob:

                        hit = True

                        agent = lookup.b[action.id_action](agent, self.entities, self.environment)
                        agent.behavior = lookup.b[action.id_action]

                        if self.produce_output:

                            self.save_state(agent)

        if not hit:

            agent = agent.behavior(agent, self.entities, self.environment)
            agent.time += 1

            if self.produce_output:

                self.save_state(agent)

        return agent
