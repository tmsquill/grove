__author__ = 'Troy Squillaci'

import itertools
import json
import numpy as np
import random
import xmltodict


class AgentDescriptor:

    aid = itertools.count().next

    def __init__(self, config=None):

        if config is None:

            raise Exception

        self.config = config

    def init_agents(self, population):

        agents = []
        obs_agents = []

        for x in xrange(population):

            agent, obs_agent = self.factory()
            mean = float(float(x) / population)

            for idx, param in enumerate(agent.params):

                param = self.config['params_upper_bounds'][idx] * np.random.normal(loc=mean, scale=0.05)
                if param < self.config['params_lower_bounds'][idx]: param = self.config['params_lower_bounds'][idx]
                elif param > self.config['params_upper_bounds'][idx]: param = self.config['params_upper_bounds'][idx]
                agent.params[idx] = param

            print 'Agent ' + str(x) + ' ' + str(agent)
            agents.append(agent)

            for idx, param in enumerate(obs_agent.params):

                param = self.config['obs_params_upper_bounds'][idx] * np.random.normal(loc=mean, scale=0.05)
                if param < self.config['obs_params_lower_bounds'][idx]: param = self.config['obs_params_lower_bounds'][idx]
                elif param > self.config['obs_params_upper_bounds'][idx]: param = self.config['obs_params_upper_bounds'][idx]
                obs_agent.params[idx] = param

            obs_agents.append(obs_agent)

        return agents, obs_agents

    def factory(self):

        id = AgentDescriptor.aid()

        return Agent(self, id), ObstacleAgent(self, id)

    def __str__(self):

        return json.dumps(self.config, sort_keys=True, indent=4)


class Agent(object):

    def __init__(self, descriptor, id):

        self.id = id
        self.config = []
        self.fitness = -1
        self.params = [random.uniform(descriptor.config['params_lower_bounds'][i],
                                      descriptor.config['params_upper_bounds'][i])
                       for i in xrange(descriptor.config['params_len'])]

    def __lt__(self, other):

        return self.fitness < other.fitness

    def __gt__(self, other):

        return self.fitness > other.fitness

    def __str__(self):

        result = ''
        result += 'AID: ' + str(self.id)
        result += ' Fitness: ' + str(self.fitness)

        for idx, param in enumerate(self.params):

            result += ' ' + str(idx) + ': ' + str(param)

        return result

    def update_xml(self, argos_xml):

        with open(argos_xml, 'r') as xml:

            self.config = xmltodict.parse(xml)

        # General
        self.config['argos-configuration']['framework']['experiment']['@random_seed'] = str(random.randint(1, 1000000))

        # iAnt Robots
        self.config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfSwitchingToSearching'] = str(round(self.params[0], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@ProbabilityOfReturningToNest'] = str(round(self.params[1], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@UninformedSearchVariation'] = str(round(self.params[2], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfInformedSearchDecay'] = str(round(self.params[3], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfSiteFidelity'] = str(round(self.params[4], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfLayingPheromone'] = str(round(self.params[5], 5))
        self.config['argos-configuration']['loop_functions']['CPFA']['@RateOfPheromoneDecay'] = str(round(self.params[6], 5))

        with open(argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(self.config, pretty=True))
            xml.truncate()


class ObstacleAgent(object):

    def __init__(self, descriptor, id):

        self.id = id
        self.config = []
        self.fitness = -1
        self.params = []

        for i in xrange(descriptor.config['obs_params_len']):

            lower = descriptor.config['obs_params_lower_bounds'][i]
            upper = descriptor.config['obs_params_upper_bounds'][i]

            param = random.uniform(-upper, upper)

            while abs(param) < lower:

                param = random.uniform(-upper, upper)

            self.params.append(param)

    def __lt__(self, other):

        return self.fitness < other.fitness

    def __gt__(self, other):

        return self.fitness > other.fitness

    def __str__(self):

        result = ''
        result += 'OAID: ' + str(self.id)
        result += ' Fitness: ' + str(self.fitness)

        for idx, param in enumerate(self.params):

            result += ' ' + str(idx) + ': ' + str(param)

        return result

    def update_xml(self, argos_xml):

        with open(argos_xml, 'r') as xml:

            self.config = xmltodict.parse(xml)

        # Obstacles
        self.config['argos-configuration']['arena']['box'][0]['body']['@orientation'] = \
            str(round(self.params[0], 3)) + ',0,0'
        self.config['argos-configuration']['arena']['box'][0]['body']['@position'] = \
            str(round(self.params[1], 3)) + ',' + str(round(self.params[2], 3)) + ',0'

        self.config['argos-configuration']['arena']['box'][1]['body']['@orientation'] = \
            str(round(self.params[3], 3)) + ',0,0'
        self.config['argos-configuration']['arena']['box'][1]['body']['@position'] = \
            str(round(self.params[4], 3)) + ',' + str(round(self.params[5], 3)) + ',0'

        self.config['argos-configuration']['arena']['box'][2]['body']['@orientation'] = \
            str(round(self.params[6], 3)) + ',0,0'
        self.config['argos-configuration']['arena']['box'][2]['body']['@position'] = \
            str(round(self.params[7], 3)) + ',' + str(round(self.params[8], 3)) + ',0'

        self.config['argos-configuration']['arena']['box'][3]['body']['@orientation'] = \
            str(round(self.params[9], 3)) + ',0,0'
        self.config['argos-configuration']['arena']['box'][3]['body']['@position'] = \
            str(round(self.params[10], 3)) + ',' + str(round(self.params[11], 3)) + ',0'

        with open(argos_xml, 'w') as xml:

            xml.write(xmltodict.unparse(self.config, pretty=True))
            xml.truncate()
