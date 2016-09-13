import re
import thriftpy


class Grammar:

    """
    Context free grammar that can be defined by:
    - Python functions.
    - Google Protocol Buffers.
    - Backus-Naur Form
    """

    NT = "NT"
    T = "T"

    def __init__(self, grammar_file):

        self.rules = {}
        self.non_terminals = set()
        self.terminals = set()
        self.start_rule = ''

        # The context-free grammar is a Backus-Naur Form file.
        if grammar_file.endswith('.bnf'):

            self.rules = load_bnf(grammar_file)
            self.representation = 'bnf'

        # The context-free grammar is a FlatBuffers file.
        elif grammar_file.endswith('.fbs'):

            self.rules = load_fbs(grammar_file)
            self.representation = 'fbs'

        # The context-free grammar is a Apache Thrift file.
        elif grammar_file.endswith('.thrift'):

            self.rules = load_thrift(grammar_file)
            self.representation = 'thrift'

        else:

            raise ValueError('grammar file is invalid', grammar_file)


def load_bnf(self, grammar_file):

    # <.+?> is a non-greedy match of anything between brackets.
    non_terminal_pattern = "(<.+?>)"
    rule_separator = "::="
    production_separator = "|"

    # Read the grammar file.
    for line in open(grammar_file, 'r'):

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


def load_fbs(grammar_file=None):

    """
    Loads and compiles a Google Protocol Buffers file into a module.
    :param grammar_file: The file path to the Google Protocol Buffers file.
    :return: The compiled module.
    """

    import os
    import subprocess

    output = subprocess.check_output(['flatc', '--python', grammar_file])

    if not output == '':

        raise IOError('incorrect file path to formal grammar')
        

def load_thrift(grammar_file=None):

    """
    Loads and compiles an Apache Thrift file into a module.
    :param grammar_file: The file path to the Apache Thrift file.
    :return: The compiled module.
    """

    import os

    return thriftpy.load(grammar_file, module_name=os.path.splitext(os.path.basename(grammar_file))[0] + '_thrift')
