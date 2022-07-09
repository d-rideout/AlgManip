# Not necessarily just logical reasoning.
# We start with mathematical recursion. (17jun022)

# print(__name__)

# if __name__=='__main__':
#   import recursion as rc
# else:
import AlgManip.recursion as rc
# import recursion as rc

# debug = True
debug = False

# Internal state variables
rrl = None
G = {}  # node db indexed by (var, it)
# dict: laziness ==> avoid computations over all nodes
#   n = 0   # store number of nodes?

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

  def __init__(sf, var, it):
    'Each node is characterized by a variable labeled by an index tuple'
    # Does node already exist?
#     n = G.get(it)
#     if n:
# #       sf = n  Surely this is the Wrong Thing, no??
#       sf.var = n.var
#       return

    # Can I get away with using tuple instead of list for index?
    sf.var = var
    sf.it = it
    sf.dp = None
    global G
    G[(var,it)] = sf
    #     node.G.append(sf)
#     node.n += 1

  def __str__(s): return f'node {s.var.name}{s.it}'

  def updateDep(sf):
    print('updating dependencies for', sf)
    if rrl: # only know recursion at the moment (21jun022)
      for rr in rrl: # recursion relation
        if rr.lhs!=sf.var: continue
        if sf.dp: print(sf, "already has dependency (FIXME)")
        # lhs of rr matches sf:
        # check min index of relation
        if debug: print(sf.it, rr.lhsMins)
        for i, m in zip(sf.it, rr.lhsMins):
          if debug: print(f'{i} vs {m}')
          if i<m: break
        else:
          sf.dp = [] # build dependency list [ (var, it), ... ]
          for r in rr.rhs: # (1+ns)-tuples (var, (slot, offset), (slot, offset), ...)
            if debug: print('var r=',r)
  #           t = r[0], # var, index tuple
            it = () # var, index tuple
            for s in r[1:]:
              if debug: print('slot=',s)
              it += sf.it[s[0]]+s[1],
            print('depends on', r[0], it)
            sf.dp.append((r[0],it))
    else: print('unclear on how to decide on dependency of', sf)
    if sf.dp==None: sf.dp = 0 # 0 ==> no dependency
    if debug: print('new dep:', sf.dp)
  

# Wrapper function that takes a node 'name', and either returns it from G or creates it
# Because I don't want multiple copies of the same node, because updates can get lost I would think. 
# def nf(var, it):
def nf(vt):
  'return node associated with var tuple'
#   n = G.get((var,it))
  n = G.get(vt)
  if n: return n
  return node(vt[0],vt[1]) #var,it)


# def recurse(rl):
#   '''execute the recursion or just declare it?
# Have user just edit rcl directly?
def recursion(rl):
  '''Declare recursion
  rl = recursion relation list'''
  global rrl
  rrl = rl

  
def request(nd):
  'Request node nd, and return its value if possible'
  # Do we want to allow request without return of value?
  print('Requested', nd)
  
  # Does nd have dependencies?
#   print(dir(nd))
#   dp = dir(nd).get('dp')
#   if not 'dp' in dir(nd)
  if nd.dp==None: nd.updateDep()
  if debug: print(nd.dp)

  if nd.dp:
    for d in nd.dp: request(nf(d))
  else: print("compute it!")
