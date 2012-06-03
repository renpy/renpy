# This file contains code that manages the distribution of Ren'Py games 
# and Ren'Py proper.
#
# In this module, all files and paths are stored in unicode. Full paths
# might include windows path separators (\), but archive paths and names we
# deal with/match against use the unix separator (/).


init python in distribute:

    from store import config, persistent
    import store.project as project

    from change_icon import change_icons

    import sys
    import os
    import json
    import subprocess
    import hashlib

    # The default list of ignore patterns. The user should be able to 
    # add to this.
    IGNORE_PATTERNS = [
        ("**/.*", None),
        ("**/thumbs.db", None),
        ("thumbs.db", None),
        ("**~", None),
        ("**.bak", None),
        ("**.old", None),
        ("**.new", None),
        ("*/#*", None),
        ("#*", None),
        ]
    
    BASEDIR_PATTERNS = [
        ("*.py", None),
        ("*.sh", None),
        ("*.app/", None),
        ("*.dll", None),
        ("*.manifest", None),
        
        ("/lib/", None),
        ("/renpy/", None),
        ("/update/", None),
        ("/common/", None),
        ("/update/", None),
        
        ("/icon.ico", None),
        ("/icon.icns", None),
        ("manifest.xml", None),
        ("/archived/", None),
        ("/tmp/", None),
        ("/launcherinfo.py", None),
        ("/project.json", None),
            
        ("**", "all"),
        ]

    ENGINE_PATTERNS = [
        ( "**/*.pyc", None),
    
        ( "/renpy.py", "all"),
        ( "/renpy/**", "all"),
        ( "/common/**", "all"),

        # Windows-specific patterns.
        ( "/python*.dll", "windows" ),
        ( "/msvcr*.dll", "windows"),
        ( "/Microsoft.VC*.CRT.manifest", "windows"),
        ( "/lib/dxwebsetup.exe", "windows"),
        ( "/lib/windows-x86/**", "windows"),
        
        # Linux patterns. 
        ( "/renpy.sh", "linux"),
        ( "/lib/linux-x86/**", "linux"),
        ( "/lib/linux-x64/**", "linux"),
        ( "/lib/python", "linux"),
        
        # Mac patterns.
        ( "/renpy.app/Contents/Ren'Py Launcher", None),
        ( "/renpy.app/Contents/Info.plist", None),
        ( "/renpy.app/Contents/Resources/launcher.py", None),
        ( "/renpy.app/Contents/Resources/launcher.icns", None),
        ( "/renpy.app/**", "mac"),
        
        # Shared patterns.
        ( "/lib/", "windows linux"),
        ]
    
    # Patterns that match files that should be given the executable bit.
    XBIT_PATTERNS = [
        "renpy.sh",
        "lib/**/*.so.*",
        "lib/**/*.so",
        "lib/**/.dylib",
        "renpy.app/**/*.so.*",
        "renpy.app/**/*.so",
        "renpy.app/Contents/MacOS/*",
        "lib/python",
        "lib/**/python.real",
    ]
    
    import collections
    import os
    import io
    import re

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
                regexp += r'[^/]*'
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
        else:
            return False

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
            self.executable = False
            
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
                        
                # Make a copy.
                f = f.copy()
                
                f.name = app + "/Contents/Resources/autorun/" + f.name
                rv.append(f)
                
            rv.append(File(app + "/Contents/Resources/autorun", None, True, False))
            rv.sort()
    
            return rv


    class Distributor(object):
        """
        This manages the process of building distributions.
        """
        
        def __init__(self, project, destination=None, reporter=None):
    
            # The project we want to distribute.
            self.project = project
    
            # Map from file list name to file list.
            self.file_lists = collections.defaultdict(FileList)

            self.base_name = project.name
            self.executable_name = project.name
    
            # The destination directory.
            if destination is None:
                self.destination = persistent.projects_directory
            else:
                self.destination = destination

            # Status reporter.
            self.reporter = reporter

            # The platforms we can build for.
            self.linux = False
            self.mac = False
            self.windows = False
            self.all = True

            # The various executables, which change names based on self.executable_name.
            self.app = self.executable_name + ".app"
            self.exe = self.executable_name + ".exe"
            self.sh = self.executable_name + ".sh"
            self.py = self.executable_name + ".py"

            self.reporter.info(_("Scanning project files."))
            self.scan_and_classify(project.path, IGNORE_PATTERNS + BASEDIR_PATTERNS)

            self.reporter.info(_("Scanning Ren'Py files."))
            self.scan_and_classify(config.renpy_base, IGNORE_PATTERNS + ENGINE_PATTERNS)

            # Add the platform-specific files.
            self.add_mac_files()
            self.add_windows_files()

            # Assign the x-bit as necessary.
            self.mark_executable()

            # Rename the executable-like files.
            self.rename()

            # The time of the update version.
            self.update_version = int(time.time())

            # Create the normal packages.
            if self.linux:
                self.make_package("linux", "tar.bz2", "linux all")
            if self.windows:
                self.make_package("windows", "zip", "windows all")
            if self.mac:
                self.make_package("mac", "zip", "mac all", mac_transform=True)
            if self.all:
                self.make_package("all", "zip", "linux windows mac all")

            # Create the update packages.
            if self.linux:
                self.make_package("linux", "update", "linux all")
            if self.windows:
                self.make_package("windows", "update", "windows all")
            if self.mac:
                self.make_package("mac", "update", "mac all")
            if self.all:
                self.make_package("all", "update", "linux windows mac all")

            self.finish_updates()


        def scan_and_classify(self, directory, patterns):
            """
            Walks through the `directory`, finds files and directories that
            match the pattern, and assds them to the appropriate file list. 
            
            `patterns`
                A list of pattern, file_list tuples. The pattern is a string
                that is matched using match. File_list is either
                a space-separated list of file lists to add the file to, 
                or None to ignore it.
            
                Directories are matched with a trailing /, but added to the 
                file list with the trailing / removed.
            """
            
            def walk(name, path):
                is_dir = os.path.isdir(path)

                if is_dir:
                    match_name = "/" + name + "/"
                else:
                    match_name = "/" + name

                for pattern, file_list in patterns:
                    if match(match_name, pattern):
                        break
                else:
                    pattern = None
                    file_list = None
                    
                if file_list is None:
                    return

                for fl in file_list.split():
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

        def temp_filename(self, name):
            self.project.make_tmp()
            return os.path.join(self.project.tmp, name)

        def add_file(self, file_list, name, path):
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
        
            f = File(name, path, False, False)
        
            for fl in file_list.split():
                self.file_lists[fl].append(f)
                
        def add_mac_files(self):
            """
            Add mac-specific files to the distro.
            """
            
            # Rename the executable.
            self.add_file("mac", "renpy.app/Contents/MacOS/" + self.executable_name, "renpy.app/Contents/MacOS/Ren'Py Launcher")
            
            # Update the plist file.
            quoted_name = self.executable_name.replace("&", "&amp;").replace("<", "&lt;")
            fn = self.temp_filename("Info.plist")
            
            with io.open(os.path.join(config.renpy_base, "renpy.app/Contents/Info.plist"), "r", encoding="utf-8") as old:
                data = old.read()
                
            data = data.replace("Ren'Py Launcher", quoted_name)
                
            with io.open(fn, "w", encoding="utf-8") as new:
                new.write(data)
                
            self.add_file("mac", "renpy.app/Contents/Info.plist", fn)

            # Update the launcher script.            
            quoted_name = self.executable_name.replace("\"", "\\\"")
            fn = self.temp_filename("launcher.py")
            
            with io.open(os.path.join(config.renpy_base, "renpy.app/Contents/Resources/launcher.py"), "r", encoding="utf-8") as old:
                data = old.read()
                
            data = data.replace("Ren'Py Launcher", quoted_name)
                
            with io.open(fn, "w", encoding="utf-8") as new:
                new.write(data)
                
            self.add_file("mac", "renpy.app/Contents/Resources/launcher.py", fn)

            # Icon file.
            custom_fn = os.path.join(self.project.path, "icon.icns")
            default_fn = os.path.join(config.renpy_base, "renpy.app/Contents/Resources/launcher.icns")
            
            if os.path.exists(custom_fn):
                self.add_file("mac", "renpy.app/Contents/Resources/launcher.icns", custom_fn)
            else:
                self.add_file("mac", "renpy.app/Contents/Resources/launcher.icns", default_fn)

        def add_windows_files(self):
            """
            Adds windows-specific files.
            """
            
            icon_fn = os.path.join(self.project.path, "icon.ico")
            old_exe_fn = os.path.join(config.renpy_base, "renpy.exe")
            
            if os.path.exists(icon_fn):
                exe_fn = self.temp_filename("renpy.exe")

                with open(exe_fn, "wb") as f:                    
                    f.write(change_icons(old_exe_fn, icon_fn))

            else:
                exe_fn = old_exe_fn
            
            self.add_file("windows", "renpy.exe", exe_fn) 

        def mark_executable(self):
            """
            Marks files as executable.
            """
            
            for l in self.file_lists.values():
                for f in l:
                    for pat in XBIT_PATTERNS:                        
                        if match(f.name, pat):    
                            f.executable = True

        def rename(self):
            """
            Rename files in all lists to match the executable names.
            """
            
            def rename_one(fn):
                parts = fn.split('/')
                p = parts[0]
                
                if p == "renpy.app":
                    p = self.app
                elif p == "renpy.exe":
                    p = self.exe
                elif p == "renpy.sh":
                    p = self.sh
                elif p == "renpy.py":
                    p = self.py
                    
                parts[0] = p
                return "/".join(parts)
            
            for l in self.file_lists.values():
                for f in l:
                    f.name = rename_one(f.name)

        def make_package(self, variant, format, file_lists, mac_transform=False):
            """
            Creates a package file in the projects directory. 

            `variant`
                The name of the variant to package. This is appended to the base name to become
                part of the file and directory names.

            `format`
                The format things will be packaged in. This should be one of "zip", "tar.bz2", or 
                "update". 
            
            `file_lists`
                A string containing a space-separated list of file_lists to include in this 
                package.
                        
            `mac_transform`
                True if we should apply the mac transform to the filenames before including 
                them.
            """
            
            fl = FileList.merge([ self.file_lists[i] for i in file_lists.split() ])
            fl = fl.copy()
            fl.sort()

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
                    
            update = { variant : { "version" : self.update_version, "files" : update_files, "directories" : update_directories, "xbit" : update_xbit } }

            update_fn = self.temp_filename("current.json")
            with open(update_fn, "w") as f:
                json.dump(update, f)
            
            fl.append(File("update", None, True, False))
            fl.append(File("update/current.json", update_fn, False, False))
            
            # The mac transform.
            if mac_transform:
                fl.mac_transform(self.app, [])
            
            # If we're not an update file, prepend the directory.

            if format != "update":
                filename = self.base_name + "-" + variant
                fl.prepend_directory(filename)
            else:
                filename = variant

            filename = os.path.join(self.destination, filename)
            
            if format == "tar.bz2":
                filename += ".tar.bz2"
                pkg = TarPackage(filename, "w:bz2")
            elif format == "update":
                filename += ".update"
                pkg = TarPackage(filename, "w", notime=True)
            elif format == "zip":
                filename += ".zip"
                pkg = ZipPackage(filename)
                
            for i, f in enumerate(fl):
                self.reporter.progress(variant + " " + format, i, len(fl))
                        
                if f.directory:
                    pkg.add_directory(f.name, f.path)
                else:
                    pkg.add_file(f.name, f.path, f.executable)

            self.reporter.progress_done()
            pkg.close()


            if format == "update":
                # Build the zsync file.
                # TODO: This should use an included copy of zsyncmake.
                self.reporter.info(_("Making zsync file."))
                subprocess.check_call([ 
                    "zsyncmake", 
                    "-z", renpy.fsencode(filename), 
                    "-u", variant + ".update.gz", 
                    "-o", renpy.fsencode(os.path.join(self.destination, variant + ".zsync")) ])

        def finish_updates(self):
            """
            Indexes the updates, then removes the .update files.
            """
            
            index = { }
            
            def add_variant(variant):
                fn = renpy.fsencode(os.path.join(self.destination, variant + ".update"))
                with open(fn, "rb") as f:
                    digest = hashlib.sha256(f.read()).hexdigest()
                    
                index[variant] = { "version" : self.update_version, "digest" : digest }
                
                os.unlink(fn)

            if self.linux:
                add_variant("linux")
                
            if self.windows:
                add_variant("windows")
                
            if self.mac:
                add_variant("mac")
                
            if self.all:
                add_variant("all")
                
            fn = renpy.fsencode(os.path.join(self.destination, "updates.json"))
            with open(fn, "wb") as f:
                json.dump(index, f)


        def dump(self):
            for k, v in sorted(self.file_lists.items()):
                print
                print k + ":"

                v.sort()

                for i in v:
                    print "   ", i.name, "xbit" if i.executable else ""


    class TextReporter(object):
        """
        Displays progress on the command line.
        """
        
        def info(self, msg):
            print msg
            
        def progress(self, what, done, total):
            sys.stdout.write("\rWriting {}: {} of {}".format(what, done, total))
            sys.stdout.flush()
            
        def progress_done(self):
            print
        

    def distribute_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("project", help="The path to the project directory.")
        ap.add_argument("--destination", default=None, action="store", help="The directory where the packaged files should be placed.")

        args = ap.parse_args()
        
        p = project.Project(args.project)
        
        Distributor(p, destination=args.destination, reporter=TextReporter())
        
        return False
        
    renpy.arguments.register_command("distribute", distribute_command)
            
label distribute:

    $ distribute.Distributor(project.current)

    jump front_page
    

 
        
    
    
