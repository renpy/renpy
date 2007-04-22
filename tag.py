#!/usr/bin/env renpython

import renpy
import renpy.subprocess
version = renpy.version[7:]

import sys
if "retag" in sys.argv[1:]:
    renpy.subprocess.call([ "svn", "rm",  'http://www.bishoujo.us/svn/renpy/tags/' + version, "-m", "Tagging " + version ])
    

renpy.subprocess.call([ "svn", "copy", ".",  'http://www.bishoujo.us/svn/renpy/tags/' + version, "-m", "Tagging " + version ])
