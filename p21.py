""" Python script to implement P1 of Phase 2 of Python Learning Program """

def swap_dictionary(dictionary):
    """ function to swap a dictionary keys <--> values
        if not possible, outputs 'Swap is not possible' """
    result = {}
    valid = True
    if isinstance(dictionary, dict):
        partial = zip(*[dictionary.values(), dictionary.keys()])
        for element in partial:
            # actually here, the key can be an object which has the hash function
            # so there must be a better way to check for that
            if isinstance(element[0], (list, tuple)) or element[0] in result:
                valid = False
            else:
                result[element[0]] = element[1]
    else:
        valid = False
    return result if valid else "Swap is not possible!"

def test_swap_dictionary_empty():
    """ pytest unittest for swap_dictionary with an empty dictionary """
    assert swap_dictionary({}) == {}

def test_swap_dictionary_error():
    """ pytest unittest for swap_dictionary with different badinput types """
    assert swap_dictionary('{}') == "Swap is not possible!"
    assert swap_dictionary([]) == "Swap is not possible!"
    assert swap_dictionary(("", [])) == "Swap is not possible!"

def test_swap_dictionary_examples():
    """ pytest unittest for swap_dictionary with pdf examples """
    assert swap_dictionary({'a': 123, 'b': 456}) == {123: 'a', 456: 'b'}
    assert swap_dictionary({'a': (1, 2, [3])}) == "Swap is not possible!"
