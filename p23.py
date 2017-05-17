""" Python script to implement the 3rd exercise of the 2nd Phase in Python Learning Program
    or musings on how ethical and helpful it is to use stackoverflow:
    http://stackoverflow.com/questions/3931627/how-to-build-a-python-decorator-with-optional-parameters """

import timeit
import cProfile
import pstats
import StringIO
import time
from functools import wraps

def time_slow(threshold=0.0):
    """ decorator that takes an optional parameter
        so how decorators work:
        - threshold might be the function that is getting decorated
        - threshold might be an argument to the function that is getting decorated
          in which case the actual function is passed magically to another nested function def """
    result = None
    # if time_slow was "called" without paranthesis
    if callable(threshold):
        @wraps(threshold)
        def func_wrapper():
            """ add how much time it took to run the function """
            #func_name = "{}".format(getattr(threshold, '__name__'))
            profiler = cProfile.Profile()
            profiler.enable()
            threshold()
            profiler.disable()
            sstream = StringIO.StringIO()
            sortby = 'time'
            profiler_stats = pstats.Stats(profiler, stream=sstream).sort_stats(sortby)
            profiler_stats.print_stats()
            print sstream.getvalue()
            #seconds = timeit.timeit(stmt=func_name, setup="import p23", number=1)
            #if seconds >= threshold:
            #    print "it took {0:.2f} seconds to run {1}".format(seconds, func_name)
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

def my_timer(func):
    """ simple timer for a function """
    start = time.time()
    func()
    end = time.time()
    total = float(end) - float(start)
    return total

def time_slow2(threshold=0.0):
    """ decorator that takes an optional parameter """
    if callable(threshold):
        @wraps(threshold)
        def func_wrapper():
            """ add how much time it took to run the function """
            func_name = "{0}()".format(getattr(threshold, '__name__'))
            seconds = my_timer(threshold)
            result = "it took {0:.2f} seconds to run {1}".format(seconds, func_name)
            print result
            return result
        return func_wrapper
    else:
        def time_func(func):
            """ function decorator test """
            @wraps(func)
            def func_wrapper():
                """ add how much time it took to run the function """
                func_name = "{0}()".format(getattr(func, '__name__'))
                seconds = my_timer(func)
                result = ""
                if float(seconds) >= float(threshold): # make sure both are float?
                    result = "it took {0:.2f} seconds to run {1}".format(seconds, func_name)
                    print result
                return result
            return func_wrapper
    return time_func

@time_slow(threshold=0.05)
def myfast():
    """ some function to be decorated """
    pass

@time_slow2(threshold=0.05)
def sleep_0_7_sec():
    """ some function to be decorated """
    time.sleep(0.7)
    print "done"

@time_slow2(threshold=0.4)
def sleep_0_3_sec():
    """ some function to be decorated """
    time.sleep(0.3)
    print "done"

def test_time_slow_with_threshold():
    """ test time_slow decorator with a threshold """
    myfast()
    result = sleep_0_7_sec()
    assert "it took 0.70 seconds" in result
    result = sleep_0_3_sec()
    assert result is ""

@time_slow
def myfast2():
    """ some function to be decorated """
    pass

def test_time_slow():
    """ test time_slow decorator without a threshold """
    myfast2()
    # no assert yet, working on it
