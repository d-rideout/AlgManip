import AlgManip.util as u

class poly:
  # store as list of 2-lists (coef, exp) for starters
  # keep them sorted by exponent
  # I wonder if a dict might be more sensible
  def __init__(s, lt=([0,0],)):
#     print('creating poly with', lt, 'of type', type(lt), type(lt[0]))
#     print('poly:', lt)
#     if not type(lt[0]) == "<class 'tuple'>": die('please construct with list of tuples')
    if not isinstance(lt[0],(list,tuple)):
      u.die('please construct poly with list of lists:' + str(lt))
    s.p = lt

#   def __del__(s): print('destroying poly instance with', len(s.p), 'terms...')
    
  def __str__(s):
    retval = ''
    sp = ''
    for t in s.p:
      c = t[0]
      if c<-1: cs = f'- {-c} '
      elif c==-1: cs = '- '
      elif c==1: cs = '+ '
      else: cs = f'+ {c} '
      if not c: continue
      es = ''
      e = t[1]
      if e==0: es = '1'
      elif e==1: es = 'q'
      else: es = f'q^{e}'
      retval += sp+cs+es
      sp = ' '
    return retval

  def __imul__(s,o):
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
  
  def __rmul__(s, i):
    print(f'multiplying {i} times {s}')
    for t in s.p: t[0] *= i
    return s

  def __iadd__(s, o):
    print(f'adding {o} to {s}')
    if isinstance(o,int):
      if s.p[0][1] != 0: u.die("first term isn't constant?")
      s.p[0][0] += o
    else:
      if not isinstance(o,poly): die('adding non-(int,poly) to poly')
      print('adding two polynomials')
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
