# Plotting variables used in poly.py:
mplsym = ('o', 'x', '+', 'v')
gnuplot = False # True  # gnuplot style display


def die(msg): #, exception=None):
  'abort gracefully with message but without complicated stack trace'
#   'Pass an exception if you want a stack trace??' really only relevant if die() does something additional
  print(msg)
#   if exception: raise exception
#   else:
#   exit()  ipython does not like exit??
  raise SystemExit


# Do I want to do this???
# It seems to ask questions about how list is implemented, which seems to go
# against portability.  Will try to avoid answering these questions...
# (14jan023)
class myList(list):
  def __getitem__(s,i):
    print('calling myList.__getitem__')
    if i >= len(s): raise IndexError(f'{i} >= {len(s)}')
    return list.__setitem__(s,i)
  def __setitem__(s,i,v):
    print('calling myList.__setitem__')
    if i >= len(s): raise IndexError(f'{i} >= {len(s)}')
    list.__setitem__(s,i,v)


def incList(l, min, max):
  'increment list of ints (see recursion.py)'
  ns = len(l)
  if not ns: die('incrementing empty list??')
  for i in range(ns):
    if l[i]<max:
      l[i] += 1
      return False
    else: l[i] = min[i]
  return True
