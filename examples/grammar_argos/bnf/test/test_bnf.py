# Required Imports
import random

from grammar import Grammar

# Backus-Naur Form
bnf = '../foraging.bnf'

# Generate random sequence for AST creation.
sequence = [random.randint(0, 128) for _ in xrange(128)]

# Parse the Google Protocol Buffer into a Grammar object.
grammar = Grammar(bnf)

ast = grammar.generate(sequence)

print '\nGenerated AST\n'
print ast
