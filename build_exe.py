#!/usr/bin/env python

from distutils.core import setup
import py2exe
import sys

sys.argv[1:] = [ 'py2exe', '--bundle', '2', '-x', '-a', '--dll-excludes', 'w9xpopen.exe' ]

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

print
print "Press return to quit."
raw_input()
