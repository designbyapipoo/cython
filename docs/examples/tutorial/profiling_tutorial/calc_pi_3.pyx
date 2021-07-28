# cython: profile=True




cdef inline double recip_square(int i) except -1.0:
    return 1. / (<long> i * i)

def approx_pi(int n=10000000):
    cdef double val = 0.
    cdef int k
    for k in range(1, n + 1):
        val += recip_square(k)
    return (6 * val) ** .5
