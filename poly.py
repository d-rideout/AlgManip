import matplotlib.pyplot as plt
# import math as m
import scipy.special as ss
import AlgManip.util as u

class poly:
  # store as list of 2-lists (coef, exp) for starters
  # keep them sorted by exponent
  # I wonder if a dict might be more sensible
  def __init__(s, lt=([0,0],)):
    'Defaults to zero polynomial'
    # I think it is handy to store the constant term regardless (14jun022)
    # print('creating poly with', lt, 'of type', type(lt), type(lt[0]))
    # print('poly:', lt)
    if not isinstance(lt[0],(list,tuple)):
      u.die('please construct poly with list of lists:' + str(lt))
    s.p = lt

  # def __del__(s): print('destroying poly instance with', len(s.p), 'terms...')
  # deconstructors do not have to be explicitly called in Python!

  def __str__(s): # convert to pretty string
    retval = ''
    sp = ''
    if u.gnuplot:
      msm = '*'
      esm = '**'
    else:
      msm = ' ' # multiply symbol
      esm = '^' # exponent symbol
    for t in s.p:
      co = t[0]
      if co<-1: cs = f'- {-co}'+msm
      elif co==-1: cs = '- '
      elif co==1: cs = '+ '
      else: cs = f'+ {co}'+msm
      if not co: continue
      es = ''
      ex = t[1]
      if ex==0:
        if co==1: es = '1'
        else:
          es = ''
          cs = cs[:-1] # trim multiplication symbol on constant term
      elif ex==1: es = 'q'
      else: es = f'q{esm}{ex}'
      retval += sp+cs+es
      sp = ' '
    return retval

  def __imul__(s,o): # *=
    pd = {} # key exponent val coeff
    for tl in s.p:
      for tr in o.p:
#         print(f'multiplying {tl} with {tr}')
        e = tl[1]+tr[1]
#         print(e)
        if e in pd: pd[e] += tl[0]*tr[0]
        else: pd[e] = tl[0]*tr[0]
#     print(sorted(pd))
    p = []
    for e in sorted(pd): p.append([pd[e],e])
    return poly(p)
  
  def __rmul__(s, i): # i * poly
#     print(f'multiplying {i} times {s}')
    for t in s.p: t[0] *= i
    return s

  def __iadd__(s, o): # +=
#     print(f'adding {o} to {s}')
    if isinstance(o,int):
      if s.p[0][1] != 0: u.die("first term isn't constant?")
      s.p[0][0] += o
    else:
      if not isinstance(o,poly): die('adding non-(int,poly) to poly')
#       print('adding two polynomials')
      pd = {} # key exponent val coeff
      for t in s.p:
        if t[1] in pd:
          pd[t[1]] += t[0]
          die('duplicate term found!')
        else: pd[t[1]] = t[0]
      for t in o.p:
        if t[1] in pd: pd[t[1]] += t[0]
        else: pd[t[1]] = t[0]
      s.p = [] # too violent??
      for e in sorted(pd): s.p.append([pd[e],e])
#       for t in s.p:
#         e = t[1]
#         if e in pd: t[0] = pd[e]
    return s

  def plot(s, xs, f=None, m=None):
    '''xs = list of x values
    multiply polynomial by f if given'''
#     if not 'markers' in dir(s): s.markers = it.cycle(u.mplsym)
    ys = []
    for x in xs:
      y = 0.
      for n in s.p: y += n[0]*x**n[1]
      if f: y *= f(x)
      ys.append(y)
    if not 'mi' in dir(s): s.mi = 0
    #     print('plotting with marker:', u.mplsym[s.mi])
    if m==None: m = u.mplsym[s.mi]
    plt.plot(xs, ys, marker=m)
    s.mi += 1
#     plt.plot(xs, [f(x) for x in xs], marker='x')


def omqn(n): # (Think about how to generalize this later)
  'returns (1-q)^n'
  rv = []
  s = 1
  for i in range(n+1):
    rv.append([s*ss.comb(n,i, exact=True),i])
    s *= -1
  return poly(rv)


def str2poly(st):
  '''convert string output of poly (__str__ method) into poly
  (assuming non-gnuplot string)'''
  # (using brute-force approach 'for fun'...)

  # convert input string st to list of terms
  tl = []
  t = None
  for c in st:
    if c=='+' or c=='-':
#       print(c, end='')
      if t: tl.append(t)
      t = c
    elif c==' ': continue
    else: t += c
#   print(tl)

  # parse terms
  pl = []
  for t in tl:
    co = ''
    ex = ''
    mode = 'c'
    for c in t:
      if c=='+' or c=='^': continue
      if c=='q':
        mode = 'e'
        continue
      if mode=='c': co += c
      else: ex += c
    if co=='': co = '1'
    elif co=='-': co = '-1'
    if ex=='':
      if mode=='c': ex = '0'
      else: ex = '1'
    pl.append([int(co),int(ex)])

  return poly(pl)
