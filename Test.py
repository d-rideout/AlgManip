#!/usr/bin/env python3
'Test code'

from sys import argv

if len(argv)<2:
  print("specify tests to run {poly, graph, all}")
  exit

if 'poly' in argv or 'all' in argv:
  import poly as pm

  np = 0

  def checkPoly(expr, expect):
    global np
    got = str(expr)
    if got == expect:
      print(f'pass: [{got}]')
      np += 1
    else: print(f'fail: got [{got}] expect [{expect}]')

  pm.poly.sym = 'x'
  pm.poly.mv = False

  p = pm.poly()
  checkPoly(p, '0')

  p += pm.omqn(4)
  checkPoly(p, '+ 1 - 4 x + 6 x^2 - 4 x^3 + x^4')

  q = pm.poly([(1,0), (-1,1), (2,2)])
  checkPoly(q, '+ 1 - x + 2 x^2')

  p *= q
  checkPoly(p, '+ 1 - 5 x + 12 x^2 - 18 x^3 + 17 x^4 - 9 x^5 + 2 x^6')

  print(np, 'of 4 tests pass')


if 'graph' in argv or 'all' in argv:
  import graph as gm
  gm.rm.seed(0)
  np = 0
  Ns = 64

  g = gm.tn()
  # print([g.sample(n) for n in range(15)])
  for n in range(6):
    f = [0]*(n+1)
    print('n =', n)
    for s in range(Ns): f[g.sample(n)] += 1
#       print(g.sample(n), end=' ')
    print(f)
