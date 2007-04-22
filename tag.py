#!/usr/bin/env renpython

import renpy
import renpy.subprocess
version = renpy.version[7:]

renpy.subprocess.call([ "svn", "copy", ".",  'http://www.bishoujo.us/svn/renpy/tags/' + version, "-m", "Tagging " + version ])
