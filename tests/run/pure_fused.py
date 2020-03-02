# mode: run
# tag: fused, pure3.0

#cython: annotation_typing=True

from __future__ import annotations

import cython

InPy = cython.fused_type(cython.int, cython.float)

class TestCls:
    # although annotations as strings isn't recommended and generates a warning
    # it does allow the test to run on more (pure) Python versions
    def func1(self, arg: 'NotInPy'):
        """
        >>> TestCls().func1(1.0)
        'float'
        >>> TestCls().func1(2)
        'int'
        """
        return cython.typeof(arg)

    if cython.compiled:
        @cython.locals(arg = NotInPy)  # NameError in pure Python
        def func2(self, arg):
            """
            >>> TestCls().func2(1.0)
            'float'
            >>> TestCls().func2(2)
            'int'
            """
            return cython.typeof(arg)

    def cpfunc(self, arg):
        """
        >>> TestCls().cpfunc(1.0)
        'float'
        >>> TestCls().cpfunc(2)
        'int'
        """
        return cython.typeof(arg)

    def func1_inpy(self, arg: InPy):
        """
        >>> TestCls().func1_inpy(1.0)
        'float'
        >>> TestCls().func1_inpy(2)
        'int'
        """
        return cython.typeof(arg)

    @cython.locals(arg = InPy)
    def func2_inpy(self, arg):
        """
        >>> TestCls().func2_inpy(1.0)
        'float'
        >>> TestCls().func2_inpy(2)
        'int'
        """
        return cython.typeof(arg)

