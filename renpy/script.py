# This file contains code that is responsible for storing and executing a
# Ren'Py script. 

import renpy

import os.path
import os

from cPickle import loads, dumps

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

    @ivar initcode: A list of priority, Node tuples that should be
    executed in ascending priority order at init time.

    """

    def __init__(self, dir):
        """
        Loads the script by parsing all of the given files, and then
        walking the various ASTs to initialize this Script object.
        """

        self.namemap = { }
        self.initcode = [ ]

        # Find the script files to load.
        for fn in os.listdir(dir):
            if not (fn.endswith('.rpyc') or fn.endswith('.rpy')):
                continue

            fn = dir + '/' +  fn

            if fn[-1] == 'c':
                alt = fn[:-1]
            else:
                alt = fn + 'c'

            if os.path.exists(alt):
                fntime = os.stat(fn).st_mtime
                alttime = os.stat(alt).st_mtime

                if alttime > fntime:
                    continue

            self.load_file(fn)
            

        self.initcode.sort()

        # Do some generic init here.

    def load_file(self, fn):

        if fn.endswith(".rpy"):
            stmts = renpy.parser.parse(fn)
            f = file(fn + "c", "wb")
            f.write(dumps(stmts).encode('zlib'))
            f.close()
        elif fn.endswith(".rpyc"):
            f = file(fn, "rb")
            stmts = loads(f.read().decode('zlib'))
            f.close()
        else:
            assert False            

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
            raise ScriptError("could not find label '%s'." % str(label))

        return self.namemap[label]

    def has_label(self, label):
        """
        Returns true if the label exists, or false otherwise.
        """

        return label in self.namemap

def load_script(dir):

    rv = Script(dir)
    return rv
    

