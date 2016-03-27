import random
import re
import json
from types import ModuleType
import google.protobuf.descriptor as des

# TODO - Begin Debugging
import google.protobuf.text_format as tf
from google.protobuf.descriptor import FieldDescriptor
# TODO - End Debugging


class Grammar:
    """
    Context free grammar that can be defined by:
    - Python functions.
    - Google Protocol Buffers.
    - Backus-Naur Form
    """

    NT = "NT"
    T = "T"

    def __init__(self, context_free_grammar):

        self.rules = {}
        self.non_terminals = set()
        self.terminals = set()
        self.start_rule = None

        # The context-free grammar is a Google Protocol Buffer module.
        if isinstance(context_free_grammar, ModuleType):

            self.pb = context_free_grammar
            self.bnf = False

        # The context-free grammar is a Backus-Naur Form file.
        else:

            self.read_bnf_file(context_free_grammar)
            self.bnf = True

    def __str__(self):

        return 'Non-Terminal Symbols -> ' + str(self.non_terminals) + \
        '\nTerminal Symbols     -> ' + str(self.terminals) + \
        '\nRules                -> \n' + str(json.dumps(self.rules, indent=4, sort_keys=True)) + \
        '\nStart Rule           -> ' + str(self.start_rule)

    def read_bnf_file(self, file_name):

        # <.+?> is a non-greedy match of anything between brackets.
        non_terminal_pattern = "(<.+?>)"
        rule_separator = "::="
        production_separator = "|"

        # Read the grammar file.
        for line in open(file_name, 'r'):

            if not line.startswith("#") and line.strip() != "":

                # Split rules. Everything must be on one line.
                # Ensure the rule separator (that is ::=) exists on the line.
                if line.find(rule_separator):

                    lhs, productions = line.split(rule_separator)
                    lhs = lhs.strip()

                    # Verify that the non-terminal pattern is valid.
                    if not re.search(non_terminal_pattern, lhs):

                        raise ValueError("lhs is not a NT:", lhs)

                    self.non_terminals.add(lhs)

                    # The first non-terminal (on first line) becomes the start rule.
                    if self.start_rule is None:

                        self.start_rule = (lhs, self.NT)

                    # Find terminals.
                    tmp_productions = []

                    for production in [production.strip() for production in productions.split(production_separator)]:

                        tmp_production = []

                        # Production is termimal.
                        if not re.search(non_terminal_pattern, production):

                            self.terminals.add(production)
                            tmp_production.append((production, self.T))

                        # Production is non-terminal.
                        else:

                            # Match non terminal or terminal pattern
                            for value in re.findall("<.+?>|[^<>]*", production):

                                if value != '':

                                    if not re.search(non_terminal_pattern, value):
                                        symbol = (value, self.T)
                                        self.terminals.add(value)
                                    else:
                                        symbol = (value, self.NT)

                                    tmp_production.append(symbol)
                        tmp_productions.append(tmp_production)

                    # Create a rule
                    if lhs not in self.rules:

                        self.rules[lhs] = tmp_productions

                    else:

                        raise ValueError("lhs should be unique", lhs)

                else:

                    raise ValueError("Each rule must be on one line")

    def generate(self, in_seq, max_wraps=2):

        if not self.bnf:

            return self.generate_from_proto(in_seq, max_wraps)

        else:

            return self.generate_from_bnf(in_seq, max_wraps)

    def generate_from_proto(self, in_seq, wraps=2):

        """
        Uses reflection to form an AST with a Google Protocol Buffer auto-generated class.
        :param in_seq: The random sequence (list) of integers.
        :param wraps: The number of times to wrap the input.
        :return: An AST represented as an instance of a Google Protocol Buffer class.
        """

        print 'Input Sequence     -> ' + str(in_seq)

        used_in_seq = 0
        pb = self.pb.Root()
        production_choices = []
        unexpanded_symbols = [(pb, field) for field in pb.DESCRIPTOR.fields]

        while 0 < wraps and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if used_in_seq % len(in_seq) == 0 and used_in_seq > 0 and len(production_choices) > 1:

                wraps += 1

            # Expand a production.
            print '\nUnexpanded Symbols   -> ' + str(unexpanded_symbols)
            current_symbol = unexpanded_symbols.pop(0)
            print 'Current Symbol     -> ' + str(current_symbol)

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol == des.FieldDescriptor.TYPE_ENUM:

                print '<-- Terminal Symbol --->'
                setattr(current_symbol[0], current_symbol[1].name, random.choice(current_symbol[1].enum_type.values).number)

            # Otherwise the current symbol maps to a non-terminal.
            else:

                print '<-- Non-Terminal Symbol --->'

                from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

                print 'getattr(' + str(type(current_symbol[0])) + ', ' + current_symbol[1].name + ')'

                # Required field.
                if current_symbol[1].label == des.FieldDescriptor.LABEL_REQUIRED:

                    getattr(current_symbol[0], current_symbol[1].name).SetInParent()

                # Repeated field.
                elif current_symbol[1].label == des.FieldDescriptor.LABEL_REPEATED:

                    print type(current_symbol[0])

                    if isinstance(current_symbol[0], RepeatedCompositeFieldContainer):

                        current_symbol[0].add()

                    else:

                        getattr(current_symbol[0], current_symbol[1].name).add()

                # Production choices are children of the current symbol.
                production_choices = getattr(self.pb, current_symbol[1].message_type.name).DESCRIPTOR.fields
                print 'Production Choices -> ' + str(production_choices)

                # Gather all required productions.
                repeated = [(getattr(current_symbol[0], current_symbol[1].name), _) for _ in production_choices if _.label == des.FieldDescriptor.LABEL_REPEATED]
                unexpanded_symbols = repeated + unexpanded_symbols
                print '(Repeated Productions) -> ' + str(repeated)

                from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

                # Gather all required productions.
                if isinstance(current_symbol[0], RepeatedCompositeFieldContainer):

                    required = 0

                else:

                    required = [(getattr(current_symbol[0], current_symbol[1].name), _) for _ in production_choices if _.label == des.FieldDescriptor.LABEL_REQUIRED]
                    unexpanded_symbols = required + unexpanded_symbols

                print '(Required Productions) -> ' + str(required)

                # Select a production.
                current_production = int(in_seq[used_in_seq % len(in_seq)] % len(production_choices))
                print 'Current Production -> ' + str(production_choices[current_production])

                # Use an input if there was more then 1 choice.
                if len(production_choices) > 1:

                    used_in_seq += 1

                # Chosen production.
                chosen = production_choices[current_production]

                # Derivation order is left to right (depth-first).
                #unexpanded_symbols.insert(0, (getattr(current_symbol[0], current_symbol[1].name), chosen))

        # Not completely expanded.
        if len(unexpanded_symbols) > 0:

            return None, used_in_seq

        return output, used_in_seq

    def generate_from_bnf(self, in_seq, wraps=2):

        """
        Forms an AST from a random input sequence and a Backus-Naur Form file.
        :param in_seq: The random sequence (list) of integers.
        :param wraps: The number of times to wrap the input.
        :return: An AST represented as an XML file.
        """

        print 'Input Sequence     -> ' + str(in_seq)

        used_in_seq = 0
        output = []
        production_choices = []
        unexpanded_symbols = [self.start_rule]

        while 0 < wraps and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if used_in_seq % len(in_seq) == 0 and used_in_seq > 0 and len(production_choices) > 1:

                wraps -= 1

            # Expand a production.
            # TODO: print '\nUnexpanded Symbols -> ' + str(unexpanded_symbols)
            current_symbol = unexpanded_symbols.pop(0)
            # TODO: print 'Current Symbol     -> ' + str(current_symbol)

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol[1] != self.NT:

                # TODO: print '<-- Terminal Symbol --->'
                output.append(current_symbol[0])

            # Otherwise the current symbol maps to a non-terminal.
            else:

                # TODO: print '<-- Non-Terminal Symbol --->'

                production_choices = self.rules[current_symbol[0]]
                # TODO: print 'Production Choices -> ' + str(production_choices)

                # Select a production.
                current_production = int(in_seq[used_in_seq % len(in_seq)] % len(production_choices))
                # TODO: print 'Current Production -> ' + str(production_choices[current_production])

                # Use an input if there was more then 1 choice.
                if len(production_choices) > 1:

                    used_in_seq += 1

                # Derivation order is left to right (depth-first).
                unexpanded_symbols = production_choices[current_production] + unexpanded_symbols

            # TODO: print 'Output             -> ' + str(output)

        # TODO: Determine correct action here.
        # Not completely expanded.
        # if len(unexpanded_symbols) > 0:
        #
        #     raise ValueError('Unable to fully expand grammar.')

        return output, used_in_seq
