import AlgManip.util as util

# class union:
# (class will be useful when user wants more than one union in parallel (14jun022))
def union(Es):
  '''Write measure of union as sum over intersections.
  Return sequence of signed non-empty subsets of input set of events Es
  as list of 2-tuples (sign, list of atomic events)'''
  #def __init__(s,Es):
  if not isinstance(Es, (tuple, list)):
    util.die('Please provide list-like object to AlgManip.union.union()')
#     s.n = len(Es)
  n = len(Es)
  
  for x in range(1, 1<<n):
    if not x%(1<<23): print('considering set', x) # maybe once every 45 min?
    ct = 0
    s = []
    for i in range(0, n):
      if 1<<i & x:
        ct += 1
        s.append(Es[i])
    if ct%2: sign = 1
    else: sign = -1
    yield (sign, s)
