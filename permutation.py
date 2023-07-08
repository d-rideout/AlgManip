class Perm(tuple): # let's start with tuples as the internal representation,
                   # since that is what itertools chose? 7jul023
  '''instances are elements of the symmetric group
  They are interpreted as an active transformation on the identity
  (0, 1, 2, ...).
  (l0, l1, l2, ...) (0, 1, 2, ...) = (l0, l1, l2, ...)
  with a non-identity on the right:
  (3, 0, 1, 2) (1, 3, 0, 2) = (0, 2, 3, 1)'''
#   def __mul__(s, o): return Perm([s[r] for r in o])
  def __mul__(s, o): return Perm([o[r] for r in s])
