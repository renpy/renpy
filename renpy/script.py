# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import os
import imp
import difflib
import md5
import time
import marshal

from cPickle import loads, dumps

# The version of the dumped script.
script_version = renpy.script_version

# The version of the bytecode cache.
BYTECODE_VERSION = 1

# The python magic code.
MAGIC = imp.get_magic()

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
        for i in block_list:
            all_stmts.append(i)
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

        # Set us up as renpy.game.script, so things can use us while
        # we're loading.
        renpy.game.script = self

        if os.path.exists(renpy.config.renpy_base + "/lock.txt"):
            self.key = file(renpy.config.renpy_base + "/lock.txt", "rb").read()
        else:
            self.key = None

        self.namemap = { }
        self.all_stmts = [ ]
        self.all_pycode = [ ]
        self.record_pycode = True

        # Bytecode caches.
        self.bytecode_oldcache = { }
        self.bytecode_newcache = { }
        self.bytecode_dirty = False

        self.translator = renpy.translation.ScriptTranslator()

        self.init_bytecode()
        self.scan_script_files()

        self.translator.chain_translates()

        self.serial = 0

    def scan_script_files(self):
        """
        Scan the directories for script files.
        """

        # A list of all files in the search directories.
        dirlist = renpy.loader.listdirfiles()

        # A list of directory, filename w/o extension pairs. This is
        # what we will load immediately.
        self.script_files = [ ]

        # Similar, but for modules:
        self.module_files = [ ]

        for dir, fn in dirlist: #@ReservedAssignment

            if fn.endswith(".rpy"):
                if dir is None:
                    continue

                fn = fn[:-4]
                target = self.script_files
            elif fn.endswith(".rpyc"):
                fn = fn[:-5]
                target = self.script_files
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

    def load_script(self):

        script_files = self.script_files

        # Sort script files by filename.
        script_files.sort()

        initcode = [ ]

        for fn, dir in script_files: #@ReservedAssignment
            self.load_appropriate_file(".rpyc", ".rpy", dir, fn, initcode)

        # Make the sort stable.
        initcode = [ (prio, index, code) for index, (prio, code) in
                     enumerate(initcode) ]

        initcode.sort()

        self.initcode = [ (prio, code) for prio, index, code in initcode ]


    def load_module(self, name):

        files = [ (fn, dir) for fn, dir in self.module_files if fn == name ] #@ReservedAssignment

        if not files:
            raise Exception("Module %s could not be loaded." % name)

        if len(files) > 2:
            raise Exception("Module %s ambiguous, multiple variants exist." % name)

        fn, dir = files[0] #@ReservedAssignment
        initcode = [ ]

        self.load_appropriate_file(".rpymc", ".rpym", dir, fn, initcode)

        if renpy.parser.report_parse_errors():
            raise SystemExit(-1)

        self.translator.chain_translates()

        return initcode

    def assign_names(self, stmts, fn):
        # Assign names to statements that don't have one already.

        all_stmts = collapse_stmts(stmts)

        version = int(time.time())

        for s in all_stmts:
            if s.name is None:
                s.name = (fn, version, self.serial)
                self.serial += 1


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

    def load_file_core(self, dir, fn): #@ReservedAssignment

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
                self.record_pycode = False
                old_data, old_stmts = self.load_file_core(dir, fn + "c")
                self.merge_names(old_stmts, stmts)
                del old_data
                del old_stmts
            except:
                pass
            finally:
                self.record_pycode = True

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

    def load_file(self, dir, fn, initcode): #@ReservedAssignment

        # Actually do the loading.
        data, stmts = self.load_file_core(dir, fn)
        if data is None:
            return False

        # Check the key.
        if self.key is None:
            self.key = data['key']
        elif self.key != data['key']:
            raise Exception( fn + " does not share a key with at least one .rpyc file. To fix, delete all .rpyc files, or rerun Ren'Py with the --lock option.")

        self.finish_load(stmts, initcode)
        return True

    def load_string(self, filename, filedata):
        """
        Loads Ren'Py script from a string.

        `filename`
            The filename that's assigned to the data.

        `filedata`
            A unicode string to be loaded.

        Return the list of statements making up the root block, and a
        list of init statements that need to be run.
        """

        stmts = renpy.parser.parse(filename, filedata)

        if stmts is None:
            return None, None

        self.assign_names(stmts, filename)

        initcode = [ ]
        stmts = self.finish_load(stmts, initcode, False)

        return stmts, initcode


    def finish_load(self, stmts, initcode, check_names=True):
        """
        Given `stmts`, a list of AST nodes comprising the root block,
        finishes loading it (this includes chaining statements and
        adding them to the name map.)

        `initcode`
            A list we append init statements to.

        `check_names`
            If true, produce duplicate name errors.

        Returns a list of statements that corresponds to the top-level block
        in initcode after transformation.
        """

        # Generate translate nodes.
        renpy.translation.restructure(stmts)

        # All of the statements found in file, regardless of nesting
        # depth.
        all_stmts = collapse_stmts(stmts)

        # Take the translations.
        self.translator.take_translates(all_stmts)

        # Chain together the statements in the file.
        renpy.ast.chain_block(stmts, None)

        # Check each node individually.
        for node in all_stmts:

            # Check to see if the name is defined twice. If it is,
            # report the error.
            name = node.name

            if name in self.namemap and check_names:
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

        # Compile bytecode from the file.
        self.update_bytecode()

        # Exec early python.
        for node in all_stmts:
            node.early_execute()

        if self.all_stmts is not None:
            self.all_stmts.extend(all_stmts)

        return stmts

    def load_appropriate_file(self, compiled, source, dir, fn, initcode): #@ReservedAssignment
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

            if rpydigest == rpycdigest and renpy.game.args.command != "compile": #@UndefinedVariable

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

        # Update all of the PyCode objects in the system with the loaded
        # bytecode.
        for i in self.all_pycode:

            key = i.get_hash() + MAGIC

            code = self.bytecode_oldcache.get(key, None)

            if code is None:

                self.bytecode_dirty = True

                old_ei = renpy.game.exception_info
                renpy.game.exception_info = "While compiling python block starting at line %d of %s." % (i.location[1], i.location[0])

                try:

                    if i.mode == 'exec':
                        code = renpy.python.py_compile_exec_bytecode(i.source, filename=i.location[0], lineno=i.location[1])
                    elif i.mode == 'eval':
                        code = renpy.python.py_compile_eval_bytecode(i.source, filename=i.location[0], lineno=i.location[1])

                except SyntaxError, e:

                    text = e.text

                    if text is None:
                        text = ''

                    try:
                        text = text.decode("utf-8")
                    except:
                        text = text.decode("latin-1")

                    pem = renpy.parser.ParseError(
                        filename = e.filename,
                        number = e.lineno,
                        msg = e.msg,
                        line = text,
                        pos = e.offset)

                    renpy.parser.parse_errors.append(pem.message)

                    continue

                renpy.game.exception_info = old_ei

            i.source = None
            self.bytecode_newcache[key] = code
            i.bytecode = marshal.loads(code)

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
