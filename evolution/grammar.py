import random
import re
from types import ModuleType
import google.protobuf.descriptor as des


class Grammar:
    """ Context Free Grammar """

    NT = "NT"
    T = "T"

    def __init__(self, context_free_grammar):

        self.rules = {}
        self.non_terminals, self.terminals = set(), set()
        self.start_rule = None

        if isinstance(context_free_grammar, ModuleType):

            self.pb = context_free_grammar
            self.bnf = False

        else:

            self.read_bnf_file(context_free_grammar)
            self.bnf = True

    def __str__(self):

        return "%s %s %s %s" % (self.terminals, self.non_terminals, self.rules, self.start_rule)

    def read_bnf_file(self, file_name):

        # <.+?> Non greedy match of anything between brackets.
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

    def generate_from_proto(self, in_seq, max_wraps=2):

        """
        Uses reflection to form an AST with a Google Protocol Buffer auto-generated class.
        :param in_seq: The random sequence (list) of integers.
        :param max_wraps: The number of times to wrap the input.
        :return: An AST represented as an instance of a Google Protocol Buffer class.
        """

        used_input = 0
        wraps = 0
        ast = self.pb.Root()
        production_choices = []

        unexpanded_symbols = [(ast, f) for f in ast.DESCRIPTOR.fields]

        iter = 1

        while wraps < max_wraps and len(unexpanded_symbols) > 0:

            # Debugging Print
            print '\nIteration ' + str(iter)
            iter = iter + 1
            print '(Unexpanded Symbols): ' + str(unexpanded_symbols)

            # Wrap around the input.
            if used_input % len(in_seq) == 0 and used_input > 0 and len(production_choices) > 1:

                wraps += 1

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            print '(Current Symbol) Parent: ' + str(current_symbol[0]) + \
                ' Name: ' + str(current_symbol[1].name) + ' Type: ' + str(current_symbol[1].type)

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol[1].type == des.FieldDescriptor.TYPE_ENUM:

                print '(Current Symbol) -> Terminal Symbol'
                print 'Enum Values: ' + str(current_symbol[1].enum_type.values_by_name)
                setattr(current_symbol[0], current_symbol[1].name, random.choice(current_symbol[1].enum_type.values).number)

            # Otherwise the current symbol maps to a non-terminal.
            else:

                print '(Current Symbol) -> Non-Terminal Symbol'

                # Required field (type message).
                if current_symbol[1].label == des.FieldDescriptor.LABEL_REQUIRED:

                    getattr(current_symbol[0], current_symbol[1].name).SetInParent()

                # Repeated field (type message).
                elif current_symbol[1].label == des.FieldDescriptor.LABEL_REPEATED:

                    print 'Fields: ' + str([f for f in current_symbol[0].DESCRIPTOR.fields])

                    getattr(current_symbol[0], current_symbol[1].name).add()

                # Production choices are children of the current symbol.
                production_choices = getattr(self.pb, current_symbol[1].message_type.name).DESCRIPTOR.fields

                print 'Production Choices: ' + str(production_choices)

                # Gather all required productions.
                repeated = [(getattr(current_symbol[0], current_symbol[1].name), _) for _ in production_choices if _.label == des.FieldDescriptor.LABEL_REPEATED]
                unexpanded_symbols = repeated + unexpanded_symbols
                print 'Repeated Productions: ' + str(repeated)

                # Gather all required productions.
                required = [(getattr(current_symbol[0], current_symbol[1].name), _) for _ in production_choices if _.label == des.FieldDescriptor.LABEL_REQUIRED]
                unexpanded_symbols = required + unexpanded_symbols
                print 'Required Productions: ' + str(required)

                # =====

                # Select a production.
                current_production = int(in_seq[used_input % len(in_seq)] % len(production_choices))

                print 'Current Production: ' + str(current_production)

                # Use an input if there was more then 1 choice.
                if len(production_choices) > 1:

                    used_input += 1

                # Chosen production.
                chosen = production_choices[current_production]

                # Derivation order is left to right (depth-first).
                #unexpanded_symbols.insert(0, (getattr(current_symbol[0], current_symbol[1].name), chosen))

        # Not completely expanded.
        if len(unexpanded_symbols) > 0:

            return None, used_input

        return ast, used_input

    def generate_from_bnf(self, _input, max_wraps=2):

        """Map input via rules to output. Returns output and used_input"""
        used_input = 0
        wraps = 0
        output = []
        production_choices = []

        unexpanded_symbols = [self.start_rule]

        while wraps < max_wraps and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if used_input % len(_input) == 0 and used_input > 0 and len(production_choices) > 1:

                wraps += 1

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol[1] != self.NT:

                output.append(current_symbol[0])

            # Otherwise the current symbol maps to a non-terminal.
            else:

                production_choices = self.rules[current_symbol[0]]

                # Select a production.
                current_production = int(_input[used_input % len(_input)] % len(production_choices))

                # Use an input if there was more then 1 choice.
                if len(production_choices) > 1:

                    used_input += 1

                # Derivation order is left to right (depth-first).
                unexpanded_symbols = production_choices[current_production] + unexpanded_symbols

        # Not completely expanded.
        if len(unexpanded_symbols) > 0:

            return None, used_input

        output = "".join(output)

        return output, used_input
