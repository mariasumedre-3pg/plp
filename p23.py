""" Python script to implement the 3rd exercise of the 2nd Phase in Python Learning Program
    or musings on how ethical and helpful it is to use stackoverflow:
    http://stackoverflow.com/questions/3931627/how-to-build-a-python-decorator-with-optional-parameters """

import timeit
from functools import wraps

def time_slow(threshold=1.00):
    """ decorator that takes an optional parameter
        so how decorators work:
        - threshold might be the function that is getting decorated
        - threshold might be an argument to the function that is getting decorated
          in which case the actual function is passed magically to another nested function def """
    result = None
    # if time_slow was "called" without paranthesis and possibly params
    if callable(threshold):
        @wraps(threshold)
        def func_wrapper():
            """ add how much time it took to run the function """
            func_name = "p23.{}".format(getattr(threshold, '__name__'))
            seconds = timeit.timeit(stmt=func_name, setup="import p23", number=1)
            print "it took {0:.2f} seconds to run {1}".format(seconds, func_name)
        result = func_wrapper
    else: # if time_slow was "called" with paranthesis and possibly params
        def time_func(func):
            """ function decorator test """
            @wraps(func)
            def func_wrapper():
                """ add how much time it took to run the function """
                func_name = "p23.{}".format(getattr(func, '__name__'))
                seconds = timeit.timeit(stmt=func_name, setup="import p23", number=1)
                print "it took {0:.2f} seconds to run {1}".format(seconds, func_name)
            return func_wrapper
        result = time_func
    return result

@time_slow(threshold=0.05)
def myfast():
    """ some function to be decorated """
    pass

def test_time_slow_with_threshold():
    """ test time_slow decorator with a threshold """
    myfast()
    # no assert yet, working on it

@time_slow
def myfast2():
    """ some function to be decorated """
    pass

def test_time_slow():
    """ test time_slow decorator without a threshold """
    myfast2()
    # no assert yet, working on it
