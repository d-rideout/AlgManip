#!/usr/bin/env python3

'Test code'

import poly as pm

np = 0

def check(expr, expect):
  global np
  got = str(expr)
  if got == expect:
    print(f'pass: [{got}]')
    np += 1
  else: print(f'fail: got [{got}] expect [{expect}]')

pm.poly.sym = 'x'
p = pm.poly()
check(p, '0')

p += pm.omqn(4)
check(p, '+ 1 - 4 x + 6 x^2 - 4 x^3 + x^4')

q = pm.poly([(1,0), (-1,1), (2,2)])
check(q, '+ 1 - x + 2 x^2')

p *= q
check(p, '+ 1 - 5 x + 12 x^2 - 18 x^3 + 17 x^4 - 9 x^5 + 2 x^6')

print(np, 'of 4 tests pass')
