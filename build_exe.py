#!/usr/bin/env python

from distutils.core import setup
import py2exe
import sys

if len(sys.argv) != 2:
    print "Usage: build_exe.py <prefix>"
    print ""
    print "Builds <prefix>.exe."
    print "Expects icons in <prefix>.ico."

    sys.exit(-1)

def program(name):
    return dict(script="run_game.py",
                icon_resources=[ (0, name + ".ico"),
                                 ],
                dest_base=name)

programs = [
    program(sys.argv[1]),
    ]

sys.argv[1:] = [ 'py2exe', '--bundle', '1', '-x', '-a', '--dll-excludes', 'w9xpopen.exe' ]

setup(name="RenPy",
      windows=programs,
      console=[ "console.py" ],
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
