#!/usr/bin/env python

from distutils.core import setup
import py2exe

setup(name="RenPy",
      windows=[ "run_game.py" ],
      console=[ "archiver.py" ],
      zipfile='lib/renpy.zip',
      )
