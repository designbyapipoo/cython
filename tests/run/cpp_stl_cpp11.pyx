# mode: run
# tag: cpp, werror
# distutils: extra_compile_args=-std=c++0x

from libcpp.vector cimport vector

ctypedef vector[int] ivector

def test_vector_emplace():
    """
    >>> test_vector_emplace()
    [0, 7]
    """
    cdef ivector v
    v.emplace(v.end())
    v.emplace(v.end(), 7)
    return v

def test_vector_emplace_back():
    """
    >>> test_vector_emplace_back()
    [0, 7]
    """
    cdef ivector v
    v.emplace_back()
    v.emplace_back(7)
    return v

def test_vector_shrink_to_fit():
    """
    >>> test_vector_shrink_to_fit()
    """
    cdef ivector v
    v.shrink_to_fit()

def test_vector_data():
    """
    >>> test_vector_data()
    """
    cdef ivector v = ivector(7)
    assert v.data()
