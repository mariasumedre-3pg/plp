""" Python script to implement the first problem of the third phase in
    Python Learning Program:
        P1. Given a binary tree encoded as a tuple (node_label, left_node_tuple, right_node_tuple)
        write an iterator / generator that returns the nodes of the tree in pre-order.
        Example:
        Input: ('b', ('a', None, None), ('z', ('c', None, None), ('zz', None, None)))
        Output: b, a, z, c, zz
    """

def help_nodes(some_tuple):
    """ see if we can make a generator thing to not duplicate code """
    value = True # assume there is a value in the generator (do...while?)
    side = pre_nodes(some_tuple)
    while value:
        value = next(side)
        if value:
            yield value


def pre_nodes((node_label, left_node_tuple, right_node_tuple)):
    """ generator function thing to return the nodes in preorder"""
    yield node_label

    if left_node_tuple is not None:
        for node in help_nodes(left_node_tuple):
            yield node

    if right_node_tuple is not None:
        for node in help_nodes(right_node_tuple):
            yield node
    yield None


def use_pre_nodes(param):
    """ use the generator that iterates throught the tree """
    #for element in pre_nodes(param):
    #    if element:
    #        print "{0}, ".format(element),
    # this might defeat the purpose of a generator
    a_list = [element for element in pre_nodes(param) if element]
    print ', '.join(a_list)


def test_p1_example():
    """ check the test from the p1 example in plp pdf """
    argument = ('b', ('a', None, None), ('z', ('c', None, None), ('zz', None, None)))
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == ['b', 'a', 'z', 'c', 'zz']


def build_a_tuple(count=1):
    """ build a tuple recursively with a tree structure """
    result = None
    if count:
        result = ('a', build_a_tuple(count - 1), None)
    return result


def test_combinations():
    """ check various combinations of valid trees """
    argument = ('b', ('a', None, ('aa', None, None)), ('z', ('c', None, None), ('zz', None, None)))
    expected = ['b', 'a', 'aa', 'z', 'c', 'zz']
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    argument = (None, None, None)
    expected = []
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    argument = ('a', None, None)
    expected = ['a']
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    argument = ('a', ('b', None, None), None)
    expected = ['a', 'b']
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    argument = ('a', None, (2, None, None))
    expected = ['a', 2]
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    argument = (None, ('a', None, None), ('aa', None, None))
    expected = ['a', 'aa']
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    argument = ('a', None, None)
    expected = ['a']
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

def test_big_structures():
    """ test pre_nodes using bigger tuples """
    # start reasonably with a depth of 10
    argument = build_a_tuple(10)
    expected = ['a'] * 10
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    # increase to 50
    argument = build_a_tuple(50)
    expected = ['a'] *50
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    # increase to 100
    argument = build_a_tuple(100)
    expected = ['a'] * 100
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected

    # increase to 461 <- at 462 there is an error: RuntimeError: maximum recursion depth exceeded
    argument = build_a_tuple(461)
    expected = ['a'] * 461
    a_list = [element for element in pre_nodes(argument) if element]
    assert a_list == expected
