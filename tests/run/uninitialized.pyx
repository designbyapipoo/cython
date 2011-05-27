# mode: run
# tag: control-flow, uninitialized

def conditional(cond):
    """
    >>> conditional(True)
    []
    >>> conditional(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    if cond:
        a = []
    return a

def inside_loop(iter):
    """
    >>> inside_loop([1,2,3])
    3
    >>> inside_loop([])
    Traceback (most recent call last):
    ...
    UnboundLocalError: i
    """
    for i in iter:
        pass
    return i

def try_except(cond):
    """
    >>> try_except(True)
    []
    >>> try_except(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    try:
        if cond:
            a = []
        raise ValueError
    except ValueError:
        return a

def try_finally(cond):
    """
    >>> try_finally(True)
    []
    >>> try_finally(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    try:
        if cond:
            a = []
        raise ValueError
    finally:
        return a

def deleted(cond):
    """
    >>> deleted(False)
    {}
    >>> deleted(True)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    a = {}
    if cond:
        del a
    return a

def test_nested(cond):
    """
    >>> test_nested(True)
    <built-in function a>
    >>> test_nested(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    if cond:
        def a():
            pass
    return a

def test_outer(cond):
    """
    >>> test_outer(True)
    {}
    >>> test_outer(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    if cond:
        a = {}
    def inner():
        return a
    return a

def test_inner(cond):
    """
    >>> test_inner(True)
    {}
    >>> test_inner(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    if cond:
        a = {}
    def inner():
        return a
    return inner()

def test_class(cond):
    """
    >>> test_class(True) #doctest: +ELLIPSIS
    <class uninitialized.A at 0x...>
    >>> test_class(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: A
    """
    if cond:
        class A:
            pass
    return A
