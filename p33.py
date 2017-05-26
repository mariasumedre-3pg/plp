""" Python script to implement the third problem of the third phase of Python Learning Program """


class SingletonMeta(type):
    """ Metaclass to try enforcing the singleton """
    registry = {}
    registry_old = {}

    @classmethod
    def get_instance(mcs, key, *args, **kwds):
        "return instance and also "
        print "use custom constructor for", key
        mcs.registry[key].__init__(*args, **kwds)
        return mcs.registry[key]

    def __new__(mcs, name, bases, dictionary):
        print 'new:', mcs, name, bases
        dictionary['__name__'] = name
        new_class = super(SingletonMeta, mcs).__new__(mcs, name, bases, dictionary)

        instance = None
        for base in bases:
            if hasattr(base, '__metaclass__') and base.__metaclass__ == SingletonMeta:
                instance = mcs.registry_old[base.__name__].__new__(new_class)
                print "instance created with old base", base
                break
        if instance is None:
            print "instance created with base", bases[0]
            instance = bases[0].__new__(new_class)

        mcs.registry[name] = instance
        mcs.registry_old[name] = new_class

        dictionary['__new__'] = lambda self, *args, **kwds: mcs.get_instance(name, *args, **kwds)

        singleton_class = super(SingletonMeta, mcs).__new__(mcs, name, bases, dictionary)

        return singleton_class


class SomeClass(object):
    """ some class to that should be a singleton """
    __metaclass__ = SingletonMeta
    def __init__(self, x=None):
        """ initializes a integer x with 0, if singleton then only once(?) """
        if x is not None:
            self.x = x

class Foo(SomeClass):
    "test subclasses singletons stuff"
    def __init__(self, argument):
        "test when init is called"
        SomeClass.__init__(self, 0)
        print "I am Foo with argument:", argument, self.x

class Bar(SomeClass):
    "test subclasses singletons stuff"
    def __init__(self):
        "test when init is called"
        SomeClass.__init__(self, 0)
        print "I am Bar:", self.x

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

    instance.x = 12
    instance2 = SomeClass()
    assert instance2.x == 12

    assert OtherClass() is OtherClass()
    assert OtherClass() == OtherClass()

def test_singleton_values():
    """ test the singleton with values """
    instance = SomeClass()
    instance.x = 12

    instance2 = SomeClass()
    assert instance2.x == 12

def test_2_singleton_not_alike():
    """ test the singleton with the address thing """
    instance1 = SomeClass()
    instance2 = OtherClass()
    assert instance1 is not instance2
    assert instance1 != instance2

def test_subclass():
    """ test a subclass of the singleton """
    instance1 = Foo(2)
    assert instance1 == Foo(2)
    assert instance1 is Foo(2)

    instance2 = Bar()
    assert instance2 == Bar()
    assert instance2 is Bar()

    assert instance1 != instance2
    assert instance1 is not instance2
    instance1.x = -3
    assert instance2.x == 0
