import inspect
import utils

from ete3 import Tree, TreeNode
from thriftpy.protocol import TBinaryProtocol
from thriftpy.transport import TMemoryBuffer


class ParseTree:

    def __init__(self, grammar=None, genotype=None, *args, **kwargs):

        self.grammar = grammar
        self.genotype = genotype
        self.used_genes = 0
        self.wraps = 2
        self.base = Tree()

        if grammar.representation == 'bnf':

            self.root = self.base.add_child(child=TreeNode(name='Root'))

        elif grammar.representation == 'thrift':

            self.root = self.base.add_child(TreeNode(name=grammar.rules.Root.__name__))
            self.root.add_features(obj=grammar.rules.Root(), codon_index=None, codon_pick=None)

    def __str__(self):

        return self.root.get_ascii(show_internal=True)

    def generate(self):

        """
        Generates a parse tree. The generation type depends on the representation of the grammar
        object (BNF, Proto, Thrift).
        :return: The generated parse tree built with the input sequence.
        """

        getattr(self, 'generate_from_' + self.grammar.representation)()

    def generate_from_bnf(self):

        """
        Forms a parse tree from a Backus-Naur Form grammar and a genotype.
        :return: An parse tree represented as a list.
        """

        production_choices = []
        unexpanded_symbols = [self.start_rule]

        while 0 < self.wraps and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if self.used_genes % len(self.genotype) == 0 and self.used_genes > 0 and len(production_choices) > 1:

                self.wraps -= 1

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol[1] != self.NT:

                self.root.append(current_symbol[0])

            # Otherwise the current symbol maps to a non-terminal.
            else:

                production_choices = self.rules[current_symbol[0]]

                # Select a production.
                current_production = int(self.genotype[self.used_genes % len(self.genotype)] % len(production_choices))

                # Use an input if there was more then 1 choice.
                if len(production_choices) > 1:

                    self.used_genes += 1

                # Derivation order is left to right (depth-first).
                unexpanded_symbols = production_choices[current_production] + unexpanded_symbols

    def generate_from_thrift(self):

        """
        Uses reflection to form a parse tree with an Apache Thrift auto-generated class and genotype.
        :return: A parse tree represented as an instance of a Apache Thrift class.
        """

        production_choices = []
        unexpanded_symbols = utils.discover_children(self.root)

        while self.wraps > 0 and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if self.used_genes % len(self.genotype) == 0 and self.used_genes > 0 and len(production_choices) > 1:

                self.wraps -= 1

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            # Instantiate current symbol, if able.
            if inspect.isclass(current_symbol.t_type):

                current_symbol.add_features(obj=current_symbol.t_type())

                if getattr(current_symbol.t_parent, current_symbol.t_name) is None:

                    setattr(current_symbol.t_parent, current_symbol.t_name, current_symbol.obj)

            # Non-terminal symbol (List).
            if isinstance(current_symbol.t_type, tuple):

                if getattr(current_symbol.t_parent, current_symbol.t_name) is None:

                    setattr(current_symbol.t_parent, current_symbol.t_name, list())

                production_choices = utils.extract_list_productions(current_symbol)
                amount = int(self.genotype[self.used_genes % len(self.genotype)] % 10)

                self.used_genes += 1

                for _ in xrange(amount):

                    unexpanded_symbols.insert(0, production_choices)

            # Non-terminal symbol (List Element)
            elif isinstance(getattr(current_symbol.t_parent, current_symbol.t_name), list):

                setattr(current_symbol.t_parent, current_symbol.t_name, getattr(current_symbol.t_parent, current_symbol.t_name) + [current_symbol.obj])

                production_choices = utils.discover_children(current_symbol)

                # Required fields.
                unexpanded_symbols = production_choices + unexpanded_symbols

            # Non-terminal symbol.
            elif hasattr(current_symbol.obj, 'thrift_spec') and not isinstance(getattr(current_symbol.t_parent, current_symbol.t_name), list):

                production_choices = utils.discover_children(current_symbol)

                # Required fields.
                unexpanded_symbols = production_choices + unexpanded_symbols

            # Terminal symbol.
            else:

                attrs = [attr for attr in dir(current_symbol.obj) if not callable(attr) and not attr.startswith('_')]

                chosen_name = attrs[int(self.genotype[self.used_genes % len(self.genotype)] % len(attrs))]
                chosen_value = getattr(current_symbol.obj, chosen_name)

                current_symbol.add_child(TreeNode(name=chosen_name))
                setattr(current_symbol.t_parent, current_symbol.t_name, chosen_value)
                self.used_genes += 1

    def serialize(self):

        """
        Serializes a parse tree into binary.
        :param parse_tree: The parse tree to serialize.
        :return: The serialized parse tree.
        """

        transport = TMemoryBuffer()
        protocol = TBinaryProtocol(transport)
        self.root.obj.write(protocol)
        return transport.getvalue()
