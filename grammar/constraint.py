blacklists = None
whitelists = None


def find_blacklists(thrift):

    """
    Finds all blacklists in a Apache Thrift module.
    :param thrift: The Apache Thrift module to search.
    :return: The list of blacklists contained in the Apache Thrift module.
    """

    global blacklists
    blacklists = {blacklist: getattr(thrift, blacklist) for blacklist in dir(thrift) if 'blacklist' in blacklist}


def find_whitelists(thrift):

    """
    Finds all whitelists in a Apache Thrift module.
    :param thrift: The Apache Thrift module to search.
    :return: The list of whitelists contained in the Apache Thrift module.
    """

    global whitelists
    whitelists = {whitelist: getattr(thrift, whitelist) for whitelist in dir(thrift) if 'whitelist' in whitelist}


def verify_lists(blacklist, whitelist):

    """
    Verifies that a given blacklist and whitelist do not contain an invalid mapping. An invalid mapping
    occurs if there exists a key in both lists such a non-empty intersection of the resulting sets is present.
    :param blacklist: The blacklist.
    :param whitelist: The whitelist.
    """

    if blacklist and whitelist:

        for name in set(blacklist).intersection(set(whitelist)):

            if not blacklist[name].intersection(whitelist[name]) == set():

                raise ValueError('blacklist and whitelist cannot contain the same element ' +
                                 str(name) + ' -> ' + str(blacklist[name]))


def apply_constraint(parse_tree=None, constraint=None, constraint_type=None):

    # TODO - This needs to be made generic, which is a huge task. This ad hoc solution will suffice for now.

    """
    Applies a given contraint (a blacklist or whitelist) to a parse tree.
    :param parse_tree: The parse tree to apply the constraint to.
    :param constraint: The constraint to be applied to the parse tree.
    :param constraint_type: The type of constraint. Can either be a blacklist or whitelist (as 'bl' or 'wl').
    """

    for rule in parse_tree.root.obj.rules:

        behavior_ids = set([behavior.id_behavior for behavior in rule.behaviors])

        print 'Here are the behavior ids: ' + str(behavior_ids)

        print 'Actions (Before): ' + str(rule.actions)

        for behavior_id in behavior_ids:

            if behavior_id in constraint:

                hits = constraint[behavior_id]

                print 'Behavior ID: ' + str(behavior_id) + ' -> ' + str(hits)

                print 'Actions: ' + str(rule.actions)

                for action in rule.actions:

                    print 'Action: ' + str(action)

                    if constraint_type is 'bl' and action.id_action in hits:

                        print 'Removing ' + str(action) + ' from ' + str(rule.actions)
                        rule.actions.remove(action)

                    elif constraint_type is 'wl' and action.id_action not in hits:

                        rule.actions.remove(action)

        print 'Actions (After): ' + str(rule.actions) + '\n'
