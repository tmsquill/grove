# Required Imports
import random
from evolution.grammar import Grammar

# Google Protocol Buffer
import examples.grammar_argos.proto.ast_pb2 as pb
import google.protobuf.text_format as tf

# Generate random sequence for AST creation.
#sequence = [random.randint(0, 128) for _ in xrange(128)]
sequence = [0, 11, 127, 45, 38, 71, 16, 104, 124, 80, 31, 48, 64, 119, 43, 25, 24, 34, 116, 34, 56, 14, 82, 127, 89, 77, 125, 96, 20, 24, 69, 114, 50, 20, 93, 35, 66, 10, 44, 108, 63, 120, 30, 120, 124, 75, 65, 112, 95, 79, 54, 0, 4, 87, 103, 118, 100, 65, 105, 117, 101, 120, 126, 101, 61, 30, 17, 76, 99, 60, 24, 59, 108, 27, 79, 12, 110, 50, 31, 98, 38, 96, 26, 114, 65, 95, 18, 103, 109, 109, 103, 2, 82, 57, 30, 105, 43, 13, 1, 33, 44, 99, 123, 27, 48, 95, 11, 90, 60, 22, 79, 70, 53, 2, 73, 83, 25, 58, 66, 60, 107, 109, 99, 66, 80, 23, 10, 114]

# Parse the Google Protocol Buffer into a Grammar object.
grammar = Grammar(pb)
ast = grammar.generate(sequence)

print '\nGenerated AST\n'
print tf.MessageToString(ast[0])
