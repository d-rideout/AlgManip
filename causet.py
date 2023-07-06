import yaml
from os.path import dirname
import AlgManip.graph as gm

debug = False

# Always read poscau database upon import?
# with open(dirname(__file__) + '/poscau.yaml', 'r') as fp:
fp = open(dirname(__file__) + '/poscau.yaml', 'r')
# poscau = yaml.safe_load_all(fp)
poscau = yaml.safe_load(fp)
#for doc in poscau: print(doc)
  #print(len(poscau))
# print('poscau =', poscau)

# Graph settings for small causets
gm.Graph.size = 's'
gm.Graph.nl = True
gm.Graph.verb = False


def nextCauset():
  # what to call this??  iterCauset??  but I don't want to imply completeness!
  # poscauTraverse??  pcTrav? 5jul023
  #for doc in poscau: print(type(doc), doc)
  # Do I want to use multiple docs?
  # global poscau -- seems not necessary
  if debug: print('nextCauset():', poscau)
  for c in poscau:
    if debug: print('c=', c)
    if isinstance(c, dict):
      if debug: print('dict')
      n = c['n']
#       sbs = c['sbs']
    else:
#       print(c[0]) # name
      yield c[0], gm.Graph(n,c[1], c[2])


ch1 = gm.Graph(1)

ch2 = gm.Graph(2,1)
ch2.sbs = 'tcr'
ach2 = gm.Graph(2)
ach2.sbs = 'tcr'

# We just provide links for now
ch3 = gm.Graph(3,5)
ch3.sbs = 'tr'
V = gm.Graph(3,5)
V.sbs = 'tr'

# Proposal:
# * store poscau in a yaml file
# * store structure of poscau in igraph
