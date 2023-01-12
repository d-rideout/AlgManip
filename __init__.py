print('Importing AlgManip python package module')


# import sys # Anybody can access this via AlgManip.sys
# print(sys.path)
# sys.path.insert(1,'AlgManip')
# Commented above line to understand all this, see docs.python.org/3/reference/import.html @ 5.3 Searching (5jan023)
# print(sys.path)

# This allows files within AlgManip to import other files in AlgManip directly.
# But is this silly?
# What happens if someone does not put AlgManip in a directory which is in
# their python path?
# Oh, I think this question is answered in the sentences below?
# Please understand all this! The code below may be helpful for this. (29nov022)

# My local imports are not package imports when called from other directories.
# But am I duplicating modules this way?  Probably.  How do people manage this?
#   print('module __name__ (from perspective of importing program) =', __name__, end='\n\n')
#   # __name__ is just a string!

# I think the current reality is that, since AlgManip can now be found from my
# PYTHONPATH, I can use that full module path name for all internal modules as
# well.  And the AlgManip package module is only loaded once, regardless of
# which sub-modules are subsequently imported.
# If someone wants to put AlgManip in a place which is inaccessible from PYTHONPATH, then it may not work without some workaround as above.
# Note that local python programs such as Test.py can omit the AlgManip prefix, if they will be called from ./
# Though the modules that it calls' modules will still be accessed via the AlgManip package. (11jan023)


if True: # Maintain log of calling programs
  import os
  from datetime import date
  main = os.environ['_']
  cwd = os.getcwd() + '/'
  date = str(date.today())

  print(f'(from {main} running in {cwd} on {date})', end='\n\n')

  packageDir = os.path.dirname(__file__)
  logfile = open(packageDir+'/.usageLog', 'a')
#   logfile.write('\t'.join(('Date\t', 'Program\t\t\t', 'cwd'))+os.linesep)
  logfile.write('\t'.join((date, main, cwd))+os.linesep)
  logfile.close()

#   print('package module init file =', __file__)
#   # https://www.delftstack.com/howto/python/get-directory-from-path-in-python
#   print('package module directory =', os.path.dirname(__file__), end='\n\n')

#   print('dir() (names in current scope):', dir(), end='\n\n')

#   print(os.name)
#   print('cwd:', os.getcwd())
#   print(os.listdir())
#   print(*os.environ) (no idea why .keys() fails to list keys!)
#   print(os.environ['_'])

#   exit()

#   print('__dict__:', __dict__, end='\n\n')
#   print('__name__.__dict__:', __name__.__dict__, end='\n\n')
# neither the current scope nor the string object __name__ have a __dict__ attribute:
# global scope never has __dict__ it seems.  i.e. no one can ever use __dict__ as a local name.
# And __name__ is a string class.  dir() returns a class's methods, but classes implemented in C (such as the built-in class str) do not have a __dict__ attribute.
# https://stackoverflow.com/questions/9502183/python-why-is-dict-attribute-not-in-built-in-class-instances (29nov022)

# User defined classes, class instances and functions have __dict__ attribute:
# class junk: pass
#   print("empty class's __dict__ attribute:", junk.__dict__) # classes have __dict__attributes
#   print("empty class instance's __dict__ attribute:", junk().__dict__) # classes have __dict__attributes
#
# #   print(os.__dict__) # as do modules (but it is enormous for os)
#
#   def junkf(): pass
#   print("empty function's __dict__ attribute:", junkf.__dict__)

# TODO:
# ----
# * include hour?  time? (10jan023)
# * grab argument of python3? (10jan023)
# * count num entries? (10jan023)
