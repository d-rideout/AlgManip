#!/usr/bin/env python3
'Module which performs row operations'

from sys import argv
from copy import deepcopy
import fractions as f # docs.python.org/3/library/fractions.html
import poly as pm
pm.poly.mv = False
po = False # matrix contains polynomial entries

debug = False
# debug = True

# fme = None
# 2, 2 # show formula for this matrix element
           # assume row is not involved in row swaps for now
           # Please use internal indices for now
           # IN GENERAL I SHOULD NEED TO COMPUTE THE ENTIRE COLUMN!
           # AND DON'T FORGET THAT THE MULTIPLIERS IN THE ROW XFORMS ARE THEMSELVES FUNCTIONS OF MATRIX ELEMENTS!!

def prm(M):
  print('\nM=')
  for r in M:
    print('[ ', end='')
    if po:
      for c in r: print(f'({c})', end=' ')
    else:
      for c in r: print('%3s' % c, end=' ')
    print(']')
#   if fme: print(p)
#   print()
#   for r in M:
#     print('[ ', end='')
#     if po:
#       for c in r: print(f'({id(c)})', end=' ')
#     else:
#       for c in r: print('%3s' % c, end=' ')
#     print(']')


# Store matrix as list of rows
M = [[]]
h = [] # command history

# Read matrix from command line
# a/b c/d ... e/f, ... (; is captured by shell)
# print(argv)
if len(argv)<2:
  print('''Perform row operations on matrix
Specify matrix on command line as space separated list of elements
Put , or + after last element of all but the last row''')
# separated rows of space separated columns')
  exit()
ri = 0 # row index
for x in argv[1:]:
  if 'l' in x:
    po = True
    pm.poly.sym = 'l'
  elif 's' in x:
    po = True
    pm.poly.sym = 's'
  if debug: print(f'[{x}]')
  if x[-1]==',' or x[-1]=='+':
    x = x[:-1]
    M[ri].append(x)
    ri += 1
    M.append([])
  else: M[ri].append(x)

m = len(M)
n = len(M[0])
print(f'{m} x {n} matrix')

# Convert matrix elements into algebraic types
for ri in range(m):
  for ci in range(n):
    if po: M[ri][ci] = pm.str2rat(M[ri][ci])
    else: M[ri][ci] = f.Fraction(M[ri][ci])

# o2c = list(range(m)) # permutation map from original row indices to the current ones
# c2o = list(range(m)) # inverse of o2c
# # All indices start at 0 internally, but 1 from user's perspective.
# nswaps = 0

# Polynomial wrapping
# if fme:
#   def pi(i,j):
#     "map from matrix indices to variable index"
#     global n
#     return n*i + j
#
#   def pt(i,j): # polynomial term
#     "return polynomial of one matrix element?"
#     print(f'pt(): requested poly of matrix elt {i},{j}')
#     return pm.poly({tuple([0]*pi(i,j)+[1]):1})
# #     maybe construct from dict is simpler
# #     el.append(1)
# #     print(el)
# #     return pm.poly()
#
#   vn = [] # variable names
#   for r in range(m):
#     for c in range(n): vn.append(pi(r,c))
#
#   p = pt(fme[0],fme[1])
    
while 1:
  prm(M)
  cmd = input('> ')
  h.append(cmd)
  cmd = cmd.split()
  if debug: print(cmd)
  if cmd: vb = cmd.pop(0)
  else: vb = ''
  # special commands
  if vb=='q': break
  if vb=='' or vb=='?':
    print('''Command    'Lay et al'         Detail
r i [x] j  replacement         row i <- row i + x row j
i i j      interchange (swap)  rows i & j
s i x      scaling             of row i by x
q          quit / exit
u          undo
|?|h       help''')
    continue
  if vb=='u':
    M = M0
    continue

  M0 = deepcopy(M)
  if vb=='r':
    rr = int(cmd[0])
    if len(cmd)>2:
      if po: x = pm.str2rat(cmd[1])
      else: x = f.Fraction(cmd[1])
    else: x = 1
    ro = int(cmd[-1])
    print(f'Replace row {rr} with {x} x row {ro}')
    rr -= 1
    ro -= 1
    for c in range(n):
      if debug: print('col', c)
      if isinstance(M[rr][c],int) and po:
        M[rr][c] = pm.ratFunc(M[rr][c],None) + x*M[ro][c]
        #print(type(M[rr][c]), f'M{c} = M')
      else:
        M[rr][c] += x*M[ro][c]
        #print(type(M[rr][c]), f'M{c} += M')
#     for c in range(n): M[rr][c] = M[rr][c] + x*M[ro][c]
#     if fme:
#       if rr==fme[0]: p += x*pt(ro,fme[1])
# #       elif ro==fme[0]: p += x*pt(ro,fme[1])


  elif vb=='s':
    r = int(cmd[0])-1 # row to scale
    if po: x = pm.str2rat(cmd[1])
    else: x = f.Fraction(cmd[1])
    print(f'Scale row {r+1} by {x}')
    for c in range(n): M[r][c] *= x

  elif vb=='i':
    r1 = int(cmd[0])-1
    r2 = int(cmd[1])-1
    print(f'Interchange rows {r1+1} and {r2+1}')
    r = M[r1]
    M[r1] = M[r2]
    M[r2] = r
#     if fme:
#       o2c[r1], o2c[r2] = o2c[r2], o2c[r1]
#       c2o[r1], c2o[r2] = c2o[r2], c2o[r1]
#       if nswaps: print('FIXME: Handling of row permutations is likely incorrect!')
#       nswaps += 1

  else: print(f'invalid verb {vb}')

# Save history?
print('Command history:')
for cm in h: print(cm)
