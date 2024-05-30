# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy

import __future__
import collections
import hashlib
import os
import difflib
import time
import marshal
import struct
import zlib
import sys

from renpy.compat.pickle import loads, dumps
import shutil

# The version of the dumped script.
script_version = renpy.script_version

# The version of the bytecode cache.
BYTECODE_VERSION = 1

# The python magic code.
if PY2:
    import heapq
    import imp
    MAGIC = imp.get_magic()

    # Change this to force a recompile when required.
    MAGIC += b'_v2.1'

else:
    from importlib.util import MAGIC_NUMBER as MAGIC

    # Change this to force a recompile when required.
    MAGIC += b'_v3.1'

# A string at the start of each rpycv2 file.
RPYC2_HEADER = b"RENPY RPC2"


# The name of the obsolete and new bytecode cache files.
OLD_BYTECODE_FILE = "cache/bytecode.rpyb"
BYTECODE_FILE = "cache/bytecode-{}{}.rpyb".format(sys.version_info.major, sys.version_info.minor)


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

    rv = [ ]

    for i in stmts:
        i.get_children(rv.append)

    return rv


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
            with open(renpy.config.renpy_base + "/lock.txt", "rb") as f:
                self.key = f.read()
        else:
            self.key = None

        self.namemap = { }
        self.all_stmts = [ ]
        self.all_pycode = [ ]
        self.all_pyexpr = [ ]

        # A list of statements that haven't been analyzed.
        self.need_analysis = [ ]

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

        self.digest = hashlib.md5(renpy.version_only.encode("utf-8"))

        self.loaded_rpy = False
        self.backup_list = [ ]

        self.duplicate_labels = [ ]

        # A list of initcode, priority, statement pairs.
        self.initcode = [ ]

        # A set of (fn, dir) tuples for scripts that have already been
        # loaded.
        self.loaded_scripts = set()

        # A set of languages to load.
        self.load_languages = set()

    def choose_backupdir(self):

        if renpy.mobile:
            return None

        for i in [ "script_version.txt", "script_version.rpy", "script_version.rpyc" ]:
            if renpy.loader.loadable(i):
                return None

        backups = renpy.__main__.path_to_saves(renpy.config.gamedir, "backups") # @UndefinedVariable

        if backups is None:
            return

        basename = os.path.basename(renpy.config.basedir)
        backupdir = renpy.os.path.join(renpy.exports.fsencode(backups),
                                       renpy.exports.fsencode(basename))

        renpy.exports.write_log("Backing up script files to %r:", backupdir)

        return backupdir

    def make_backups(self):

        backup_list = self.backup_list
        self.backup_list = [ ]

        if os.environ.get("RENPY_DISABLE_BACKUPS", "") == "I take responsibility for this.":
            return

        if not self.loaded_rpy:
            return

        if renpy.mobile:
            return

        backupdir = self.choose_backupdir()
        if backupdir is None:
            return

        for fn, checksum in backup_list:

            if not fn.startswith(renpy.config.gamedir):
                continue

            if not os.path.exists(fn):
                continue

            short_fn = renpy.exports.fsencode(fn[len(renpy.config.gamedir) + 1:])

            base, ext = os.path.splitext(short_fn)

            if PY2:
                hex_checksum = checksum[:8].encode("hex")
            else:
                hex_checksum = checksum[:8].hex()

            target_fn = os.path.join(
                backupdir,
                base + "." + hex_checksum + ext,
                )

            if os.path.exists(target_fn):
                continue

            try:
                os.makedirs(os.path.dirname(target_fn), 0o700) # type: ignore
            except Exception:
                pass

            try:
                shutil.copy(fn, target_fn) # type: ignore
            except Exception:
                pass

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

        for dir, fn in dirlist: # @ReservedAssignment

            if fn.endswith("_ren.py"):
                if dir is None:
                    continue

                fn = fn[:-7]
                target = self.script_files

            elif fn.endswith(".rpy"):
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

    def script_filter(self, fn, dir):
        """
        This determines if a script file should be loaded.
        during this call to load_script.
        """

        if not renpy.config.defer_tl_scripts:
            return True

        if (renpy.game.args.command != "run") or renpy.game.args.compile or renpy.game.args.lint:
            return True

        parts = fn.split("/")

        if parts[0] == 'tl':
            if len(parts) <= 2:
                return True

            if parts[1] == "None":
                return True

            if parts[1] in self.load_languages:
                return True

            return False

        return True

    def load_script(self):

        script_files = self.script_files

        # Sort script files by filename.
        # We need this key to prevent possible crash when comparing None to str
        # during sorting
        script_files.sort(key=lambda item: ((item[0] or ""), (item[1] or "")))

        initcode = [ ]

        count = 0
        skipped = 0

        for fn, dir in script_files: # @ReservedAssignment

            count += 1
            renpy.display.presplash.progress("Loading script...", count, len(script_files))

            # Pump the presplash window to prevent marking
            # our process as unresponsive by OS
            renpy.display.presplash.pump_window()

            if (fn, dir) in self.loaded_scripts:
                continue

            if not self.script_filter(fn, dir):
                skipped += 1
                continue

            self.loaded_scripts.add((fn, dir))

            self.load_appropriate_file(".rpyc", [ "_ren.py", ".rpy" ], dir, fn, initcode)

        if skipped:
            renpy.display.log.write("{} script files skipped.".format(skipped))

        initcode.sort(key=lambda i: i[0])

        self.initcode.extend(initcode)

        self.translator.chain_translates()

        return initcode

    def load_module(self, name):

        files = [ (fn, dir) for fn, dir in self.module_files if fn == name ] # @ReservedAssignment

        if not files:
            raise Exception("Module %s could not be loaded." % name)

        if len(files) > 2:
            raise Exception("Module %s ambiguous, multiple variants exist." % name)

        fn, dir = files[0] # @ReservedAssignment
        initcode = [ ]

        self.load_appropriate_file(".rpymc", [ ".rpym" ], dir, fn, initcode)

        if renpy.parser.report_parse_errors():
            raise SystemExit(-1)

        initcode.sort(key=lambda i: i[0])

        self.translator.chain_translates()

        return initcode

    def include_module(self, name):
        """
        Loads a module with the provided name and inserts its
        initcode into the script current initcode
        """
        module_initcode = self.load_module(name)
        if not module_initcode:
            return

        # We may not insert elements at or prior the current id!
        current_id = renpy.game.initcode_ast_id

        if module_initcode[0][0] < self.initcode[current_id][0]:
            raise Exception("Module %s contains nodes with priority lower than the node that loads it" % name)

        merge_id = current_id + 1
        current_tail = self.initcode[merge_id:]

        # Since script initcode and module initcode are both sorted,
        # we can use heap to merge them
        new_tail = current_tail +  module_initcode
        new_tail.sort(key=lambda i: i[0])

        self.initcode[merge_id:] = new_tail

    def assign_names(self, stmts, fn):
        # Assign names to statements that don't have one already.

        all_stmts = collapse_stmts(stmts)

        version = int(time.time())

        for s in all_stmts:
            if s.name is None:
                s.name = (fn, version, self.serial)
                self.serial += 1

    def merge_names(self, old_stmts, new_stmts, used_names):

        old_stmts = collapse_stmts(old_stmts)
        new_stmts = collapse_stmts(new_stmts)

        old_info = [ i.diff_info() for i in old_stmts ]
        new_info = [ i.diff_info() for i in new_stmts ]

        sm = difflib.SequenceMatcher(None, old_info, new_info)

        for oldl, newl, count in sm.get_matching_blocks():
            for i in range(count):
                old = old_stmts[oldl + i]
                new = new_stmts[newl + i]

                if (new.name is None) and (old.name not in used_names):
                    new.name = old.name
                    used_names.add(new.name)

    def load_string(self, filename, filedata, linenumber=1):
        """
        Loads Ren'Py script from a string.

        `filename`
            The filename that's assigned to the data.

        `filedata`
            A unicode string to be loaded.

        Return the list of statements making up the root block, and a
        list of init statements that need to be run.
        """

        stmts = renpy.parser.parse(filename, filedata, linenumber=linenumber)

        if stmts is None:
            return None, None

        renpy.parser.release_deferred_errors()
        if renpy.parser.parse_errors:
            return None, None

        self.assign_names(stmts, filename)
        self.static_transforms(stmts)

        initcode = [ ]

        stmts = self.finish_load(stmts, initcode, False)

        initcode.sort(key=lambda i: i[0])

        return stmts, initcode

    def finish_load(self, stmts, initcode, check_names=True, filename=None):
        """
        Given `stmts`, a list of AST nodes comprising the root block,
        finishes loading it.

        `initcode`
            A list we append init statements to.

        `check_names`
            If true, produce duplicate name errors.

        `filename`
            If given, a filename that overrides the filename found inside the
            file.

        Returns a list of statements that corresponds to the top-level block
        in initcode after transformation.
        """

        if not stmts:
            return stmts

        # Chain together the statements in the file.
        renpy.ast.chain_block(stmts, None)

        # All of the statements found in file, regardless of nesting
        # depth.

        all_stmts = [ ]
        for i in stmts:
            i.get_children(all_stmts.append)

        for i in all_stmts:
            if isinstance(i, renpy.ast.RPY):
                a, b = i.rest
                if a == "python":
                    if b == "3":
                        b = "division"
                    if b in __future__.all_feature_names:
                        renpy.python.file_compiler_flags[i.filename] |= getattr(__future__, b).compiler_flag
                    else:
                        raise Exception("Unknown __future__ : {!r}.".format(b))

        # Take the translations.
        self.translator.take_translates(all_stmts)

        # Fix the filename for a renamed .rpyc file.
        if filename is not None:
            filename = renpy.lexer.elide_filename(filename)

            if not all_stmts[0].filename.lower().endswith(filename.lower()):

                if filename[-1] != "c":
                    filename += "c"

                for i in all_stmts:
                    i.filename = filename

        def check_name(node):

            if not check_names:
                return

            if renpy.mobile:
                return

            bad_name = None
            bad_node = None
            old_node = None

            name = node.name

            if name in self.namemap:

                bad_name = name
                bad_node = node
                old_node = self.namemap[name]

                if not isinstance(bad_name, basestring):

                    raise ScriptError("Name %s is defined twice, at %s:%d and %s:%d." %
                                      (repr(bad_name),
                                       old_node.filename, old_node.linenumber,
                                       bad_node.filename, bad_node.linenumber))

                else:

                    if renpy.config.allow_duplicate_labels:
                        return

                    self.duplicate_labels.append(
                        u'The label {} is defined twice, at File "{}", line {}:\n{}and File "{}", line {}:\n{}'.format(
                            bad_name, old_node.filename, old_node.linenumber,
                            renpy.lexer.get_line_text(old_node.filename, old_node.linenumber),
                            bad_node.filename, bad_node.linenumber,
                            renpy.lexer.get_line_text(bad_node.filename, bad_node.linenumber),
                        ))

        self.update_bytecode()

        for node in all_stmts:

            name = node.name

            check_name(node)

            # Add the name to the namemap.
            self.namemap[name] = node

            # Add any init nodes to self.initcode.
            if node.get_init:
                init = node.get_init()
                if init:
                    initcode.append(init)

            if node.early_execute:
                node.early_execute()

        if self.all_stmts is not None:
            self.all_stmts.extend(all_stmts)

        self.need_analysis.extend(all_stmts)

        return stmts

    def write_rpyc_header(self, f):
        """
        Writes an empty version 2 .rpyc header to the open binary file `f`.
        """

        f.write(RPYC2_HEADER)

        for _i in range(3):
            f.write(struct.pack("III", 0, 0, 0))

    def write_rpyc_data(self, f, slot, data):
        """
        Writes data into `slot` of a .rpyc file. The data should be a binary
        string, and is compressed before being written.
        """

        f.seek(0, 2)

        start = f.tell()
        data = zlib.compress(data, 3)
        f.write(data)

        f.seek(len(RPYC2_HEADER) + 12 * (slot - 1), 0)
        f.write(struct.pack("III", slot, start, len(data)))

        f.seek(0, 2)

    def write_rpyc_md5(self, f, digest):
        """
        Writes the md5 to the end of a .rpyc file.
        """

        f.seek(0, 2)
        f.write(digest)

    def read_rpyc_data(self, f, slot):
        """
        Reads the binary data from `slot` in a .rpyc (v1 or v2) file. Returns
        the data if the slot exists, or None if the slot does not exist.
        """

        # f.seek(0)
        header_data = f.read(1024)

        # header = f.read(len(RPYC2_HEADER))

        # Legacy path.
        if header_data[:len(RPYC2_HEADER)] != RPYC2_HEADER:
            if slot != 1:
                return None

            f.seek(0)
            data = f.read()

            return zlib.decompress(data)

        # RPYC2 path.
        pos = len(RPYC2_HEADER)

        while True:
            header_slot, start, length = struct.unpack("III", header_data[pos:pos + 12])

            if slot == header_slot:
                break

            if header_slot == 0:
                return None

            pos += 12

        f.seek(start)
        data = f.read(length)

        return zlib.decompress(data)

    def static_transforms(self, stmts):
        """
        This performs transformations on the script that can be performed
        statically. When possible, these transforms are stored in slot 2
        of the rpyc file.
        """

        # Generate translate nodes.
        renpy.translation.restructure(stmts)

    def load_file(self, dir, fn): # @ReservedAssignment

        # Used to only find the deferred parse errors from this file.
        old_deferred_parse_errors = renpy.parser.deferred_parse_errors
        renpy.parser.deferred_parse_errors = collections.defaultdict(list)

        try:

            if fn.endswith(".rpy") or fn.endswith(".rpym") or fn.endswith("_ren.py"):

                if not dir:
                    raise Exception("Cannot load rpy/rpym/ren.py file %s from inside an archive." % fn)

                base, _, game = dir.replace("\\", "/").rpartition("/")
                olddir = base + "/old-" + game

                fullfn = dir + "/" + fn

                if fn.endswith("_ren.py"):
                    rpycfn = fullfn[:-7] + ".rpyc"
                    oldrpycfn = olddir + "/" + fn[:-7] + ".rpyc"
                else:
                    rpycfn = fullfn + "c"
                    oldrpycfn = olddir + "/" + fn + "c"

                stmts = renpy.parser.parse(fullfn)

                data = { }
                data['version'] = script_version
                data['key'] = self.key or 'unlocked'
                data['deferred_parse_errors'] = renpy.parser.deferred_parse_errors

                if stmts is None:
                    return data, [ ]

                used_names = set()

                for mergefn in [ oldrpycfn, rpycfn ]:

                    old_all_pyexpr = self.all_pyexpr
                    self.record_pycode = False
                    self.all_pyexpr = None

                    # See if we have a corresponding .rpyc file. If so, then
                    # we want to try to upgrade our .rpy file with it.
                    try:

                        with open(mergefn, "rb") as rpycf:
                            bindata = self.read_rpyc_data(rpycf, 1)

                        if bindata is not None:
                            old_data, old_stmts = loads(bindata)
                            self.merge_names(old_stmts, stmts, used_names)

                            del old_data
                            del old_stmts
                    except Exception:
                        pass
                    finally:
                        self.record_pycode = True
                        self.all_pyexpr = old_all_pyexpr

                self.assign_names(stmts, renpy.lexer.elide_filename(fullfn))

                pickle_data_before_static_transforms = dumps((data, stmts))

                self.static_transforms(stmts)

                pickle_data_after_static_transforms = dumps((data, stmts))

                if not renpy.macapp:
                    try:
                        with open(rpycfn, "wb") as f:
                            self.write_rpyc_header(f)
                            self.write_rpyc_data(f, 1, pickle_data_before_static_transforms)
                            self.write_rpyc_data(f, 2, pickle_data_after_static_transforms)

                            with open(fullfn, "rb") as fullf:
                                rpydigest = hashlib.md5(fullf.read()).digest()

                            self.write_rpyc_md5(f, rpydigest)
                    except Exception:
                        import traceback
                        traceback.print_exc()

                self.loaded_rpy = True

            elif fn.endswith(".rpyc") or fn.endswith(".rpymc"):

                data = None
                stmts = None

                with renpy.loader.load(fn, tl=False) as f:
                    for slot in [ 2, 1 ]:
                        try:
                            bindata = self.read_rpyc_data(f, slot)

                            if bindata:
                                data, stmts = loads(bindata)
                                break

                        except Exception:
                            pass

                        f.seek(0)

                    else:
                        return None, None

                    if data is None:
                        print("Failed to load", fn)
                        return None, None

                    if not isinstance(data, dict):
                        return None, None

                    if self.key and data.get('key', 'unlocked') != self.key:
                        return None, None

                    if data['version'] != script_version:
                        return None, None

                    if slot < 2:
                        self.static_transforms(stmts)

                    renpy.parser.deferred_parse_errors = data.get('deferred_parse_errors', None) or collections.defaultdict(list)

            else:
                return None, None

            return data, stmts

        finally:

            # Restore the deferred parse errors.
            for k, v in renpy.parser.deferred_parse_errors.items():
                old_deferred_parse_errors[k].extend(v)

            renpy.parser.deferred_parse_errors = old_deferred_parse_errors



    def load_appropriate_file(self, compiled, source_extensions, dir, fn, initcode): # @ReservedAssignment
        data = None

        source = source_extensions[-1]

        renpy.game.exception_info = "While loading the script."

        # This can only be a .rpyc file, since we're loading it
        # from an archive.
        if dir is None:

            rpyfn = fn + source
            lastfn = fn + compiled
            data, stmts = self.load_file(dir, fn + compiled)

            if data is None:
                raise Exception("Could not load from archive %s." % (lastfn,))

            with renpy.loader.load(fn + compiled, tl=False) as f:
                f.seek(-hashlib.md5().digest_size, 2)
                digest = f.read(hashlib.md5().digest_size)

        else:

            # Otherwise, we're loading from disk. So we need to decide if
            # we want to load the rpy or the rpyc file.
            rpycfn = dir + "/" + fn + compiled
            rpyfn = None # prevent the spurious warning.
            rpydigest = None

            rpyfns = [ ]

            for source in source_extensions:
                rpyfn = dir + "/" + fn + source

                renpy.loader.add_auto(rpyfn)

                if os.path.exists(rpyfn):
                    rpyfns.append((source, rpyfn))

            if len(rpyfns) > 1:
                raise Exception("{} conflict, and can't exist in the same game.".format(" and ".join(i[1] for i in rpyfns)))
            elif rpyfns:
                source, rpyfn = rpyfns[0]

                with open(rpyfn, "rb") as f:
                    rpydigest = hashlib.md5(f.read()).digest()
            else:
                source = source_extensions[-1]
                rpyfn = dir + "/" + fn + source_extensions[-1]

            try:
                if os.path.exists(rpycfn):
                    with open(rpycfn, "rb") as f:
                        f.seek(-hashlib.md5().digest_size, 2)
                        rpycdigest = f.read(hashlib.md5().digest_size)
                else:
                    rpycdigest = None
            except Exception:
                rpycdigest = None

            digest = None

            if os.path.exists(rpyfn) and os.path.exists(rpycfn):

                # Are we forcing a compile?
                force_compile = renpy.game.args.compile # type: ignore

                # Use the source file here since it'll be loaded if it exists.
                lastfn = rpyfn

                data, stmts = None, None

                try:

                    if rpydigest == rpycdigest and not force_compile:

                        data, stmts = self.load_file(dir, fn + compiled)

                        if data is None:
                            print("Could not load " + rpycfn)

                except Exception:
                    renpy.display.log.write("While loading %r", rpycfn)
                    renpy.display.log.exception()

                    if "RENPY_RPYC_EXCEPTIONS" in os.environ:
                        print("While loading", rpycfn)
                        raise

                if data is None:
                    data, stmts = self.load_file(dir, fn + source)

                digest = rpydigest

            elif os.path.exists(rpycfn):
                lastfn = rpycfn
                data, stmts = self.load_file(dir, fn + compiled)

                digest = rpycdigest

            elif os.path.exists(rpyfn):
                lastfn = rpyfn
                data, stmts = self.load_file(dir, fn + source)

                digest = rpydigest

            if digest is not None:
                self.backup_list.append((rpyfn, digest))

        if data is None:
            raise Exception("Could not load file %s." % lastfn) # type: ignore

        # Check the key.
        if self.key is None:
            self.key = data['key']
        elif self.key != data['key']:
            raise Exception(fn + " does not share a key with at least one .rpyc file. To fix, delete all .rpyc files, or rerun Ren'Py with the --lock option.")

        self.finish_load(stmts, initcode, filename=lastfn) # type: ignore

        self.digest.update(digest) # type: ignore

    def init_bytecode(self):
        """
        Init/Loads the bytecode cache.
        """

        if renpy.game.args.compile_python:
            return

        # Load the oldcache.
        try:
            with renpy.loader.load(BYTECODE_FILE) as f:
                version, cache = loads(zlib.decompress(f.read()))
                if version == BYTECODE_VERSION:
                    self.bytecode_oldcache = cache

        except Exception:
            pass

    def update_bytecode(self):
        """
        Compiles the PyCode objects in self.all_pycode, updating the
        cache. Clears out self.all_pycode.
        """

        renpy.python.compile_warnings = [ ]

        for i in self.all_pyexpr:
            try:
                renpy.python.py_compile(i, 'eval')
            except Exception:
                pass

        self.all_pyexpr = [ ]

        # Update all of the PyCode objects in the system with the loaded
        # bytecode.

        for i in self.all_pycode:

            key = i.get_hash() + MAGIC

            flags = renpy.python.file_compiler_flags.get(i.location[0], 0)
            if flags:
                if flags == __future__.division.compiler_flag:
                    # avoid triggering a recompile
                    key += b"_py3"
                else:
                    key += b"_flags" + str(flags).encode("utf-8")

            warnings_key = ("warnings", key)

            code = self.bytecode_oldcache.get(key, None)

            if code is None:

                self.bytecode_dirty = True

                old_ei = renpy.game.exception_info
                renpy.game.exception_info = "While compiling python block starting at line %d of %s." % (i.location[1], i.location[0])

                try:

                    if i.mode == 'exec':
                        code = renpy.python.py_compile_exec_bytecode(i.source, filename=i.location[0], lineno=i.location[1], py=i.py)
                    elif i.mode == 'hide':
                        code = renpy.python.py_compile_hide_bytecode(i.source, filename=i.location[0], lineno=i.location[1], py=i.py)
                    elif i.mode == 'eval':
                        code = renpy.python.py_compile_eval_bytecode(i.source, filename=i.location[0], lineno=i.location[1], py=i.py)

                except SyntaxError as e:

                    text = e.text

                    if text is None:
                        text = ''

                    pem = renpy.parser.ParseError(
                        filename=e.filename,
                        number=e.lineno,
                        msg=e.msg,
                        line=text,
                        pos=e.offset)

                    renpy.parser.parse_errors.append(pem.message)

                    continue

                renpy.game.exception_info = old_ei

                if renpy.python.compile_warnings:
                    self.bytecode_newcache[warnings_key] = renpy.python.compile_warnings
                    renpy.python.compile_warnings = [ ]

            else:

                if warnings_key in self.bytecode_oldcache:
                    self.bytecode_newcache[warnings_key] = self.bytecode_oldcache[warnings_key]

            self.bytecode_newcache[key] = code
            i.bytecode = marshal.loads(code) # type: ignore

        self.all_pycode = [ ]

    def save_bytecode(self):
        if renpy.macapp:
            return

        if self.bytecode_dirty:
            try:
                fn = renpy.loader.get_path(BYTECODE_FILE)

                with open(fn, "wb") as f:
                    data = (BYTECODE_VERSION, self.bytecode_newcache)
                    f.write(zlib.compress(dumps(data), 3))
            except Exception:
                pass

            fn = renpy.loader.get_path(OLD_BYTECODE_FILE)
            try:
                os.unlink(fn)
            except Exception:
                pass

    def lookup(self, label):
        """
        Looks up the given label in the game. If the label is not found,
        raises a ScriptError.
        """

        if isinstance(label, renpy.parser.SubParse):
            label = label.block[0].name

        label = renpy.config.label_overrides.get(label, label)
        original = label

        rv = self.namemap.get(label, None)

        if (rv is None) and (renpy.config.missing_label_callback is not None):
            label = renpy.config.missing_label_callback(label)
            rv = self.namemap.get(label, None)

        if rv is None:
            raise ScriptError("could not find label '%s'." % str(original))

        return self.namemap[label]

    def has_label(self, label):
        """
        Returns true if the label exists, or false otherwise.
        """

        if isinstance(label, renpy.parser.SubParse):

            if not label.block:
                return False

            label = label.block[0].name

        label = renpy.config.label_overrides.get(label, label)

        return label in self.namemap

    def lookup_or_none(self, label):
        """
        Looks up the label if it exists, or returns None if it does not.
        """

        if label is None:
            return None

        if not self.has_label(label):
            return None

        return self.lookup(label)

    def analyze(self):
        """
        Analyzes all statements that need analysis.
        """

        for i in self.need_analysis:
            i.analyze()

        self.need_analysis = [ ]

    def report_duplicate_labels(self):
        if not renpy.config.developer:
            return

        if renpy.config.ignore_duplicate_labels:
            return

        renpy.parser.parse_errors = self.duplicate_labels

        if renpy.parser.report_parse_errors():
            raise SystemExit(-1)
