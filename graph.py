'Fast DAG (directed acyclic graph) module' # include all graphs?
# 'Fast digraph module' (drop the acyclic assumption?)

def i2bit(i,j): return j*(j-1)//2+i  # Map from pair of indices i<j to bit

def popcount(n): return bin(n).count('1')
# www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html
# First comment suggests that this is not completely terrible??
# Python 3.10 has more native popcount?
# Just use this for now and profile (12jul022)


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


# u = (1<<i2bit(n-2,n-1)+1)-1 complete graph / chain (?)


# if debug:
#   print('i j bit_num')
#   for j in range(1,n):
#     for i in range(j): print(i,j, gm.i2bit(i,j))
# #   print('bn i  j')
# #   for i in range(1<<nc2): print(i, bit2i(i))
# #   exit()
#   print()
