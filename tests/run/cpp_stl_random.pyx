# mode: run
# tag: cpp, cpp11

from libcpp.random cimport mt19937, random_device, uniform_int_distribution, \
    uniform_real_distribution, bernoulli_distribution, binomial_distribution, \
    geometric_distribution, negative_binomial_distribution, poisson_distribution, \
    exponential_distribution, gamma_distribution, weibull_distribution, \
    extreme_value_distribution, normal_distribution, lognormal_distribution, \
    chi_squared_distribution, cauchy_distribution, fisher_f_distribution, student_t_distribution
from libc.float cimport DBL_MAX as DBL_MAX_


DBL_MAX = DBL_MAX_


def mt19937_seed_test():
    """
    >>> print(mt19937_seed_test())
    1608637542
    """
    cdef mt19937 rd = mt19937(42)
    return rd()


def mt19937_reseed_test():
    """
    >>> print(mt19937_reseed_test())
    1608637542
    """
    cdef mt19937 rd
    rd.seed(42)
    return rd()


def mt19937_min_max():
    """
    >>> x, y = mt19937_min_max()
    >>> print(x)
    0
    >>> print(y)  # 2 ** 32 - 1 because mt19937 is 32 bit.
    4294967295
    """
    cdef mt19937 rd
    return rd.min(), rd.max()


def mt19937_discard(z):
    """
    >>> x, y = mt19937_discard(13)
    >>> print(x)
    1972458954
    >>> print(y)
    1972458954
    """
    cdef mt19937 rd = mt19937(42)
    # Throw away z random numbers.
    rd.discard(z)
    a = rd()

    # Iterate over z random numbers.
    rd.seed(42)
    for _ in range(z + 1):
        b = rd()
    return a, b


ctypedef fused any_dist:
    uniform_int_distribution[int]
    uniform_real_distribution[double]
    bernoulli_distribution
    binomial_distribution[int]
    geometric_distribution[int]
    negative_binomial_distribution[int]
    poisson_distribution[int]
    exponential_distribution[double]
    gamma_distribution[double]
    weibull_distribution[double]
    extreme_value_distribution[double]
    normal_distribution[double]
    lognormal_distribution[double]
    chi_squared_distribution[double]
    cauchy_distribution[double]
    fisher_f_distribution[double]
    student_t_distribution[double]


cdef sample_or_range(any_dist dist, bint sample):
    """
    This helper function returns a sample if `sample` is truthy and the range of the distribution
    if `sample` is falsy. We use a fused type to avoid duplicating the conditional statement in each
    distribution test.
    """
    cdef random_device rd
    if sample:
        return dist(mt19937(rd()))
    else:
        return dist.min(), dist.max()


def uniform_int_distribution_test(a, b, sample=True):
    """
    >>> uniform_int_distribution_test(0, 0)
    0
    >>> uniform_int_distribution_test(0, 1) < 2
    True
    >>> uniform_int_distribution_test(5, 9, False)
    (5, 9)
    """
    cdef uniform_int_distribution[int] dist = uniform_int_distribution[int](a, b)
    return sample_or_range[uniform_int_distribution[int]](dist, sample)


def uniform_real_distribution_test(a, b, sample=True):
    """
    >>> uniform_real_distribution_test(0, 0)
    0.0
    >>> x = uniform_real_distribution_test(0, 5)
    >>> 0 < x and x < 5
    True
    >>> uniform_real_distribution_test(3, 8, False)
    (3.0, 8.0)
    """
    cdef uniform_real_distribution[double] dist = uniform_real_distribution[double](a, b)
    return sample_or_range[uniform_real_distribution[double]](dist, sample)


def bernoulli_distribution_test(proba, sample=True):
    """
    >>> bernoulli_distribution_test(0)
    False
    >>> bernoulli_distribution_test(1)
    True
    >>> bernoulli_distribution_test(0.7, False)
    (False, True)
    """
    cdef bernoulli_distribution dist = bernoulli_distribution(proba)
    return sample_or_range[bernoulli_distribution](dist, sample)


def binomial_distribution_test(n, proba, sample=True):
    """
    >>> binomial_distribution_test(10, 0)
    0
    >>> binomial_distribution_test(10, 1)
    10
    >>> x = binomial_distribution_test(100, 0.5)
    >>> 30 < x and x < 70 or x  # Passes with high probability (>99.9%).
    True
    >>> binomial_distribution_test(75, 0.3, False)
    (0, 75)
    """
    cdef binomial_distribution[int] dist = binomial_distribution[int](n, proba)
    return sample_or_range[binomial_distribution[int]](dist, sample)


def geometric_distribution_test(proba, sample=True):
    """
    >>> geometric_distribution_test(1)
    0
    >>> x = geometric_distribution_test(1e-5)
    >>> x > 100 or x  # Passes with high probability (99.9%).
    True
    >>> geometric_distribution_test(0.2, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef geometric_distribution[int] dist = geometric_distribution[int](proba)
    return sample_or_range[geometric_distribution[int]](dist, sample)


def negative_binomial_distribution_test(n, p, sample=True):
    """
    >>> negative_binomial_distribution_test(5, 1)
    0
    >>> x = negative_binomial_distribution_test(1, 1e-4)
    >>> x > 10 or x  # Passes with high probability (99.9%).
    True
    >>> negative_binomial_distribution_test(10, 0.2, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef negative_binomial_distribution[int] dist = negative_binomial_distribution[int](n, p)
    return sample_or_range[negative_binomial_distribution[int]](dist, sample)


def poisson_distribution_test(rate, sample=True):
    """
    >>> poisson_distribution_test(0)
    0
    >>> x = poisson_distribution_test(1000)
    >>> 900 < x and x < 1100 or x  # Passes with high probability (99.8%).
    True
    >>> poisson_distribution_test(7, False)  # 2147483647 = 2 ** 32 - 1
    (0, 2147483647)
    """
    cdef poisson_distribution[int] dist = poisson_distribution[int](rate)
    return sample_or_range[poisson_distribution[int]](dist, sample)


def exponential_distribution_test(rate, sample=True):
    """
    >>> exponential_distribution_test(0)
    inf
    >>> exponential_distribution_test(float("inf"))
    0.0
    >>> x = exponential_distribution_test(100)
    >>> x < 0.1 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = exponential_distribution_test(1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef exponential_distribution[double] dist = exponential_distribution[double](rate)
    return sample_or_range[exponential_distribution[double]](dist, sample)


def gamma_distribution_test(shape, scale, sample=True):
    """
    >>> gamma_distribution_test(3, float("inf"))
    inf
    >>> gamma_distribution_test(3, 0)
    0.0
    >>> x = gamma_distribution_test(1000, 1)
    >>> 900 < x and x < 1100 or x  # Passes with high probability (99.8%).
    True
    >>> l, u = gamma_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef gamma_distribution[double] dist = gamma_distribution[double](shape, scale)
    return sample_or_range[gamma_distribution[double]](dist, sample)


def weibull_distribution_test(shape, scale, sample=True):
    """
    >>> weibull_distribution_test(3, float("inf"))
    inf
    >>> weibull_distribution_test(3, 0)
    0.0
    >>> x = weibull_distribution_test(100, 1)
    >>> 0.9 < x and x < 1.1 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = weibull_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef weibull_distribution[double] dist = weibull_distribution[double](shape, scale)
    return sample_or_range[weibull_distribution[double]](dist, sample)


def extreme_value_distribution_test(shape, scale, sample=True):
    """
    >>> extreme_value_distribution_test(3, 0)
    3.0
    >>> x = extreme_value_distribution_test(3, .1)
    >>> 2 < x and x < 4 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = extreme_value_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef extreme_value_distribution[double] dist = extreme_value_distribution[double](shape, scale)
    return sample_or_range[extreme_value_distribution[double]](dist, sample)


def normal_distribution_test(loc, scale, sample=True):
    """
    >>> normal_distribution_test(3, 0)
    3.0
    >>> x = normal_distribution_test(3, .3)
    >>> 2 < x and x < 4 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = normal_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef normal_distribution[double] dist = normal_distribution[double](loc, scale)
    return sample_or_range[normal_distribution[double]](dist, sample)


def lognormal_distribution_test(loc, scale, sample=True):
    """
    >>> from math import log
    >>> log(lognormal_distribution_test(3, 0))
    3.0
    >>> x = log(lognormal_distribution_test(3, .3))
    >>> 2 < x and x < 4 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = lognormal_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef lognormal_distribution[double] dist = lognormal_distribution[double](loc, scale)
    return sample_or_range[lognormal_distribution[double]](dist, sample)


def chi_squared_distribution_test(dof, sample=True):
    """
    >>> x = chi_squared_distribution_test(1000)
    >>> 850 < x and x < 1250 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = chi_squared_distribution_test(5, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef chi_squared_distribution[double] dist = chi_squared_distribution[double](dof)
    return sample_or_range[chi_squared_distribution[double]](dist, sample)


def cauchy_distribution_test(loc, scale, sample=True):
    """
    >>> cauchy_distribution_test(3, 0)
    3.0
    >>> x = cauchy_distribution_test(3, 1e-3)
    >>> 2 < x and x < 4 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = cauchy_distribution_test(1, 1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef cauchy_distribution[double] dist = cauchy_distribution[double](loc, scale)
    return sample_or_range[cauchy_distribution[double]](dist, sample)


def fisher_f_distribution_test(m, n, sample=True):
    """
    >>> x = fisher_f_distribution_test(5000, 5000)
    >>> 0.9 < x and x < 1.1 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = fisher_f_distribution_test(1, 1, False)
    >>> l
    0.0
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef fisher_f_distribution[double] dist = fisher_f_distribution[double](m, n)
    return sample_or_range[fisher_f_distribution[double]](dist, sample)


def student_t_distribution_test(dof, sample=True):
    """
    >>> x = student_t_distribution_test(1000)
    >>> -4 < x and x < 4 or x  # Passes with high probability (>99.9%).
    True
    >>> l, u = student_t_distribution_test(1, False)
    >>> l == -DBL_MAX or l == -float("inf")
    True
    >>> u == DBL_MAX or u == float("inf")
    True
    """
    cdef student_t_distribution[double] dist = student_t_distribution[double](dof)
    return sample_or_range[student_t_distribution[double]](dist, sample)
