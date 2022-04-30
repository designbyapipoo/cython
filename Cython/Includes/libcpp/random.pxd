from libc.stdint cimport uint_fast32_t


cdef extern from "<random>" namespace "std" nogil:
    cdef cppclass random_device:
        ctypedef uint_fast32_t result_type
        random_device() except +
        result_type operator()() except +

    cdef cppclass mt19937:
        ctypedef uint_fast32_t result_type
        mt19937() except +
        mt19937(result_type seed) except +
        result_type operator()() except +
        result_type min() except +
        result_type max() except +
        void discard(size_t z) except +
        void seed(result_type seed) except +

    cdef cppclass uniform_int_distribution[T]:
        ctypedef T result_type
        uniform_int_distribution() except +
        uniform_int_distribution(T, T) except +
        result_type operator()[Generator](Generator&) except +
        result_type min() except +
        result_type max() except +

    cdef cppclass uniform_real_distribution[T]:
        ctypedef T result_type
        uniform_real_distribution() except +
        uniform_real_distribution(T, T) except +
        result_type operator()[Generator](Generator&) except +
        result_type min() except +
        result_type max() except +

    cdef cppclass bernoulli_distribution:
        ctypedef bint result_type
        bernoulli_distribution() except +
        bernoulli_distribution(double) except +
        result_type operator()[Generator](Generator&) except +
        result_type min() except +
        result_type max() except +

    cdef cppclass binomial_distribution[T]:
        ctypedef T result_type
        binomial_distribution() except +
        binomial_distribution(T, double) except +
        result_type operator()[Generator](Generator&) except +
        result_type min() except +
        result_type max() except +

    cdef cppclass geometric_distribution[T]:
        ctypedef T result_type
        geometric_distribution() except +
        geometric_distribution(double) except +
        result_type operator()[Generator](Generator&) except +
        result_type min() except +
        result_type max() except +


    cdef cppclass negative_binomial_distribution[T]:
        ctypedef T result_type
        negative_binomial_distribution() except +
        negative_binomial_distribution(T, double) except +
        result_type operator()[Generator](Generator&) except +
        result_type min() except +
        result_type max() except +

    cdef cppclass poisson_distribution[T]:
        ctypedef T result_type
        poisson_distribution() except +
        poisson_distribution(double) except +
        result_type operator()[Generator](Generator&) except +
        result_type min() except +
        result_type max() except +
