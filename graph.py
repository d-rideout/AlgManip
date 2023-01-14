'''Fast graph module

(The vertices of the graph are labeled with values taken from a poset, which
is usually the natural numbers.  A partial ordering of the labels can
be used to induce a partial order on the vertices, and thus, after transitive
closure, convert the graph into a causal set.)'''
# [How to handle spacelike vertices connected by an edge?
# Just keep these as a second relation defined on the vertex set??]'''
import scipy.special as ss # binomial coefficients
import random as rm        # to generate random graphs
import fractions as fm     # python standard numbers
import math as mm          # e.g. log

# Trying to understand all this module path business:
# import sys
# print(sys.path)
import AlgManip.util as um
# for m in sys.modules.keys():
#   if m.__contains__('numpy'): continue
#   if m.__contains__('scipy'): continue
#   print(m)
# # exit()
# # quit()
# sys.exit()

debug = False

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
# Note that a single memory access of a 'small graph' costs O(n^2)
# (reading through n^2 X's), while it is only O(1) for a 'large graph'.
# (Of course what is X?  An int?  What does that mean in python?  A byte?
#  A bit?  And this matters greatly for such tiny numbers.)
# I suppose the best way to answer such questions (besides digging into source
# code) is to run experiments.  Any volunteers?
#
# I am suspecting that all non-small graphs can be considered 'medium'!
# There is no need for 'large' graphs.  Or maybe outside of a C implementation??
# Parallel environment? (27sep022)
# size = 'm'

# class binrep:
#   '''binary representation of graph
#   lower case because it is intended to be internal to the graph module'''
#   def __init__(s, n, gr):
#     assert size == 'm', "assuming size == m for now"

# math.stackexchange.com/questions/31207/graph-terminology-vertex-node-edge-arc
# Let's prefer 'node' to 'vertex', since the latter comes from geometry
# And prefer 'node' to 'element', since the latter is not generally used for graphs
# And 'edge' to 'arc' since the former is more common?  Though it comes from geometry.  Can I avoid the term? (10jan023)

class Graph:
  '''Class attributes: Set these before calling constructor
     [make any of these instance attributes if the need arises (12jan023)]
  dg   : directed graph? - used for output currently
  size : 'm|s|l' maybe, see above comments for some discussion
  nl   : assume natural labeling is known at the outset and fixed

  Instance attributes: (not necessarily defined for a given instance)
  n  : number of vertices/nodes/elts
  gr : binary representation of graph (details depend on size above)
       (medium graphs hold useless 0 in gr[0])
  nn : node names (indexed by natural label, for output)
  nd : node_dict key name val dict keys
       nl:natural label
       in: inbound edge set
       out: outbound edge set
       edge sets stored by names -- natural labels may change
  st : state of binary edge storage
       (edges stored in nd are those that have been explicitly declared)
       (gr=None) : no binary storage
       None : none of the below
       'u'  : unknown
       'tc' : transitively closed
       'tr' : transitively reduced
       'tcr' : both transitively closed and reduced
               (for partial orders of height <=2)
#   tc : Is graph(?) transitively closed? ('u' for unknown(?)) [deprecated (12jan023)]

  Class methods:
  writeDag    : write dot file (just hard coding dag aspect for now (16nov022))
  transClose  : assuming dag, add all relations/edges implied by transitivity
  transReduce : assuming dag, remove all relations/edges implied by transitivity (transClose first!)

  If you have a natural labeling of a causet,
  use it to populate nn and gr directly (and set nl=True).
  Else use methods.
  <Graph instance>[i] indexes into the gr instance attribute'''
  dg = True
  size = 'm'
  nl = False

  def __init__(s, n=0, gr=None):
    '''Please pass number of nodes n if it is known, otherwise it defaults to 0.
    gr can be an int for a small graph, or a list of ints for a large graph
    Please update st attribute after edges are added, if known (and n>2)'''
    #     assert s.size == size, "global size disagrees with class size"
    if s.nl: print("Constructing graph assuming known labeling")
    else:
      print("Constructing graph with non-natural labeling")
      if n:
        print("Ignoring input n.  Please use addNode() or addEdge() methods to populate graph")
        n = 0
    if n==0 and s.nl: print("WARNING: nl causets are not guaranteed to learn their true size from the edges alone")
    s.n = n
    if gr==None and s.nl: gr = [0]*n
    if n>2: s.st = 'u'
    else: s.st = 'tcr'
    s.gr = gr
    if s.nl: s.nn = [None]*n
    else: s.nn = []
    if s.nl: s.nd = None
    else: s.nd = {}

    if s.size != 'm':
      print("WARNING: Some graph methods may implicitly assume Graph.size == 'm'?")

  def __getitem__(s, i):
    assert s.size=='m', "currently assumes medium graphs"
    l = len(s.gr)
    if l>s.n: s.n=l
    if l <= i: s.gr += [0]*(i+1-l)
    return s.gr[i]

  def __setitem__(s, i, v):
    assert s.size=='m', "currently assumes medium graphs"
    s.gr[i] = v

  def __str__(s): # cf pypi.org/project/diGraph ?
    if s.size != 's': return f'<med graph on {s.n} nodes>'
    rv = ''
    spc = ''
    if dg: rn = '<'
    else: rn = '-'
    for j in range(1,s.n):
      for i in range(j):
        if s.g & 1<<i2bit(i,j):
          rv += sp + f'{i}{rn}{j}'
          spc = ' '
    return rv

  def _buildBinRep(s):
    'reconstruct binary representation of graph and nn[]'
    s.gr = [0]*s.n
    s.nn = [None]*s.n
    # Assuming graph is acyclic!!(?)
    for x in s.nd: # fill in past(x)
      xl = s.nd[x]['nl']
      for pstx in s.nd[x]['in']: s[xl] |= 1<<s.nd[pstx]['nl']
      s.nn[xl] = x

  def _dumpState(s):
    'dump state for debugging'
    print(f'n = {s.n}')
    print(f'gr = {s.gr}')
    print(f'nn = {s.nn}')
#     print(f'nd = {s.nd}')
    for x in s.nd:
      print(f'[{x}]:')
      print('nl =', s.nd[x]['nl'])
      print('in =', s.nd[x]['in'])
      print('out =', s.nd[x]['out'])

  def addNode(s, x): # take multiple nodes? (10jan023)
    "Add node x, coding 'generic' version first"
#     if not s.nd: s.nd = {} # write all this as another method?? (10jan023)
    if x in s.nd: return
    s.nd[x] = {'nl':s.n, 'in':set(), 'out':set()}
    s.nn.append(x)
    if debug: print('addNode: nn =', s.nn)
    s.n += 1

  def addEdge(s, x, y): # Will one want to add undirected edges? (10jan023)
    """Add directed edge from node x to node y"""
#     coding 'generic' version first"""
    print(f"[{x}] \prec [{y}]")
    s.st = 'u' # I don't see how to avoid this easily?
               # Should we have some convention when nl == True?? (12jan023)
    if s.nl: # if using natural labels to identify nodes
      s[y] |= 1<<x # This assumes size=='m'!
      return
    s.addNode(x); s.addNode(y)
    # Is edge consistent with natural labeling?
    xl = s.nd[x]['nl']; yl = s.nd[y]['nl']
    print(f'Is {xl} < {yl}?')
    assert xl != yl
    if xl > yl: # x and y are in wrong relation given natural labeling
#       try:
      print(f"{xl} \prec {yl} -- attempting to fix")
      # shove all natural labels y .. to right
      pstx = s.nd[x]['in']
      for tmp in s.nn[yl:xl]:
        s.nd[tmp]['nl'] += 1
        if tmp in pstx:
          print("Naive attempt to maintain natural labeling of nodes failed.")
          um.die("Not sure how to handle") # nor what is going to happen...")
          # ... super unclear on the try-else -- I did not indent anything yet (11jan023)
      s.nd[x]['nl'] = yl
      print(s.nn)
      s.nn.insert(yl, x)
      print(s.nn)
      s.nn.pop(xl+1)
      print(s.nn) #, end='\n\n')
#       else:
      s.gr = None # destroy binary representation since it will be wrong now
      s.nn = None
      if debug: s._dumpState()
    # Store edge
    s.nd[x]['out'].add(y)
    s.nd[y]['in'].add(x)
    assert s.size == 'm'
    if s.gr != None: s[yl] |= 1<<xl
#     s.tc = False

  def queryEdge(s, x, y):
    '''query presence of edge using node names, in either direction
    Uses binary representation so can query after transitive closure
    returns 2-tuple with earlier node on left if edge present [too complicated? (12jan023)]
    or False if no binary representation [also too complicated? (12jan023)]'''
    if not s.gr: return False
    xl = s.nd[x]['nl']
    yl = s.nd[y]['nl']
    if xl>yl: xl, yl = yl, xl
    if debug: print(f'queryEdge:')
    if 1<<xl & s.gr[yl]: return s.nn[xl], s.nn[yl]
#     return 1<<xl & s.gr[yl]

  def writeDag(s, fnr=None, st=None):
    '''Write dag to .dot file for graphviz
    fnr = filename root
    st = string to add to dot file : Please add '#' to beginning of comments!'''
    # dag ==> digraph.  Separate method writeG() can output undirected graph
    if s.size!='m':
      print('graphviz output of non-medium graphs not implemented yet')
      return
    if s.gr==None: s._buildBinRep()
    if not s.st or s.st[-1]!='r': s.transReduce() # too wonky? (12jan023)
    if not fnr: fnr = f'dag{s.n:04}' #.dot'
    fp = open(fnr+'.dot', 'w', newline='')
    fp.write('digraph "'+fnr+'" {\n rankdir=BT; concentrate=true; node[shape=plaintext];\n')
    if s.nn:
      for i, nn in enumerate(s.nn): fp.write(f'{i} [label="{nn}"]\n')
    for x in range(s.n):
      w = s.gr[x]
      if w:
        for b in range(w.bit_length()):
          if 1<<b & w: fp.write(f'{b}->{x}; ')
        fp.write('\n')
      else: fp.write(f'{x};\n') # PERF: sometimes redundant
    if st: fp.write(st+'\n')
    fp.write('}\n')
    print(f'time dot -Tpdf -o {fnr}.pdf {fnr}.dot')

  def transClose(s):
    'Compute transitive closure of graph interpreted as a dag'
    if s.size != 'm':
      print("Transitive closure of non-medium graphs not implemented yet")
      return
    if s.gr==None: s._buildBinRep()
    if debug: print(f'transClose: nl={s.nl} gr={s.gr}')
    for j in range(2,s.n): # i < j
      for i in range(1,j):
        if 1<<i & s.gr[j]: s.gr[j] |= s.gr[i]
    s.tc = True

  def transReduce(s):
    'Compute transitive reduction of graph interpreted as a dag'
    if s.st and s.st[-1] == 'r': return
    if s.st == 'u': print('Unknown transitive closure state -- assuming the worst')
    if s.st != 'tc': s.transClose()
#     elif s.tc == 'u': print("WARNING: Unknown transitive closure state -- transitive reduction may be incorrect")
    if s.size != 'm':
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
  '''sequence (t_n \geq 0) (in decreasing order of chainlikeness?)
  const\tt_n = 1\t\t(default)
  efac\tt_n = 2^n/n!
  harm\tt_n = 1/(n+1)
  quad\tt_n = 1/(n^2+1)
  dfac\tt_n = 1/n!!
  llfac\tt_n = ceil(log2(log2(n+2)+2))/n!
  fac\tt_n = 1/n!
  mybin\tt_n = 0 for n>2
  forest\tt_0=t_1 = 1, t_n = 0 n > 1'''
  # n should probably be passed to the constructor instead of to sample()?
  # exact=False seems to lead to float overflows?!
  # But it is very slow for n \gtsim 2^10 -- need to write numerically stable approximations (27sep022)
  def __init__(s,ty='const'):
    s.ts = None # for finite sequences
    # s.df is the *denominator* (function)
    # (Maybe this is too confusing now that I am using Fraction()s?)
    if ty=='const': s.df = lambda n: 1
    elif ty=='harm': s.df = lambda n: fm.Fraction(n+1)
    elif ty=='quad': s.df = lambda n: fm.Fraction(n*n+1)
    elif ty=='dfac': s.df = lambda n: fm.Fraction(ss.factorial2(n, exact=True))
    elif ty=='fac': s.df = lambda n: fm.Fraction(ss.factorial(n, exact=True))
    elif ty=='llfac':
      s.df = lambda n: fm.Fraction( ss.factorial(n, exact=True),
                                   int( mm.log(mm.log(n+1,2)+1,2) +1.5 ) )
#       s.df = lambda n: fm.Fraction(ss.factorial(n, exact=True),
#                                    mm.ceil(mm.log(mm.log(n+2,2)+2,2)))
    elif ty=='efac': s.df = lambda n: fm.Fraction(ss.factorial(n, exact=True), 2**n)
    elif ty=='mybin': s.ts = (5,3,1) # NOTE: tn>0 will always be dominated by last entry!
    elif ty=='forest': s.ts = (1,1)
    else: print(f'sequence {ty} not recognized yet')
    s.type = ty # store type as string?
#     if ts:
#       s.cum = []
#       sum = 0
#       for x in ts:
#         sum += x
#         s.cum.append(sum)
#       print('cum:', s.cum)

  def __getitem__(s,i):
    print('WARNING: tn.__getitem__() is not maintained -- likely returning wrong result')
    return 1/s.df(i) # f'index {i}'
  # Will this ever be used? (27sep022)
  # Does anyone really need tns directly?

  def sample(s,n, verb=False):
    '''Sample from 'cardinality distribution' defined by (tn) (and n)
    n is label == cardinality of 'existing' nodes'''
    if not s.ts:
      weights = [ss.comb(n,k, exact=True)/s.df(k) for k in range(n+1)]
      if verb: print([f'{x.numerator}/{x.denominator}' for x in weights])
      return rm.choices(range(n+1), weights)[0]
    else:
      N = len(s.ts)
      if n<N: N = n+1
      weights = [ss.comb(n,k, exact=True)*s.ts[k] for k in range(N)]
      if verb: print('weights:', weights)
      return rm.choices(range(N), weights)[0]
#       return rm.choices(range(2), cum_weights=[1,n+1])[0] # forest
    # PERF: Am I going to be called many times, for each n??
    # I assume not for now. (16sep022)
    # PERF: How to start from middle? (16sep022)
    # I leave it to the random.choices() function for now (26sep022)
    #     totW = 2**n # assuming t_n = 1 for now (16sep022)
    # just use tn as its own iterator or sequence type to random.choices()  say
    # which passes cumulative weights


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
