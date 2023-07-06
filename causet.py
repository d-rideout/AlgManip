import yaml
from os.path import dirname
import AlgManip.graph as gm

debug = False

# Is this general enough for util.py?
class abbrevDict(dict):
  'dict for abbreviations, which can handle unabbreviated keys'
  def __getitem__(s,i):
    if not i in s: return i
    else: return super().__getitem__(i)

# Always read poscau database upon import?
# with open(dirname(__file__) + '/poscau.yaml', 'r') as fp:
# nicer not to have to enclose everything in the with scope
fp = open(dirname(__file__) + '/poscau.yaml', 'r')
poscau = yaml.safe_load_all(fp)
# poscau = yaml.safe_load(fp)

# Read keyword definitions
kw = next(poscau)
# print(kw.keys()) just store set of keywords? 5jul023
# print(next(poscau))
# for k in next(poscau): kw[k] =

# Read causet abbreviations
causetName = abbrevDict(next(poscau))
getCauset = {}

# Graph settings for small causets
gm.Graph.size = 's'
gm.Graph.nl = True
gm.Graph.verb = False

nc = None
def nextCauset():
  # what to call this??  iterCauset??  but I don't want to imply completeness!
  # poscauTraverse??  pcTrav? 5jul023
  #for doc in poscau: print(type(doc), doc)
  # Do I want to use multiple docs?
  # global poscau -- seems not necessary
  global nc # I think because I define it here before using it
  if debug: print('nextCauset():', poscau)
  for c in next(poscau):
    if debug: print('c=', c)
    if isinstance(c, int):
      n = c
      if n: print(nc, 'causets\n')
      print('n =', n)
      nc = 0
    elif isinstance(c, dict):
      for k in c:
        if not k in kw: print('unrecognized key:', k)
      print('dict-based causets not implemented yet')
    else:
      c += [None]*(4-len(c)) # this is not super-safe: can forget elts in middle
      #       if len(c)==4: yield c[0], gm.Graph(n,c[1], c[2]), c[3]
      #       else: yield c[0], gm.Graph(n,c[1], c[2]), None
      getCauset[c[0]] = (causetName[c[0]], n, c[1], c[2], c[3])
      nc += 1
      yield c[0], gm.Graph(n,c[1], c[2]), c[3]
  print('...')

# Do we want these?
# ch1 = gm.Graph(1)
#
# ch2 = gm.Graph(2,1)
# ch2.sbs = 'tcr'
# ach2 = gm.Graph(2)
# ach2.sbs = 'tcr'
#
# ch3 = gm.Graph(3,5)
# ch3.sbs = 'tr'
# V = gm.Graph(3,5)
# V.sbs = 'tr'

# Proposal:
# * store structure of poscau in igraph?
