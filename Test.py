#!/usr/bin/env ipython
#!/usr/bin/env python3 -- ipython is slower but so much nicer for debugging! (14jan023)
'Test code'

# Status:
# * poly tests seem to be broken -- please fix (14jan023)
# * graph tests pass out to n=5 for the default const (tn) (14jan023)

# Fix these tests, but
# consider migrating to unittest before devoting a huge amount of effort coding
# new tests here. (14jan023)

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

  po = pm.poly()
  check(po, '0')

  po += pm.omqn(4)
  check(po, '+ 1 - 4 x + 6 x^2 - 4 x^3 + x^4')

  qo = pm.poly([(1,0), (-1,1), (2,2)])
  check(qo, '+ 1 - x + 2 x^2')

  po *= qo
  check(po, '+ 1 - 5 x + 12 x^2 - 18 x^3 + 17 x^4 - 9 x^5 + 2 x^6')

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
