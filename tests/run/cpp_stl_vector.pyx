# mode: run
# tag: cpp, werror

from cython.operator cimport dereference as d
from cython.operator cimport preincrement as incr

from libcpp.vector cimport vector

ctypedef vector[int] ivector

def test_constructors(int canary):
    """
    >>> test_constructors(7)
    ([], [7, 7], [0, 0], [7, 7], [7, 7])
    """
    cdef ivector v1 = ivector()
    cdef ivector v2 = ivector(2, canary)
    cdef ivector v3 = ivector(2)
    cdef ivector v4 = ivector(v2.begin(), v2.end())
    cdef ivector v5 = ivector(v2)
    return v1, v2, v3, v4, v5

def test_assign(int canary):
    """
    >>> test_assign(7)
    ([7, 7], [7, 7])
    """
    cdef ivector v1, v2
    v1.assign(2, canary)
    v2.assign(v1.begin(), v1.end())
    return v1, v2

def test_access(ivector v, int i):
    """
    >>> test_access((1, 2, 3), 1)
    (2, 2, 1, 3)
    >>> test_access((1, 2, 3), 5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    IndexError: ...
    """
    return v.at(i), v[i], v.front(), v.back()

def test_capacity(ivector v):
    """
    >>> all(test_capacity((1, 2, 3)))
    True
    """
    v.reserve(9)
    v.resize(5)
    v.resize(7, 0)
    return not v.empty(), v.size() > 0, v.max_size() > 0, v.capacity() > 0

def test_modifiers():
    """
    >>> test_modifiers()
    (0, 0)
    """
    cdef ivector v1 = ivector(3)
    cdef ivector v2 = ivector(3)
    v2.insert(v2.end(), 1)
    v2.insert(v2.end(), v1.begin(), v1.end())
    v1.clear()
    v2.pop_back()
    v2.erase(v2.begin())
    v2.erase(v2.begin(), v2.end())
    return v1.size(), v2.size()

def test_swap(ivector v1, ivector v2):
    """
    >>> test_swap((1, 2), (3, 4))
    ([3, 4], [1, 2])
    """
    v1.swap(v2)
    return v1, v2

def simple_test(double x):
    """
    >>> simple_test(55)
    3
    """
    v = new vector[double]()
    try:
        v.push_back(1.0)
        v.push_back(x)
        from math import pi
        v.push_back(pi)
        return v.size()
    finally:
        del v

def list_test(L):
    """
    >>> list_test([1,2,4,8])
    (4, 4)
    >>> list_test([])
    (0, 0)
    >>> list_test([-1] * 1000)
    (1000, 1000)
    """
    v = new vector[int]()
    try:
        for a in L:
            v.push_back(a)
        return len(L), v.size()
    finally:
        del v

def index_test(L):
    """
    >>> index_test([1,2,4,8])
    (1.0, 8.0)
    >>> index_test([1.25])
    (1.25, 1.25)
    """
    v = new vector[double]()
    try:
        for a in L:
            v.push_back(a)
        return v[0][0], v[0][len(L)-1]
    finally:
        del v


def index_set_test(L):
    """
    >>> index_set_test([1,2,4,8])
    (-1.0, -8.0)
    >>> index_set_test([1.25])
    (-1.25, -1.25)
    """
    v = new vector[double]()
    try:
        for a in L:
            v.push_back(a)
        for i in range(v.size()):
            d(v)[i] = -d(v)[i]
        return d(v)[0], d(v)[v.size()-1]
    finally:
        del v

def iteration_test(L):
    """
    >>> iteration_test([1,2,4,8])
    1
    2
    4
    8
    """
    v = new vector[int]()
    try:
        for a in L:
            v.push_back(a)
        it = v.begin()
        while it != v.end():
            a = d(it)
            incr(it)
            print(a)
    finally:
        del v

def reverse_iteration_test(L):
    """
    >>> reverse_iteration_test([1,2,4,8])
    8
    4
    2
    1
    """
    v = new vector[int]()
    try:
        for a in L:
            v.push_back(a)
        it = v.rbegin()
        while it != v.rend():
            a = d(it)
            incr(it)
            print(a)
    finally:
        del v

def nogil_test(L):
    """
    >>> nogil_test([1,2,3])
    3
    """
    cdef int a
    with nogil:
        v = new vector[int]()
    try:
        for a in L:
            with nogil:
                v.push_back(a)
        return v.size()
    finally:
        del v

def item_ptr_test(L, int i, int x):
    """
    >>> item_ptr_test(range(10), 7, 100)
    [0, 1, 2, 3, 4, 5, 6, 100, 8, 9]
    """
    cdef vector[int] v = L
    cdef int* vi_ptr = &v[i]
    vi_ptr[0] = x
    return v
