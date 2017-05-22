""" Python script to implement the first problem of the third phase in
    Python Learning Program
    P1. Given a binary tree encoded as a tuple (node_label, left_node_tuple, right_node_tuple)
    write an iterator / generator that returns the nodes of the tree in pre-order.
    Example:
    Input: ('b', ('a', None, None), ('z', ('c', None, None), ('zz', None, None)))
    Output: b, a, z, c, zz
    """

def test((node_label, left_node_tuple, right_node_tuple)):
    """ generator function thing"""
    #import pdb
    #pdb.set_trace()
    #print "yielding node_label {0}".format(node_label)
    yield node_label

    #pdb.set_trace()
    if left_node_tuple is not None:
        left = test(left_node_tuple)
        val = next(left)
        #print "yielding left val {0}".format(val)
        yield val
        while val is not None:
            val = next(left)
            #print "yielding left val (while) {0}".format(val)
            yield val

    #pdb.set_trace()
    if right_node_tuple is not None:
        right = test(right_node_tuple)
        val = next(right)
        #print "yielding right val {0}".format(val)
        yield val
        while val is not None:
            val = next(right)
            #print "yielding right val (while) {0}".format(val)
            yield val

    yield None


def use_test(param):
    """ use the generator that iterates throught the tree """
    for element in test(param):
        if element:
            print "{0},".format(element),
