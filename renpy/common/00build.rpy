# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

# Contains functions and variables that control the building of
# distributions.

init -1500 python in build:

    from store import config


    def make_file_lists(s):
        """
        Turns `s` into a (perhaps empty) list of file_lists.

        If `s` is a list or None, then returns it. If it's a string, splits
        it on whitespace. Otherwise, errors out.
        """

        if s is None:
            return s
        elif isinstance(s, list):
            return s
        elif isinstance(s, basestring):
            return s.split()

        raise Exception("Expected a string, list, or None.")



    def pattern_list(l):
        """
        Apply file_lists to the second argument of each tuple in a list.
        """

        rv = [ ]

        for pattern, groups in l:
            rv.append((pattern, make_file_lists(groups)))

        return rv

    # Patterns that are used to classify Ren'Py.
    renpy_patterns = pattern_list([
        ( "**~", None),
        ( "**/#*", None),
        ( "**/.*", None),
        ( "**.old", None),
        ( "**.new", None),
        ( "**.rpa", None),

        ( "**/*.pyc", None),

        ( "renpy.py", "all"),

        ( "renpy/", "all"),
        ( "renpy/**.py", "renpy"),
        ( "renpy/**.pyx", "renpy"),
        ( "renpy/**.pyd", "renpy"),
        ( "renpy/**.pxi", "renpy"),
        ( "renpy/common/", "all"),
        ( "renpy/common/_compat/**", "renpy"),
        ( "renpy/common/**.rpy", "renpy"),
        ( "renpy/common/**.rpym", "renpy"),
        ( "renpy/common/_compat/**", "renpy"),
        ( "renpy/common/**", "all"),
        ( "renpy/**", "all"),

        # Ignore Ren'Py and renpy.exe.
        ( "lib/*/renpy", None),
        ( "lib/*/renpy.exe", None),

        # Windows patterns.
        ( "lib/windows-i686/**", "windows"),

        # Linux patterns.
        ( "lib/linux-*/**", "linux"),

        # Mac patterns
        ( "lib/darwin-x86_64/**", "mac"),

        # Shared patterns.
        ( "/lib/**", "windows linux mac"),
        ( "renpy.sh", "linux mac"),
    ])

    def classify_renpy(pattern, groups):
        """
        Classifies files in the Ren'Py base directory according to pattern.
        """

        renpy_patterns.append((pattern, make_file_lists(groups)))

    # Patterns that are relative to the base directory.

    early_base_patterns = pattern_list([
        ("*.py", None),
        ("*.sh", None),
        ("*.app/", None),
        ("*.dll", None),
        ("*.manifest", None),

        ("lib/", None),
        ("renpy/", None),
        ("update/", None),
        ("common/", None),
        ("update/", None),

        ("icon.ico", None),
        ("icon.icns", None),
        ("project.json", None),

        ("log.txt", None),
        ("errors.txt", None),
        ("traceback.txt", None),
        ("image_cache.txt", None),
        ("text_overflow.txt", None),
        ("dialogue.txt", None),
        ("dialogue.tab", None),
        ("profile_screen.txt", None),
        ("files.txt", None),

        ("tmp/", None),
        ("game/saves/", None),
        ("game/bytecode.rpyb", None),

        ("archived/", None),
        ("launcherinfo.py", None),
        ("android.txt", None),

        (".android.json", "android"),
        ("android-*.png", "android"),
        ("android-*.jpg", "android"),
        ("ouya_icon.png", None),

        ("ios-presplash.*", "ios"),
        ("ios-launchimage.png", None),
        ("ios-icon.png", None),

        ("web-presplash.png", "web"),
        ("web-presplash.jpg", "web"),

        ])

    base_patterns = [ ]

    late_base_patterns = pattern_list([
        (".*", None),
        ("**", "all")
        ])

    def classify(pattern, file_list):
        """
        :doc: build

        Classifies files that match `pattern` into `file_list`.
        """

        base_patterns.append((pattern, make_file_lists(file_list)))

    def clear():
        """
        :doc: build

        Clears the list of patterns used to classify files.
        """

        base_patterns[:] = [ ]

    def remove(l, pattern):
        """
        Removes the pattern from the list.
        """

        l[:] = [ (p, fl) for i in l if p != pattern ]

    # Archiving.

    archives = [ ]

    def archive(name, file_list="all"):
        """
        :doc: build

        Declares the existence of an archive. If one or more files are
        classified with `name`, `name`.rpa is build as an archive. The
        archive is included in the named file lists.
        """

        archives.append((name, make_file_lists(file_list)))

    archive("archive", "all")

    # Documentation patterns.

    documentation_patterns = [ ]

    def documentation(pattern):
        """
        :doc: build

        Declares a pattern that matches documentation. In a mac app build,
        files matching the documentation pattern are stored twice - once
        inside the app package, and again outside of it.
        """

        documentation_patterns.append(pattern)

    xbit_patterns = [
        "**.sh",
        "**/*.so.*",
        "**/*.so",
        "**/*.dylib",

        "lib/**/python",
        "lib/**/pythonw",
        "lib/**/zsync",
        "lib/**/zsyncmake",

        "**.app/Contents/MacOS/*",

        "**.app/Contents/MacOS/lib/**/python",
        "**.app/Contents/MacOS/lib/**/pythonw",
        "**.app/Contents/MacOS/lib/**/zsync",
        "**.app/Contents/MacOS/lib/**/zsyncmake",
        ]

    def executable(pattern):
        """
        :doc: build

        Adds a pattern marking files as executable on platforms that support it.
        (Linux and Macintosh)
        """

        xbit_patterns.append(pattern)

    # Packaging.

    packages = [ ]

    def package(name, format, file_lists, description=None, update=True, dlc=False, hidden=False):
        """
        :doc: build

        Declares a package that can be built by the packaging
        tool.

        `name`
            The name of the package.

        `format`
            The format of the package. A string containing a space separated
            list of:

            zip
                A zip file.
            tar.bz2
                A tar.bz2 file.
            directory
                A directory containing the files.
            dmg
                A Macintosh DMG containing the files.
            app-zip
                A zip file containing a macintosh application.
            app-directory
                A directory containing the mac app.
            app-dmg
                A macintosh drive image containing a dmg. (Mac only.)

            The empty string will not build any package formats (this
            makes dlc possible).

        `file_lists`
            A list containing the file lists that will be contained
            within the package.

        `description`
            An optional description of the package to be built.

        `update`
            If true and updates are being built, an update will be
            built for this package.

        `dlc`
            If true, any zip or tar.bz2 file will be built in
            standalone DLC mode, without an update directory.

        `hidden`
            If true, this will be hidden from the list of packages in
            the launcher.
        """

        formats = format.split()

        for i in formats:
            if i not in [ "zip", "app-zip", "tar.bz2", "directory", "dmg", "app-directory", "app-dmg" ]:
                raise Exception("Format {} not known.".format(i))

        if description is None:
            description = name

        d = {
            "name" : name,
            "formats" : formats,
            "file_lists" : make_file_lists(file_lists),
            "description" : description,
            "update" : update,
            "dlc" : dlc,
            "hidden" : hidden,
            }

        packages.append(d)

    package("pc", "zip", "windows linux renpy all", "PC: Windows and Linux")
    package("linux", "tar.bz2", "linux renpy all", "Linux x86/x86_64")
    package("mac", "app-zip app-dmg", "mac renpy all", "Macintosh x86_64")
    package("win", "zip", "windows renpy all", "Windows x86")
    package("market", "zip", "windows linux mac renpy all", "Windows, Mac, Linux for Markets")
    package("steam", "zip", "windows linux mac renpy all", hidden=True)
    package("android", "directory", "android all", hidden=True, update=False, dlc=True)
    package("ios", "directory", "ios all", hidden=True, update=False, dlc=True)
    package("web", "zip", "web all", update=False, dlc=True)

    # Data that we expect the user to set.

    # A base name that's used to create the other names.
    name = None

    # The name of directories in the archives.
    directory_name = ""

    # The name of executables.
    executable_name = ""

    # A verbose name to include in package info.
    display_name = ""

    # Should we include update information into the archives?
    include_update = False

    # A verbose version to include in the update.
    version = None

    # Are we building Ren'Py?
    renpy = False

    # Should we exclude empty directories from the zip and tar files?
    exclude_empty_directories = True

    # The key used for google play.
    google_play_key = None

    # The salt used for google play.
    google_play_salt = None

    # The destination things are built in.
    destination = "{directory_name}-dists"

    # Should we allow the use of an integrated GPU on platforms that support
    # both discrete and integrated GPUs?
    allow_integrated_gpu = True

    # The itch.io project name.
    itch_project = None

    # Should we include the old Ren'Py themes?
    include_old_themes = True

    # The identity used for codesigning and dmg building.
    mac_identity = None

    # The command used for mac codesigning.
    mac_codesign_command = [ "/usr/bin/codesign", "--entitlements={entitlements}", "--options=runtime", "--timestamp", "-s", "{identity}", "-f", "--deep", "--no-strict", "{app}" ]

    # The command used to build a dmg.
    mac_create_dmg_command = [ "/usr/bin/hdiutil", "create", "-format", "UDBZ", "-volname", "{volname}", "-srcfolder", "{sourcedir}", "-ov", "{dmg}" ]

    # The command used to sign a dmg.
    mac_codesign_dmg_command = [ "/usr/bin/codesign", "--timestamp", "-s", "{identity}", "-f", "{dmg}" ]

    # Do we want to add the script_version file?
    script_version = True


    # This function is called by the json_dump command to dump the build data
    # into the json file.
    def dump():

        rv = { }

        excludes = [ ]

        if not include_old_themes:
            excludes.extend([
                ( "renpy/common/_compat/**", None),
                ( "renpy/common/_roundrect/**", None),
                ( "renpy/common/_outline/**", None),
                ( "renpy/common/_theme**", None),
            ])

        import sys

        if "_ssl" not in sys.modules:
            excludes.extend([
                ( "lib/**/_ssl.*", None),
            ])

        rv["directory_name"] = directory_name
        rv["executable_name"] = executable_name
        rv["include_update"] = include_update

        rv["packages"] = packages
        rv["archives"] = archives
        rv["documentation_patterns"] = documentation_patterns
        rv["base_patterns"] = early_base_patterns + base_patterns + late_base_patterns
        rv["renpy_patterns"] = excludes + renpy_patterns
        rv["xbit_patterns"] = xbit_patterns
        rv["version"] = version or directory_name
        rv["display_name"] = display_name or config.name or executable_name

        rv["exclude_empty_directories"] = exclude_empty_directories

        rv["allow_integrated_gpu"] = allow_integrated_gpu

        rv["renpy"] = renpy

        rv["script_version"] = script_version

        rv["destination"] = destination.format(
            directory_name=directory_name,
            executable_name=executable_name,
            display_name=display_name,
            version=rv["version"],
        )

        if google_play_key:
            rv["google_play_key"] = google_play_key

        if google_play_salt:
            rv["google_play_salt"] = google_play_salt

        if itch_project:
            rv["itch_project"] = itch_project

        if mac_identity:
            rv["mac_identity"] = mac_identity
            rv["mac_codesign_command"] = mac_codesign_command
            rv["mac_create_dmg_command"] = mac_create_dmg_command
            rv["mac_codesign_dmg_command"] = mac_codesign_dmg_command

        return rv

init 1500 python in build:

    if version is None:
        version = config.version

    if name is not None:

        if not directory_name:

            directory_name = name

            if config.version:
                directory_name += "-" + version

        if not executable_name:

            executable_name = name
