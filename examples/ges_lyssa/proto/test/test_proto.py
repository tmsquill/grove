# Required Imports
import random

from grammar import Grammar
# Google Protocol Buffer
import examples.grammar_argos.proto.foraging_pb2 as pb
import google.protobuf.text_format as tf

# Generate random sequence for AST creation.
sequence = [random.randint(0, 128) for _ in xrange(128)]

# Parse the Google Protocol Buffer into a Grammar object.
grammar = Grammar(pb)
ast = grammar.generate(sequence)

print '\nGenerated AST\n'
print tf.MessageToString(ast[0])
