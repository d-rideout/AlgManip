import yaml
from os.path import dirname
import AlgManip.graph as gm

# Always read poscau database upon import?
# with open(dirname(__file__) + '/poscau.yaml', 'r') as fp:
fp = open(dirname(__file__) + '/poscau.yaml', 'r')
# poscau = yaml.safe_load_all(fp)
poscau = yaml.safe_load(fp)
#for doc in poscau: print(doc)
  #print(len(poscau))



gm.Graph.size = 's'
gm.Graph.nl = True
gm.Graph.verb = False

print(poscau)

def junk(): print('junk')

def nextCauset():
  # what to call this??  iterCauset??  but I don't want to imply completeness!
  #for doc in poscau: print(type(doc), doc)
  # Do I want to use multiple docs?
  print('hi')
  # global poscau
  print('nextCauset():', poscau)
  for c in poscau:
    print('c=', c)
    if isinstance(c, dict):
      print('dict')
      n = c['n']
      sbs = c['sbs']
    else:
      print(c[0])
      yield gm.Graph(n,c[1])


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

# Can provide generator function which yields sequence of small causets
# Can store details in a tuple of tuples for each n

# Proposal:
# * store poscau in a yaml file
# * store structure of poscau in igraph
