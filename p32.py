""" Python script to implement the second problem of the third phase of the Python Learning Program
    P2. Write a generator that returns all the subsets of a given set. Example:
        Input: set([1, 2, 3])
        Output: set([1, 2, 3]), set([2, 3]), set([1, 3]), set([3]), set([1,
        2]), set([2]), set([1]), set([])
    """
from itertools import chain, ifilter, permutations, imap

def gsubsets(given_set):
    """ generator that returns all the subsets of a given set """
    size = len(given_set) - 1
    while size > 0:
        aux = permutations(given_set, size)
        for item in aux:
            if sorted(item) == list(item):
                yield set(item)
        size = size - 1

    yield set([])

def isubsets(given_set):
    """ iterable that returns all the subsets of a given set """
    size = len(given_set)
    result = imap(set,
                  ifilter(lambda x: sorted(x) == list(x),
                          chain(*[permutations(given_set, index) for index in range(size)])))
    return result


SUBSET_LIST = [set([1, 2]), set([1, 3]), set([2, 3]), set([1]), set([2]), set([3]), set([])]
SUBSET_LIST2 = [set(['a', 'b']),
                set(['a', 'c']),
                set(['b', 'c']),
                set(['a']),
                set(['b']),
                set(['c']),
                set([])]

def test_isubsets_example():
    """ test the iterable subset with the example in pdf """
    argument = set([1, 2, 3])

    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item in SUBSET_LIST

def test_gsubsets_example():
    """ test the generator subset with the example in pdf """
    argument = set([1, 2, 3])

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item in SUBSET_LIST

def test_subsets_empty():
    """ test subsets with the empty set """
    argument = set([])
    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item == set([])

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item == set([])

    argument = set()
    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item == set()

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item == set()

    argument = set([()])
    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item == set([])

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item == set([])

def test_subsets_chars():
    """ test the subsets iterable and generator with sets of characters """
    argument = set(['a', 'b', 'c'])

    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item in SUBSET_LIST2

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item in SUBSET_LIST2
