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

# This file contains code to write the reflect.json file. This file contains
# information about the game that's used to reflect on the contents,
# including how to navigate around the game.

import inspect
import json
import sys
import os

import renpy


# A list of (name, filename, linenumber) tuples, for various types of 
# name. These are added to as the definitions occur.
definitions = [ ]
transforms = [ ]
screens = [ ]


# Does a file exist? We cache the result here.
file_exists_cache = { }

def file_exists(fn):
    rv = file_exists_cache.get(fn, None)

    if rv is None:
        fullfn = renpy.parser.unelide_filename(fn)
        
        rv = os.path.exists(fullfn)
        file_exists_cache[fn] = rv
        
    return rv


def command():
    ap = renpy.arguments.ArgumentParser(description="Dumps information about the game to a JSON file.")
    
    ap.add_argument("filename", action="store", default=None, nargs="?", help="The filename to write the information to. If left blank, stdout will be used.")
    ap.add_argument("--private", action="store_true", default=False, help="Include private names. (Names beginning with _.)")
    ap.add_argument("--common", action="store_true", default=False, help="Include names found in the common directory.")
    
    args = ap.parse_args()
    
    def filter(name, filename): #@ReservedAssignment
        """
        Returns true if the name is included by the filter, or false if it is excluded.
        """
        
        if name.startswith("_") and not args.private:
            return False

        if not file_exists(filename):
            return False
        
        if filename.startswith("common/"):
            return args.common
        
        if not filename.startswith("game/"):
            return False
        
        return True

    result = { }
    
    # The JSON object we return.   
    location = { }
    result["location"] = location

    # Labels.
    label = location["label"] = { }
    
    for name, n in renpy.game.script.namemap.iteritems():
        filename = n.filename
        line = n.linenumber
        
        if not isinstance(name, basestring):
            continue

        if not filter(name, filename):
            continue
        
        label[name] = [ filename, line ]
        
        
    # Definitions.
    define = location["define"] = { }
    
    for name, filename, line in definitions:
        if not filter(name, filename):
            continue
        
        define[name] = [ filename, line ]

    # Screens.
    screen = location["screen"] = { }
    
    for name, filename, line in screens:
        if not filter(name, filename):
            continue
        
        screen[name] = [ filename, line ]

    # Transforms.
    transform = location["transform"] = { }
    
    for name, filename, line in transforms:
        if not filter(name, filename):
            continue
        
        transform[name] = [ filename, line ]
        
        
    # Code.
    code = location["code"] = { }
        
    for name, o in inspect.getmembers(renpy.store):
        
        if inspect.isclass(o) or inspect.isfunction(o):
            try:
                filename = inspect.getfile(o)
                _lines, line = inspect.getsourcelines(o)
            except:
                pass
            
            if not filter(name, filename):
                continue
            
            code[name] = [ filename, line ]
        
    if args.filename is not None:
        with file(args.filename, "w") as f:
            json.dump(result, f)
    else:
        json.dump(result, sys.stdout, indent=2)
        
    
