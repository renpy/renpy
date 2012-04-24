#!/usr/bin/env renpython
#@PydevCodeAnalysisIgnore

import renpy
import renpy.subprocess
version = renpy.version[7:]

import sys
if "retag" in sys.argv[1:]:
    renpy.subprocess.call([ "bzr", "tag", "--delete", version ])
    
renpy.subprocess.call([ "bzr", "tag", version ])
    

