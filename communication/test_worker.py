__author__ = 'Troy Squillaci'

import proto.cpfa_pb2 as cpfa_pb2
import zmq
import random
import time
import os
import subprocess

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

def random_cpfa():

    cpfa = cpfa_pb2.Cpfa()
    cpfa.probabilityOfSwitchingToSearching = random.uniform(0, 10)
    cpfa.probabilityOfReturningToNest = random.uniform(0, 10)
    cpfa.uninformedSearchVariation = random.uniform(0, 10)
    cpfa.rateOfInformedSearchDecay = random.uniform(0, 10)
    cpfa.rateOfSiteFidelity = random.uniform(0, 10)
    cpfa.rateOfLayingPheromone = random.uniform(0, 10)
    cpfa.rateOfPheromoneDecay = random.uniform(0, 10)

    return cpfa

os.chdir(os.path.expanduser('~/ARGoS/iAnt-ARGoS-master'))

subprocess.Popen(['./gaworker'], shell=False)

while True:

    cpfa = random_cpfa()

    print str(cpfa)

    time.sleep(3)

    socket.send(cpfa.SerializeToString())

    print '(Master) ' + socket.recv()
