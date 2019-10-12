# mode: run
# tag: cpp, werror, cpp11

from libcpp cimport bool
from libcpp.algorithm cimport all_of, any_of, none_of
from libcpp.vector cimport vector


cdef bool is_odd(int i):
    return i % 2


def all_odd(vector[int] values):
    """
    Test all_of with is_odd predicate.

    >>> all_odd([3, 5, 7, 11, 13, 17, 19, 23])
    True
    >>> all_odd([3, 4])
    False
    """
    return all_of(values.begin(), values.end(), is_odd)


def any_odd(vector[int] values):
    """
    Test any_of with is_odd predicate.

    >>> any_odd([1, 2, 3, 4])
    True
    >>> any_odd([2, 4, 6, 8])
    False
    """
    return any_of(values.begin(), values.end(), is_odd)


def none_odd(vector[int] values):
    """
    Test none_of with is_odd predicate.

    >>> none_odd([2, 4, 6, 8])
    True
    >>> none_odd([1, 2, 3, 4])
    False
    """
    return none_of(values.begin(), values.end(), is_odd)

