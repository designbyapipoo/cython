# cython: profile=True

@cython.cfunc
@cython.inline
@cython.exceptval(-1.0)
def recip_square(i: cython.int) -> cython.double:
    return 1. / (cython.cast(cython.long, i) * i)

def approx_pi(n: cython.int = 10000000):
    val: cython.double = 0.
    k: cython.int
    for k in range(1, n + 1):
        val += recip_square(k)
    return (6 * val) ** .5
