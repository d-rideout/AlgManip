partitionNumbers = (1,1,2,3,5,7,11,15,22,30,42,56,77,101,135,176,231,297,385,490,627,792,1002,1255,1575,1958,2436,3010,3718,4565,5604,6842,8349,10143,12310,14883,17977,21637,26015,31185,37338,44583,53174,63261,75175,89134,105558,124754,147273,173525)

def qpoch(q, n=None):
  '''(q,q)_n = [n]_q! (1-q)^n = (1-q)(1-q^2)...(1-q^n)
  no n ==> (q,q)_infinity aka Euler function'''
  if n==None:
    m = 1
    eps = 1e-11
    prevVal = 1
    val = 1-q
    while abs(prevVal-val) > eps:
      m += 1
      prevVal = val
      val *= 1-q**m
#     print('converged at n=', m, 'at q=', q, 'to within eps=', eps)
    return val
  if n==0: return 1 # [0]_q! (1-q)^0 = 1
#   if n==1: return 1-q # Is this a good idea?
  return (1-q**n)*qpoch(q,n-1) # Is recursive definition less efficient? (15jun022)

  
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
