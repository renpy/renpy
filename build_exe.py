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

sys.argv[1:] = [ 'py2exe' ]

setup(name="RenPy",
      windows=programs,
      console=[ "archiver.py", "add_from.py", "console.py", "dump_text.py" ],
      zipfile='lib/renpy.zip',
      )
