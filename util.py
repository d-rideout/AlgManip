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
