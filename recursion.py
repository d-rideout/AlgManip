from os.path import exists
import AlgManip.util as u

class var:
  def __init__(sf, name, mins):
    'mins is tuple of min value for each slot'
    if type(mins)==int: u.die('Please pass tuple for second argument')
    sf.name = name
    sf.mins = mins
  def __str__(sf): return sf.name
  def __repr__(sf): return f'<var: {sf.name} mins: {sf.mins}>'

  
class relation:
  def __init__(sf, lhs, rhs):
    '''lhs: var
    ns = num slots
    rhs: tuple of (1+ns)-tuples (var, (slot, offset), (slot, offset), ...)
    first slot is 0'''
    print('lhs:', lhs)
    sf.lhs = lhs
    print('rhs:')
    sf.lhsMins = [0]*len(lhs.mins)
    for t in rhs:
      print(' t = ', t)
      for v in t[1:]:
        print('  v = ', v)
        if sf.lhsMins[v[0]]+v[1] < 0: sf.lhsMins[v[0]] = -v[1]
    # Be sure mins are at least as large as required for the variables
    for s in range(len(lhs.mins)):
      if sf.lhsMins[s] < lhs.mins[s]: sf.lhsMins[s] = lhs.mins[s]


def recursionCauset(fn, rl):
  if exists(fn): print(fn, 'exists, overwriting')
  rt = fn[:-4]
  fp = open(fn, 'w')
  fp.write(f'# dot -Tpdf -o {rt}.pdf {fn}\ndigraph "{rt}" ')
  fp.write('{\nrankdir=BT; concentrate=true; node[shape=plaintext];\n')
  for r in rl: print(r.lhs, r.lhsMins)

  fp.write('}\n')
  fp.close()
