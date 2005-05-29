# This file contains code that is responsible for storing and executing a
# Ren'Py script. 

import renpy

import os.path
import os

from pickle import loads, dumps

# The version of the dumped script.
script_version = renpy.script_version

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

    @ivar all_stmts: A list of all statements, that have been found
    in every file. Useful for lint, but tossed if lint is not performed
    to save memory.

    """

    def __init__(self, node_callback=None):
        """
        Loads the script by parsing all of the given files, and then
        walking the various ASTs to initialize this Script object.
        """

        self.namemap = { }
        self.initcode = [ ]
        self.all_stmts = [ ]
        
        # A list of all files in the search directories.
        dirlist = [ ]

        for dirname in renpy.config.searchpath:
            for fn in os.listdir(dirname):
                dirlist.append(dirname + "/" + fn)

        # Files to ensure (because they are the alts of files that
        # have been processed.)
        ignore = [ ]

        for fn in dirlist:

            if not (fn.endswith('.rpyc') or fn.endswith('.rpy')):
                continue

            if fn in ignore:
                continue

            if fn[-1] == 'c':
                alt = fn[:-1]
            else:
                alt = fn + 'c'

            if os.path.exists(alt):
                fntime = os.stat(fn).st_mtime
                alttime = os.stat(alt).st_mtime

                if alttime > fntime:
                    continue

            ignore.append(alt)

            # print "Loading", fn

            if self.load_file(fn, node_callback):
                continue

            print "Couldn't load %s, trying %s instead." % (fn, alt)

            if self.load_file(alt, node_callback):
                continue

            raise Exception("Could not load %s or %s." % (fn, alt))
            

        # Make the sort stable.
        initcode = [ (prio, index, code) for index, (prio, code) in
                     enumerate(self.initcode) ]
                     
        initcode.sort()
        
        self.initcode = [ (prio, code) for prio, index, code in initcode ]



        # Do some generic init here.

    def load_file(self, fn, node_callback):

        if fn.endswith(".rpy"):
            stmts = renpy.parser.parse(fn)
            f = file(fn + "c", "wb")
            f.write(dumps((script_version, stmts), -1).encode('zlib'))
            f.close()
        elif fn.endswith(".rpyc"):
            f = file(fn, "rb")

            try:
                version, stmts = loads(f.read().decode('zlib'))
            except ValueError:
                return False

            if version != script_version:
                return False
            
            f.close()
        else:
            return False

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

            if node_callback:
                node_callback(node)

            # Check to see if the name is defined twice. If it is,
            # report the error.
            name = node.name
            if name in self.namemap:
                old = self.namemap[name]

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

        self.all_stmts.extend(all_stmts)

        return True

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

def load_script():
    rv = Script()
    return rv
    

