# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file is responsible for running the Ren'Py remote control interface,
# which consists of reading commands off of standard input, and executing 
# them. When --remote is given to Ren'Py, the remote function is called once
# in a while, either by an underlay or by the error display.

# The following commands are supported:
#
# warp <file>:<line>
# Warps to the given filename and line number, like with the --warp
# command line option.
#
# quit
# Causes Ren'Py to quit entirely.
#
# Empty lines are ignored. (This lets us clear out outstanding errors.)

import renpy
import os
import os.path

commandfile = "command.%d.txt" % os.getpid()

def remote():
    
    if not os.path.exists(commandfile):
        return 

    cmd = file(commandfile, "r").readline()
    cmd = cmd.replace("\n", "").replace("\r", "")

    os.unlink(commandfile)
    
    # Break it up into parts.
    if " " in cmd:
        cmd, arg = cmd.split(" ", 1)
    else:
        arg = ""
    
    # Deal with commands.
    if cmd == "":
        return

    elif cmd == "warp":
        renpy.game.options.warp = arg
        raise renpy.game.UtterRestartException()
    
    elif cmd == "quit":
        raise renpy.game.QuitException()
        
    else:
        print "Unknown command:", cmd
        
    
        
