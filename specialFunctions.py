# Taken from github.com/ectomancer/pure_python/blob/main/q-analog.ipynb on 14jun022

from typing import List, TypeVar

Numeric = TypeVar('Numeric', int, float, complex)

EMPTY_PRODUCT = 1
EMPTY_SUM = 0
MINUS_ONE = -1

def q_poch(a: Numeric, q: Numeric, n: int=None) -> Numeric:
    """Pure Python q-Pochhammer symbol (a;q)_n is the q-analog of Pochhammer symbol.
    Also called q-shifted factorial.
    (a;q)_n = q_poch(a, q, n)
    (a;q)_infinity = q_poch(a, q) (aka Euler function when a=q)
    """
    #Special case of q-binomial thereom.
    if n is None:
        sum = EMPTY_SUM
        for n in range(30):
            sum += MINUS_ONE**n*q**(n*(n - 1)/2)/q_poch(q, q, n)*a**n
        return sum
    if not n:
        return 1
    signum_n = 1
    if n < 0:
        n = abs(n)
        signum_n = -1
    product = EMPTY_PRODUCT
    if signum_n == 1:
        for k in range(n):
            product *= 1 - a*q**k
    else:
        for k in range(1, n + 1):
            product *= 1/(1 - a/q**k)
    return product
