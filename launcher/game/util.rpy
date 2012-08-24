# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python in util:
    import os
    
    def walk(directory, base=None):
        """
        Walks through the directories and files underneath `directory`, 
        yielding (name, isdir) tuples. The names are given relative to 
        `base`, which defaults to `directory` if None.
        """

        directory = renpy.fsdecode(directory)
        
        if base is None:
            base = directory
        else:
            base = renpy.fsdecode(base)
 
        for subdir, directories, files in os.walk(directory):
            for fn in directories:
                fullfn = os.path.join(subdir, fn)
                relfn = os.path.relpath(fullfn, base)
                
                relfn = relfn.replace("\\", "/")
                
                yield relfn, True

            for fn in files:
                fullfn = os.path.join(subdir, fn)
                relfn = os.path.relpath(fullfn, base)

                relfn = relfn.replace("\\", "/")
                
                yield relfn, False
    
