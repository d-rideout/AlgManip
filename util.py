mplsym = ('o', 'x', '+', 'v')
gnuplot = False # True  # gnuplot style display

def die(msg):
  print(msg)
  exit()
  
def incList(l, min, max):
  'increment list if ints'
  ns = len(l)
  if not ns: die('incrementing empty list??')
  for i in range(ns):
    if l[i]<max:
      l[i] += 1
      return False
    else: l[i] = min[i]
  return True
