""" learn about the generators """
import itertools


def divides(number):
    """ need a function instead of putting lambda drectly """
    return lambda x: x % number


def integers(start_=2):
    """ instead of itertools.count(2), generator function thing"""
    index = start_
    while True:
        yield index
        index += 1


def primes():
    """ generator function thing for prime numbers """
    sieve = integers()  # itertools.count(2)
    while True:
        prime = next(sieve)
        yield prime
        sieve = itertools.ifilter(divides(prime), sieve)
        # sieve = (num for num in sieve if divides(primes)(num))
