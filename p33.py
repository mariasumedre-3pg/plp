""" Python script to implement the third problem of the third phase of Python Learning Program """

def utility(dictionary, key, cls):
    'help with putting a class object in the class dictionary from the meta'
    print "enter the custom constructor for", key
    if key not in dictionary:
        dictionary[key] = cls()
    return dictionary[key]

class Meta(type):
    """ Metaclass to try enforcing the singleton """
    registry = {}

    def __new__(mcs, name, bases, dictionary):
        print 'new:', mcs, name, bases, dictionary
        # this is the class that would be usually created
        new_class = type(name, bases, dictionary)
        # change the __new__ in the class' definition to return the instance we create in utility
        dictionary['__new__'] = lambda cls: utility(mcs.registry, cls.__class__, new_class)
        # change class definition to include updated dictionary(?)
        singleton_class = type(name, bases, dictionary)
        # return new class definition
        return singleton_class
        #return super(Meta, mcs).__new__(mcs, name, bases, dictionary)


class SomeClass(object):
    """ some class to that should be a singleton """
    __metaclass__ = Meta
    def __init__(self):
        """ initializes a integer x with 0, if singleton then only once(?) """
        self.x = 0


def test_singleton():
    """ test the singleton with the address thing """
    instance = SomeClass()
    assert instance is SomeClass()
