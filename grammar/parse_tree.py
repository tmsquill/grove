import constraint
import evolution.config
import evolution.ga
import inspect
import utils

from thriftpy.protocol import TBinaryProtocol
from thriftpy.transport import TMemoryBuffer


class TreeNode(object):

    def __init__(self, parent, data):

        self.parent = parent
        self.data = data


class ParseTreeNode(TreeNode):

    def __init__(self, parent, data):

        self.codon_index = None
        self.codon_pick = None

        super(self.__class__, self).__init__(parent, data)


class ParseTree:

    def __init__(self, grammar, genome):

        self.grammar = grammar
        self.genome = genome
        self.used_genes = 0
        self.wraps = 2

        if grammar.representation == 'bnf':

            # TODO - Change to parse tree node.
            self.root = []

        elif grammar.representation == 'proto':

            # TODO - Change to parse tree node.
            self.root = None

        elif grammar.representation == 'thrift':

            # TODO - Change to parse tree node.
            self.root = ParseTreeNode(None, grammar.rules.Root())

    def generate(self):

        """
        Generates a parse tree. The generation type depends on the representation of the grammar
        object (BNF, Proto, Thrift).
        :return: The generated parse tree built with the input sequence.
        """

        getattr(self, 'generate_from_' + self.grammar.representation)()

    def generate_from_bnf(self):

        """
        Forms a parse tree from a Backus-Naur Form grammar and genome.
        :return: An parse tree represented as a list.
        """

        log = evolution.config.grove_config['logging']['grammar']

        if log:

            evolution.ga.log.debug('Input Sequence     -> ' + str(self.genome))

        production_choices = []
        unexpanded_symbols = [self.start_rule]

        while 0 < self.wraps and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if self.used_genes % len(self.genome) == 0 and self.used_genes > 0 and len(production_choices) > 1:

                self.wraps -= 1

            if log:

                evolution.ga.log.debug('\nUnexpanded Symbols -> ' + str(unexpanded_symbols))

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            if log:

                evolution.ga.log.debug('Current Symbol     -> ' + str(current_symbol))

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol[1] != self.NT:

                if log:

                    evolution.ga.log.debug('<-- Terminal Symbol -->')

                self.root.append(current_symbol[0])

            # Otherwise the current symbol maps to a non-terminal.
            else:

                if log:

                    evolution.ga.log.debug('<-- Non-Terminal Symbol -->')

                production_choices = self.rules[current_symbol[0]]

                if log:

                    evolution.ga.log.debug('Production Choices -> ' + str(production_choices))

                # Select a production.
                current_production = int(self.genome[self.used_genes % len(self.genome)] % len(production_choices))

                if log:

                    evolution.ga.log.debug('Current Production -> ' + str(production_choices[current_production]))

                # Use an input if there was more then 1 choice.
                if len(production_choices) > 1:

                    self.used_genes += 1

                # Derivation order is left to right (depth-first).
                unexpanded_symbols = production_choices[current_production] + unexpanded_symbols

            evolution.ga.log.debug('Output             -> ' + str(self.root))

    def generate_from_proto(self):

        """
        Uses reflection to form a parse tree with a Google Protocol Buffer auto-generated class and genome.
        :return: A parse tree represented as an instance of a Google Protocol Buffer class.
        """

        import google.protobuf.descriptor as des
        import google.protobuf.text_format as tf
        from google.protobuf.descriptor import FieldDescriptor
        from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
        import random

        log = evolution.config.grove_config['logging']['grammar']

        if log:

            evolution.ga.log.debug('Input Sequence     -> ' + str(self.genome))

        production_choices = []
        unexpanded_symbols = [(self.root, field) for field in self.root.DESCRIPTOR.fields]

        while 0 < self.wraps and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if self.used_genes % len(self.genome) == 0 and self.used_genes > 0 and len(production_choices) > 1:

                self.wraps += 1

            if log:

                evolution.ga.log.debug('\nUnexpanded Symbols -> ' + str(unexpanded_symbols))

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            if log:

                evolution.ga.log.debug('Current Symbol     -> ' + str(current_symbol))

            # If the current symbol maps to a terminal, append the symbol.
            if current_symbol == des.FieldDescriptor.TYPE_ENUM:

                if log:

                    evolution.ga.log.debug('<-- Terminal Symbol -->')

                setattr(current_symbol[0], current_symbol[1].name, random.choice(current_symbol[1].enum_type.values).number)

            # Otherwise the current symbol maps to a non-terminal.
            else:

                if log:

                    evolution.ga.log.debug('<-- Non-Terminal Symbol (List) -->')

                from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

                if log:

                    evolution.ga.log.debug('getattr(' + str(type(current_symbol[0])) + ', ' + current_symbol[1].name + ')')

                # Required field.
                if current_symbol[1].label == des.FieldDescriptor.LABEL_REQUIRED:

                    getattr(current_symbol[0], current_symbol[1].name).SetInParent()

                # Repeated field.
                elif current_symbol[1].label == des.FieldDescriptor.LABEL_REPEATED:

                    if isinstance(current_symbol[0], RepeatedCompositeFieldContainer):

                        current_symbol[0].add()

                    else:

                        getattr(current_symbol[0], current_symbol[1].name).add()

                # Production choices are children of the current symbol.
                production_choices = getattr(self.pb, current_symbol[1].message_type.name).DESCRIPTOR.fields

                if log:

                    evolution.ga.log.debug('Production Choices -> ' + str(production_choices))

                # Gather all required productions.
                repeated = [(getattr(current_symbol[0], current_symbol[1].name), _) for _ in production_choices if _.label == des.FieldDescriptor.LABEL_REPEATED]
                unexpanded_symbols = repeated + unexpanded_symbols

                if log:

                    evolution.ga.log.debug('Repeated Productions -> ' + str(repeated))

                # Gather all required productions.
                if isinstance(current_symbol[0], RepeatedCompositeFieldContainer):

                    required = 0

                else:

                    required = [(getattr(current_symbol[0], current_symbol[1].name), _) for _ in production_choices if _.label == des.FieldDescriptor.LABEL_REQUIRED]
                    unexpanded_symbols = required + unexpanded_symbols

                if log:

                    evolution.ga.log.debug('(Required Productions) -> ' + str(required))

                # Select a production.
                current_production = int(self.genome[self.used_genes % len(self.genome)] % len(production_choices))
                print 'Current Production -> ' + str(production_choices[current_production])

                # Use an input if there was more then 1 choice.
                if len(production_choices) > 1:

                    self.used_genes += 1

                # Chosen production.
                chosen = production_choices[current_production]

                # Derivation order is left to right (depth-first).
                #unexpanded_symbols.insert(0, (getattr(current_symbol[0], current_symbol[1].name), chosen))

        # Not completely expanded.
        if len(unexpanded_symbols) > 0:

            return None, self.used_genes

    def generate_from_thrift(self):

        """
        Uses reflection to form a parse tree with an Apache Thrift auto-generated class and genome.
        :return: A parse tree represented as an instance of a Apache Thrift class.
        """

        log = evolution.config.grove_config['logging']['grammar']

        if log:

            evolution.ga.log.debug('Input Sequence     -> ' + str(self.genome))

        production_choices = []
        unexpanded_symbols = utils.wrap_thrift_spec(self.root.data).values()

        # Find the blacklists and whitelists for terminal symbols.
        blacklists = constraint.find_blacklists(self.grammar.rules)
        whitelists = constraint.find_whitelists(self.grammar.rules)

        while 0 < self.wraps and len(unexpanded_symbols) > 0:

            # Wrap around the input.
            if self.used_genes % len(self.genome) == 0 and self.used_genes > 0 and len(production_choices) > 1:

                self.wraps -= 1

            if log:

                evolution.ga.log.debug('\nUnexpanded Symbols -> ' + str(unexpanded_symbols))

            # Expand a production.
            current_symbol = unexpanded_symbols.pop(0)

            # Instantiate current symbol, if able.
            if inspect.isclass(current_symbol[2]):

                instance = current_symbol[2]()

                if getattr(current_symbol[4], current_symbol[1]) is None:

                    setattr(current_symbol[4], current_symbol[1], instance)

                current_symbol = (current_symbol[0], current_symbol[1], instance, current_symbol[3], current_symbol[4])

            if log:

                evolution.ga.log.debug('Current Symbol     -> ' + str(current_symbol))
                evolution.ga.log.debug(type(getattr(current_symbol[4], current_symbol[1])))

            # Non-terminal symbol (List).
            if isinstance(current_symbol[2], tuple):

                if log:

                    evolution.ga.log.debug('<-- Non-Terminal Symbol (List) -->')

                if getattr(current_symbol[4], current_symbol[1]) is None:

                    setattr(current_symbol[4], current_symbol[1], list())

                production_choices = utils.extract_list_productions(current_symbol)

                if log:

                    evolution.ga.log.debug('Production Choices -> ' + str(production_choices))

                amount = int(self.genome[self.used_genes % len(self.genome)] % 10)

                if log:

                    evolution.ga.log.debug('Amount             -> ' + str(amount))

                self.used_genes += 1

                for _ in xrange(amount):

                    unexpanded_symbols.insert(0, production_choices)

            # Non-terminal symbol (List Element)
            elif isinstance(getattr(current_symbol[4], current_symbol[1]), list):

                if log:

                    evolution.ga.log.debug('<-- Non-Terminal Symbol (List Element) -->')
                    evolution.ga.log.debug(getattr(current_symbol[4], current_symbol[1]))

                setattr(current_symbol[4], current_symbol[1], getattr(current_symbol[4], current_symbol[1]) + [current_symbol[2]])

                if log:

                    evolution.ga.log.debug(getattr(current_symbol[4], current_symbol[1]))

                production_choices = utils.wrap_thrift_spec(current_symbol[2]).values()

                if log:

                    evolution.ga.log.debug('Production Choices -> ' + str(production_choices))

                # Required fields.
                unexpanded_symbols = production_choices + unexpanded_symbols

            # Non-terminal symbol.
            elif hasattr(current_symbol[2], 'thrift_spec') and not isinstance(getattr(current_symbol[4], current_symbol[1]), list):

                if log:

                    evolution.ga.log.debug('<-- Non-Terminal Symbol -->')

                production_choices = utils.wrap_thrift_spec(current_symbol[2]).values()

                if log:

                    evolution.ga.log.debug('Production Choices -> ' + str(production_choices))

                # Required fields.
                unexpanded_symbols = production_choices + unexpanded_symbols

            # Terminal symbol.
            else:

                name = current_symbol[2].__class__.__name__.lower()

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

                #print current_symbol[2], blacklist, whitelist

                if log:

                    evolution.ga.log.debug('<-- Terminal Symbol -->')

                attrs = [attr for attr in dir(current_symbol[2]) if not callable(attr) and not attr.startswith('_')]

                if log:

                    evolution.ga.log.debug('Choices            -> ' + str(attrs))

                setattr(current_symbol[4], current_symbol[1], getattr(current_symbol[2], attrs[int(self.genome[self.used_genes % len(self.genome)] % len(attrs))]))
                self.used_genes += 1

            evolution.ga.log.debug('Output             -> ' + str(self.root))

    def serialize(self):

        """
        Serializes a parse tree into binary.
        :param parse_tree: The parse tree to serialize.
        :return: The serialized parse tree.
        """

        transport = TMemoryBuffer()
        protocol = TBinaryProtocol(transport)
        self.root.data.write(protocol)
        return transport.getvalue()
