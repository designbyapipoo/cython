# mode: run
# ticket: t5356

cimport cython


@cython.overflowcheck(True)
cdef size_t _mul_checked(size_t a, size_t b) except? -1:
    return a * b


def f(size_t[:] a, size_t[:] b):
    """
    >>> f(memoryview(b"12"), memoryview(b"345"))
    6
    """
    return _mul_checked(a.shape[0], b.shape[0])

