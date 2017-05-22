""" Python script to implement the first problem of the third phase in
    Python Learning Program
    P1. Given a binary tree encoded as a tuple (node_label, left_node_tuple, right_node_tuple)
    write an iterator / generator that returns the nodes of the tree in pre-order.
    Example:
    Input: ('b', ('a', None, None), ('z', ('c', None, None), ('zz', None, None)))
    Output: b, a, z, c, zz
    """

def pre_nodes((node_label, left_node_tuple, right_node_tuple)):
    """ generator function thing"""
    yield node_label

    if left_node_tuple is not None:
        value = True # assume there is a value in the generator (do...while?)
        left = pre_nodes(left_node_tuple)
        while value:
            value = next(left)
            if value:
                yield value

    if right_node_tuple is not None:
        value = 1 # assume there is a value in the generator
        right = pre_nodes(right_node_tuple)
        while value:
            value = next(right)
            if value:
                yield value
    yield None


def use_pre_nodes(param):
    """ use the generator that iterates throught the tree """
    #for element in pre_nodes(param):
    #    if element:
    #        print "{0}, ".format(element),
    # this might defeat the purpose of a generator
    a_list = [element for element in pre_nodes(param) if element]
    print ', '.join(a_list)
