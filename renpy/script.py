# This file contains code that is responsible for storing and executing a
# Ren'Py script. 

import renpy.parser
import renpy.ast
import os
import cPickle

class ScriptError(Exception):
    """
    Exception that is raised if the script is somehow inconsistent,
    or otherwise wrong.
    """

class Script(object):
    """
    This class represents a Ren'Py script, which is parsed out of a
    collection of script files. Once parsing and initial analysis is
    complete, this object can be serialized out and loaded back in,
    so it shouldn't change at all after that has happened.

    @ivar namemap: A map from the name of an AST node to the AST node
    itself.  This is used for jumps, calls, and to find the current
    node when loading back in a save. The names may be strings or
    integers, strings being explicit names provided by the user, and
    integers being names synthesised by renpy.    

    @ivar initcode: A list of ASTs that should be run as the script
    is being initialized. (This is really a list of the first statements
    in init: blocks)

    """

    def __init__(self, files):
        """
        Loads the script by parsing all of the given files, and then
        walking the various ASTs to initialize this Script object.
        """

        self.namemap = { }
        self.initcode = [ ]

        for fn in files:
            self.load_file(fn)

        # Do some generic init here.

    def load_file(self, fn):

        stmts = renpy.parser.parse(fn)

        # All of the statements found in file, regardless of nesting
        # depth.
        all_stmts = [ ]

        def extend_all(block_list):
            all_stmts.extend(block_list)

            for i in block_list:
                extend_all(i.get_children())

        extend_all(stmts)

        # Chain together the statements in the file.
        renpy.ast.chain_block(stmts, None)

        # Check each node individually.
        for node in all_stmts:

            # Check to see if the name is defined twice. If it is,
            # report the error.
            name = node.name
            if name in self.namemap:
                old = namemap[name]

                raise ScriptError("Name %s is defined twice: at %s:%d and %s:%d." %
                                  (repr(name),
                                   old.filename, old.linenumber,
                                   node.filename, node.linenumber))

            # Otherwise, add the name to the namemap. 
            self.namemap[name] = node

            # Add any init nodes to self.initcode.
            init = node.get_init()
            if init:
                self.initcode.append(init)

    def lookup(self, label):
        """
        Looks up the given label in the game. If the label is not found,
        raises a ScriptError.
        """

        if label not in self.namemap:
            raise ScriptError("could not find label '%s'." % label)

        return self.namemap[label]

    def has_label(self, label):
        """
        Returns true if the label exists, or false otherwise.
        """

        return label in self.namemap

def load_script(dir):
    files = os.listdir(dir)        
    files = [ dir + '/' + f for f in files if f.endswith(".rpy") ]

    if files:
        rv = Script(files)
        pscript = cPickle.dumps(rv, cPickle.HIGHEST_PROTOCOL).encode("zlib")

        f = file(dir + "/script", "w")
        f.write(pscript)
        f.close()

        return rv
    
    else:

        f = file(dir + "/script", "r")
        rv = cPickle.loads(f.read().decode("zlib"))
        f.close()

        return rv

