#!/usr/bin/env python

from distutils.core import setup
import py2exe

setup(name="RenPy",
      windows=[ dict(script="run_game.py",
                     icon_resources=[(1, "icon.ico")]) ],
      console=[ "archiver.py" ],
      zipfile='lib/renpy.zip',
      )
