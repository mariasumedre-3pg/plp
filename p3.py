''' Python script to implement P3 of Python Learning Program
    And some unittests for it (at the end of the file) '''

import unittest
#import pytest
import copy

def my_sort(input_f, output_f):
    ''' Sorting algorithm for P3
        First sorting attempt '''
    data = read_file(input_f)
    dict_list = build_dict_list(data)
    dict_order = dict_sort_order(dict_list) #first sorting method
    write_file(dict_order, output_f)
    return dict_order

def my_sort2(input_f, output_f):
    ''' Sorting algorithm for P3
        Second sorting attempt '''
    data = read_file(input_f)
    dict_list = build_dict_list(data)
    dict_order = dict_sort(dict_list) #second sorting method
    write_file(dict_order, output_f)
    return dict_order

def my_sort3(input_f, output_f):
    ''' Sorting algorithm for P3
        Third sorting attempt '''
    data = read_file(input_f)
    dict_list = build_dict_list(data)
    dict_order = dict_sort_with_key(dict_list) #second sorting method
    write_file(dict_order, output_f)
    return dict_order

def read_file(filepath):
    ''' read file and return the strings within in a list of strings '''
    lines = []
    with open(filepath, 'r') as fpointer:
        lines = [line.strip() for line in fpointer]
        #for line in fpointer:
        #    # strip start and end of line of any whitespace characters
        #    lines.append(line.strip())
    return lines

def build_dict_list(data):
    """ build a list of dictionaries from the list of strings
        which could have been read from a file (or from another source)
        """
    # list of all dictionaries found in file, which will be returned
    dictionaries = []
    # because we parse one line at a time,
    # we are adding key-value pairs in a (temp) dictionary and
    # only after we read newline will we add the (temp) dictionary to list of dictionaries
    current_dictionary = {}
    for line in data:
        line = line.strip()
        # stackoverflow tells me that '==' uses __cmp__ while 'is' checks address
        if line:
            # there should be 2 values: the key and the pair
            lines = line.split(' ')
            # adding the same key cases a KeyError exception to be thrown,
            # so we check for that case
            if len(lines) > 1 and (lines[0] not in current_dictionary):
                current_dictionary[lines[0]] = lines[1]
        # if we read a newline, then the temp dictionary is ready
        # to be added to the list of dictionaries
        elif current_dictionary:
            dictionaries.append(current_dictionary)
            current_dictionary = {}
    # append last dictionary, if it exists (i.e. no endline at end of input file)
    if current_dictionary:
        dictionaries.append(current_dictionary)
    return dictionaries

def dict_sort_order(dict_list):
    ''' actually sort the dictionary list
        meaning, provide an order in the result list
        it probably needs improvement '''
    result = []
    # make a copy to not modify the passed param/arg
    copy_dict_list = copy.deepcopy(dict_list)
    # while there are items in the copy, keep removing items from it
    while copy_dict_list != []:
        # find minimum
        idx, item = min_dict(copy_dict_list)
        # put in the result the index from the original list
        result.append(dict_list.index(item))
        # remove that minimum
        copy_dict_list.pop(idx)

    return result

def dict_sort(dict_list):
    ''' sort a list of dictionaries based on the
        dict_less_than (dict_int_less_than) method/function '''
    sorted_list = sorted(dict_list, cmp=dict_int_less_than)
    return sorted_list

def dict_sort_with_key(dict_list):
    ''' sort a list of dictionaries based on the
        dict_less_than (dict_key_less_than) method/function '''
    sorted_list = sorted(dict_list, key=dict_key_less_than)
    return sorted_list

def write_file(dict_list, filepath):
    ''' write the provided sorted order in the provided filepath '''
    # open file in writemode - i think this creates the file, if it doesn't exist
    with open(filepath, 'w') as fpointer:
        for dict_idx in dict_list:
            fpointer.write(str(dict_idx) + '\n')

def min_dict(dict_list):
    ''' find the minimum of the dictionaries '''
    # return the index of the minimum
    min_idx = None
    # return the minimum
    minimum = None
    # check types before iterating
    if isinstance(dict_list, (list, tuple)):
        for idx, item in enumerate(dict_list):
            # check if there is a dictionary,
            # that we don't have the first minimum (first element of dictionary,
            # that the item is less than our minimum so far
            if isinstance(item, dict) and ((min_idx is None) or (dict_less_than(item, minimum))):
                min_idx = idx
                minimum = item
    return (min_idx, minimum)

def dict_int_less_than(dict_a, dict_b):
    ''' an adapter for the cmp function for sorted
        it uses the dict_less_than and converts the
        boolean result to int '''
    result = 0
    result_bool = dict_less_than(dict_a, dict_b)
    if result_bool is True:
        result = -1
    elif result_bool is False:
        result = 1
    return result

def dict_key_less_than(dictionary):
    ''' an adapter for the key function for sorted
        it adds the keys and the values together in a string '''
    keys = sorted(dictionary.keys())
    result = ""
    for key in keys:
        result += dictionary[key]
    # this doesn't work :(
    #result = reduce((lambda key1, key2: str(dictionary[key1]) + str(dictionary[key2])),
    #               keys)
    return result

def dict_less_than(dict_a, dict_b):
    ''' the comparison operation for two dicts
        there's a sort here as well: for the keys
        there's an assumption that the keys are the same
        between dict_a and dict_b '''
    # result is undefined at start
    result = None

    # get the keys, we compare through these
    keys_a = dict_a.keys()
    keys_b = dict_b.keys()

    while result is None and keys_a != [] and keys_b != []:
        # setup some variables: the lowest key and its value
        # for each dictionary
        min_a = min(keys_a)
        min_b = min(keys_b)

        value_a = dict_a[min_a]
        value_b = dict_b[min_b]

        # import ipdb; ipdb.set_trace()
        if value_a > value_b:
            result = False
        elif value_a < value_b:
            result = True
        #if the values are equal, we check next keys in the dictionaries (result still None)
        elif value_a == value_b:
            # remove minimums from the keys, so min will take the next minimum,
            # which is greater than this minimum
            keys_a.remove(min_a)
            keys_b.remove(min_b)
    if result is None:
        result = False
    return result

class SortTest(unittest.TestCase):
    ''' class to test the my_sort function'''
    def test_sortsimple(self):
        ''' test sorting an empty dictionary '''
        exp = [2, 1, 0]
        input_f = 'dictionaries.in'
        output_f = 'dictionaries.out'
        result = my_sort(input_f, output_f)
        self.assertListEqual(result, exp, "test sorting an empty dict")

def test_simple():
    """Equivalent test in pytest"""
    exp = [2, 1, 0]
    input_f = 'dictionaries.in'
    output_f = 'dictionaries.out'
    result = my_sort(input_f, output_f)
    assert result == exp

##########################################################
### Test the methods for second sorting with pytest
##########################################################

DATA_STRINGS = ["",
                "name lancelot",
                "weapon sword",
                "faction arthur",
                "",
                "name guinevera",
                "faction arthur",
                "weapon diplomacy",
                "",
                "name arthur",
                "weapon excalibur",
                "faction arthur",
               ]

DATA_INT = ["",
            "x 12",
            "y 1.3",
            "z 0",
            "",
            "x 12693947295",
            "y 2.3",
            "z 4",
            "",
            "x 11.7",
            "y 1",
            "z 0"
           ]

DATA_STRINGS_SORTED = [{'name': 'arthur',
                        'faction': 'arthur',
                        'weapon': 'excalibur'},
                       {'name': 'guinevera',
                        'faction': 'arthur',
                        'weapon': 'diplomacy'},
                       {'name': 'lancelot',
                        'faction': 'arthur',
                        'weapon': 'sword'}]

DATA_INT_SORTED = [{'y': '1', 'x': '11.7', 'z':'0'},
                   {'y': '1.3', 'x': '12', 'z':'0'},
                   {'y': '2.3', 'x': '12693947295', 'z':'4'}
                  ]

def test_mysort2():
    """ test the second sorting method """
    exp = DATA_STRINGS_SORTED
    input_f = 'dictionaries.in'
    output_f = 'dictionaries.out'
    result = my_sort2(input_f, output_f)
    assert result == exp

def test_dict_sort():
    """ test dict_sort which is used in the second sorting method """
    # build the list of dictionaries
    exp_dict_list = [DATA_STRINGS_SORTED[2], DATA_STRINGS_SORTED[1], DATA_STRINGS_SORTED[0]]
    dict_list = build_dict_list(DATA_STRINGS)
    assert dict_list == exp_dict_list
    # check the sorting
    result = dict_sort(dict_list)
    assert result == DATA_STRINGS_SORTED

def test_dict_sort_key():
    """ test dict_sort which is used in the second sorting method """
    # build the list of dictionaries
    exp_dict_list = [DATA_STRINGS_SORTED[2], DATA_STRINGS_SORTED[1], DATA_STRINGS_SORTED[0]]
    dict_list = build_dict_list(DATA_STRINGS)
    assert dict_list == exp_dict_list
    # check the sorting
    result = dict_sort_with_key(dict_list)
    assert result == DATA_STRINGS_SORTED

def test_dict_sort_key_int():
    """ test dict_sort which is used in the second sorting method """
    # build the list of dictionaries
    exp_dict_list = [DATA_INT_SORTED[1], DATA_INT_SORTED[2], DATA_INT_SORTED[0]]
    dict_list = build_dict_list(DATA_INT)
    assert dict_list == exp_dict_list
    # check the sorting
    result = dict_sort_with_key(dict_list)
    assert result == DATA_INT_SORTED
