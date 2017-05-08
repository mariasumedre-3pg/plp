''' a python script to just try things out '''

def cheeseshop(kind, *arguments, **keywords):
    '''example from docs.python.org with the sorted dictionary keys

        just copied down...'''
    print "-- Do you have any", kind, "?"
    print "-- I'm very sorry, we're all out of", kind
    for arg in arguments:
        print arg
    print "-" * 40
    keys = sorted(keywords.keys())
    for keyword in keys:
        print keyword, ":", keywords[keyword]


def my_flatten(my_list, maxdepth=1):
    ''' first flatten version
        my_list - list (of lists) to flatten
        maxdepth - max levels of nesting which are flattened
        '''
    result = []
    #if depth is 0, return an empty list and don't process any further
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

def my_flatten2(my_list, maxdepth):
    ''' second flatten version
        my_list - list (of lists) to flatten - i change this list
        maxdepth - max levels of nesting which are flattened
        '''
    if maxdepth <= 0:
        del my_list[:]
        return

    # remember index in my_list where to insert flattened elements
    idx = 0
    # loop through copy of list because we're modifying the list
    for element in my_list[:]:
        if isinstance(element, (tuple, list)):
            #flatten the list (in case it contains nested lists)
            my_flatten2(element, (maxdepth - 1))
            #delete the list, the contents is in element
            del my_list[idx]
            #add element back to the list, and update index
            for flatidx, flatelement in enumerate(element):
                my_list.insert(idx+flatidx, flatelement)
            idx += len(element)
        else:
            idx += 1


def flatten(list_a, list_b, max_depth):
    ''' p1: return concatenation of 2 flattened lists to a max depth level of max_depth
        list_a - first of the two lists
        list_b - second of the two lists
        max_depth - max level of list nested-ness '''
    both = list_a + list_b
    return my_flatten(both, max_depth)


def flatten2(list_a, list_b, max_depth):
    ''' p1: flatten 2 lists to a max depth level of max_depth
        list_a - first of the two lists
        list_b - second of the two lists
        max_depth - max level of list nested-ness '''
    my_flatten2(list_a, max_depth)
    my_flatten2(list_b, max_depth)
