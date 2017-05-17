""" Python script to implement the 3rd exercise of the second Phase in Python Learning Program """

import timeit
from functools import wraps

def time_func(func):
    """ function decorator test """
    @wraps(func)
    def func_wrapper():
        """ add how much time it took to run the function """
        func_name = "p23.{}".format(getattr(func, '__name__'))
        seconds = timeit.timeit(stmt=func_name, setup="import p23", number=1)
        print "it took {0:.2f} seconds to run {1}".format(seconds, func_name)
    return func_wrapper

def time_slow(threshold):
    """ decorator that takes an optional parameter """
    return time_func

@time_slow(threshold=0.05)
def myfast():
    """ some function to be decorated """
    pass

@time_func
def myfast2():
    """ some function to be decorated """
    pass
