__author__ = 'Troy Squillaci'


def extract_by_agent(generations=None):

    extracted = [[] for sentinel in xrange(len(generations[0].agents[0]))]

    for generation in generations:

        for idx, agent_set in enumerate(generation.agents):

            extracted[idx].append(agent_set)

    return extracted
