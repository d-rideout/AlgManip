import matplotlib.pyplot as plt
import scipy.special as ss # binomial coefficients
# import AlgManip.util as u
# from . import util
# from .util import *
import util as u

# debug = True
debug = False

class poly:
  'polynomial with integer coefficients'
  sym = 'q' # name of variable(s)
  mv = None # multi-variable polynomials
  # (This is a property of a family of polynomials, not a single polynomial.)
  # It is safest for the user to set this attribute value manually, but it can
  # probably be deduced from context if not?
  # False ==> never check if multi-variable

  # store as dict: keys tuple of exponents val coefficient
  # **last exponent must be non-zero**

  def __init__(s, p={}):
    'Defaults to zero polynomial'
    # Can also construct from list of lists (coef, exp0, exp1, ...) (deprecate?)

    if isinstance(p, dict): s.p = p
    elif isinstance(p,(list,tuple)): # deprecate this?
      s.p = {}
      for t in p: s.p[tuple(t[1:])] = t[0]
    else: u.die('please construct poly with dict or list of lists:' + str(p))

  # def __del__(s): print('destroying poly instance with', len(s.p), 'terms...')
  # deconstructors do not have to be explicitly called in Python!

  def __str__(s): # convert to pretty string
    # Check multi-variable status
    if poly.mv==None:
      for e in s.p:
        if len(e)>1:
          poly.mv = True
          break
#       else: poly.mv = False -- need to recheck every time

    # True : write using multi-variable assumption
    # False : write using single variable assumption
    # None : must assume multi-variable

    retval = ''
    sp = '' # space between terms
    if u.gnuplot:
      msm = '*'
      esm = '**'
    else:
      msm = ' ' # multiply symbol
      esm = '^' # exponent symbol
    for ext,co in sorted(s.p.items()):
      if debug: print(f'co={co} ext=', ext)

      # compute exponent string
      es = '' # exponent string
      esp = '' # space between factors
      for i, ex in enumerate(ext):
        if debug: print(f'var {i} ex {ex} esp [{esp}]')
        # get variable name
        if poly.mv==False: s = poly.sym
        else: s = f'{poly.sym}{i}'

        if ex==0: continue
        elif ex==1: es += esp+s
        else: es += esp+f'{s}{esm}{ex}'
        esp = ' '

      # compute coefficient string
      if co<-1:
        cs = f'- {-co}'
        if es: cs += msm
      elif co==-1: cs = '- '
      elif co==1:
        cs = '+ '
        if not es: cs += '1'
      else:
        cs = f'+ {co}' #+msm
        if es: cs += msm
      if not co: continue

      if debug: print(f'sp=[{sp}] cs=[{cs}] es=[{es}]')
      retval += sp+cs+es
      sp = ' '
    if retval=='': retval = '0'
    return retval


  def mul(s,o):
    # Don't want to mess with changing dict in place
    p = {}
    for elt,cl in s.p.items():
      for ert,cr in o.p.items():
#         print(f'multiplying {tl} with {tr}')
        ept = []
        for el,er in zip(elt, ert):
          ept.append(el+er)
        ept = tuple(ept)
        if ept in p: p[ept] += cl*cr
        else: p[ept] = cl*cr
    return p
#     return poly(p) can i just pass the dict?

  
  def __imul__(s,o): # *=
    s.p = s.mul(o)
    return s

  def __mul__(s,o): return poly(s.mul(o)) # poly * o

  def __rmul__(s, i): # i * poly
#     print(f'multiplying {i} times {s}')
    for e in s.p: s.p[e] *= i
    return s


  def __iadd__(s, o): # +=
#     print(f'adding {o} to {s}')
    if isinstance(o,int):
#       if s.p[0][1] != 0: u.die("first term isn't constant?")
      s.p[()] += o # Is it possible to have an empty key?  Do we want an empty tuple anyway?
    else:
      if not isinstance(o,poly):
        print(type(o))
        u.die(o+'adding non-(int,poly) to poly')
      # print('adding two polynomials')
#       pd = {} # key exponent val coeff
#       for t in s.p:
#         if t[1] in pd:
#           pd[t[1]] += t[0]
#           die('duplicate term found!')
#         else: pd[t[1]] = t[0]
      for e,c in o.p.items():
#         if t[1] in pd: pd[t[1]] += t[0]
        if e in s.p: s.p[e] += c
        else: s.p[e] = c
        if not s.p[e]: del s.p[e]
#       for e in sorted(pd): s.p.append([pd[e],e])
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


def omqn(n):
  f'returns (1-{poly.sym})^n'
  # (Think about how to generalize this later)
  # --> Overload ** to do multinomial expansion
  rv = []
  s = 1
  for i in range(n+1):
    rv.append([s*ss.comb(n,i, exact=True),i])
    s *= -1
  return poly(rv)


def str2poly(st):
  '''convert string output of poly (__str__ method) into poly
  (assuming non-gnuplot string)'''
  # (using brute-force (non-regex) approach 'for fun'...)

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
      if c==poly.sym: # 'q':
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
