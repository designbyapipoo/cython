cimport cython

@cython.dataclasses.dataclass
cdef class MyDataclass:
    # fields can be declared using annotations
    a: cython.int = 0
    b: double = cython.dataclasses.field(default_factory = lambda: 10, repr=False)

    # fields can also be declared using `cdef`:
    cdef str c
    c = "hello"  # assignment of default value on a separate line

    # cython equivalents to InitVar and typing.ClassVar also work
    d: cython.dataclasses.InitVar[double] = 5
    e: cython.typing.ClassVar[list] = []
