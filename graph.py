'''Fast 'Lorentzian-focused' graph module

There are many graph packages available.  Most (or all?) are designed from what
I call a "Riemannian" perspective, by which I essentially just mean that one
first designs for generic graphs, and maybe, or maybe not, considers directed
acyclic graphs (dags) as a relatively unimportant special case.  I want to
design from what I call a "Lorentzian" perspective, in which dags are central,
and generalizations to non-acyclic graphs are permitted, but are not regarded
as a central use case.  The core design is intended to be optimized for
handling acyclic directed graphs.

The vertices of the graph are labeled with values taken from a poset, which is
usually the natural numbers.  A partial ordering of the labels can be used to
induce a partial order on the vertices, and thus, after transitive closure,
assuming that the label order is everywhere consistent with the edge
directions, convert the graph into a causal set.  (If unfamiliar, regard a
causal set as a finite, transitively closed, dag.)'''

import scipy.special as ss # binomial coefficients
import random as rm        # to generate random graphs
import fractions as fm     # python standard numbers
import math as mm          # e.g. log
from copy import deepcopy
from itertools import permutations # docs.python.org/3/library/itertools.html#itertools.permutations

# Trying to understand all this module path business:
# import sys
# print(sys.path)
import AlgManip.permutation as pm
import AlgManip.util as um
# for m in sys.modules.keys():
#   if m.__contains__('numpy'): continue
#   if m.__contains__('scipy'): continue
#   print(m)
# # exit()
# # quit()
# sys.exit()

# debug = False
debug = True

# # Is this general enough to warrant not being internal?
# # Yes - user will likely need it.
# # general enough to go into util.py?
# # No - wait until some other module needs it.
# def tup2hex(tup):
#   'convert tuple to hex int, with high end first'
#   n = 0
#   s = 0
#   for h in tup[::-1]:
#     n += h<<s
#     s += 4
#   return n

# Will this be needed elsewhere?
def _tup2st(t):
  'convert tuple to string of symbols (used in Bijections class)'
  ts = ''
  for x in t: ts += str(x)
  return ts
def _idtup(t):
  'Is t an identity tuple? (used in Bijections class)'
#   if debug: print('_idtup():', t, tuple(range(len(t))), t==tuple(range(len(t))))
  return t == tuple(range(len(t)))

class Bijections(set):
  'class to manage collections of bijective maps'
  # Use ints to store maps?  Leading 0's are suppressed.  See tup2hex() above.
  # But it should be a lot more space efficient? 6jul023
  # store identity to facilitate 'in' queries, but omit from output
  def __init__(s, x):
    'construct with either a string or a set of tuples'
    # Probably should make x optional, and if none or so call super().__init__()
#     s.i = n
    if isinstance(x, str): s.t = 'st'
    else: s.t = 'set'
    if debug: print('building Bijections instance from', type(x))
#     s.bj = x # should I just write s = x or something??
    s = x # should I just write s = x or something??
  def __bool__(s): return bool(s.bj) # should empty tuple ==> false?
#   def __contains__(s,x): if
  def __iter__(s):
    print('called __iter__')
    return s.bj.__iter__()
  def __str__(s):
    if s.t=='s': return s.bj
    else:
      o = len(s.bj)
      if o<2: return 'Id' # identity is assumed to always be present
      #       n = len( -- how to check for identity, to remove it??
      #       id = tuple(range(len(t)))
      sep = ''
      rv = ''
      for t in s.bj:
        if _idtup(t): continue
#         if debug: print('Bijections.__str__:', t) #, '-->', end=' ')
        # rv = ' '.join([_tup2st(t) for t in s.bj])
        rv += sep+_tup2st(t)
        sep = ' '
      if o>2: rv += f' o{o}' # num bijections (order of 'group')
      return rv
  def __repr__(s): print('This should be able to be written to a yaml file')


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
# u = (1<<i2bit(n-2,n-1)+1)-1 complete graph / chain (?)
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

class node: # lower case because it is internal (and nested classes are really confusing)
  def __init__(s, nl, pst=None, fut=None):
    if pst==None: pst = set()
    if fut==None: fut = set()
    s.nl = nl
    s.pst = pst
    s.fut = fut

class Graph:
  # make class attributes instance attributes if the need arises (12jan023)
  '''Class attributes: Set these before calling constructor
  dg   : directed graph? - used for output currently
  size : 'm|s|l' maybe, see above comments for some discussion
  nl   : assume application code knows natural labeling (though not necessarily
         number of nodes!)
  verb : verbose output

  Instance attributes: (not necessarily defined for a given instance)
  n  : number of vertices/nodes/elts
  gr : binary representation of graph (details depend on size above)
       (medium graphs hold useless 0 in gr[0])
  grr: transitively reduced binary representation
  NOT SURE I AM HANDLING THIS PROPERLY IN causet.py!!!
  nn : node names (indexed by natural label, for output)
  nd : node_dict key name val dict keys [better to make .nd[x] node objects?]
       nl:natural label
       in: inbound edge set
       out: outbound edge set
       edge sets stored by names -- natural labels may change
  sbs : state of binary edge storage
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
  writeDag     : write dot file (just hard coding dag aspect for now (16nov022))
  transClose   : assuming dag, add all relations/edges implied by transitivity
  transReduce  : assuming dag, remove all relations/edges implied by transitivity (transClose first!)
  automorphism : Is map an automorphism?
  aut          : print automorphism group of graph
  natlab       : list natural labelings of causet

  If you have a natural labeling of a causet,
  use it to populate nn and gr directly (and set nl=True).
  Else use methods.
  <Graph instance>[i] indexes into the gr instance attribute'''
  dg = True
  size = 'm'
  nl = False
  verb = True

  def __init__(s, n=0, gr=None, sbs=None):
    '''Please pass number of nodes n if it is known, otherwise it defaults to 0.
    gr can be an int for a small graph, or a list of ints for a large graph
    Please update sbs instance attribute (state of binary edge storage) after edges are added, if known (and n>2)

    Even in the case of nl, the graph size may not be known at time of construction!'''
    #     assert s.size == size, "global size disagrees with class size"
    if s.dg: directed = ' directed '
    else: directed = ' '
    if s.nl:
      if s.verb:
        print("Constructing"+directed+"graph assuming known labeling")
        if n==0: print("... with default n=0: Consider adding nodes via addNode() method.")
          #print("Using natural labeling but with unknown n.  Please add nodes via addNode() method")
          #print("WARNING: nl causets are not guaranteed to learn their true size from the edges alone")
      if gr==None:
        if s.size=='m': gr = [0]*n
        elif s.size=='s': gr = 0
        else: um.die('Unknown graph size')
      # s.nn = [None]*n
      s.nn = um.myList([None]*n)
      # print(type(s.nn))
      s.nd = None
    else:
      print("Constructing"+directed+"graph with non-natural labeling")
      if n:
        print("Ignoring input n.  Please use addNode() or addEdge() methods to populate graph")
        n = 0
      s.nn = []
      s.nd = {}
    s.n = n
    if sbs: s.sbs = sbs
    elif n>2: s.sbs = 'u'
    else: s.sbs = 'tcr'
    s.gr = gr
    if s.size != 'm' and s.verb: print("WARNING: Some graph methods may implicitly assume Graph.size == 'm'?")

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
    if s.dg: rn = '<'
    else: rn = '-'
    disconnected = [True]*s.n
    for j in range(1,s.n):
      for i in range(j):
        if s.gr & 1<<i2bit(i,j):
          rv += spc + f'{i}{rn}{j}'
          disconnected[i] = disconnected[j] = False
          spc = ' '
    for i in range(s.n):
      if disconnected[i]:
        rv += spc + str(i)
        spc = ' '
    return rv

  def __format__(s, fmt):
    #print('format requested:', fmt)
    return f'{str(s):{fmt}}'

  def _buildBinRep(s):
    'reconstruct binary representation of graph and nn[]'
    if debug: print('Reconstructing binary representation')
    if s.n:
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
    if not s.nd: return
    for x in s.nd:
      print(f'[{x}]:')
      print('nl =', s.nd[x]['nl'])
      print('in =', s.nd[x]['in'])
      print('out =', s.nd[x]['out'])

  def addNode(s, x): # accept multiple nodes too? (10jan023)
    # Might want to allow unnamed nodes too (14jan023)
    "Add node x" #, coding 'generic' version first"
    if debug: print(f'addNode: {x} nd={s.nd}')
    if s.nd!=None: # \equiv nl currently (14jan023)
      if x in s.nd: return
      s.nd[x] = {'nl':s.n, 'in':set(), 'out':set()}
    s.nn.append(x)
    if debug: print('addNode: nn =', s.nn)
    s.n += 1

  def _relabel(s):
    '''Attempt to find natural labeling of graph
    I *think* this works for non-transitive digraphs'''
    nl = 0
    done = set()
    newdone = set()
    print(f'relabeling {s.n}-node digraph')
#     if debug:
#       print('Before relabeling:')
#       s._dumpState()
    while nl<s.n:
      progress = False
      done.update(newdone)
      for xn in s.nd:
  #       print(f'x={x}')
        if xn in done: continue
#         if debug: print(f"{s.nd[xn]['in']} \ {done}")
        if not s.nd[xn]['in']-done:
          s.nd[xn]['nl'] = nl
          nl += 1
          newdone.add(xn)
          progress = True
      if not progress: um.die('Relabeling failed: Graph contains cycle?')
    s.gr = None # destroy binary representation since it will be wrong now
    s.nn = []
#     if debug:
#       print('After relabeling:')
#       s._dumpState()

  def addEdge(s, x, y): # Will one want to add undirected edges? (10jan023)
    """Add directed edge from node x to node y"""
#     coding 'generic' version first"""
    print(f"[{x}] \prec [{y}]")
    s.sbs = 'u' # I don't see how to avoid this easily?
               # Should we have some convention when nl == True?? (12jan023)
    if s.nl: # if using natural labels to identify nodes
      s[y] |= 1<<x # This assumes size=='m'!
      return
    s.addNode(x); s.addNode(y)
    # Is edge consistent with natural labeling?
    xl = s.nd[x]['nl']; yl = s.nd[y]['nl']
    print(f'Is {xl} < {yl}?')
    assert xl != yl
    # Store edge
    s.nd[x]['out'].add(y)
    s.nd[y]['in'].add(x)
    if xl > yl: # x and y are in wrong relation given natural labeling
      print(f"{xl} \prec {yl} -- attempting to fix")
      s._relabel()
#       if debug: s._dumpState()
    assert s.size == 'm'
    if s.gr != None: s[yl] |= 1<<xl
#     s.tc = False  Why is this commented?? (15jan023)

  def prec(s, x, y):
    'fast query of x \prec y for small graphs?  Assumes x<y.'
    # PERF: include order check??
    return s.gr & 1<<i2bit(x,y)

  def queryEdge(s, x, y):
    '''query presence of edge using node names, in either direction
    Uses binary representation so can query after transitive closure
    returns 2-tuple with earlier node on left if edge present [too complicated? (12jan023)]
    or False if no binary representation [also too complicated? (12jan023)]'''
    if not s.gr: return False
    if not (x in s.nd and y in s.nd): return False # non-existent nodes are not part of edges
    xl = s.nd[x]['nl']
    yl = s.nd[y]['nl']
    if xl>yl: xl, yl = yl, xl
    if debug:
      s._dumpState()
      print(f'queryEdge: xl={xl} yl={yl}')
    if 1<<xl & s.gr[yl]: return s.nn[xl], s.nn[yl]
#     return 1<<xl & s.gr[yl]

  def writeDag(s, fnr=None, ast=None):
    '''Write dag to .dot file for graphviz
    fnr = filename root
    ast = string to add to dot file : Please add '#' to beginning of comments!
    Uses grr instead of gr.  Is this a problem??'''
    # dag ==> digraph.  Separate method writeG() can output undirected graph
    if s.size=='l':
      print('graphviz output of large graphs not implemented yet')
      return
    if s.gr==None: s._buildBinRep()
    if not s.sbs or s.sbs[-1]!='r':
      if not s.transReduce(): # too wonky? (12jan023)
        print("transitive reduction failed -- aborting writeDag")
        return
    if not fnr: fnr = f'dag{s.n:04}' #.dot'
    fp = open(fnr+'.dot', 'w', newline='')
    fp.write('digraph "'+fnr+'" {\n rankdir=BT; concentrate=true; node[shape=plaintext];\n')
    if s.nn:
      for i, nn in enumerate(s.nn):
        if nn: fp.write(f'{i} [label="{nn}"]\n')
        else: fp.write(f'{i}\n')
    for x in range(s.n):
      if s.size=='m':
        w = s.grr[x]
        if w:
          for b in range(w.bit_length()):
            if 1<<b & w: fp.write(f'{b}->{x}; ')
          fp.write('\n')
        else: fp.write(f'{x};\n') # PERF: sometimes redundant
      else:
        for w in range(x):
          if s.prec(w,x): fp.write(f'{w}->{x}; ')
        fp.write('\n')
    if ast: fp.write(ast+'\n')
    fp.write('}\n')
    print(f'time dot -Tpdf -o {fnr}.pdf {fnr}.dot')

  def transClose(s):
    'Compute transitive closure of graph interpreted as a dag'
    if s.size != 'm':
      print("Transitive closure of non-medium graphs not implemented yet")
      return
    if s.gr==None: s._buildBinRep()
    if debug: print(f'in  transClose: nl={s.nl} gr={s.gr}')
    for j in range(2,s.n): # i < j
      for i in range(1,j):
        if 1<<i & s.gr[j]: s.gr[j] |= s.gr[i]
    s.tc = True
    if debug: print(f'out transClose: nl={s.nl} gr={s.gr}')

  def transReduce(s):
    'Compute transitive reduction of graph interpreted as a dag'
    # def pstx(x):
    #   'return int which is 1 in past(x) region'
    #   return 1<<x*(x+1)//2-1
    # def pstx(x):
    #       'return int which is 1 in past(x) region'
    #       return (1<<x*(x+1)//2) - (1<<x*(x-1)//2)
    # for x in range(1,5):
    #   big = (1<<x*(x+1)//2)-1
    #   lit = (1<<x*(x-1)//2)-1
    #   print(x, bin(big), bin(lit), bin(big-lit),
    #                            bin(pstx(x)))
    if s.sbs and s.sbs[-1] == 'r': return
    if s.sbs == 'u': print('Unknown transitive closure state -- assuming the worst')
    if s.sbs != 'tc': s.transClose()
#     elif s.tc == 'u': print("WARNING: Unknown transitive closure state -- transitive reduction may be incorrect")
    if s.size != 'm':
      print("Transitive reduction of non-medium graphs not implemented yet")
      return False
    s.grr = deepcopy(s.gr)
    for j in range(s.n-1,1,-1): # i < j
      for i in range(j-1, 0, -1):
        try:
          #if s.size=='m':
          if 1<<i & s.grr[j]: s.grr[j] &= ~s.grr[i] # note that relation should be irreflexive
          #else: pass
            # below is wrong.  Want to subtract past(i) from j.  z picks out past(i), but then it needs to be shifted up to j and then subtracted
            # if i2bit(i,j):
            #   z = (1<<i*(i+1)//2) - (1<<i*(i-1)//2)
            #   # print(bin(z), bin(s.grr&z), bin(~(s.grr&z)))
            #   # s.grr &= ~(s.grr&z)
            #   s.grr &= s.grr^z
        except IndexError: print('index error:', i,j)

  def npst(s, x):
    'return cardinality of past(x)'
    assert s.size=='s'
    np = 0
    for i in range(x):
      if s.prec(i,x): np += 1
    return np

  def automorphism(s, phi):
    '''Is phi an automorphism?
    Possibly making numerous unstated assumptions.  e.g. not checking input.
    phi is 'list' of natural number labels (i.e. a permutation)'''
    # assuming binary storage for now
    #print('Is', map, 'an automorphism?')
    for y in range(1,s.n):
      for x in range(y):
        px, py = phi[x],phi[y]
        #print(x,y, s.prec(x,y), end=' : ')
        #print(px,py)
        if s.prec(x,y):
          if px>py: return False
          if not s.prec(px,py): return False
        else:
          if px>py: px,py = py,px
          if s.prec(px,py):
            #print(px,'\prec',py)
            return False
    return True

  def aut(s):
    'return automorphism group of graph, as Bijections instance'
    if not s.gr: return Bijections(f'S{s.n}')
#     # Compute cardinality of pasts
#     npsts = {}
#     for x in range(s.n):
#       n = s.npst(x)
#       #npst.append(s.npst(x))
#       if n in npsts: npsts[n].append(x)
#       else: npsts[n] = [x]
#     print(npsts)
#
#     # Cycle through permutations of 'level sets'
#     phi = [None]*s.n
#     for np in npsts:
#       print('np=', np)
#       for npp in permutations(npsts[np]):
#         print(npp)
#         for i,v in zip(npsts[np],npp):
#           print('i,v=', i,v)
#           phi[i] = v
#         # ... I need to build a generator function which loops over these permutations.
#         yield here or something
    rv = set()
    perms = permutations(range(s.n))
    rv.add(next(perms)) # identity always in automorphism group
    for phi in perms:
      if s.automorphism(phi): rv.add(phi)
      #     print('Graph.aut:', rv)
    return Bijections(rv)
  #     if rv:
  #     else: return Bijections('Id')

  def natlab(s, autG=None):
    '''compute natural labelings of causet
    optionally modulo automorphism group'''
    if debug:
      print('natlab(): autG =', autG, end=' : ')
      if autG: print('true')
      else: print('false')

    # antichains are trivially complicated
    if not s.n: return Bijections('none')
    elif not s.gr:
      if autG: return Bijections('Id')
      else: return Bijections(f'S{s.n}')

    # precompute list of links
    links = []
    for y in range(1, s.n):
      for x in range(y):
        if s.prec(x,y): links.append((x,y))

    # loop over every possible labeling
    perms = permutations(range(s.n))
#     next(perms) # ignore identity
    rv = set() # set of permutations (tuples), identity always valid
    rv.add(next(perms)) # tuple as element
    for l in perms:
      if debug: print('considering', l)
      for x,y in links:
        if l[x]>l[y]: break
      else:
        print('okay')
        if autG: # Does gl already appear in rv, for some g \in autG
          if debug: print('is elt of Gl already included?')
          # multiply l by every g \in autG, and ask if it is in rv
          for g in autG:
            if debug:
              print('g:', type(g), type(l)) #, type(g*l))
              print('g =', g, l, g*l)
            # if so then skip it
            if g*l in rv:
              print('yep')
              break
            # as an added bonus, can ask which of the two are smaller, and keep the smaller.  This should yield a canonical representative of the labeling, rather than a representative which depends on this algorithm 7jul023
          else: rv.add(l)
        else: rv.add(l)
    return Bijections(rv)


# Random Graphs via 'Generalized Percolation'
# (aka 'CSG models', ala Rideout & Sorkin 1999)
# See also Bucicovschi & Meyer & Rideout 2023???
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

if __name__=='__main__':
  Graph.nl = True
  Graph.size = 's'

  if True:
    #inPr = 0b001011001000010001000
    #inPr = 0b0010110001011001000010001000
    inPr9 = 0b001001010010110001011001000010001000
    inPr10 = 0b110110111001001010010110001011001000010001000
    inPr11 = 0b0011011111110110111001001010010110001011001000010001000
    inPr12 = 0b001011011110011011111110110111001001010010110001011001000010001000
    inPr = Graph(12, inPr12)
    inPr.sbs = 'tc'
    print(inPr)
    #print(inequivPrecur.automorphism((3,4,5,6,7,8,0,1,2)))
    #print(inequivPrecur.automorphism((1,2,0,4,5,3,7,8,6)))
    inPr.aut()

    inPr.writeDag()
  else:
    cs = Graph(4,0b011110)
    print('cs=', cs)
    cs._dumpState()
    print(cs.automorphism((1,2,0,3)))
    cs.aut()
    cs.writeDag()
