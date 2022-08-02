import matplotlib.pyplot as plt
import scipy.special as ss # binomial coefficients
import copy
# import AlgManip.util as u
import util as u

debug = 0 # 2 max verbosity

class poly:
  'polynomial with integer coefficients'
  sym = 'q' # name of variable(s)
  mv = None # multi-variable polynomials
  # (These are properties of a family of polynomials, not a single polynomial.)
  # It is safest for the user to set these attributes manually, but it can
  # probably be deduced from context if not?
  # False ==> never check if multi-variable

  # Polynomial is stored as list of dicts (factors)
  # dict: keys tuple of exponents val coefficient
  # **last exponent in tuple must be non-zero (NO 0, !!)**

  def __init__(s, p={}):
    '''Defaults to zero polynomial
    for the moment we construct only from single factor
    list construction of single factor is deprecated -- please use dict for each factor'''
    # Can also construct from list of lists (coef, exp0, exp1, ...) for the moment
    # p is a single factor here!  Notation is confusing!! (1aug022)

    if debug: print(f'poly constructor: type={type(p)} val=[{p}]')
    if isinstance(p, dict):
#       if p
      s.p = [p]
    elif isinstance(p,(list,tuple)): #DEPRECATED single factor list construction
      s.p = [{}]
      for t in p: s.p[0][tuple(t[1:])] = t[0]
    elif isinstance(p,int): # WARNING: promoting int to poly.  Is this what I want?
      s.p = [{():p}]
    else: u.die('please construct poly with dict or list of lists:' + str(p))

  # def __del__(s): print('destroying poly instance with', len(s.p), 'terms...')
  # deconstructors do not have to be explicitly called in Python!

  def __str__(sf): # convert to pretty string
    # Check multi-variable status
    if poly.mv==None:
      for f in sf.p:
        for e in f:
          if len(e)>1:
            poly.mv = True
            break
#       else: poly.mv = False -- need to recheck every time

    # True : write using multi-variable assumption
    # False : write using single variable assumption
    # None : must assume multi-variable

    # 'Global' Settings
    sp = '' # space between terms
    if u.gnuplot:
      msm = '*'
      esm = '**'
    else:
      msm = ' ' # multiply symbol
      esm = '^' # exponent symbol

    retval = ''
    if debug: print(len(sf.p), 'factors:', sf.p)
    for fd in sf.p:
      fs = ''
      if debug: print('fac dict:', fd)
      for ext,co in sorted(fd.items()):
        if debug>1: print(f'co={co} ext=', ext)

        # compute exponent string
        es = '' # exponent string
        esp = '' # space between factors
  #       if poly.mv:
        for i, ex in enumerate(ext):
          if debug>1: print(f'var {i} ex {ex} esp [{esp}]')
          # get variable name
          if poly.mv==False: sym = poly.sym
          else: sym = f'{poly.sym}{i}'

          if ex==0: continue
          elif ex==1: es += esp+sym
          else: es += esp+f'{sym}{esm}{ex}'
          esp = ' '
  #       else: es = str(ext)

        # compute coefficient string
        if co<-1:
          cs = f'- {-co}'
          if es: cs += msm
        elif co==-1:
          cs = '- '
          if es=='': cs += '1'
        elif co==1:
          cs = '+ '
          if not es: cs += '1'
        else:
          cs = f'+ {co}' #+msm
          if es: cs += msm
        if not co: continue

        if debug>1: print(f'sp=[{sp}] cs=[{cs}] es=[{es}]')
        fs += sp+cs+es
        sp = ' '
      if fs=='': return '0'
      if len(sf.p)>1: retval += f'({fs})'
      else: return fs
    return retval


  def mul(s,o):
    print(type(o), o)
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
#     s.p = s.mul(o)
    if isinstance(o,int): s.__rmul__(o) # write s = o * s instead?
    else: s.p.append(o)
    return s

  def __mul__(s,o):
    print(f'poly mul called on {type(s)}[{s}] * {type(o)}[{o}]')
    return poly(s.mul(o)) # poly * o

  def __rmul__(s, i): # i * poly
    "multiplies first factor by integer"
    print(f'poly rmul called on {type(s)}[{s}] * {type(i)}[{i}]')
    # This operation should not change s!  Only *= should do such a thing.
    pr = copy.deepcopy(s)
    for e in pr.p[0]: pr.p[0][e] *= i
    return pr


  def add(s, o):
    if debug: print(f'poly.add: [{type(s)}={s}] + [{type(o)}={o}]')
    if len(s.p)>1: u.die('need to multiply out factors of poly')
    f = copy.deepcopy(s.p[0]) # WARNING: Probably should only be for iadd

    print(type(s.p[0]), id(s.p[0]), '-->', type(f), id(f))
    if isinstance(o,int):
#       if s.p[0][1] != 0: u.die("first term isn't constant?")
      print('poly.add: fac1 =', s.p[0])
      f[()] += o # Is it possible to have an empty key?  Do we want an empty tuple anyway?
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
      for e,c in o.p[0].items():
#         if t[1] in pd: pd[t[1]] += t[0]
        if e in f: f[e] += c
        else: f[e] = c
        if not f[e]: del f[e]
#       for e in sorted(pd): s.p.append([pd[e],e])
#       for t in s.p:
#         e = t[1]
#         if e in pd: t[0] = pd[e]
    return f

  def __iadd__(s, o): return poly(s.add(o)) # +=
  # This seems wrong.  Look at mul et al.

  def __add__(s,o):
    print(f'poly add called on {type(s)}[{s}] + {type(o)}[{o}]')
    return poly(s.add(o))
#     if len(s.p)>1: die('trying to add to multi-factor poly')


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


def str2poly(st): # build this into poly constructor?
  '''convert string into poly
  returns int if possible'''
  # output of poly (__str__ method) into poly
  #  (assuming non-gnuplot string)'''
  # (using brute-force (non-regex) approach 'for fun'...)
  if debug: print(f'str2poly [{st}]')

  # convert input string st to list of terms
  tl = []
  tm = '' # term
  for c in st:
    if debug: print(c, end='')
    if c=='+' or c=='-':
      if tm: tl.append(tm)
      tm = c
    elif c==' ': continue
    else: tm += c
  tl.append(tm) # grab last term
#   print(tl)

  # parse terms
  pd = {}
  for t in tl:
    if debug: print(f'parsing term [{t}]')
    co = ''
    ex = ''
    mode = 'c'
    for c in t:
      if c=='+' or c=='^': continue
      if c==poly.sym:
        mode = 'e'
        continue
      if mode=='c': co += c
      else: ex += c
    if co=='': co = '1'
    elif co=='-': co = '-1'
    if ex=='':
      if mode=='c': ex = '0'
      else: ex = '1'
    #     pl.append([int(co),int(ex)])
    ex = int(ex)
    if ex: pd[ex,] = int(co)
    else: pd[()] = int(co)

  if len(tl)==1 and ex==0: return int(co)
  return poly(pd)


def str2rat(st): # build this into ratFunc constructor?
  '''convert string into ratFunc
  returns simplest possible object (can be poly or int)'''
  # ignore () for the moment and assume simple format
  p = ''
  n = None
  for c in st:
    if c=='/':
      n = p
      p = ''
    else: p += c
  if n: return ratFunc(str2poly(n),str2poly(p))
  else:
#     if ...
    return str2poly(p) #poly({(0,):1}))
#   else: return ratFunc(str2poly(p),1) #poly({(0,):1}))


class ratFunc(poly):
  'rational function (ratio of polynomials)'

  def __init__(s, pn, pd):
    'numerator and denominator can be polys or argument to poly constructor ints'
    #     print(type(pn), isinstance(pn,poly))
    s.n = pn
    s.d = pd

  def __str__(s):
    return f'({s.n})/({s.d})'
