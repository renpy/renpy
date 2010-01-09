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

# This file contains code that is responsible for storing and executing a
# Ren'Py script. 

import renpy

import os.path
import os
import imp
import difflib
import md5
import time

from cPickle import loads, dumps

# The version of the dumped script.
script_version = renpy.script_version

# The version of the bytecode cache.
BYTECODE_VERSION = 1

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

    def __init__(self):
        """
        Loads the script by parsing all of the given files, and then
        walking the various ASTs to initialize this Script object.
        """

        # A key that's used to lock the script file, should that
        # prove necessary.
        self.key = renpy.game.options.lock

        if self.key is None:
            if os.path.exists(renpy.config.renpy_base + "/lock.txt"):
                self.key = file(renpy.config.renpy_base + "/lock.txt", "rb").read()

        self.namemap = { }
        self.all_stmts = [ ]
        self.all_pycode = [ ]

        # Bytecode caches.
        self.bytecode_oldcache = { }
        self.bytecode_newcache = { }
        self.bytecode_dirty = False

        # Init the bytecode compiler.
        self.init_bytecode()
        
        # A list of all files in the search directories.
        dirlist = renpy.loader.listdirfiles()

        # A list of directory, filename w/o extension pairs. This is
        # what we will load immediately.
        script_files = [ ]

        # Similar, but for modules:
        self.module_files = [ ]
        
        for dir, fn in dirlist:

            if fn.endswith(".rpy"):
                if dir is None:
                    continue

                fn = fn[:-4]
                target = script_files
            elif fn.endswith(".rpyc"):
                fn = fn[:-5]
                target = script_files
            elif fn.endswith(".rpym"):
                if dir is None:
                    continue

                fn = fn[:-5]
                target = self.module_files
            elif fn.endswith(".rpymc"):
                fn = fn[:-6]
                target = self.module_files
            else:
                continue
                
            if (fn, dir) not in target:
                target.append((fn, dir))

                
        # Sort script files by filename.
        script_files.sort()

        initcode = [ ]
        
        for fn, dir in script_files:
            self.load_appropriate_file(".rpyc", ".rpy", dir, fn, initcode)

        # Make the sort stable.
        initcode = [ (prio, index, code) for index, (prio, code) in
                     enumerate(initcode) ]
                     
        initcode.sort()
        
        self.initcode = [ (prio, code) for prio, index, code in initcode ]


    def load_module(self, name):

        files = [ (fn, dir) for fn, dir in self.module_files if fn == name ]

        if not files:
            raise Exception("Module %s could not be loaded." % name)

        if len(files) > 2:
            raise Exception("Module %s ambiguous, multiple variants exist." % name)

        fn, dir = files[0]
        initcode = [ ]

        self.load_appropriate_file(".rpymc", ".rpym", dir, fn, initcode)

        if renpy.parser.report_parse_errors():
            raise SystemExit(-1)
        
        return initcode
        
    def assign_names(self, stmts, fn):
        # Assign names to statements that don't have one already.

        all_stmts = collapse_stmts(stmts)

        version = int(time.time())
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
        
        if fn.endswith(".rpy") or fn.endswith(".rpym"):

            if not dir:
                raise Exception("Cannot load rpy/rpym file %s from inside an archive." % fn) 

            fullfn = dir + "/" + fn

            stmts = renpy.parser.parse(fullfn)
            
            data = { }
            data['version'] = script_version
            data['key'] = self.key or 'unlocked'

            if stmts is None:
                return data, [ ]

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
                rpydigest = md5.md5(file(fullfn, "rU").read()).digest()
                f = file(dir + "/" + fn + "c", "wb")
                f.write(dumps((data, stmts), 2).encode('zlib'))
                f.write(rpydigest)
                f.close()
            except:
                pass

        elif fn.endswith(".rpyc") or fn.endswith(".rpymc"):

            f = renpy.loader.load(fn)

            try:
                data, stmts = loads(f.read().decode('zlib'))
            except:
                raise
            
            if not isinstance(data, dict):
                return None, None

            if self.key and data.get('key', 'unlocked') != self.key:
                return None, None
            
            if data['version'] != script_version:
                return None, None

            f.close()
        else:
            return None, None

        return data, stmts



    def load_file(self, dir, fn, initcode):


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

        early = [ ]
        
        # Check each node individually.
        for node in all_stmts:

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
                initcode.append(init)

            # Add any PyCode to all_pycode.
            self.all_pycode.extend(node.get_pycode())

            if isinstance(node, renpy.ast.EarlyPython):
                early.append(node)
            
        # Compile bytecode from the file.
        self.update_bytecode()

        # Exec early python.
        for node in early:
            node.early_execute()
        
        self.all_stmts.extend(all_stmts)

        return True

    
    def load_appropriate_file(self, compiled, source, dir, fn, initcode):
        # This can only be a .rpyc file, since we're loading it
        # from an archive.
        if dir is None:
            if not self.load_file(dir, fn + compiled, initcode):
                raise Exception("Could not load from archive %s.%s" % (fn, compiled))
            return
            
        # Otherwise, we're loading from disk. So we need to decide if
        # we want to load the rpy or the rpyc file.
        rpyfn = dir + "/" + fn + source
        rpycfn = dir + "/" + fn + compiled

        if os.path.exists(rpyfn) and os.path.exists(rpycfn):
            rpydigest = md5.md5(file(rpyfn, "rU").read()).digest()
            f = file(rpycfn, "rb")
            f.seek(-md5.digest_size, 2)
            rpycdigest = f.read(md5.digest_size)
            f.close()

            if rpydigest == rpycdigest and not renpy.game.options.compile:

                if self.load_file(dir, fn + compiled, initcode):
                    return

                print "Could not load " + rpycfn

            if not self.load_file(dir, fn + source, initcode):
                raise Exception("Could not load file %s." % rpyfn) 

        elif os.path.exists(rpycfn):
            if not self.load_file(dir, fn + compiled, initcode):
                raise Exception("Could not load file %s." % rpycfn) 

        elif os.path.exists(rpyfn):
            if not self.load_file(dir, fn + source, initcode):
                raise Exception("Could not load file %s." % rpyfn) 
        
    
    def init_bytecode(self):
        """
        Init/Loads the bytecode cache.
        """

        # Load the oldcache.
        try:
            version, cache = loads(renpy.loader.load("bytecode.rpyb").read().decode("zlib"))
            if version == BYTECODE_VERSION:
                self.bytecode_oldcache = cache
        except:
            pass

        
    def update_bytecode(self):
        """
        Compiles the PyCode objects in self.all_pycode, updating the
        cache. Clears out self.all_pycode.
        """
        
        magic = imp.get_magic()
        
        # Update all of the PyCode objects in the system with the loaded
        # bytecode.
        for i in self.all_pycode:

            codes = self.bytecode_oldcache.get(i.location, { })

            if magic in codes:
                code = codes[magic]
                
            else:

                self.bytecode_dirty = True
                
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
            self.bytecode_newcache[i.location] = codes

        self.all_pycode = [ ]


    def save_bytecode(self):
        
        if self.bytecode_dirty:
            try:
                data = (BYTECODE_VERSION, self.bytecode_newcache)
                f = file(os.path.join(renpy.config.searchpath[0], "bytecode.rpyb"), "wb")
                f.write(dumps(data, 2).encode("zlib"))
                f.close()
            except:
                pass

        

    def lookup(self, label):
        """
        Looks up the given label in the game. If the label is not found,
        raises a ScriptError.
        """

        label = renpy.config.label_overrides.get(label, label)
        
        if label not in self.namemap:
            raise ScriptError("could not find label '%s'." % str(label))

        return self.namemap[label]

    def has_label(self, label):
        """
        Returns true if the label exists, or false otherwise.
        """

        label = renpy.config.label_overrides.get(label, label)

        return label in self.namemap

def load_script():
    rv = Script()
    return rv
    

