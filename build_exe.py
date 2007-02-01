#!/usr/bin/env python

from distutils.core import setup
import py2exe
import sys
import zipfile

sys.argv[1:] = [ 'py2exe', '--bundle', '2', '-a', '--dll-excludes', 'w9xpopen.exe' ]

setup(name="RenPy",
      windows=[ dict(script="renpy.py",
                     dest_base="renpy",
                     icon_resources=[ (0, "newicon.ico") ] ) ],
      
      console=[ dict(script="renpy.py", dest_base="console") ],

      zipfile='renpy.code',

      options={ 'py2exe' : { 'excludes' : [ 'doctest',
                                            'pygame.macosx',
                                            'pygame.surfarray',
                                            'pygame.mixer',
                                            'pygame.mixer_music',
                                            'Numeric',  ],
                             'optimize' : 2,
                             } },
      )


zfold = zipfile.ZipFile("dist/renpy.code")
zfnew = zipfile.ZipFile("renpy.code", "w", zipfile.ZIP_STORED)

seen = { }

for fn in zfold.namelist():
    if fn.startswith("renpy/"):
        continue

    if fn in seen:
        continue

    seen[fn] = True
    
    zfnew.writestr(fn, zfold.read(fn))

zfold.close()
zfnew.close()

print
print "Press return to quit."
raw_input()
