# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code that manages the distribution of Ren'Py games
# and Ren'Py proper.
#
# In this module, all files and paths are stored in unicode. Full paths
# might include windows path separators (\), but archive paths and names we
# deal with/match against use the unix separator (/).

init python in distribute:

    from store import config, persistent
    import store.project as project
    import store.interface as interface
    import store.archiver as archiver
    import store.updater as updater
    import store as store

    from change_icon import change_icons

    import sys
    import os
    import json
    import subprocess
    import hashlib
    import struct
    import collections
    import os
    import io
    import re
    import plistlib
    import time
    import shutil

    def py(s):
        """
        Formats a string with information about the python version.
        """

        return s.format(
            major=sys.version_info.major,
            minor=sys.version_info.minor,
        )

    # Going from 7.4 to 7.5 or 8.0, the library directory changed.
    RENPY_PATCH = py("""\
def change_renpy_executable():
    import sys, os, renpy, site

    if hasattr(site, "RENPY_PLATFORM") and hasattr(sys, "renpy_executable") and (renpy.linux or renpy.windows):
        sys.renpy_executable = os.path.join(renpy.config.renpy_base, "lib", "py{major}-" + site.RENPY_PLATFORM, os.path.basename(sys.renpy_executable))

change_renpy_executable()
""")

    match_cache = { }

    def compile_match(pattern):
        """
        Compiles a pattern for use with match.
        """

        regexp = ""

        while pattern:
            if pattern.startswith("**"):
                regexp += r'.*'
                pattern = pattern[2:]
            elif pattern[0] == "*":
                regexp += r'[^/]*/?'
                pattern = pattern[1:]
            elif pattern[0] == '[':
                regexp += r'['
                pattern = pattern[1:]

                while pattern and pattern[0] != ']':
                    regexp += pattern[0]
                    pattern = pattern[1:]

                pattern = pattern[1:]
                regexp += ']'

            else:
                regexp += re.escape(pattern[0])
                pattern = pattern[1:]

        regexp += "$"

        return re.compile(regexp, re.I)

    def match(s, pattern):
        """
        Matches a glob-style pattern against s. Returns True if it matches,
        and False otherwise.

        ** matches every character.
        * matches every character but /.
        [abc] matches a, b, or c.

        Things are matched case-insensitively.
        """

        regexp = match_cache.get(pattern, None)
        if regexp is None:
            regexp = compile_match(pattern)
            match_cache[pattern] = regexp

        if regexp.match(s):
            return True

        if regexp.match("/" + s):
            return True

        return False

    def hash_file(fn):
        """
        Returns the hash of `fn`.
        """

        sha = hashlib.sha256()

        with open(renpy.fsencode(fn), "rb") as f:
            while True:

                data = f.read(8 * 1024 * 1024)

                if not data:
                    break

                sha.update(data)

        return sha.hexdigest()

    class File(object):
        """
        Represents a file that we can distribute.

        self.name
            The name of the file as it will be stored in the archives.

        self.path
            The path to the file on disk. None if it won't be stored
            on disk.

        self.directory
            True if this is a directory.

        self.executable
            True if this is an executable that should be distributed
            with the xbit set.
        """

        def __init__(self, name, path, directory, executable):
            self.name = name
            self.path = path
            self.directory = directory
            self.executable = executable

        def __repr__(self):
            if self.directory:
                extra = "dir"
            elif self.executable:
                extra = "x-bit"
            else:
                extra = ""

            return "<File {!r} {!r} {}>".format(self.name, self.path, extra)

        def copy(self):
            return File(self.name, self.path, self.directory, self.executable)

        def hash(self, hash, distributor):
            """
            Update hash with information about this entry.
            """

            key = (self.name, self.directory, self.executable)

            hash.update(repr(key).encode("utf-8"))

            if self.path is None:
                return

            if self.directory:
                return

            if self.name == "update/current.json":
                return

            if self.path in distributor.hash_cache:
                digest = distributor.hash_cache[self.path]
            else:
                digest = hash_file(self.path)

            hash.update(digest.encode("utf-8"))

        def reprefix(self, old, new):
            rv = self.copy()

            if self.name.startswith(old):
                rv.name = new + self.name[len(old):]

            return rv

    class FileList(list):
        """
        This represents a list of files that we know about.
        """

        def sort(self):
            list.sort(self, key=lambda a : a.name)

        def copy(self):
            """
            Makes a deep copy of this file list.
            """

            rv = FileList()

            for i in self:
                rv.append(i.copy())

            return rv

        def filter_empty(self):
            """
            Makes a deep copy of this file list with empty directories
            omitted.
            """

            rv = FileList()

            needed_dirs = set()

            for i in reversed(self):

                if (not i.directory) or (i.name in needed_dirs):
                    rv.insert(0, i.copy())

                    directory, _sep, _filename = i.name.rpartition("/")
                    needed_dirs.add(directory)

            return rv

        def add_missing_directories(self):
            """
            Adds to this file list all directories that are needed by other
            entries in this file list.
            """

            rv = self.copy()

            seen = set()
            required = set()

            for i in self:
                seen.add(i.name)

                name = i.name

                while "/" in name:
                    name = name.rpartition("/")[0]
                    required.add(name)

            for name in required - seen:
                rv.append(File(name, None, True, False))

            rv.sort()

            return rv


        @staticmethod
        def merge(l):
            """
            Merges a list of file lists into a single file list with no
            duplicate entries.
            """

            rv = FileList()

            seen = set()

            for fl in l:
                for f in fl:
                    if f.name in seen:
                        continue

                    rv.append(f)
                    seen.add(f.name)

            return rv

        def prepend_directory(self, directory):
            """
            Modifies this file list such that every file in it has `directory`
            prepended.
            """

            for i in self:
                i.name = directory + "/" + i.name

            self.insert(0, File(directory, None, True, False))


        def mac_transform(self, app, documentation):
            """
            Creates a new file list that has the mac transform applied to it.

            The mac transform places all files that aren't already in <app> in
            <app>/Contents/Resources/autorun. If it matches one of the documentation
            patterns, then it appears both inside and outside of the app.
            """

            rv = FileList()

            for f in self:

                # Already in the app.
                if f.name == app or f.name.startswith(app + "/"):
                    rv.append(f)
                    continue

                # If it's documentation, keep the file. (But also make
                # a copy.)
                for pattern in documentation:
                    if match(f.name, pattern):
                        rv.append(f)

                    if match("/" + f.name, pattern):
                        rv.append(f)

                # Make a copy.
                f = f.copy()

                f.name = app + "/Contents/Resources/autorun/" + f.name
                rv.append(f)

            rv.append(File(app + "/Contents/Resources/autorun", None, True, False))
            rv.sort()

            return rv

        def mac_lib_transform(self, app, duplicate):
            """
            Creates a new file list that has lib/darwin-x86_64 and lib/pythonlib2.7
            copied into the mac app, the latter iff it's not duplicated elsewhere or
            duplicate is set.
            """

            prefix = py("lib/py{major}-mac-universal")

            for f in list(self):

                if f.name.startswith("lib/python") and (not duplicate):
                    name = app + "/Contents/Resources/" + f.name

                elif f.name.startswith(prefix):
                    name = app + "/Contents/MacOS/" + f.name[len(prefix)+1:]

                else:
                    continue

                new = f.copy()
                new.name = name
                self.append(new)

                if not duplicate:
                    self.remove(f)

            self.sort()


        def hash(self, distributor):
            """
            Returns a hex digest representing this file list.
            """

            sha = hashlib.sha256()

            for f in sorted(self, key=lambda a : a.name):
                f.hash(sha, distributor)

            if PY2:
                return sha.hexdigest().decode("utf-8")
            else:
                return sha.hexdigest()

        def split_by_prefix(self, prefix):
            """
            Returns two filelists, one that contains all the files starting with prefix,
            and one tht contains all other files.
            """

            yes = FileList()
            no = FileList()

            for f in self:
                if f.name.startswith(prefix):
                    yes.append(f)
                else:
                    no.append(f)

            return yes, no

        def reprefix(self, old, new):
            """
            Returns a new file list with all the paths reprefixed.
            """

            rv = FileList()

            for f in self:
                rv.append(f.reprefix(old, new))

            return rv


    class Distributor(object):
        """
        This manages the process of building distributions.
        """

        def __init__(self, project, destination=None, reporter=None, packages=None, build_update=True, open_directory=False, noarchive=False, packagedest=None, report_success=True, scan=True, macapp=None, force_format=None, files_filter=None):
            """
            Distributes `project`.

            `destination`
                The destination in which the distribution will be placed. If None,
                uses a default location.

            `reporter`
                An object that's used to report status and progress to the user.

            `packages`
                If not None, a list of packages to distributed. If None, all
                packages are distributed.

            `build_update`
                Will updates be built?

            `open_directory`
                If true, the directory containing the built files will be opened
                if the build succeeds.

            `noarchive`
                If true, files will not be placed into archives.

            `packagedest`
                If given, gives the full path to the single package (without any
                extensions).

            `report_success`
                If true, we report that the build succeeded.

            `macapp`
                If given, the path to a macapp that's used instead of
                the macapp that's included with Ren'Py.

            `force_format`
                If given, forces the format of the distribution to be this.

            `files_filter`
                If given, use this object to decide which files must be included.
                The object must contains the `filter(file, variant, format)`
                method which must return True is the file must be included.
            """

            # A map from a package to a unique update version hash.
            self.update_versions = { }

            # Map from destination file with extension to (that file's hash,
            # hash of the file list)
            self.build_cache = { }

            # A map from file to its hash.
            self.hash_cache = { }

            # A map from a list of file lists and formats to a single integrated
            # file list with transforms applied.
            self.file_list_cache = { }

            # Status reporter.
            self.reporter = reporter

            if packagedest is not None:
                if packages is None or len(packages) != 1:
                    raise Exception("Packagedest requires a single package be given.")

            # Safety - prevents us from releasing a launcher that won't update.
            if store.UPDATE_SIMULATE:
                raise Exception("Cannot build distributions when UPDATE_SIMULATE is True.")

            # The project we want to distribute.
            self.project = project

            # Logfile.
            self.log = open(self.temp_filename("distribute.txt"), "w")

            # The path to the mac app.
            self.macapp = macapp

            # Start by scanning the project, to get the data and build
            # dictionaries.
            data = project.data

            if scan:
                self.reporter.info(_("Scanning project files..."))
                project.update_dump(force=True, gui=False, compile=project.data['force_recompile'])

            if project.data['force_recompile']:
                import compileall

                compileall.compile_dir(
                    os.path.join(config.renpy_base, "renpy"),
                    ddir="renpy/",
                    force=True,
                    quiet=True,
                )

            if project.dump.get("error", False):
                raise Exception("Could not get build data from the project. Please ensure the project runs.")

            self.build = build = project.dump['build']

            # Map from file list name to file list.
            self.file_lists = collections.defaultdict(FileList)

            self.base_name = build['directory_name']
            self.executable_name = build['executable_name']
            self.pretty_version = build['version']

            if (" " in self.base_name) or (":" in self.base_name) or (";" in self.base_name):
                reporter.info(_("Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."), pause=True)
                self.log.close()
                return

            # The destination directory.
            if destination is None:
                destination = build["destination"]
                parent = os.path.dirname(project.path)
                self.destination = os.path.join(parent, destination)
            else:
                self.destination = destination

            if not packagedest:
                try:
                    os.makedirs(self.destination)
                except Exception:
                    pass

                self.load_build_cache()

            self.packagedest = packagedest

            self.include_update = build['include_update']
            self.build_update = self.include_update and build_update

            # The various executables, which change names based on self.executable_name.
            self.app = self.executable_name + ".app"
            self.exe = self.executable_name + ".exe"
            self.exe32 = self.executable_name + "-32.exe"
            self.sh = self.executable_name + ".sh"
            self.py = self.executable_name + ".py"

            self.documentation_patterns = build['documentation_patterns']

            build_packages = [ ]

            for i in build['packages']:
                name = i['name']

                if packages is None:
                    if not i['hidden']:
                        build_packages.append(i)
                elif name in packages:
                    build_packages.append(i)

            if not build_packages:
                self.reporter.info(_("No packages are selected, so there's nothing to do."), pause=True)
                self.log.close()
                return

            self.scan_and_classify(project.path, build["base_patterns"])

            if noarchive:
                self.ignore_archives(build['archives'])
            else:
                self.archive_files(build["archives"])

            # Add Ren'Py.
            self.reporter.info(_("Scanning Ren'Py files..."))
            self.scan_and_classify(config.renpy_base, build["renpy_patterns"])

            if build["_sdk_fonts"]:
                for k in list(self.file_lists.keys()):
                    self.file_lists[k] = self.file_lists[k].reprefix("sdk-fonts", "game")

            # Add Python (with the same name as our executables)
            self.add_python()

            # Build the mac app and windows exes.
            self.add_mac_files()
            self.add_windows_files()
            self.add_main_py()

            # Add the main.py.
            self.add_main_py()

            # Add generated/special files.
            if build['renpy']:
                self.add_renpy_distro_files()
            else:
                self.add_renpy_game_files()

            # Assign the x-bit as necessary.
            self.mark_executable()

            # Merge file lists, as needed.
            self.merge_file_lists()

            # Rename the executable-like files.
            self.rename()

            # Sign the mac app once on Ren'Py.
            if self.build["renpy"]:
                fl = self.file_lists['binary']
                app, rest = fl.split_by_prefix(self.app)
                if app:
                    app = self.sign_app(app, macapp)
                    fl = FileList.merge([ app, rest ])
                    self.file_lists['binary'] = fl
                else:
                    raise Exception("No mac app found.")

            # The time of the update version.
            self.update_version = int(time.time())

            self.files_filter = files_filter

            for p in build_packages:

                formats = p["formats"]
                if force_format is not None:
                    formats = [ force_format ]

                for f in formats:

                    self.make_package(
                        p["name"],
                        f,
                        p["file_lists"],
                        dlc=p["dlc"])

                if self.build_update and p["update"]:
                    self.make_package(
                        p["name"],
                        "update",
                        p["file_lists"],
                        dlc=p["dlc"])

            wait_parallel_threads()

            if self.build_update:
                self.finish_updates(build_packages)

            if not packagedest:
                self.save_build_cache()

            # Finish up.
            self.log.close()

            if report_success:
                self.reporter.info(_("All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."))

            if open_directory:
                renpy.run(store.OpenDirectory(self.destination, absolute=True))

        def scan_and_classify(self, directory, patterns):
            """
            Walks through the `directory`, finds files and directories that
            match the pattern, and assigns them to the appropriate file list.

            `patterns`
                A list of pattern, file_list tuples. The pattern is a string
                that is matched using match. File_list is either
                a space-separated list of file lists to add the file to,
                or None to ignore it.

                Directories are matched with a trailing /, but added to the
                file list with the trailing / removed.
            """

            def walk(name, path):

                # Ignore ASCII control characters, like (Icon\r on the mac).
                if re.search('[\x00-\x19]', name):
                    return

                is_dir = os.path.isdir(path)

                if is_dir:
                    match_name = name + "/"
                else:
                    match_name = name

                for pattern, file_list in patterns:

                    if match(match_name, pattern):

                        # When we have ('test/**', None), avoid excluding test.
                        if (not file_list) and is_dir:
                            new_pattern = pattern.rstrip("*")
                            if (pattern != new_pattern) and match(match_name, new_pattern):
                                continue

                        break

                else:
                    print(str(match_name), "doesn't match anything.", file=self.log)

                    pattern = None
                    file_list = None

                print(str(match_name), "matches", str(pattern), "(" + str(file_list) + ").", file=self.log)

                if file_list is None:
                    return

                for fl in file_list:
                    f = File(name, path, is_dir, False)
                    self.file_lists[fl].append(f)

                if is_dir:

                    for fn in os.listdir(path):
                        walk(
                            name + "/" + fn,
                            os.path.join(path, fn),
                            )

            for fn in os.listdir(directory):
                walk(fn, os.path.join(directory, fn))

        def merge_file_lists(self):
            """
            For each (old, new) in self.build['merge'], merge the old list
            into the new list.
            """

            for old, new in self.build['merge']:
                self.file_lists[new] = FileList.merge([
                    self.file_lists[old],
                    self.file_lists[new]])

        def rescan(self, oldlist, directory):
            """
            Scans `directory`, and produces a filelist from it. Returns the
            produced filelist.

            `oldlist`
                Is a filelist. If a file has the xbit set in the oldlist, it
                has the xbit set in the new list.
            """

            executable = set()

            for f in oldlist:
                if f.executable:
                    executable.add(f.name)

            rv = FileList()

            def walk(name, path):

                # Ignore ASCII control characters, like (Icon\r on the mac).
                if re.search('[\x00-\x19]', name):
                    return

                is_dir = os.path.isdir(path)

                f = File(name, path, is_dir, name in executable)
                rv.append(f)

                if is_dir:

                    for fn in os.listdir(path):
                        walk(
                            name + "/" + fn,
                            os.path.join(path, fn),
                            )

            for fn in os.listdir(directory):
                walk(fn, os.path.join(directory, fn))

            return rv

        def temp_filename(self, name):
            self.project.make_tmp()
            return os.path.join(self.project.tmp, name)

        def add_file(self, file_list, name, path, executable=False):
            """
            Adds a file to the file lists.

            `file_list`
                A space-separated list of file list names.

            `name`
                The name of the file to be added.

            `path`
                The path to that file on disk.
            """

            if not os.path.exists(path):
                raise Exception("{} does not exist.".format(path))

            if isinstance(file_list, basestring):
                file_list = file_list.split()

            f = File(name, path, False, executable)

            for fl in file_list:
                self.file_lists[fl].append(f)

        def add_directory(self, file_list, name):
            """
            Adds an empty directory to the file lists.
            """

            if isinstance(file_list, basestring):
                file_list = file_list.split()

            f = File(name, None, True, False)

            for fl in file_list:
                self.file_lists[fl].append(f)


        def ignore_archives(self, archives):
            """
            Ignore archiving commands by adding the files that would be in
            archives into packages instead.
            """

            for arcname, file_lists in archives:
                if not self.file_lists[arcname]:
                    continue

                for f in self.file_lists[arcname]:
                    for fl in file_lists:
                        self.file_lists[fl].append(f)

        def archive_files(self, archives):
            """
            Add files to archives.
            """

            for arcname, file_list in archives:

                if not self.file_lists[arcname]:
                    continue

                arcfn = arcname + ".rpa"
                arcpath = self.temp_filename(arcfn)

                af = archiver.Archive(arcpath)

                fll = len(self.file_lists[arcname])

                for i, entry in enumerate(self.file_lists[arcname]):

                    if entry.directory:
                        continue

                    self.reporter.progress(_("Archiving files..."), i, fll)

                    name = "/".join(entry.name.split("/")[1:])
                    af.add(name, entry.path)

                self.reporter.progress_done()

                af.close()

                self.add_file(file_list, "game/" + arcfn, arcpath)

        def add_renpy_game_files(self):
            """
            Add Ren'Py file to the game.
            """

            LICENSE_TXT = os.path.join(config.renpy_base, "LICENSE.txt")

            if os.path.exists(LICENSE_TXT):
                self.add_file("renpy", "renpy/LICENSE.txt", LICENSE_TXT)

            if self.build["script_version"]:

                if (not os.path.exists(os.path.join(self.project.path, "game", "script_version.rpy"))) and \
                    (not os.path.exists(os.path.join(self.project.path, "game", "script_version.rpyc"))):

                    script_version_txt = self.temp_filename("script_version.txt")

                    with open(script_version_txt, "w") as f:
                        f.write(unicode(repr(renpy.renpy.version_tuple[:-1])))

                    self.add_file("all", "game/script_version.txt", script_version_txt)

        def add_file_list_hash(self, list_name):
            """
            Hashes a file list, then adds that file to the Ren'Py distribution.
            """

            tfn = self.temp_filename(list_name + "_hash.txt")

            with open(tfn, "w") as tf:
                tf.write(self.file_lists[list_name].hash(self))

            self.add_file("binary", "launcher/game/" + list_name + "_hash.txt", tfn)
            self.add_file(list_name, list_name + "/hash.txt", tfn)

        def add_renpy_distro_files(self):
            """
            Add additional files to Ren'Py.
            """

            self.add_file_list_hash("rapt")
            self.add_file_list_hash("renios")
            self.add_file_list_hash("web")

            tmp_fn = self.temp_filename("renpy.py")

            with open(os.path.join(config.renpy_base, "renpy.py"), "rb") as f:
                data = f.read()

            with open(tmp_fn, "wb") as f:
                f.write(b"#!/usr/bin/env python3\n")
                f.write(data)

            self.add_file("source_only", "renpy.py", tmp_fn, True)


        def write_plist(self):

            display_name = self.build['display_name']
            executable_name = self.executable_name
            version = self.build['version']

            plist = dict(
                CFBundleDevelopmentRegion="English",
                CFBundleDisplayName=display_name,
                CFBundleExecutable=executable_name,
                CFBundleIconFile="icon",
                CFBundleIdentifier="com.domain.game",
                CFBundleInfoDictionaryVersion="6.0",
                CFBundleName=display_name,
                CFBundlePackageType="APPL",
                CFBundleShortVersionString=version,
                CFBundleVersion=time.strftime("%Y.%m%d.%H%M%S"),
                LSApplicationCategoryType="public.app-category.simulation-games",
                CFBundleDocumentTypes = [
                    {
                        "CFBundleTypeOSTypes" : [ "****", "fold", "disk" ],
                        "CFBundleTypeRole" : "Viewer",
                    },
                    ],
                UTExportedTypeDeclarations = [
                    {
                        "UTTypeConformsTo" : [ "public.python-script" ],
                        "UTTypeDescription" : "Ren'Py Script",
                        "UTTypeIdentifier" : "org.renpy.rpy",
                        "UTTypeTagSpecification" : { "public.filename-extension" : [ "rpy" ] }
                    },
                    ],
                NSHighResolutionCapable=True,
                )

            if self.build.get('allow_integrated_gpu', False):
                plist["NSSupportsAutomaticGraphicsSwitching"] = True

            plist.update(self.build.get("mac_info_plist", { }))

            rv = self.temp_filename("Info.plist")

            if PY2:
                plistlib.writePlist(plist, rv)
            else:
                with open(rv, "wb") as f:
                    plistlib.dump(plist, f)

            return rv

        def add_python(self):

            if self.build['renpy']:
                windows = 'binary'
                linux = 'binary'
                linux_i686 = 'binary'
                mac = 'binary'
                raspi = 'linux_arm'
            else:
                windows = 'windows'
                linux = 'linux'
                linux_i686 = 'linux_i686'
                mac = 'mac'
                raspi = 'linux_arm'

            prefix = py("lib/py{major}-")

            if os.path.exists(linux_i686):

                self.add_file(
                    linux_i686,
                    prefix + "linux-i686/" + self.executable_name,
                    os.path.join(config.renpy_base, prefix + "linux-i686/renpy"),
                    True)

            self.add_file(
                linux,
                prefix + "linux-x86_64/" + self.executable_name,
                os.path.join(config.renpy_base, prefix + "linux-x86_64/renpy"),
                True)

            armfn = os.path.join(config.renpy_base, prefix + "linux-armv7l/renpy")

            if os.path.exists(armfn):

                self.add_file(
                    raspi,
                    prefix + "linux-armv7l/" + self.executable_name,
                    armfn,
                    True)

            aarch64fn = os.path.join(config.renpy_base, prefix + "linux-aarch64/renpy")

            if os.path.exists(aarch64fn):

                self.add_file(
                    raspi,
                    prefix + "linux-aarch64/" + self.executable_name,
                    aarch64fn,
                    True)

            self.add_file(
                mac,
                prefix + "mac-universal/" + self.executable_name,
                os.path.join(config.renpy_base, prefix + "mac-universal/renpy"),
                True)

        def add_mac_files(self):
            """
            Add mac-specific files to the distro.
            """

            if self.build['renpy']:
                filelist = "binary"
            else:
                filelist = "mac"

            contents = self.app + "/Contents"

            self.add_directory(filelist, self.app)
            self.add_directory(filelist, contents)
            self.add_directory(filelist, contents + "/MacOS")

            plist_fn = self.write_plist()
            self.add_file(filelist, contents + "/Info.plist", plist_fn)

            self.add_file(filelist,
                contents + "/MacOS/" + self.executable_name,
                os.path.join(config.renpy_base, py("lib/py{major}-mac-universal/renpy")))


            custom_fn = os.path.join(self.project.path, "icon.icns")
            default_fn = os.path.join(config.renpy_base, "launcher/icon.icns")

            if os.path.exists(custom_fn):
                icon_fn = custom_fn
            else:
                icon_fn = default_fn

            resources = contents + "/Resources"

            self.add_directory(filelist, resources)
            self.add_file(filelist, resources + "/icon.icns", icon_fn)

            if not self.build['renpy']:
                self.add_directory(filelist, contents + "/MacOS/lib")
                self.add_directory(filelist, contents + py("/MacOS/lib/py{major}-mac-universal"))
                self.add_directory(filelist, contents + py("/Resources/lib/python{major}.{minor}"))

            self.file_lists[filelist].mac_lib_transform(self.app, self.build['renpy'])

        def add_windows_files(self):
            """
            Adds windows-specific files.
            """

            if self.build['renpy']:
                windows = 'binary'
                windows_i686 = 'binary'
            else:
                windows = 'windows'
                windows_i686 = 'windows_i686'


            icon_fn = os.path.join(self.project.path, "icon.ico")


            def write_exe(src, dst, tmp, fl):
                """
                Write the exe found at `src` (taken as relative to renpy-base)
                as `dst` (in the distribution). `tmp` is the name of a tempfile
                that is written if one is needed.
                """

                if fl == "windows_i686":
                    should_change_icon = self.build["change_icon_i686"]
                else:
                    should_change_icon = True

                src = os.path.join(config.renpy_base, src)
                tmp = self.temp_filename(tmp)

                if should_change_icon and os.path.exists(icon_fn) and os.path.exists(src):

                    with open(tmp, "wb") as f:
                        f.write(change_icons(src, icon_fn))

                else:
                    tmp = src

                if os.path.exists(tmp):
                    self.add_file(fl, dst, tmp)

            if PY2:

                if self.build["include_i686"]:
                    write_exe("lib/py2-windows-i686/renpy.exe", self.exe32, self.exe32, windows_i686)
                    write_exe("lib/py2-windows-i686/pythonw.exe", "lib/py2-windows-i686/pythonw.exe", "pythonw-32.exe", windows_i686)

                write_exe("lib/py2-windows-x86_64/renpy.exe", self.exe, self.exe, windows)
                write_exe("lib/py2-windows-x86_64/pythonw.exe", "lib/py2-windows-x86_64/pythonw.exe", "pythonw-64.exe", windows)

            else:

                write_exe("lib/py3-windows-x86_64/renpy.exe", self.exe, self.exe, windows)
                write_exe("lib/py3-windows-x86_64/pythonw.exe", "lib/py3-windows-x86_64/pythonw.exe", "pythonw-64.exe", windows)


        def add_main_py(self):
            if self.build['renpy']:
                return

            self.add_file("web", "main.py", os.path.join(config.renpy_base, "renpy.py"))

        def mark_executable(self):
            """
            Marks files as executable.
            """

            for l in self.file_lists.values():
                for f in l:
                    for pat in self.build['xbit_patterns']:
                        if match(f.name, pat):
                            f.executable = True

                        if match("/" + f.name, pat):
                            f.executable = True

        def rename(self):
            """
            Rename files in all lists to match the executable names.
            """

            major_sh = py("renpy{major}.sh")

            def rename_one(fn):
                parts = fn.split('/')
                p = parts[0]

                if p == major_sh:
                    p = self.sh
                elif p == "renpy.sh":
                    p = self.sh
                elif p == "renpy.py":
                    p = self.py

                parts[0] = p
                return "/".join(parts)

            for l in self.file_lists.values():
                for f in l:
                    f.name = rename_one(f.name)

        def run(self, message, command, **kwargs):
            """
            Runs a command.
            """

            self.reporter.info(message)

            cmd = [ renpy.fsencode(i.format(**kwargs)) for i in command ]

            # print("\"" + "\" \"".join(cmd) + "\"")

            try:
                import sys, os
                isatty = os.isatty(sys.stdin.fileno())
            except Exception:
                isatty = False

            if isatty:
                subprocess.check_call(cmd)
            else:
                subprocess.check_call(cmd, stdout=self.log, stderr=subprocess.STDOUT)


        def sign_app(self, fl, appzip):
            """
            Signs the mac app contained in appzip.
            """

            if self.macapp:
                return self.rescan(fl, self.macapp)

            identity = self.build.get('mac_identity', None)

            if identity is None:
                return fl

            # Figure out where it goes.
            if appzip:
                dn = "sign.app-standalone"
            else:
                dn = "sign.app-crossplatform"

            dn = self.temp_filename(dn)

            if os.path.exists(dn):
                shutil.rmtree(dn)

            # Unpack the app.
            pkg = DirectoryPackage(dn)

            for i, f in enumerate(fl):
                self.reporter.progress(_("Unpacking the Macintosh application for signing..."), i, len(fl))

                if f.directory:
                    pkg.add_directory(f.name, f.path)
                else:
                    pkg.add_file(f.name, f.path, f.executable)

            pkg.close()

            # Sign the mac app.
            self.run(
                _("Signing the Macintosh application...\n(This may take a long time.)"),
                self.build["mac_codesign_command"],
                identity=identity,
                app=os.path.join(dn, self.app),
                entitlements=os.path.join(config.gamedir, "entitlements.plist"),
                )

            # Rescan the signed app.
            fl = self.rescan(fl, dn)

            return fl

        def make_dmg(self, volname, sourcedir, dmg):
            """
            Packages `sourcedir` as a dmg.
            """

            identity = self.build.get('mac_identity', None)

            if identity is None:
                identity = ''

            self.run(
                _("Creating the Macintosh DMG..."),
                self.build["mac_create_dmg_command"],
                identity=identity,
                volname=volname,
                sourcedir=sourcedir,
                dmg=dmg,
            )

            if self.build.get("mac_codesign_dmg_command", None):

                self.run(
                    _("Signing the Macintosh DMG..."),
                    self.build["mac_codesign_dmg_command"],
                    identity=identity,
                    volname=volname,
                    sourcedir=sourcedir,
                    dmg=dmg,
                )

        def workaround_mac_notarization(self, fl):
            """
            This works around mac notarization by compressing the unsigned,
            un-notarized, binaries in lib/py3-mac-universal.
            """

            fl = fl.copy()

            for f in fl:
                if py("/lib/py{major}-mac-universal/") in f.name:
                    with open(f.path, "rb") as inf:
                        data = inf.read()

                    tempfile = self.temp_filename(os.path.basename(f.name) + ".macho")

                    with open(tempfile, "wb") as outf:
                        outf.write(b"RENPY" + data)

                    f.name += ".macho"
                    f.path = tempfile

            return fl

        def prepare_file_list(self, format, file_lists):
            """
            Prepares a master list of files, given the format and file lists.
            This also takes care of the mac transforms, and signing the app
            if necessary.
            """

            macapp = (format in { "app-zip", "app-directory", "app-dmg" })
            key = (macapp, tuple(file_lists))

            if key in self.file_list_cache:
                return self.file_list_cache[key].copy()

            fl = FileList.merge([ self.file_lists[i] for i in file_lists ])
            fl = fl.copy()
            fl.sort()

            if self.build.get("exclude_empty_directories", True):
                fl = fl.filter_empty()

            fl = fl.add_missing_directories()

            if macapp:
                fl = fl.mac_transform(self.app, self.documentation_patterns)

            if not self.build["renpy"]:

                app, rest = fl.split_by_prefix(self.app)

                if app:
                    app = self.sign_app(app, macapp)

                    fl = FileList.merge([ app, rest ])

            self.file_list_cache[key] = fl
            return fl.copy()

        def make_package(self, variant, format, file_lists, dlc=False):
            """
            Creates a package file in the projects directory.

            `variant`
                The name of the variant to package. This is appended to the base name to become
                part of the file and directory names.

            `format`
                The format things will be packaged in. See the table of formats below.
            `file_lists`
                A string containing a space-separated list of file_lists to include in this
                package.

            `dlc`
                True if we want to build a non-update file in DLC mode.
            """
            filename = self.base_name + "-" + variant
            path = os.path.join(self.destination, filename)


            # A map from the name of the format, to the options that will be
            # used with it. The fields are:
            #
            # - The extension used.
            # - Is this a directory based format?
            # - Should the directory be turned into a dmg?
            # - Should a directory name be prepended?

            FORMATS = {
                "update" : (".update", False, False, False),

                "tar.bz2" : (".tar.bz2", False, False, True),
                "zip" : (".zip", False, False, True),
                "directory" : ("", True, False, False),
                "dmg" : ("-dmg", True, True, True),

                "app-zip" : (".zip", False, False, False),
                "app-directory" : ("-app", True, False, False),
                "app-dmg" : ("-app-dmg", True, True, False),

                "bare-tar.bz2" : (".tar.bz2", False, False, False),
                "bare-zip" : (".zip", False, False, False),
            }

            if format not in FORMATS:
                raise Exception("Format %r is unknown." % format)

            ext, directory, dmg, prepend = FORMATS[format]

            mac_identity = self.build.get('mac_identity', None)

            if dmg and (mac_identity is None):
                return

            if self.packagedest:
                path = self.packagedest

            fl = self.prepare_file_list(format, file_lists)

            # Write the update information.
            update_files = [ ]
            update_xbit = [ ]
            update_directories = [ ]

            for i in fl:
                if not i.directory:
                    update_files.append(i.name)
                else:
                    update_directories.append(i.name)

                if i.executable:
                    update_xbit.append(i.name)

            self.update_versions[variant] = fl.hash(self)

            update = { variant : { "version" : self.update_versions[variant], "base_name" : self.base_name, "files" : update_files, "directories" : update_directories, "xbit" : update_xbit } }

            update_fn = os.path.join(self.destination, filename + ".update.json")

            if self.include_update and (variant not in [ 'ios', 'android', 'source']) and (not format.startswith("app-")):

                with open(update_fn, "wb" if PY2 else "w") as f:
                    json.dump(update, f, indent=2)

                if (not dlc) or (format == "update"):
                    fl.append(File("update", None, True, False))
                    fl.append(File("update/current.json", update_fn, False, False))

            # If we're not an update file, prepend the directory.
            if (not dlc) and prepend:
                fl.prepend_directory(filename)

            # The path to the DMG, if we're going to make one.
            dmg_path = path + ".dmg"

            full_filename = filename + ext
            path += ext

            if self.build['renpy']:
                fl_hash = fl.hash(self)
            else:
                fl_hash = '<not building renpy>'

            file_hash, old_fl_hash = self.build_cache.get(full_filename, ("", ""))

            if (not directory) and (old_fl_hash == fl_hash) and not(self.build['renpy'] and (variant == "sdk")):

                if file_hash:
                    self.build_cache[full_filename] = (file_hash, fl_hash)

                return

            def done():
                """
                This is called when the build of the package is done, either
                in this thread or a background thread.
                """

                if self.include_update and not self.build_update and not dlc:
                    if os.path.exists(update_fn):
                        os.unlink(update_fn)

                if not directory:
                    file_hash = hash_file(path)
                else:
                    file_hash = ""

                if file_hash:
                    self.build_cache[full_filename] = (file_hash, fl_hash)

            if format == "tar.bz2" or format == "bare-tar.bz2":
                pkg = TarPackage(path, "w:bz2")
            elif format == "update":
                pkg = UpdatePackage(path, filename, self.destination)
            elif format == "zip" or format == "app-zip" or format == "bare-zip":
                if self.build['renpy']:
                    pkg = ExternalZipPackage(path)
                else:
                    pkg = ZipPackage(path)
            elif dmg:

                def make_dmg():
                    self.make_dmg(filename, path, dmg_path)
                    shutil.rmtree(path)

                pkg = DMGPackage(path, make_dmg)

                fl = self.workaround_mac_notarization(fl)

            elif directory:
                pkg = DirectoryPackage(path)

            # If we want to build in parallel.
            if self.build['renpy']:
                pkg = ParallelPackage(pkg, done, variant + "." + format)
                done = None

            for i, f in enumerate(fl):
                self.reporter.progress(_("Writing the [variant] [format] package."), i, len(fl), variant=variant, format=format)

                if f.directory:
                    pkg.add_directory(f.name, f.path)
                else:
                    if self.files_filter is not None and not self.files_filter.filter(f, variant, format):
                        # Ignore file
                        continue
                    pkg.add_file(f.name, f.path, f.executable)

            self.reporter.progress_done()


            if format == "update":
                # Build the zsync file.

                self.reporter.info(_("Making the [variant] update zsync file."), variant=variant)

            pkg.close()

            if done is not None:
                done()


        def finish_updates(self, packages):
            """
            Indexes the updates, then removes the .update files.
            """

            if not self.build_update:
                return

            index = { }

            if self.build['renpy']:
                index["monkeypatch"] = RENPY_PATCH

            def add_variant(variant):

                digest = self.build_cache[self.base_name + "-" + variant + ".update"][0]

                sums_size = os.path.getsize(self.destination + "/" + self.base_name + "-" + variant + ".sums")

                index[variant] = {
                    "version" : self.update_versions[variant],
                    "pretty_version" : self.pretty_version,
                    "digest" : digest,
                    "zsync_url" : self.base_name + "-" + variant + ".zsync",
                    "sums_url" : self.base_name + "-" + variant + ".sums",
                    "sums_size" : sums_size,
                    "json_url" : self.base_name + "-" + variant + ".update.json",
                    }

                fn = renpy.fsencode(os.path.join(self.destination, self.base_name + "-" + variant + ".update"))

                if os.path.exists(fn):
                    os.unlink(fn)

            for p in packages:
                if p["update"]:
                    add_variant(p["name"])

            fn = renpy.fsencode(os.path.join(self.destination, "updates.json"))
            with open(fn, "wb" if PY2 else "w") as f:
                json.dump(index, f, indent=2)


        def save_build_cache(self):
            if not self.build['renpy']:
                return

            fn = renpy.fsencode(os.path.join(self.destination, ".build_cache"))

            with open(fn, "w", encoding="utf-8") as f:
                for k, v in self.build_cache.items():
                    l = "\t".join([k, v[0], v[1]]) + "\n"
                    f.write(l)

        def load_build_cache(self):
            if not self.build['renpy']:
                return

            fn = renpy.fsencode(os.path.join(self.destination, ".build_cache"))

            if not os.path.exists(fn):
                return

            with open(fn, "rb") as f:
                for l in f:
                    if not l:
                        continue

                    l = l.decode("utf-8").rstrip()
                    l = l.split("\t")

                    self.build_cache[l[0]] = (l[1], l[2])

            os.unlink(fn)

        def dump(self):
            for k, v in sorted(self.file_lists.items()):
                print()
                print(k + ":")

                v.sort()

                for i in v:
                    print("   ", i.name, "xbit" if i.executable else "")

    class GuiReporter(object):
        """
        Displays progress using the gui.
        """

        def __init__(self):
            # The time at which we should next report progress.
            self.next_progress = 0

        def info(self, what, pause=False, **kwargs):
            if pause:
                interface.info(what, **kwargs)
            else:
                interface.processing(what, **kwargs)

        def progress(self, what, complete, total, **kwargs):

            if (complete > 0) and (time.time() < self.next_progress):
                return

            interface.processing(what, _("Processed {b}[complete]{/b} of {b}[total]{/b} files."), complete=complete, total=total, **kwargs)

            self.next_progress = time.time() + .05

        def progress_done(self):
            return


    class TextReporter(object):
        """
        Displays progress on the command line.
        """

        def info(self, what, pause=False, **kwargs):
            what = what.replace("[", "{")
            what = what.replace("]", "}")
            what = what.format(**kwargs)
            print(what)

        def progress(self, what, done, total, **kwargs):
            what = what.replace("[", "{")
            what = what.replace("]", "}")
            what = what.format(**kwargs)

            sys.stdout.write("\r{} - {} of {}".format(what, done + 1, total))
            sys.stdout.flush()

        def progress_done(self):
            sys.stdout.write("\n")


    def distribute_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("--destination", "--dest", default=None, action="store", help="The directory where the packaged files should be placed.")
        ap.add_argument("--packagedest", default=None, action="store", help="If given, gives the full path to the package file, without extensions." )
        ap.add_argument("--no-update", default=True, action="store_false", dest="build_update", help="Prevents updates from being built.")
        ap.add_argument("--package", action="append", help="If given, a package to build. Defaults to building all packages.")
        ap.add_argument("--no-archive", action="store_true", help="If given, files will not be added to archives.")
        ap.add_argument("--macapp", default=None, action="store", help="If given, the path to a signed and notarized mac app.")
        ap.add_argument("--format", default=None, action="store", help="The format of package to build.")

        ap.add_argument("project", help="The path to the project directory.")

        args = ap.parse_args()

        p = project.Project(args.project)

        if args.package:
            packages = args.package
        else:
            packages = None

        Distributor(p, destination=args.destination, reporter=TextReporter(), packages=packages, build_update=args.build_update, noarchive=args.no_archive, packagedest=args.packagedest, macapp=args.macapp, force_format=args.format)

        return False

    renpy.arguments.register_command("distribute", distribute_command)


    def update_old_game(project, reporter, compile):
        if compile:
            reporter.info(_("Recompiling all rpy files into rpyc files..."))
            project.launch([ "compile", "--keep-orphan-rpyc" ], wait=True)

        files = [fn + "c" for fn in project.script_files()
                 if fn.startswith("game/") and project.exists(fn + "c")]
        len_files = len(files)

        if not files:
            return

        TEMP_OLD_GAME_DIR = project.temp_filename("old-game")
        if os.path.isdir(TEMP_OLD_GAME_DIR):
            shutil.rmtree(TEMP_OLD_GAME_DIR)

        for i, src in enumerate(files):
            reporter.progress(_("Copying files..."), i, len_files)
            dst = project.temp_filename("old-" + src)
            try:
                os.makedirs(os.path.dirname(dst))
            except Exception:
                pass
            shutil.copyfile(os.path.join(project.path, src), dst)

        reporter.progress_done()

        OLD_GAME_DIR = os.path.join(project.path, "old-game")
        if os.path.isdir(OLD_GAME_DIR):
            shutil.rmtree(OLD_GAME_DIR)

        shutil.copytree(TEMP_OLD_GAME_DIR, OLD_GAME_DIR)

    def update_old_game_command():
        ap = renpy.arguments.ArgumentParser("Back-ups all rpyc files into old-game directory.")
        ap.add_argument("project", help="The path to the project directory.")

        args = ap.parse_args()

        update_old_game(project.Project(args.project), TextReporter(), True)

        return False

    renpy.arguments.register_command("update_old_game", update_old_game_command)

label distribute:

    python hide:

        data = project.current.data
        d = distribute.Distributor(project.current,
            reporter=distribute.GuiReporter(),
            packages=data['packages'],
            build_update=data['build_update'],
            open_directory=True,
            )


    jump post_build

label update_old_game:
    python hide:
        distribute.update_old_game(project.current, distribute.GuiReporter(), False)
    return
