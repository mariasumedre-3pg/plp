""" Python script to implement P1 of Phase 2 of Python Learning Program """

def help_check_element(element):
    """ helper function for swap_dictionary to check if an element can be used
        as key to a dictionary
        element should be a tuple"""
    result = True
    # by trial i found out that lists, dictionaries and sets cannot be dictionary keys
    if isinstance(element, (list, dict, set)):
        result = False
    # tuples can be dictionary keys as long as they don't contain the evil types above
    elif isinstance(element, tuple):
        for item in element:
            # recursion, again?
            result = help_check_element(item)
            if not result: # break as soon as we found a false result, and return the failure
                break
    return result


def swap_dictionary(dictionary):
    """ function to swap a dictionary keys <--> values
        if not possible, outputs 'Swap is not possible' """
    result = {}
    valid = True
    if isinstance(dictionary, dict):
        partial = zip(*[dictionary.values(), dictionary.keys()])
        for element in partial:
            # actually here, the key can be any object which has the __hash__ function defined
            # there must be a better way to check for that, without actually checking for __hash__
            # since that is forbidden
            if help_check_element(element[0]) and (element[0] not in result):
                result[element[0]] = element[1]
            else:
                valid = False
                break
    else:
        valid = False
    return result if valid else "Swap is not possible!"

def test_swap_dictionary_empty():
    """ pytest unittest for swap_dictionary with an empty dictionary """
    assert swap_dictionary({}) == {}

def test_swap_dictionary_error():
    """ pytest unittest for swap_dictionary with different bad input types """
    assert swap_dictionary('{}') == "Swap is not possible!"
    assert swap_dictionary([]) == "Swap is not possible!"
    assert swap_dictionary(("", [])) == "Swap is not possible!"
    assert swap_dictionary({'one': 1, 'two': 2, 'three': 1}) == "Swap is not possible!"

def test_swap_dictionary_examples():
    """ pytest unittest for swap_dictionary with pdf examples """
    assert swap_dictionary({'a': 123, 'b': 456}) == {123: 'a', 456: 'b'}
    assert swap_dictionary({'a': (1, 2, [3])}) == "Swap is not possible!"

def test_swap_dictionary_other():
    """ other combinations of values and keys in a dictionary """
    # test with a list
    assert swap_dictionary({'a': [1, 2, [3]]}) == "Swap is not possible!"
    # test with a tuple with a set inside
    assert swap_dictionary({'a': (1, 2, {3})}) == "Swap is not possible!"
    # test with a tuple with a set inside, but not on last position, to check if it breaks from for
    # if it doesn't, then the last value (3) is valid and helper function fails
    assert swap_dictionary({'a': (1, {2}, 3)}) == "Swap is not possible!"
    # test with a tuple with a dictionary inside
    assert swap_dictionary({'a': ({1: 2}, 2, 3)}) == "Swap is not possible!"
    # test with a tuple with a dictionary in second position
    assert swap_dictionary({'a': (0, {1: 2}, 2, 3)}) == "Swap is not possible!"
    # test with a nested tuple that should work
    assert swap_dictionary({'a': (1, (2, 3), 3)}) == {(1, (2, 3), 3): 'a'}
    # test with both key and value the same
    assert swap_dictionary({'a': 'a'}) == {'a': 'a'}
    assert swap_dictionary({953: 953}) == {953: 953}
    assert swap_dictionary({('a', 'b'): ('a', 'b')}) == {('a', 'b'): ('a', 'b')}
    # test with strings
    assert swap_dictionary({'a': 'a longer key here'}) == {'a longer key here': 'a'}
    assert swap_dictionary({'a longer value here': 'a'}) == {'a': 'a longer value here'}
    # i wonder ...
    assert swap_dictionary({u'a longer value here': u'a'}) == {u'a': u'a longer value here'}

