from ete3 import TreeNode


def discover_children(object=None):

    """
    Discovers all children defined in the thrift_spec of an instance of a thrift auto-generated class.
    :param object: The treenode object to search to discover the children.
    :return: The discovered children, wrapped in treenodes.
    """

    nodes = []

    for spec in object.obj.thrift_spec.values():

        node = TreeNode(name=spec[1])
        node.add_features(t_parent=object.obj, t_name=spec[1], t_type=spec[2])
        object.add_child(node)
        nodes.append(node)

    return nodes


def extract_list_productions(object):

    """
    Extracts production choices from a list and returns them wrapped in treenodes.
    :param object: The list wrapped in a treenode to extract from.
    :return: Possible production choices from the list, wrapped in treenodes.
    """

    object.t_type = object.t_type[1]

    return object
