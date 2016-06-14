def wrap_thrift_spec(object):

    """
    Wraps the class of an instance of a thrift auto-generated class into its thrift spec.
    :param object: An instance of a thrift auto-generated class.
    :return: The thrift spec of that class with the object included in each tuple.
    """

    return dict((key, value + (object,)) for key, value in object.thrift_spec.iteritems())


def extract_list_productions(object):

    """
    Extracts production choices from a list.
    :param object: The list to extract from.
    :return: Possible production choices from the list.
    """

    return object[2][0], object[1], object[2][1], object[3], object[4]
