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

def popcount(n): return b.bit_count() #!!
#bin(n).count('1')
# www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html
# First comment suggests that this is not completely terrible??!
# Python 3.10 has more native popcount?
# Just use this for now and profile (12jul022)

# What is a small graph?  oeis.org/A161680/list
#  n nc2
#  6  15
#  8  28  seems safe
# 11  55  maybe this is a good cutoff?
# 14  91
# 16 120  or this?
# 23 253  or this??
# 32 496
# 45 990
# What are the widest registers for integer instructions?  512 bit? 2048 bit???
# How does python handle wide integers?
# Note that a single memory access of a 'small graph' costs O(n^2) (reading through n^2 X's), while it is only O(1) for a 'large graph'.
# (Of course what is X?  An int?  What does that mean in python?  A byte?
#  A bit?  And this matters greatly for such tiny numbers.)
# I suppose the best way to answer such questions (besides digging into source
# code) is to run experiments.  Any volunteers?

# I am suspecting that all non-small graphs can be considered 'medium'!
# There is no need for 'large' graphs.  Or maybe outside of a C implementation??
# Parallel environment? (27sep022)

class graph:
  dag = False
  size = 'm' # make this an attribute of an instance?
  # Do I want to pass n each time, or make it global?
  def __init__(s, n=0, gr=[]):
    'gr can be an int for a small graph, or a list of ints for a large graph'
    s.n = n
    s.gr = gr
  def __str__(s): # cf pypi.org/project/diGraph ?
    if graph.size != 's': return f'med graph on {s.n} nodes'
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
  def writeDag(s, fr=None):
    'Write dag to .dot file for graphviz'
    # dag ==> digraph.  Separate method writeG() can output undirected graph
    if s.size!='m':
      print('graphviz output of non-medium graphs not implemented yet')
      return
    if not fr: fr = f'dag{s.n}' #.dot'
    fp = open(fr+'.dot', 'w', newline='')
    fp.write('digraph "{fr}" {\n rankdir=BT; concentrate=true; node[shape=plaintext];\n')
    for x in range(s.n):
      w = s.gr[x]
      if w:
        for b in range(w.bit_length()):
          if 1<<b & w: fp.write(f'{b}->{x}; ')
        fp.write('\n')
      else: fp.write(f'{x};\n') # PERF: sometimes redundant
    fp.write('}\n')
    print(f'time dot -Tpdf -o {fr}.pdf {fr}.dot')
  def transClose(s):
    'Compute transitive closure of graph interpreted as a dag'
    if graph.size != 'm':
      print("Transitive closure of non-medium graphs not implemented yet")
      return
    for j in range(2,s.n): # i < j
      for i in range(1,j):
        if 1<<i & s.gr[j]: s.gr[j] |= s.gr[i]
  def transReduce(s):
    '''Compute transitive reduction of graph interpreted as a dag
    Be sure to compute transitive closure first, to get the correct answer!!'''
    if graph.size != 'm':
      print("Transitive reduction of non-medium graphs not implemented yet")
      return
    for j in range(s.n-1,1,-1): # i < j
      for i in range(j-1, 0, -1):
        try:
          if 1<<i & s.gr[j]: s.gr[j] &= ~s.gr[i] # note that relation should be irreflexive
        except IndexError: print('index error:', i,j)
# u = (1<<i2bit(n-2,n-1)+1)-1 complete graph / chain (?)


# Random Graphs via 'Generalized Percolation'
# (aka 'CSG models', ala Rideout & Sorkin 1999)
# See also Bucicovschi & Meyer & Rideout 2022???
class tn:
  '''sequence (t_n \geq 0)
  const\tt_n = 1\t\t(default)
  harm\tt_n = 1/(n+1)
  quad\tt_n = 1/(n^2+1)
  fac\tt_n = 1/n!
  forest\tt_0=t_1 = 1, t_n = 0 n > 1'''
  # n should probably be passed to the constructor instead of to sample()?
  # exact=False seems to lead to float overflows?!
  # But it is very slow for n \gtsim 2^10 -- need to write numerically stable approximations (27sep022)
  def __init__(s,t='const'):
#     if t: u.die('tn constructor: Please use default (no arguments) for now')
    if t=='const': s.df = lambda n: 1
    elif t=='harm': s.df = lambda n: n+1
    elif t=='quad': s.df = lambda n: n*n+1
    elif t=='fac': s.df = lambda n: ss.factorial(n, exact=True)
    elif t=='forest': t = None # prob Bad Idea...
    else: print(f'sequence {t} not recognized yet')
    s.type = t # store type as string?
  def __getitem__(s,i): return 1/s.df(i) # f'index {i}'
  # Will this ever be used? (27sep022)
  def sample(s,n):
    "n is label == num of 'existing' nodes"
    if s.type: return rm.choices(range(n+1),
                      [ss.comb(n,i, exact=True)/s.df(i) for i in range(n+1)])[0]
    else: return rm.choices(range(2), cum_weights=[1,n+1])[0] # forest
    # PERF: Am I going to be called many times, for each n??
    # I assume not for now. (16sep022)
    # PERF: How to start from middle? (16sep022)
    # I leave it to the random.choices() function for now (26sep022)
    #     totW = 2**n # assuming t_n = 1 for now (16sep022)
    # just use tn as its own iterator or sequence type to random.choices()  say
    # which passes cumulative weights
    # does anyone really need tns directly?
#     return roll
