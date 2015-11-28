import re


class Grammar:
    """ Context Free Grammar """

    NT = "NT"
    T = "T"

    def __init__(self, bnf_file):

        if bnf_file.endswith("pybnf"):

            self.python_mode = True

        else:

            self.python_mode = False

        self.rules = {}
        self.non_terminals, self.terminals = set(), set()
        self.start_rule = None

        self.read_bnf_file(bnf_file)

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

    def generate(self, _input, max_wraps=2):

        """Map input via rules to output. Returns output and used_input"""
        used_input = 0
        wraps = 0
        output = []
        production_choices = []

        unexpanded_symbols = [self.start_rule]

        while wraps < max_wraps and len(unexpanded_symbols) > 0:

            # Wrap
            if used_input % len(_input) == 0 and used_input > 0 and len(production_choices) > 1:

                wraps += 1

            # Expand a production
            current_symbol = unexpanded_symbols.pop(0)

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol[1] != self.NT:

                output.append(current_symbol[0])

            else:

                production_choices = self.rules[current_symbol[0]]

                # Select a production
                current_production = _input[used_input % len(_input)] % len(production_choices)

                # Use an input if there was more then 1 choice
                if len(production_choices) > 1:

                    used_input += 1

                # Derviation order is left to right(depth-first)
                unexpanded_symbols = production_choices[current_production] + unexpanded_symbols

        # Not completly expanded
        if len(unexpanded_symbols) > 0:

            return None, used_input

        output = "".join(output)

        if self.python_mode:

            output = python_filter(output)

        return output, used_input


def python_filter(txt):
    """
    Create correct python syntax.

    We use {: and :} as special open and close brackets, because
    it's not possible to specify indentation correctly in a BNF
    grammar without this type of scheme.
    """

    indent_level = 0
    tmp = txt[:]
    i = 0
    while i < len(tmp):
        tok = tmp[i:i+2]
        if tok == "{:":
            indent_level += 1
        elif tok == ":}":
            indent_level -= 1
        tabstr = "\n" + "  " * indent_level
        if tok == "{:" or tok == ":}":
            tmp = tmp.replace(tok, tabstr, 1)
        i += 1
    # Strip superfluous blank lines.
    txt = "\n".join([line for line in tmp.split("\n")
                     if line.strip() != ""])
    return txt
