# "description" refers to the original functions
description = """
f2 is a symmetric parabola, x**2 - 1
f3 is a quartic polynomial with large hump in interval
f4 is step function with a discontinuity at 1
f5 is a hyperbola with vertical asymptote at 1
f6 has random values positive to left of 1, negative to right

Of course, these are not real problems. They just test how the
'good' solvers behave in bad circumstances where bisection is
really the best. A good solver should not be much worse than
bisection in such circumstance, while being faster for smooth
monotone sorts of functions.
"""


def f1(x):
    r"""f1 is a quadratic with roots at 0 and 1"""
    return x * (x - 1.)


def f1_fp(x):
    return 2 * x - 1


def f1_fpp(x):
    return 2


def f2(x):
    r"""f2 is a symmetric parabola, x**2 - 1"""
    return x**2 - 1


def f2_fp(x):
    return 2 * x


def f2_fpp(x):
    return 2


def f3(x):
    r"""A quartic with roots at 0, 1, 2 and 3"""
    return x * (x - 1.) * (x - 2.) * (x - 3.)  # x**4 - 6x**3 + 11x**2 - 6x


def f3_fp(x):
    return 4 * x**3 - 18 * x**2 + 22 * x - 6


def f3_fpp(x):