import random
import simple_pb2 as pb
from evolution.grammar import Grammar
import google.protobuf.text_format as tf
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

with PyCallGraph(output=GraphvizOutput()):

    sequence = [random.randint(0, 128) for _ in xrange(128)]

    parsed = Grammar(pb)
    ast = parsed.generate(sequence)
    print tf.MessageToString(ast[0])
