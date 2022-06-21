# Not necessarily just logical reasoning.
# We start with mathematical recursion. (17jun022)

import AlgManip.recursion as rc

# Internal state variables
rcl = None

# Use maximally lazy evaluation
# e.g. do not even compute dependencies
class node: # partly to avoid deciding upon a less generic name
  '''Instance attributes:
  var (e.g. in recursion)
  dependencies -- compute from recursion list
  val
  (guess)
  '''
  G = {}  # ground set of nodes?
  # dict: laziness ==> avoid computations over all nodes
#   n = 0   # store number of nodes?

  def __init__(sf, var, it):
    'Each node is characterized by a variable labeled by an index tuple'
    # Can I get away with using tuple instead of list?
    sf.var = var
    sf.it = it
    node.G[it] = sf
    #     node.G.append(sf)
#     node.n += 1

  def __str__(s): return f'node {s.var.name}{s.it}'
  

# def recurse(rl):
#   '''execute the recursion or just declare it?
# Have user just edit rcl directly?
def recursion(rl):
  '''Declare recursion
  rl = recursion relation list'''
  rcl = rl

  
def request(nd):
  'Request node nd'
  print('Requested', nd)
  
