''' Python script to implement P2 from Python Learning Program
    There should be a my_merger function and some unit-tests for it
'''

import unittest

def my_merger(list_a, list_b):
    ''' merge two lists which have elements of different types
        first really simple implementation, need to make this recursive(?)
        because the add is shallow
        '''
    result = {}
    if isinstance(list_a, dict) and isinstance(list_b, dict):
        keysa = sorted(list_a.keys())
        keysb = sorted(list_b.keys())
        for key in keysa:
            if key in keysb:
                result[key] = list_a[key] + list_b[key]
            else:
                print "key: ", key, " is in list_a, but not in list_b"
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
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 empty lists merged make one empty list")
        arg1 = {'x': [], 'y':[]}
        arg2 = {'x': []}
        exp = {'x': []}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "merge 2 differently empty lists")
        arg1 = {'x': []}
        arg2 = {'x': [], 'y':[]}
        exp = {'x': []}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "merge 2 differently empty lists v2")

    def test_simpledict(self):
        ''' test merger of simple dictionaries '''
        arg1 = {'x': [1, 2]}
        arg2 = {'x': [2, 3]}
        exp = {'x': [1, 2, 2, 3]}
        self.assertDictEqual(my_merger(arg1, arg2), exp, "2 empty lists merged make one empty list")


