import AlgManip.graph as gm
gm.Graph.size = 's'
gm.Graph.nl = True
gm.Graph.verb = False

ch1 = gm.Graph(1)

ch2 = gm.Graph(2,1)
ch2.sbs = 'tcr'
ach2 = gm.Graph(2)
ach2.sbs = 'tcr'

# We just provide links for now
ch3 = gm.Graph(3,5)
ch3.sbs = 'tr'
V = gm.Graph(3,5)
V.sbs = 'tr'

# Can provide generator function which yields sequence of small causets
# Can store details in a tuple of tuples for each n

Proposal:
* store poscau in a yaml file
* store structure of poscau in igraph
