__author__ = 'Troy Squillaci'

from agent import Agent, AgentDescriptor

import random
import re
import subprocess
import xmltodict


class ARGoSAgentDescriptor(AgentDescriptor):

    def __init__(self, argos_xml):

        super(ARGoSAgentDescriptor, self).__init__()

        self.argos_xml = argos_xml

    def init_agents(self):

        agents = [ARGoSAgent(self) for agent in xrange(self.agents)]

        print 'Agent Initialization'

        for agent in agents:
            print str(agent)

        return agents

    def factory(self):

        return ARGoSAgent(self)


class ARGoSAgent(Agent):

    def __init__(self, descriptor):

        super(ARGoSAgent, self).__init__()

        lower_bounds = descriptor.params_lower_bounds
        upper_bounds = descriptor.params_upper_bounds
        self.params = [random.uniform(lower_bounds[i], upper_bounds[i]) for i in xrange(descriptor.params_len)]

        self.argos_xml = descriptor.argos_xml

        with open(self.argos_xml, 'r') as xml:

            self.config = xmltodict.parse(xml)

    def run(self):

        self.config['argos-configuration']['framework']['experiment']['@random_seed'] = str(random.randint(1, 1000000))
        self.config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfSwitchingToSearching'] = str(round(self.params[0], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfReturningToNest'] = str(round(self.params[1], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@UninformedSearchVariation'] = str(round(self.params[2], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfInformedSearchDecay'] = str(round(self.params[3], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfSiteFidelity'] = str(round(self.params[4], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfLayingPheromone'] = str(round(self.params[5], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfPheromoneDecay'] = str(round(self.params[6], 5))

        with open(self.argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(self.config, pretty=True))
            xml.truncate()

        output = subprocess.check_output(['argos3 -n -c ' + self.argos_xml], shell=True, stderr=subprocess.STDOUT)

        result = re.search(r'\s(\d+),\s(\d+),\s(\d+)', output)

        self.fitness = float(float(result.group(1)) / 256)
