''' Python script to implement P1 from Python Learning Program
    There should be a my_flatten function and some unit-tests for it
'''

import unittest


def my_flatten(my_list, maxdepth=1):
    ''' first flatten version
        my_list - list (of lists) to flatten
        maxdepth - max levels of nesting which are flattened
        '''
    result = []
    #if depth is 0, return the list as is (with all its nestedness) and don't process any further
    if maxdepth <= 0:
        return my_list

    for element in my_list:
        if isinstance(element, (tuple, list)):
            temp = my_flatten(element, (maxdepth - 1))
            result.extend(temp)
            #for temp_element in temp:
            #    result.append(temp_element)
        else:
            result.append(element)

    return result

class FlattenTest(unittest.TestCase):
    ''' class to unit-test the my_flatten function which implements P1 '''

    def test_empty(self):
        ''' test my_flatten with empty list '''
        self.assertItemsEqual(my_flatten([]), [])

    def test_depth1(self):
        ''' Test depth of one '''
        tested = [1, [2]]
        expected = [1, 2]
        self.assertListEqual(my_flatten(tested, 1), expected, "just one nested list of one element")

        tested = [1, [2, [3]]]
        expected = [1, 2, [3]]
        self.assertListEqual(my_flatten(tested, 1), expected, "2 nested lists, each of 1 element")

        tested = [1, [2, [3]]]*100
        expected = [1, 2, [3]]*100
        self.assertListEqual(my_flatten(tested, 1), expected, "100 copies of two nested lists")

        tested = [1, [2, 3]]*100
        expected = [1, 2, 3]*100
        self.assertListEqual(my_flatten(tested, 1), expected, "100 copies of 1 nested list")

        tested = [1, 2, 3]
        expected = [1, 2, 3]
        self.assertListEqual(my_flatten(tested, 1), expected, "a simple list, nothing nested")

        self.assertListEqual(my_flatten([], 1), [], "empty list, but max-depth=1")

    def test_depth2(self):
        ''' Test depth of two '''
        self.assertListEqual(my_flatten([], 2), [], "empty list but depth is two")
        self.assertListEqual(my_flatten([4, 5, 6], 2), [4, 5, 6], "list with depth = 0")
        self.assertListEqual(my_flatten([4, [5, 6]], 2), [4, 5, 6], "list with depth = 1")
        tested = [4, 5, [6, 7, [8, 9], 10, 11]]
        expected = [4, 5, 6, 7, 8, 9, 10, 11]
        self.assertListEqual(my_flatten(tested, 2), expected, "list with depth = 2")
        tested = [4, 5, [6, 7, [8, 9, [99]]], [10, 11, [[12], [13, 14]]]]
        expected = [4, 5, 6, 7, 8, 9, [99], 10, 11, [12], [13, 14]]
        self.assertListEqual(my_flatten(tested, 2), expected, "list with depth = 3")

    def test_depth100(self):
        ''' Test a greater depth '''
        tested = []
        for i in range(100):
            tested = [tested, i]
        expected = range(100)
        self.assertListEqual(my_flatten(tested, 100), expected, "list with depth = 100")
        #962 is at most my recursion goes (963-> maximum recursion for a Python object)
        tested = []
        for i in range(962):
            tested = [tested, i]
        expected = range(962)
        self.assertListEqual(my_flatten(tested, 962), expected, "list with depth = 962")

    def test_depth_negative(self):
        ''' test some negative values for depth '''
        self.assertListEqual(my_flatten([], -1), [], "empty list + negative depth = empty list")
        self.assertListEqual(my_flatten([1, 2, 3], -1), [1, 2, 3], "simple list + negative depth")
        tested = [1, [2, 3]]
        expected = [1, [2, 3]]
        self.assertListEqual(my_flatten(tested, -1), expected, "nested list, negative depth")
        tested, expected = [], []
        for i in range(100):
            tested = [tested, i]
            expected = [expected, i]
        self.assertListEqual(my_flatten(tested, -1), expected, "nested list, negative depth")
