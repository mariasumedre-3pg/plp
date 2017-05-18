""" Python script to implement the 3rd exercise of the 2nd Phase in Python Learning Program
    or musings on how ethical and helpful it is to use stackoverflow:
    http://stackoverflow.com/questions/3931627/how-to-build-a-python-decorator-with-optional-parameters """

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
            profiler = cProfile.Profile()
            profiler.enable()
            threshold()
            profiler.disable()
            sstream = StringIO.StringIO()
            sortby = 'time'
            profiler_stats = pstats.Stats(profiler, stream=sstream).sort_stats(sortby)
            profiler_stats.print_stats()
            print sstream.getvalue().strip()
        result = func_wrapper
    else: # if time_slow was "called" with paranthesis and possibly params
        def time_func(func):
            """ function decorator test """
            @wraps(func)
            def func_wrapper():
                """ add how much time it took to run the function """
                profiler = cProfile.Profile()
                profiler.enable()
                func()
                profiler.disable()
                sstream = StringIO.StringIO()
                sortby = 'time'
                profiler_stats = pstats.Stats(profiler, stream=sstream).sort_stats(sortby)
                profiler_stats.print_stats()
                data = sstream.getvalue().strip()
                lines = data.splitlines()
                # check if data is as expected -> no exceptions?
                lines_no = len(lines)
                keyw1 = "function calls"
                keyw2 = " seconds"
                keyw3 = "percall"
                if lines_no > 5 and keyw1 in lines[0] and keyw2 in lines[0] and keyw3 in lines[4]:
                    print lines[0]
                    header = lines[4].strip().split(' ')
                    header = [key for key in header if key != '']
                    print ' '.join(header)
                    rows = []
                    for row in lines[5:]:
                        values = row.strip().split(' ')
                        values = [element for element in values if element != '']
                        rows.append(values)
                    for row in rows:
                        # check percall time in row, it whould be the third element
                        if len(row) > 5:
                            seconds = float(row[2])
                            if seconds >= threshold:
                                print ' '.join(row)
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
    print "running myfast"

@time_slow
def myfast2():
    """ some function to be decorated """
    print "running myfast2"

def sleep_sec(value):
    """ helper for the decorator test -> inner call takes [value] seconds """
    print "sleeping {0} seconds ...".format(str(value))
    time.sleep(value)
    print "wakeup after {0} seconds".format(str(value))

@time_slow(threshold=0.05)
def func_to_decorate():
    """ some function to be decorated """
    print "in func_to_decorate"
    sleep_sec(0.1)
    sleep_sec(0.05)
    sleep_sec(0.02)
    print "done"

@time_slow2(threshold=0.05)
def sleep_0_7_sec():
    """ some function to be decorated """
    time.sleep(0.7)
    print "done"
    return "done"

@time_slow2(threshold=0.4)
def sleep_0_3_sec():
    """ some function to be decorated """
    time.sleep(0.3)
    print "done"
    return "done"

def test_time_slow_with_threshold():
    """ test time_slow decorator with a threshold """
    myfast()
    result = sleep_0_7_sec()
    assert "it took 0.70 seconds" in result
    result = sleep_0_3_sec()
    assert result is ""

def test_time_slow():
    """ test time_slow decorator without a threshold """
    myfast2()
    func_to_decorate()
    # no assert yet, working on it
