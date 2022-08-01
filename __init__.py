print('Importing AlgManip python package module')

import sys # Anybody can access this via AlgManip.sys

# print(sys.path)
sys.path.insert(1,'AlgManip')
# print(sys.path)
# My local imports are not package imports when called from other directories
# But am I duplicating modules this way?  Probably.  How do people manage this?

if False:
  import os
  from datetime import date
  cwd = os.getcwd()
  date = date.today()

  print(f'(from {cwd} on {date})', end='\n\n')

  print('package module init file =', __file__)
  # https://www.delftstack.com/howto/python/get-directory-from-path-in-python
  print('package module directory =', os.path.dirname(__file__), end='\n\n')

  print('module __name__ (from perspective of importing program) =', __name__, end='\n\n')

  print('dir() (names in current scope):', dir(), end='\n\n')
#   print('dir(__name__):', dir(__name__), end='\n\n')
#   print(__name__.__class__)
# __name__ is just a string!

#   print('__dict__:', __dict__, end='\n\n')
#   print('__name__.__dict__:', __name__.__dict__, end='\n\n')
# neither the current scope nor the string object __name__ have a __dict__ attribute

  class junk: pass
  print("empty class's __dict__ attribute:", junk.__dict__) # classes have __dict__attributes
  print("empty class instance's __dict__ attribute:", junk().__dict__) # classes have __dict__attributes

#   print(os.__dict__) # as do modules (but it is enormous for os)

  def junkf(): pass
  print("empty function's __dict__ attribute:", junkf.__dict__)

  exit()
