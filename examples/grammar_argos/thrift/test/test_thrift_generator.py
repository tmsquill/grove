# Required Imports
import random
from evolution.grammar import Grammar

# Generate random sequence for AST creation.
sequence = [random.randint(0, 128) for _ in xrange(128)]

# Parse the Google Protocol Buffer into a Grammar object.
grammar = Grammar('../foraging.thrift')
ast = grammar.generate(sequence)

print '\nGenerated AST\n'
print ast[0]