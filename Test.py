#!/usr/bin/env python3
'Test code'

# This program has not been well maintained.  Do not bother trying to get
# tests to pass.  Either build new, passing tests, or use unittest (11jan023)

from sys import argv

if len(argv)<2:
  print("specify tests to run {poly, graph, all}")
  exit

def check(expr, expect):
  global npassed
  got = str(expr)
  if got == expect:
    print(f'pass: [{got}]')
    npassed += 1
  else: print(f'fail: got [{got}] expect [{expect}]')


if 'poly' in argv or 'all' in argv:
  import poly as pm

  npassed = 0

  pm.poly.sym = 'x'
  pm.poly.mv = False

  p = pm.poly()
  check(p, '0')

  p += pm.omqn(4)
  check(p, '+ 1 - 4 x + 6 x^2 - 4 x^3 + x^4')

  q = pm.poly([(1,0), (-1,1), (2,2)])
  check(q, '+ 1 - x + 2 x^2')

  p *= q
  check(p, '+ 1 - 5 x + 12 x^2 - 18 x^3 + 17 x^4 - 9 x^5 + 2 x^6')

  print(npassed, 'of 4 tests pass\n')


if 'graph' in argv or 'all' in argv:
  import graph as gm
  gm.rm.seed(0)
  npassed = 0

  expect = ('[64]', '[25, 39]', '[18, 36, 10]', '[10, 21, 24, 9]', '[5, 12, 30, 13, 4]', '[1, 14, 20, 14, 13, 2]', '', '', '', '') # for default 'const'

  Ns = 64
#   g = gm.tn('harm') expect numbers above come from default 'const'!
  g = gm.tn()
  # print([g.sample(n) for n in range(15)])
  for n in range(10):
    f = [0]*(n+1)
    print('n =', n)
    for s in range(Ns): f[g.sample(n)] += 1
    #       print(g.sample(n), end=' ')
    check(f, expect[n])
#     print(f)

  print(npassed, 'of 6 tests pass')
