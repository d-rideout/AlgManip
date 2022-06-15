def qpoch(q, n=None):
  '''(q,q)_n = [n]_q! (1-q)^n = (1-q)(1-q^2)...(1-q^n)
  no n ==> (q,q)_infinity aka Euler function'''
  if n==None:
    m = 0
    eps = 1e-9
    prevVal = qpoch(q,m)
    val = qpoch(q,m+1) # Though this recursive definition is surely inefficient!
    while abs(prevVal-val) > eps:
      m += 1
      prevVal = val
      val = qpoch(q,m+1)
    print('converged at n=', m, 'to within eps=', eps)
    return val
  if n==0: return 1 # [0]_q! (1-q)^0 = 1
#   if n==1: return 1-q # Is this a good idea?
  return (1-q**n)*qpoch(q,n-1)

  
# Below taken from github.com/ectomancer/pure_python/blob/main/q-analog.ipynb on 14jun022
# ---------------------------------------------------------------------------------------

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
        sum = 1 # EMPTY_SUM
        for n in range(1,23): sum += MINUS_ONE**n*q**(n*(n - 1)/2)/q_poch(q, q, n)*a**n
        # was to 30
        # Above is hitting a numeric overflow or some sort of instability near q=1
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
