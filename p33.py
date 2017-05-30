""" Python script to implement the third problem of the third phase of Python Learning Program """

import inspect

class Trololo(type):
    def __new__(cls, name, bases, dictionary):
        def mynew(cls, name, bases, dictionary):
            super()
        return super(Trololo, cls).__new__(cls, name, bases, dictionary)


class SingletonMetaClass(type):
    'from internet'

    # def __new__(cls, name, bases, dictionary):
    #     print cls, '__new__ called'
    #     return super(SingletonMetaClass, cls).__new__(cls, name, bases, dictionary)

    def __init__(cls, name, bases, dictionary):
        print cls, '__init__ called'
        super(SingletonMetaClass, cls).__init__(name, bases, dictionary)
        original_new = cls.__new__
        def my_new(cls, *args, **kwargs):
            'new returning same instance'
            print '{} {} {} __new__ called'.format(cls, args, kwargs)
            if not hasattr(cls, 'instance'):
                cls.instance = original_new(cls, *args, **kwargs)
            return cls.instance
        cls.instance = None
        cls.__new__ = staticmethod(my_new)


class SingletonMeta(type):
    """ Metaclass to try enforcing the singleton """
    #remember here the instances
    registry = {}
    #remember here the old classes, in case we need another instance
    registry_old = {}

    @classmethod
    def get_instance(mcs, key, *args, **kwds):
        "simply return instance, but arguments seem important"
        print "use custom constructor for", key
        # this now does automagically happen
        #mcs.registry[key].__init__(*args, **kwds)
        return mcs.registry[key]

    @classmethod
    def build_an_instance(mcs, bases, new_class):
        """ build an instance of new_class, making sure that if one of it's bases
            was created by SingletonMeta as well, then it has an old registry which
            can be used to build us a new instance """
        instance = None
        for base in bases:
            if hasattr(base, '__metaclass__') and base.__metaclass__ == SingletonMeta:
                instance = mcs.registry_old[base.__name__](new_class)
                print "instance created with old base", base
                break
        if instance is None:
            print "instance created with base", bases[0]
            instance = bases[0].__new__(new_class)
        return instance

    @classmethod
    def build_an_instance2(mcs, bases, new_class):
        """ build an instance of new_class, making sure that if one of it's bases
            was created by SingletonMeta as well, then it has an old registry which
            can be used to build us a new instance """
        instance = None
        for base in bases:
            if hasattr(base, '__metaclass__') and base.__metaclass__ == SingletonMeta:
                base_list = inspect.getmro(base)
                #instance = mcs.registry_old[base.__name__](new_class)
                #print "instance created with old base", base
                break
        if instance is None:
            print "instance created with base", bases[0]
            instance = bases[0].__new__(new_class)
        return instance

    def __new__(mcs, name, bases, dictionary):
        print 'new:', mcs, name, bases
        # add a __name__ attribute to the class, maybe this exists under another name?
        dictionary['__name__'] = name

        # create the class definition, this will be stored in registry_old in case
        # instances of the class are needed
        new_class = super(SingletonMeta, mcs).__new__(mcs, name, bases, dictionary)

        #build the instance
        instance = mcs.build_an_instance(bases, new_class)
        #store the instance and the original new_class
        mcs.registry[name] = instance
        mcs.registry_old[name] = new_class.__new__
        #update dictionary with new __new__ method which will apply also __init__
        #dictionary['__new__'] = lambda self, *args, **kwds: mcs.get_instance(name, *args, **kwds)
        new_class.__new__ = staticmethod(
            lambda self, *args, **kwds: mcs.get_instance(name, *args, **kwds))
        return new_class


class Example(object):
    __metaclass__ = SingletonMeta

    def __new__(cls, *args, **kwargs):
        print 'Example __new__', cls, args, kwargs
        return super(Example, cls).__new__(cls, *args, **kwargs)


class SubExample(Example):
    pass


class SomeClass(object):
    """ some class to that should be a singleton """
    __metaclass__ = SingletonMetaClass

    def __init__(self, x=None):
        """ initializes a integer x with 0, if singleton then only once(?) """
        if x is not None:
            self.x = x


class Foo(SomeClass):
    "test subclasses singletons stuff"
    def __init__(self, argument):
        "test when init is called"
        print 'Foo __init__ called'
        SomeClass.__init__(self, 0)
        print "I am Foo with argument:", argument, self.x


class Bar(SomeClass):
    "test subclasses sngletons stuff"
    def __init__(self):
        "test when init is called"
        SomeClass.__init__(self, 0)
        print "I am Bar:", self.x


class SecondFoo(Foo):
    "test seconds subclasses singletons stuff"
    def __init__(self, *args, **kwargs):
        "test when init is called"
        Foo.__init__(self, 'test')
        print "I am SecondFoo:", self.x


class OtherClass(object):
    """ some other class that should be a singleton """
    __metaclass__ = SingletonMetaClass
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

def test_subclass2():
    """ test another subclass of the singleton """
    instance1 = SecondFoo()
    assert instance1 == SecondFoo()
    assert instance1 is SecondFoo()
    assert instance1.x == 0

    instance2 = Foo('test')
    assert instance1 is not instance2
    assert instance1 != instance2

    instance1.x = -3
    assert instance1.x == -3
