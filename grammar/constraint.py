def find_blacklists(thrift):

    """
    Finds all blacklists in a Apache Thrift module.
    :param thrift: The Apache Thrift module to search.
    :return: The list of blacklists contained in the Apache Thrift module.
    """

    blacklists = {blacklist: getattr(thrift, blacklist) for blacklist in dir(thrift) if 'blacklist' in blacklist}

    return blacklists


def find_whitelists(thrift):

    """
    Finds all whitelists in a Apache Thrift module.
    :param thrift: The Apache Thrift module to search.
    :return: The list of whitelists contained in the Apache Thrift module.
    """

    whitelists = {whitelist: getattr(thrift, whitelist) for whitelist in dir(thrift) if 'whitelist' in whitelist}

    return whitelists


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
