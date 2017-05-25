""" Python script to implement the third problem of the third phase of Python Learning Program """

class SingletonMeta(type):
    """ Metaclass to try enforcing the singleton """
    registry = {}

    @classmethod
    def add_in_registry(mcs, key, cls):
        'help with putting a class object in the meta dictionary (for the class instances)'
        print "enter the custom constructor for", key
        if key not in mcs.registry:
            mcs.registry[key] = cls()
        return mcs.registry[key]

    def __new__(mcs, name, bases, dictionary):
        print 'new:', mcs, name, bases, dictionary
        # this is the class that would be usually created
        # new_class = type(name, bases, dictionary)
        new_class = super(SingletonMeta, mcs).__new__(mcs, name, bases, dictionary)
        # change the __new__ in the class' definition to return
        # the instance we create in the add_to_dict utility function
        dictionary['__new__'] = lambda cls: SingletonMeta.add_in_registry(name, new_class)
        # change class definition to include updated dictionary(?)
        singleton_class = super(SingletonMeta, mcs).__new__(mcs, name, bases, dictionary)
        # return new class definition
        return singleton_class


class SomeClass(object):
    """ some class to that should be a singleton """
    __metaclass__ = SingletonMeta
    def __init__(self):
        """ initializes a integer x with 0, if singleton then only once(?) """
        self.x = 0


class OtherClass(object):
    """ some other class that should be a singleton """
    __metaclass__ = SingletonMeta
    def __init__(self):
        """ print a message instead of initializing members
            so it is clear how many times this is actually called """
        print "I am an OtherClass instance!"


def test_singleton():
    """ test the singleton with the address thing """
    instance = SomeClass()
    assert instance is SomeClass()
    assert instance == SomeClass()

    assert OtherClass() is OtherClass()
    assert OtherClass() == OtherClass()

def test_2_singleton_not_alike():
    """ test the singleton with the address thing """
    instance1 = SomeClass()
    instance2 = OtherClass()
    assert instance1 is not instance2
    assert instance1 != instance2
