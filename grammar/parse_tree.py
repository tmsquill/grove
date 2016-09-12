import constraint
import inspect
import utils

from ete3 import Tree, TreeNode
from grove import config, logger
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

        log = config.grove_config['logging']['grammar']

        if log:

            logger.log.debug('Input Sequence     -> ' + str(self.genotype))

        production_choices = []
        unexpanded_symbols = [self.start_rule]

        while 0 < self.wraps and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if self.used_genes % len(self.genotype) == 0 and self.used_genes > 0 and len(production_choices) > 1:

                self.wraps -= 1

            if log:

                logger.log.debug('\nUnexpanded Symbols -> ' + str(unexpanded_symbols))

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            if log:

                logger.log.debug('Current Symbol     -> ' + str(current_symbol))

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol[1] != self.NT:

                if log:

                    logger.log.debug('<-- Terminal Symbol -->')

                self.root.append(current_symbol[0])

            # Otherwise the current symbol maps to a non-terminal.
            else:

                if log:

                    logger.log.debug('<-- Non-Terminal Symbol -->')

                production_choices = self.rules[current_symbol[0]]

                if log:

                    logger.log.debug('Production Choices -> ' + str(production_choices))

                # Select a production.
                current_production = int(self.genotype[self.used_genes % len(self.genotype)] % len(production_choices))

                if log:

                    logger.log.debug('Current Production -> ' + str(production_choices[current_production]))

                # Use an input if there was more then 1 choice.
                if len(production_choices) > 1:

                    self.used_genes += 1

                # Derivation order is left to right (depth-first).
                unexpanded_symbols = production_choices[current_production] + unexpanded_symbols

            logger.log.debug('Output             -> ' + str(self.root))

    def generate_from_thrift(self):

        """
        Uses reflection to form a parse tree with an Apache Thrift auto-generated class and genotype.
        :return: A parse tree represented as an instance of a Apache Thrift class.
        """

        log = config.grove_config['logging']['grammar']

        if log:

            logger.log.debug('Input Sequence     -> ' + str(self.genotype))

        production_choices = []
        unexpanded_symbols = utils.discover_children(self.root)

        # Find the blacklists and whitelists for terminal symbols.
        blacklists = constraint.find_blacklists(self.grammar.rules)
        whitelists = constraint.find_whitelists(self.grammar.rules)

        while self.wraps > 0 and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if self.used_genes % len(self.genotype) == 0 and self.used_genes > 0 and len(production_choices) > 1:

                self.wraps -= 1

            if log:

                logger.log.debug('\nUnexpanded Symbols -> ' + str(unexpanded_symbols))

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            # Instantiate current symbol, if able.
            if inspect.isclass(current_symbol.t_type):

                current_symbol.add_features(obj=current_symbol.t_type())

                if getattr(current_symbol.t_parent, current_symbol.t_name) is None:

                    setattr(current_symbol.t_parent, current_symbol.t_name, current_symbol.obj)

            if log:

                logger.log.debug('Current Symbol     -> ' + str(current_symbol))
                logger.log.debug(type(getattr(current_symbol.t_parent, current_symbol.t_name)))

            # Non-terminal symbol (List).
            if isinstance(current_symbol.t_type, tuple):

                if log:

                    logger.log.debug('<-- Non-Terminal Symbol (List) -->')

                if getattr(current_symbol.t_parent, current_symbol.t_name) is None:

                    setattr(current_symbol.t_parent, current_symbol.t_name, list())

                production_choices = utils.extract_list_productions(current_symbol)

                if log:

                    logger.log.debug('Production Choices -> ' + str(production_choices))

                amount = int(self.genotype[self.used_genes % len(self.genotype)] % 10)

                if log:

                    logger.log.debug('Amount             -> ' + str(amount))

                self.used_genes += 1

                for _ in xrange(amount):

                    unexpanded_symbols.insert(0, production_choices)

            # Non-terminal symbol (List Element)
            elif isinstance(getattr(current_symbol.t_parent, current_symbol.t_name), list):

                if log:

                    logger.log.debug('<-- Non-Terminal Symbol (List Element) -->')
                    logger.log.debug(getattr(current_symbol.t_parent, current_symbol.t_name))

                setattr(current_symbol.t_parent, current_symbol.t_name, getattr(current_symbol.t_parent, current_symbol.t_name) + [current_symbol.obj])

                if log:

                    logger.log.debug(getattr(current_symbol.t_parent, current_symbol.t_name))

                production_choices = utils.discover_children(current_symbol)

                if log:

                    logger.log.debug('Production Choices -> ' + str(production_choices))

                # Required fields.
                unexpanded_symbols = production_choices + unexpanded_symbols

            # Non-terminal symbol.
            elif hasattr(current_symbol.obj, 'thrift_spec') and not isinstance(getattr(current_symbol.t_parent, current_symbol.t_name), list):

                if log:

                    logger.log.debug('<-- Non-Terminal Symbol -->')

                production_choices = utils.discover_children(current_symbol)

                if log:

                    logger.log.debug('Production Choices -> ' + str(production_choices))

                # Required fields.
                unexpanded_symbols = production_choices + unexpanded_symbols

            # Terminal symbol.
            else:

                name = current_symbol.obj.__class__.__name__.lower()

                blacklist_name = name + '_blacklist'
                blacklist = None

                if blacklist_name in blacklists:
                    blacklist = blacklists[blacklist_name]

                whitelist_name = name + '_whitelist'
                whitelist = None

                if whitelist_name in whitelists:
                    whitelist = whitelists[whitelist_name]

                # Verify the blacklist and whitelist.
                constraint.verify_lists(blacklist, whitelist)

                if log:

                    logger.log.debug('<-- Terminal Symbol -->')

                attrs = [attr for attr in dir(current_symbol.obj) if not callable(attr) and not attr.startswith('_')]

                if log:

                    logger.log.debug('Choices            -> ' + str(attrs))

                chosen = getattr(current_symbol.obj, attrs[int(self.genotype[self.used_genes % len(self.genotype)] % len(attrs))])
                current_symbol.add_child(TreeNode(name=chosen))
                setattr(current_symbol.t_parent, current_symbol.t_name, chosen)
                self.used_genes += 1

            if log:

                logger.log.debug('Output             -> ' + str(self.root.get_ascii(show_internal=True)))

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
