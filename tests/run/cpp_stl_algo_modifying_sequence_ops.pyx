# mode: run
# tag: cpp, werror, cpp11

from libcpp cimport bool
from libcpp.algorithm cimport copy, copy_if, copy_n, copy_backward
from libcpp.iterator cimport back_inserter
from libcpp.vector cimport vector


def copy_int(vector[int] values):
    """
    Test copy.

    >>> copy_int(range(5))
    [0, 1, 2, 3, 4]
    """
    cdef vector[int] out
    copy(values.begin(), values.end(), back_inserter(out))
    return out


cdef bool is_odd(int i):
    return i % 2


def copy_int_if_odd(vector[int] values):
    """
    Test copy_if.

    >>> copy_int_if_odd(range(5))
    [1, 3]
    """
    cdef vector[int] out
    copy_if(values.begin(), values.end(), back_inserter(out), is_odd)
    return out


def copy_int_n(vector[int] values, int count):
    """
    Test copy_n.

    >>> copy_int_n(range(5), 2)
    [0, 1]
    """
    cdef vector[int] out
    copy_n(values.begin(), count, back_inserter(out))
    return out


def copy_int_backward(vector[int] values):
    """
    Test copy_backward.

    >>> copy_int_backward(range(5))
    [0, 0, 0, 0, 1, 2, 3, 4]
    """
    out = vector[int](values.size() + 3)
    copy_backward(values.begin(), values.end(), out.end())
    return out
