'Fast DAG module' # include all graphs?
# 'Fast digraph module' # include all graphs?

def i2bit(i,j): return j*(j-1)//2+i  # Map from pair of indices i<j to bit


# class digraph: # distinguish this from an ordinary graph?
# And really it is a DAG
class dag:
  def __init__(s, n, g):
    # Do I want to pass n each time, or make it global?
    s.n = n
    s.g = g
  def __str__(s): # cf pypi.org/project/diGraph ?
    rv = ''
    sp = ''
    for j in range(1,s.n):
      for i in range(j):
        if s.g & 1<<i2bit(i,j):
          rv += sp + f'{i}<{j}'
          sp = ' '
    return rv
