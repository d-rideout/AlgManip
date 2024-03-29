import yaml
from os.path import dirname
import random as rm
import AlgManip.graph as gm

debug = False

# Is this general enough for util.py?
class abbrevDict(dict):
  'dict for abbreviations, which can handle unabbreviated keys'
  def __getitem__(s,i):
    if not i in s: return i
    else: return super().__getitem__(i)

# Always read poscau database upon import?
fp = open(dirname(__file__) + '/poscau.yaml', 'r')
poscau = yaml.safe_load_all(fp)

# Read keyword definitions
kw = next(poscau) # print(kw.keys()) just store set of keywords? 5jul023

# Read OEIS counts
no = tuple(next(poscau))

# Read causet abbreviations
causetName = abbrevDict(next(poscau))
# Note that causetName will not choke on invalid abbreviations.

# Read causets
getCauset = {} # store causet info such that it can be retreived from abbrev
# getCauset would have to be used to check for typos, but it is not populated
# with children!
# Note that (the 3rd) 'next(poscau)' is just a python list! 6jul023
poscau = next(poscau)
# print(poscau)
for c in poscau:
  if isinstance(c, int): n = c
  else:
    c += [None]*(5-len(c))
    getCauset[str(c[0])] = (causetName[c[0]], n, c[1], c[2], c[3], c[4])

# Graph settings for small causets
gm.Graph.size = 's'
gm.Graph.nl = True
gm.Graph.verb = False

nc = None # num causets at each stage
n = None
def nextCauset():
  # what to call this??  iterCauset??  but I don't want to imply completeness!
  # poscauTraverse??  pcTrav? 5jul023
  '''yield all causets in poscau, as 4-tuple:
  abbrev str, Graph instance, parents list, children list'''
  # global poscau -- not necessary because it is referenced before defined
  global nc
  global n
  if debug: print('nextCauset():', poscau)
  for c in poscau: # next(poscau):
    if debug: print('c=', c)
    if isinstance(c, int):
      n = c
#       if n: print(nc, f'causets at stage {n-1}\n')
      if n: print(nc, f'of {no[n-1]} {n-1}-orders\n')
      print('n =', n)
      nc = 0
    elif isinstance(c, dict):
      for k in c:
        if not k in kw: print('unrecognized key:', k)
      print('dict-based causets not implemented yet')
    else:
      c += [None]*(5-len(c)) # this is not super-safe: can forget elts in middle
      nc += 1
      yield c[0], gm.Graph(n,c[1], c[2]), c[3], c[4]
  print('...')

def randWalk():
  '''yield random walk through poscau, choosing edges uniformly at random
  (irrespective of edge weights)'''
  c = getCauset['void']
  while c:
    yield c
#     print('  children =', c[5])
    if not c[5]: return
    rc = rm.choices(c[5])
    if isinstance(rc[0], list): rc = rc[0][0]
    else: rc = rc[0]
    c = getCauset[rc]
