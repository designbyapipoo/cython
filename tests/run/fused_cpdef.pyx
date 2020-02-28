cimport cython
import sys, io

cy = __import__("cython")

cpdef func1(self, cython.integral x):
    print "%s," % (self,),
    if cython.integral is int:
        print 'x is int', x, cython.typeof(x)
    else:
        print 'x is long', x, cython.typeof(x)


class A(object):
    meth = func1
    def __str__(self):
        return "A"

cdef class B:
    cpdef int meth(self, cython.integral x):
        print "%s," % (self,),
        if cython.integral is int:
            print 'x is int', x, cython.typeof(x)
        else:
            print 'x is long', x, cython.typeof(x)
        return 0
    def __str__(self):
        return "B"

pyfunc = func1

def test_fused_cpdef():
    """
    >>> test_fused_cpdef()
    None, x is int 2 int
    None, x is long 2 long
    None, x is long 2 long
    <BLANKLINE>
    None, x is int 2 int
    None, x is long 2 long
    <BLANKLINE>
    A, x is int 2 int
    A, x is long 2 long
    A, x is long 2 long
    A, x is long 2 long
    <BLANKLINE>
    B, x is long 2 long
    """
    func1[int](None, 2)
    func1[long](None, 2)
    func1(None, 2)

    print

    pyfunc[cy.int](None, 2)
    pyfunc(None, 2)

    print

    A.meth[cy.int](A(), 2)
    A.meth(A(), 2)
    A().meth[cy.long](2)
    A().meth(2)

    print

    B().meth(2)


midimport_run = io.StringIO()
try:
    unicode
except NameError:
    pass
else:
    # Monkey-patch midimport_run.write to accept non-unicode strings under Python 2.
    midimport_run.write = lambda c: io.StringIO.write(midimport_run, unicode(c))

realstdout = sys.stdout
sys.stdout = midimport_run

try:
    test_fused_cpdef()
except Exception as e:
    midimport_run.write(f"{e!r}\n")
finally:
    sys.stdout = realstdout

def test_midimport_run():
    """
    >>> test_midimport_run()
    None, x is int 2 int
    None, x is long 2 long
    None, x is long 2 long
    <BLANKLINE>
    None, x is int 2 int
    None, x is long 2 long
    <BLANKLINE>
    A, x is int 2 int
    A, x is long 2 long
    A, x is long 2 long
    A, x is long 2 long
    <BLANKLINE>
    B, x is long 2 long
    """
    print midimport_run.getvalue().strip('\n')


def assert_raise(func, *args):
    try:
        func(*args)
    except TypeError:
        pass
    else:
        assert False, "Function call did not raise TypeError"

def test_badcall():
    """
    >>> test_badcall()
    """
    assert_raise(pyfunc)
    assert_raise(pyfunc, 1, 2, None, 3)
    assert_raise(pyfunc[cy.int], 10, 11, None, 12)
    assert_raise(pyfunc, None, object())
    assert_raise(A().meth)
    assert_raise(A.meth)
    assert_raise(A().meth[cy.int])
    assert_raise(A.meth[cy.int])
    assert_raise(B().meth, 1, 2, 3)

def test_nomatch():
    """
    >>> func1(None, ())
    Traceback (most recent call last):
    TypeError: No matching signature found
    """

ctypedef long double long_double

cpdef multiarg(cython.integral x, cython.floating y):
    if cython.integral is int:
        print "x is an int,",
    else:
        print "x is a long,",

    if cython.floating is long_double:
        print "y is a long double:",
    elif float is cython.floating:
        print "y is a float:",
    else:
        print "y is a double:",

    print x, y

def test_multiarg():
    """
    >>> test_multiarg()
    x is an int, y is a float: 1 2.0
    x is an int, y is a float: 1 2.0
    x is a long, y is a double: 4 5.0
    >>> multiarg()
    Traceback (most recent call last):
    TypeError: Expected at least 2 arguments, got 0
    >>> multiarg(1, 2.0, 3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...2...arg...3...
    """
    multiarg[int, float](1, 2.0)
    multiarg[cy.int, cy.float](1, 2.0)
    multiarg(4, 5.0)

def test_ambiguousmatch():
    """
    >>> multiarg(5, ())
    Traceback (most recent call last):
    TypeError: Function call with ambiguous argument types
    >>> multiarg((), 2.0)
    Traceback (most recent call last):
    TypeError: Function call with ambiguous argument types
    """
