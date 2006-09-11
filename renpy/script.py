# This file contains code that is responsible for storing and executing a
# Ren'Py script. 

import renpy

import os.path
import os
import imp
import difflib

from pickle import loads, dumps

# The version of the dumped script.
script_version = renpy.script_version

class ScriptError(Exception):
    """
    Exception that is raised if the script is somehow inconsistent,
    or otherwise wrong.
    """

def collapse_stmts(stmts):
    """
    Returns a flat list containing every statement in the tree
    stmts.
    """

    all_stmts = [ ]

    def extend_all(block_list):
        all_stmts.extend(block_list)

        for i in block_list:
            extend_all(i.get_children())

    extend_all(stmts)

    return all_stmts


    

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

        self.key = None

        self.namemap = { }
        self.initcode = [ ]
        self.all_stmts = [ ]
        self.all_pycode = [ ]
        
        # A list of all files in the search directories.
        dirlist = renpy.loader.listdirfiles()

#         for dirname in renpy.config.searchpath:
#             for fn in os.listdir(dirname):
#                 dirlist.append(dirname + "/" + fn)

        # Files to ensure (because they are the alts of files that
        # have been processed.)
        ignore = [ ]

        for dir, fn in dirlist:

            if not (fn.endswith('.rpyc') or fn.endswith('.rpy')):
                continue

            if fn in ignore:
                continue

            if fn[-1] == 'c':
                alt = fn[:-1]
            else:
                alt = fn + 'c'

            if dir:
                fullfn = dir + "/" + fn
                fullalt = dir + "/" + alt

                if os.path.exists(fullfn) and os.path.exists(fullalt):
                    fntime = os.stat(fullfn).st_mtime
                    alttime = os.stat(fullalt).st_mtime

                    if alttime > fntime:
                        continue

            ignore.append(alt)

            # print "Loading", fn

            if self.load_file(dir, fn, node_callback):
                continue

            print "Couldn't load %s, trying %s instead." % (fn, alt)

            if self.load_file(dir, alt, node_callback):
                continue

            raise Exception("Could not load %s or %s." % (fn, alt))
            

        # Make the sort stable.
        initcode = [ (prio, index, code) for index, (prio, code) in
                     enumerate(self.initcode) ]
                     
        initcode.sort()
        
        self.initcode = [ (prio, code) for prio, index, code in initcode ]

        # Ensure that all of the python code found in the script has been
        # compiled into bytecode.
        self.update_bytecode()

        # Do some generic init here.

    def assign_names(self, stmts, fn):
        # Assign names to statements that don't have one already.

        all_stmts = collapse_stmts(stmts)

        version = int(os.stat(fn).st_mtime)
        serial = 0

        for s in all_stmts:
            if s.name is None:
                s.name = (fn, version, serial)
                serial += 1


    def merge_names(self, old_stmts, new_stmts):

        old_stmts = collapse_stmts(old_stmts)
        new_stmts = collapse_stmts(new_stmts)

        old_info = [ i.diff_info() for i in old_stmts ]
        new_info = [ i.diff_info() for i in new_stmts ]

        sm = difflib.SequenceMatcher(None, old_info, new_info)

        for oldl, newl, count in sm.get_matching_blocks():
            for i in range(count):
                old = old_stmts[oldl + i]
                new = new_stmts[newl + i]

                if new.name is None:
                    new.name = old.name

    def load_file_core(self, dir, fn):
        
        if fn.endswith(".rpy"):

            if not dir:
                raise Exception("Cannot load rpy file %s from inside an archive." % fn) 

            fullfn = dir + "/" + fn

            stmts = renpy.parser.parse(fullfn)

            data = { }
            data['version'] = script_version
            data['key'] = renpy.game.options.lock or 'unlocked'


            # See if we have a corresponding .rpyc file. If so, then
            # we want to try to upgrade our .rpy file with it.
            try:
                old_data, old_stmts = self.load_file_core(dir, fn + "c")
                self.merge_names(old_stmts, stmts)
                del old_stmts
            except:
                pass

            self.assign_names(stmts, fullfn)

            try:
                f = file(dir + "/" + fn + "c", "wb")
                f.write(dumps((data, stmts), 2).encode('zlib'))
                f.close()
            except:
                pass

        elif fn.endswith(".rpyc"):

            # When locking, regenerate all files.
            if renpy.game.options.lock:
                return None, None
            
            f = renpy.loader.load(fn)

            try:
                data, stmts = loads(f.read().decode('zlib'))
            except:
                raise
                return None, None

            if not isinstance(data, dict):
                return None, None

            if data['version'] != script_version:
                return None, None

            f.close()
        else:
            return None, None

        return data, stmts



    def load_file(self, dir, fn, node_callback):


        # Actually do the loading.
        data, stmts = self.load_file_core(dir, fn)
        if data is None:
            return False

        # Check the key.
        if self.key is None:
            self.key = data['key']
        elif self.key != data['key']:
            raise Exception( fn + " does not share a key with at least one .rpyc file. To fix, delete all .rpyc files, or rerun Ren'Py with the --lock option.")
            

        # All of the statements found in file, regardless of nesting
        # depth.
        all_stmts = collapse_stmts(stmts)

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

            # Add any PyCode to all_pycode.
            self.all_pycode.extend(node.get_pycode())

        self.all_stmts.extend(all_stmts)

        return True

    def update_bytecode(self):
        """
        Updates the bytecode for all the bytecode objects in renpy.PyCode.extent.
        """

        VERSION = 1

        oldcache = { }
        newcache = { }
        magic = imp.get_magic()
        dirty = False

        # Load the oldcache.
        try:
            version, cache = loads(renpy.loader.load("bytecode.rpyb").read().decode("zlib"))
            if version == VERSION:
                oldcache = cache
        except:
            pass

        # Update all of the PyCode objects in the system with the loaded
        # bytecode.
        for i in self.all_pycode:

            codes = oldcache.get(i.location, { })

            if magic in codes:
                code = codes[magic]
                
            else:

                dirty = True
                
                old_ei = renpy.game.exception_info
                renpy.game.exception_info = "While compiling python block starting at line %d of %s." % (i.location[1], i.location[0])

                if i.mode == 'exec':
                    code = renpy.python.py_compile_exec_bytecode(i.source, filename=i.location[0], lineno=i.location[1])
                elif i.mode == 'eval':
                    code = renpy.python.py_compile_eval_bytecode(i.source, filename=i.location[0], lineno=i.location[1])

                renpy.game.exception_info = old_ei
                codes[magic] = code


            i.source = None
            i.bytecode = code
            newcache[i.location] = codes


        if dirty:
            try:
                data = (VERSION, newcache)
                f = file(os.path.join(renpy.config.searchpath[0], "bytecode.rpyb"), "w")
                f.write(dumps(data, 2).encode("zlib"))
                f.close()
            except:
                pass

        self.all_pycode = None
        

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
    

