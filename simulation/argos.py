__author__ = 'Troy Squillaci'

import re
import subprocess


def argos(argos_xml=None, iant_agent=None, obs_agent=None):

    iant_agent.execute_fitness(argos_xml)
    obs_agent.execute_fitness(argos_xml)

    output = subprocess.check_output(['argos3 -n -c ' + argos_xml], shell=True, stderr=subprocess.STDOUT)
    result = re.search(r'\s(\d+),\s(\d+),\s(\d+)', output)
    iant_agent.fitness = float(float(result.group(1)) / 256)
    obs_agent.fitness = 1 - iant_agent.fitness

    return iant_agent, obs_agent