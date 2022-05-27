import AlgManip.util as util

def union(Es):
  '''Return signed list of subsets of input set of events Es
  as list of 2-tuples (sign, list of atomic events)'''
  if not isinstance(Es, tuple): util.die('please provide list-like object to union()')
  retval = []
  
  n = len(Es)
#   print(n, 1<<n)

  for x in range(1, 1<<n):
#     print(x)
    c = 0
    s = []
    for i in range(0, n):
      if 1<<i & x:
        c += 1
        s.append(Es[i])
    if c%2: sign = 1
    else: sign = -1
    retval.append((sign, s))

  return retval
  
#   for i in Es:
#     retval.append((1,[i]))
    
  
