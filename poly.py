class poly:
  # store as list of 2-tuples (coef, exp) for starters
  def __init__(s, lt):
#     print('creating poly with', lt, 'of type', type(lt), type(lt[0]))
    print('poly:', lt)
#     if not type(lt[0]) == "<class 'tuple'>": die('please construct with list of tuples')
    if not isinstance(lt[0],tuple): die('please construct with list of tuples')
    s.p = lt

#   def __del__(s): print('destroying poly instance with', len(s.p), 'terms...')
    
  def __str__(s):
    retval = ''
    sp = ''
    for t in s.p:
      c = t[0]
      if c<-1: cs = str(c)
      elif c==-1: cs = '-'
#       elif c==0: die('zero coeff')
      elif c==1: cs = '+'
      else: cs = f'+{c}'
      if not c: continue
#       if t[0]<0: plus=''
#       else: plus='+'
#       retval += sp+plus+f'{t[0]} q^{t[1]}'
      retval += sp+cs+f' q^{t[1]}'
      #       print(f'{t[0]} q^{t[1]}')
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
    for e in sorted(pd): p.append((pd[e],e))
    return poly(p)
  
