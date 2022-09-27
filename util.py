mplsym = ('o', 'x', '+', 'v')
gnuplot = False # True  # gnuplot style display

def die(msg): # Rethink how to handle this with exceptions! (16sep022)
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
