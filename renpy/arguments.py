# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

# This file handles argument parsing. Argument parsing takes place in 
# two phases. In the first phase, we only parse the arguments that are
# necessary to load the game, and run the init phase. The init phase
# can register commands and arguments. These arguments are parsed at 
# the end of the init phase, before the game begins running, and can 
# decide if the game runs or some other action occurs.

import os
import argparse 
import renpy

# The argument parser we use.
parser = None

def create_parser():
    """
    Creates a parser, and adds an initial set of arguments to it.
    """
    
    global parser
    
    ap = parser = argparse.ArgumentParser()
    
    ap.add_argument(
        "--version", action='version', version=renpy.version,
        help="Displays the version of Ren'Py in use.")
    
    ap.add_argument(
        "basedir", default=None, nargs='?',
        help="The base directory."
        )
    
    ap.add_argument(
        "--gamedir", "--game", dest="gamedir", default=None,
        help="The path to the game directory.")
    
    ap.add_argument(
        "--savedir", dest='savedir', default=None,
        help="The directory where saves and persistent data are placed.")

    ap.add_argument(
        '--compile', dest='compile', default=False, action='store_true',
        help="If present, .rpy files to be compiled to .rpyc files whenever possible, before any command is run.")
    
    ap.add_argument(
        '--profile', dest='profile', action='store_true', default=False,
        help="If present, Ren'Py will report the amount of time it takes to draw the screen.")

    ap.add_argument(
        '--trace', dest='trace', action='count', default=0,
        help="If present, Ren'Py will log a function call trace to trace.txt. Supply this twice for a more detailed trace.")

    ap.add_argument(
        '--log-startup', dest='log_startup', action='store_true', default=os.environ.get("RENPY_LOG_STARTUP", None),
        help="If present, Ren'Py will log startup times to log.txt")

    ap.add_argument(
        "--log-image-cache", '--debug-image-cache', dest='debug_image_cache', action='store_true', default=False,
        help="If present, Ren'Py will log information regarding the contents of the image cache.")

#    ap.add_argument(
#        '--warp', dest='warp', default=None,
#        help='This takes as an argument a filename:linenumber pair, and tries to warp to the statement before that line number.')
#
#
#    op.add_option('--lint', dest='lint', default=False, action='store_true',
#                  help='Run a number of expensive tests, to try to detect errors in the script.')
#
#    op.add_option('--remote', dest='remote', action='store_true',
#                  help="Allows Ren'Py to be fed commands on stdin.")
#
#    op.add_option('--rmpersistent', dest='rmpersistent', action='store_true',
#                  help="Deletes the persistent data, and exits.")


def bootstrap():
    """
    Called during bootstrap to perform an initial parse of the arguments, ignoring
    unknown arguments. Returns the parsed arguments, and a list of unknown arguments.
    """
    
    create_parser()
    return parser.parse_known_args()

def pre_init():
    """
    Called before init, to set up argument parsing.
    """
    
    create_parser()
    
def post_init():
    """
    Called after init, but before the game starts. This parses a command
    and its arguments. It then runs the command function, and returns True
    if execution should continue and False otherwise. 
    """
    
    args = parser.parse_args()    
    renpy.game.args = args
    
    # TODO: Commands.
        