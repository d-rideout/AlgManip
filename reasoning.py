# Not necessarily just logical reasoning.
# We start with mathematical recursion. (17jun022)

import AlgManip.recursion as rc

# Internal state variables
rrl = None

# Use maximally lazy evaluation
# e.g. do not even compute dependencies
class node: # partly to avoid deciding upon a less generic name
  # Instance attributes:
  # - var (e.g. in recursion)
  # - it  index tuple
  # - dp  dependencies -- compute from recursion list
  #   None ==> uninitialized
  #   0 ==> no dependency
  #   list [(var,it), ...]
  # - val
  # - (guess)

  G = {}  # node db indexed by (var, it)
  # dict: laziness ==> avoid computations over all nodes
#   n = 0   # store number of nodes?

  def __init__(sf, var, it):
    'Each node is characterized by a variable labeled by an index tuple'
    # Can I get away with using tuple instead of list?
    sf.var = var
    sf.it = it
    sf.dp = None
    node.G[(var,it)] = sf
    #     node.G.append(sf)
#     node.n += 1

  def __str__(s): return f'node {s.var.name}{s.it}'

  def updateDep(sf):
    print('updating', sf)
    if rrl: # only know recursion at the moment (21jun022)
      for rr in rrl: # recursion relation
        if rr.lhs!=sf.var: continue # print('no')
        if sf.dp: print(sf, "already has dependency (FIXME)")
        # lhs of rr matches sf:
        sf.dp = [] # build dependency list [ (var, it), ... ]
        for r in rr.rhs: # (1+ns)-tuples (var, (slot, offset), (slot, offset), ...)
          print('var r=',r)
#           t = r[0], # var, index tuple
          it = () # var, index tuple
          for s in r[1:]:
            print('slot=',s)
            it += sf.it[s[0]]+s[1],
          print('depends on', r[0], it)
          sf.dp.append((r[0],it))
    else: print('unclear on how to decide on dependency of', sf)
  

# def recurse(rl):
#   '''execute the recursion or just declare it?
# Have user just edit rcl directly?
def recursion(rl):
  '''Declare recursion
  rl = recursion relation list'''
  global rrl
  rrl = rl

  
def request(nd):
  'Request node nd'
  print('Requested', nd)
  
  # Does nd have dependencies?
#   print(dir(nd))
#   dp = dir(nd).get('dp')
#   if not 'dp' in dir(nd)
  if nd.dp==None: nd.updateDep()
  print(nd.dp)
