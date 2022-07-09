print('Importing AlgManip python package module')

if 1:
  # from os import getcwd
  import os
  from datetime import date
  cwd = os.getcwd()
  date = date.today()

  print(f'(from {cwd} on {date})')

a  print('module init file =', __file__)
  # https://www.delftstack.com/howto/python/get-directory-from-path-in-python
  print('module dir =', os.path.dirname(__file__))

  print('module name =', __name__)
