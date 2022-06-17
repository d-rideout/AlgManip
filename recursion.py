from os.path import exists
import AlgManip.util as u

debug = False

class var:
  def __init__(sf, name, mins):
    'mins is tuple of min value for each slot'
    if type(mins)==int: u.die('Please pass tuple for second argument')
    sf.name = name
    sf.mins = mins
  def __str__(sf): return sf.name
  def __repr__(sf): return f'<var: {sf.name} mins: {sf.mins}>'

  
class relation:
  def __init__(sf, lhs, rhs, cf=lambda ix: True):
    '''lhs: var
    ns = num slots
    rhs: tuple of (1+ns)-tuples (var, (slot, offset), (slot, offset), ...)
    first slot is 0
    cf = constraintFunction to check if indices valid'''
    sf.lhs = lhs
    sf.rhs = rhs
    sf.cf = cf
    if debug: print('lhs:', lhs)
    if debug: print('rhs:')
    sf.lhsMins = [0]*len(lhs.mins)
    for t in rhs:
      if debug: print(' t = ', t)
      for v in t[1:]:
        if debug: print('  v = ', v)
        if sf.lhsMins[v[0]]+v[1] < 0: sf.lhsMins[v[0]] = -v[1]
    # Be sure mins are at least as large as required for the variables
    for s in range(len(lhs.mins)):
      if sf.lhsMins[s] < lhs.mins[s]: sf.lhsMins[s] = lhs.mins[s]

  def validLHS(sf, ix): return sf.cf(ix) # invalidLHS?


def recursionCauset(fn, rl, max):
  'writes graphviz file of recursion causet'
  if exists(fn): print(fn, 'exists, overwriting')
  rt = fn[:-4]
  fp = open(fn, 'w')
  fp.write(f'# dot -Tpdf -o {rt}.pdf {fn}\ndigraph "{rt}" ')
  fp.write('{\nrankdir=BT; concentrate=true; node[shape=plaintext];\n')
  for r in rl:
    if debug: print(r.lhs, r.lhsMins)
    ix = r.lhsMins[:]
    while True:
      if not r.validLHS(ix):
        if u.incList(ix, r.lhsMins, max): break # having second thoughts about loop...
        continue
      if debug: print('index=', ix)
      if debug: fp.write('lhs='+str(r.lhs)+str(ix))
      lhs = str(r.lhs)+str(ix[0])
      for i in ix[1:]:
        lhs += '_'+str(i)
      for t in r.rhs:
#         fp.write('\n# '+str(t)+'\n')
        fp.write(f' {t[0].name}')
        for j in range(1,len(t)):
          if j>1: fp.write('_')
          fp.write(str(ix[t[j][0]]+t[j][1]))
        fp.write(f'->{lhs};')
      fp.write(f'\n')
      if u.incList(ix, r.lhsMins, max): break
  fp.write('}\n')
  fp.close()
