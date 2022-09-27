# 'Fast DAG (directed acyclic graph) module' # include all graphs?
'Fast graph module' # (drop the acyclic assumption?)
import scipy.special as ss # binomial coefficients
import random as rm
import util as u

def i2bit(i,j): return j*(j-1)//2+i  # Map from pair of indices i<j to bit
#   print('i j bit_num')
#   for j in range(1,n):
#     for i in range(j): print(i,j, gm.i2bit(i,j))
# #   print('bn i  j')
# #   for i in range(1<<nc2): print(i, bit2i(i))
# #   exit()
#   print()

def popcount(n): return bin(n).count('1')
# www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html
# First comment suggests that this is not completely terrible??!
# Python 3.10 has more native popcount?
# Just use this for now and profile (12jul022)


class graph:
  dag = False
  def __init__(s, n, gr):
    # Do I want to pass n each time, or make it global?
    s.n = n
    s.gr = gr
  def __str__(s): # cf pypi.org/project/diGraph ?
    rv = ''
    spc = ''
    if dag: rn = '<'
    else: rn = '-'
    for j in range(1,s.n):
      for i in range(j):
        if s.g & 1<<i2bit(i,j):
          rv += sp + f'{i}{rn}{j}'
          spc = ' '
    return rv


# u = (1<<i2bit(n-2,n-1)+1)-1 complete graph / chain (?)


# Random Graphs via 'Generalized Percolation'
# (aka 'CSG models', ala Rideout & Sorkin 1999)
# See also Bucicovschi & Meyer & Rideout 2022???

class tn:
  '''sequence (t_n \geq 0)
  const\tt_n = 1\t\t(default)
  harm\tt_n = 1/n'''

  def __init__(s,t=None):
    if t: u.die('tn constructor: Please use default (no arguments) for now')
    s.type = t
  def __getitem__(s,i): return 1 # f'index {i}'
  def sample(s,n):
    "n is label == num of 'existing' nodes"
    # PERF: Am I going to be called many times, for each n??
    # I assume not for now. (16sep022)
    # PERF: How to start from middle? (16sep022)
    # I leave it to the random.choices() function for now (26sep022)
#     totW = 2**n # assuming t_n = 1 for now (16sep022)
    return rm.choices(range(n+1), [ss.comb(n,i, exact=True) for i in range(n+1)])[0]
    # just use tn as its own iterator or sequence type to random.choices()  say
    # which passes cumulative weights
    # does anyone really need tns directly?
#     return roll
