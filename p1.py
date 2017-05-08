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
        self.assertListEqual(my_flatten([1, [2]], 1), [1, 2])
        self.assertListEqual(my_flatten([1, [2, [3]]], 1), [1, 2, [3]])
