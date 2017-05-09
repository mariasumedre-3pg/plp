''' Python script to implement P2 from Python Learning Program
    There should be a my_merger function and some unit-tests for it
'''

import unittest

def merge_values(value1, value2):
    ''' Utility function to add(merge) two values
        The values could be lists, numbers, strings, sets
        '''
    result = None
    try:
        # all cases that we know how to merge/add are here,
        # if we don't know how to merge/add, then exception handler makes a tuple
        if isinstance(value1, set) and isinstance(value2, set):
            result = value1.union(value2)
        elif isinstance(value1, dict) and isinstance(value2, dict):
            result = my_merger(value1, value2)
        else:
            result = value1 + value2
    except TypeError:
        result = (value1, value2)

    return result


def my_merger(dict_a, dict_b):
    ''' merge two lists which have elements of different types
        this will check if arguments are dictionaries,
        then call merge_values for each value, if the keys match
        remains to be seen what should happen if the keys do not match
        '''
    result = {}
    if isinstance(dict_a, dict) and isinstance(dict_b, dict):
        #keysa = sorted(dict_a.keys())
        #keysb = sorted(dict_b.keys())
        #for key in dict_a.keys():
        #    if key in dict_b.keys():
        #        result[key] = merge_values(dict_a[key], dict_b[key])
        #    else: # but what if is in dict_b and not in dict_a?
        #        print "key: ", key, " is in dict_a, but not in dict_b"
        # equivalent of above(?), but exercising the python one-liners
        keysa = dict_a.keys()
        keysb = dict_b.keys()
        result = {key : merge_values(dict_a[key], dict_b[key]) for key in keysa if key in keysb}
    return result


class MergerTest(unittest.TestCase):
    ''' class to unit-test the my_merger function for P2
        todo: add more tests, with other types of elements: integers, strings,
        dictionaries, nested structures, etc.
        '''

    def test_emptydict(self):
        ''' test merger of empty dictionaries '''
        arg1 = {'x': []}
        arg2 = {'x': []}
        exp = {'x': []}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 empty dicts merged make one empty dict")
        arg1 = {'x': [], 'y':[]}
        arg2 = {'x': []}
        exp = {'x': []}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "merge 2 differently empty dicts")
        arg1 = {'x': []}
        arg2 = {'x': [], 'y':[]}
        exp = {'x': []}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "merge 2 differently empty dicts v2")

    def test_simpledict(self):
        ''' test merger of simple dictionaries '''
        arg1 = {'x': [1, 2]}
        arg2 = {'x': [2, 3]}
        exp = {'x': [1, 2, 2, 3]}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 simple dicts with lists")

        arg1 = {'x': 1}
        arg2 = {'x': 4}
        exp = {'x': 5}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 simple dicts with numbers")

        arg1 = {'x': "1"}
        arg2 = {'x': "4"}
        exp = {'x': "14"}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 simple dicts with strings")

        arg1 = {'x': "1"}
        arg2 = {'x': 4}
        exp = {'x': ("1", 4)}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 simple dicts with mismatched type")

        arg1 = {'x': set([1, 2, 3])}
        arg2 = {'x': set([4, 2, 3])}
        exp = {'x': set([1, 2, 3, 4])}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 simple dicts with sets")

        arg1 = {'x': {'y': [1, 2, 3]}}
        arg2 = {'x': {'y': [4, 2, 3]}}
        exp = {'x': {'y': [1, 2, 3, 4, 2, 3]}}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 simple dicts with dicts")

    def test_mixdictionary(self):
        arg1 = {'x': [1,2,3], 'y': 1, 'z': set([1,2,3]), 'w': 'qweqwe', 't': {'a': [1, 2]}, 'm': [1]}
        arg2 = {'x': [4,5,6], 'y': 4, 'z': set([4,2,3]), 'w': 'asdf', 't': {'a': [3, 2]}, 'm': "wer"}
        exp = {'x': [1,2,3,4,5,6], 'y': 5, 'z': set([1,2,3,4]), 'w': 'qweqweasdf', 't': {'a': [1, 2, 3, 2]}, 'm': ([1], "wer")}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "dictionaries from p2")

