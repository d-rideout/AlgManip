#!/usr/bin/env python3
'Module which performs row operations.  Is this useful??'

from sys import argv
from copy import deepcopy
import fractions as f

def prm(M):
  print()
  for r in M:
    print('[ ', end='')
    for c in r: print('%3s' % c, end=' ')
    print(']')

# Store matrix as list of rows
M = [[]]
h = []

# Read matrix from command line??
# a/b c/d ... e/f, ... (; is captured by shell)
# print(argv)
ri = 0
for x in argv[1:]:
#   print(x)
  if x[-1]==',':
    x = x[:-1]
    M[ri].append(f.Fraction(x))
    ri += 1
    M.append([])
  else: M[ri].append(f.Fraction(x))

m = len(M)
n = len(M[0])
print(f'{m} x {n} matrix')
# print(M)
# print(f.Fraction(1,37))
# print(f.Fraction(37,1))
# print(f.Fraction(37,0))

while 1:
  prm(M)
  cmd = input('> ')
  h.append(cmd)
  cmd = cmd.split()
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
    if len(cmd)>2: x = f.Fraction(cmd[1])
    else: x = 1
    ro = int(cmd[-1])
    print(f'Replace row {rr} with {x} x row {ro}')
    rr -= 1
    ro -= 1
    #     xs = cmd[3:-1]
    #     if len(xs): x = int(xs)
    #     else: x = 1
    #     print(rr, ro, x)
    for c in range(n): M[rr][c] += x*M[ro][c]
    
  elif vb=='s':
    r = int(cmd[0])-1
    x = f.Fraction(cmd[1])
    print(f'Scale row {r+1} by {x}')
    for c in range(n): M[r][c] *= x

  elif vb=='i':
    r1 = int(cmd[0])-1
    r2 = int(cmd[1])-1
    print(f'Interchange rows {r1+1} and {r2+1}')
    r = M[r1]
    M[r1] = M[r2]
    M[r2] = r

  else: print(f'invalid verb {vb}')

# Save history?
for cm in h: print(cm)
