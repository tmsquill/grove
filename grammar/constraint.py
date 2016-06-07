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
