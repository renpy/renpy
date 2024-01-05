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

# Contains functions and variables that control the building of
# distributions.

init -1500 python in build:
    # Do not participate in saves.
    _constant = True

    from store import config, store

    import sys, os

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


    renpy_sh = "renpy.sh"

    if PY2:
        renpy_patterns = pattern_list([
            ("renpy/**.pyo", "all"),
            ("renpy/**__pycache__", None),
        ])

        if os.path.exists(os.path.join(config.renpy_base, "renpy2.sh")):
            renpy_sh = "renpy2.sh"

    else:
        renpy_patterns = pattern_list([
            ("renpy/**__pycache__/**.{}.pyc".format(sys.implementation.cache_tag), "all"),
            ("renpy/**__pycache__", "all"),
        ])

        if os.path.exists(os.path.join(config.renpy_base, "renpy3.sh")):
            renpy_sh = "renpy3.sh"


    # Patterns that are used to classify Ren'Py.
    renpy_patterns.extend(pattern_list([
        ( "**~", None),
        ( "**/#*", None),
        ( "**/.*", None),
        ( "**.old", None),
        ( "**.new", None),
        ( "**.rpa", None),

        ( "**/steam_appid.txt", None),

        ( "renpy.py", "all"),

        ( "renpy/", "all"),
        ( "renpy/**.py", "renpy"),

        # Ignore Cython source files.
        ( "renpy/**.pxd", None),
        ( "renpy/**.pxi", None),
        ( "renpy/**.pyx", None),

        # Ignore legacy Python bytcode files (unless allowed above).
        ( "renpy/**.pyc", None),
        ( "renpy/**.pyo", None),

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
        ( "lib/*/pythonw.exe", None),

        # Ignore the wrong Python.
        ( "lib/py3-*/" if PY2 else "lib/py2-*/", None),

        # Windows patterns.
        ( "lib/py*-windows-i686/**", "windows_i686"),
        ( "lib/py*-windows-x86_64/**", "windows"),

        # Linux patterns.
        ( "lib/py*-linux-i686/**", "linux_i686"),
        ( "lib/py*-linux-aarch64/**", "linux_arm"),
        ( "lib/py*-linux-armv7l/**", "linux_arm"),
        ( "lib/py*-linux-*/**", "linux"),

        # Mac patterns.
        ( "lib/py*-mac-*/**", "mac"),

        # Old Python library.
        ( "lib/python3.*/**" if PY2 else "lib/python2.*/**", None),

        # Shared patterns.
        ( "lib/**", "windows linux mac android ios"),
        ( renpy_sh, "linux mac"),
    ]))


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
        ("*.keystore", None),
        ("update.pem", None),

        ("lib/", None),
        ("renpy/", None),
        ("update/", None),
        ("common/", None),
        ("update/", None),

        ("old-game/", None),
        ("base/", None),

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
        ("memory.txt", None),

        ("tmp/", None),
        ("game/saves/", None),
        ("game/bytecode.rpyb", None),

        ("archived/", None),
        ("launcherinfo.py", None),
        ("android.txt", None),

        ("game/presplash*.*", "all"),

        ("android.json", "android"),
        (".android.json", "android"),
        ("android-*.png", "android"),
        ("android-*.jpg", "android"),
        ("ouya_icon.png", None),

        ("ios-presplash.*", "ios"),
        ("ios-launchimage.png", None),
        ("ios-icon.png", None),

        ("web-presplash.png", "web"),
        ("web-presplash.jpg", "web"),
        ("web-presplash.webp", "web"),
        ("web-icon.png", "web"),
        ("progressive_download.txt", "web"),

        ("steam_appid.txt", None),

        ("game/" + renpy.script.BYTECODE_FILE, "all"),
        ("game/cache/bytecode-311.rpyb", "web"),
        ("game/cache/bytecode-*.rpyb", None),
        ("game/cache/build_info.json", None),
        ("game/cache/build_time.txt", None),

    ])


    base_patterns = [ ]

    late_base_patterns = pattern_list([
        (".*", None),
        ("**", "all")
        ])

    def classify(pattern, file_list):
        """
        :doc: build

        Classifies files that match `pattern` into `file_list`, which can
        also be an archive name.

        If the name given as `file_list` doesn't exist as an archive or file
        list name, it is created and added to the set of valid file lists.
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

        l[:] = [ (p, fl) for p, fl in l if p != pattern ]

    # Archiving.

    archives = [ ]

    def archive(name, file_list="all"):
        """
        :doc: build

        Declares the existence of an archive, whose `name` is added to the
        list of available archive names, which can be passed to
        :func:`build.classify`.

        If one or more files are classified with `name`, `name`.rpa is
        built as an archive, and then distributed in packages including
        the `file_list` given here. ::

            build.archive("secret", "windows")

        If any file is included in the "secret" archive using the
        :func:`build.classify` function, the file will be included inside
        the secret.rpa archive in the windows builds.

        As with the :func:`build.classify` function, if the name given as
        `file_list` doesn't exist as a file list name, it is created and
        added to the set of valid file lists.
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

        "lib/py*-linux-*/*",
        "lib/py*-mac-*/*",

        "**.app/Contents/MacOS/*",
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

    def package(name, format, file_lists, description=None, update=True, dlc=False, hidden=False, update_only=False):
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
                A zip file containing a macintosh application. This format
                doesn't support the Ren'Py updater.
            app-directory
                A directory containing the mac app. This format
                doesn't support the Ren'Py updater.
            app-dmg
                A macintosh drive image containing a dmg. (Mac only.) This format
                doesn't support the Ren'Py updater.
            bare-zip
                A zip file without :var:`build.directory_name`
                prepended.
            bare-tar.bz2
                A zip file without :var:`build.directory_name`
                prepended.
            null
                Used to produce only updates, without the main package.

            The empty string will not build any package formats (this
            makes dlc possible).

        `file_lists`
            A list containing the file lists that will be included
            in the package.

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
            if i not in { "zip", "app-zip", "tar.bz2", "directory", "dmg", "app-directory", "app-dmg", "bare-zip", "bare-tar.bz2", "null" }:
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

        global packages
        packages = [ i for i in packages if i["name"] != name ]

        packages.append(d)

    package("gameonly", "null", "all", "Game-Only Update for Mobile", hidden=True)

    package("pc", "zip", "windows linux renpy all", "PC: Windows and Linux")
    package("linux", "tar.bz2", "linux linux_arm renpy all", "Linux")
    package("mac", "app-zip app-dmg", "mac renpy all", "Macintosh")
    package("win", "zip", "windows renpy all", "Windows")
    package("market", "bare-zip", "windows linux mac renpy all", "Windows, Mac, Linux for Markets")

    package("steam", "zip", "windows linux mac renpy all", hidden=True)
    package("android", "directory", "android all", hidden=True, update=False, dlc=True)
    package("ios", "directory", "ios all", hidden=True, update=False, dlc=True)
    package("web", "zip", "web renpy all", hidden=True, update=False, dlc=True)

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

    # Maps from files to itch.io channels.
    itch_channels = {
        "*-all.zip" : "win-osx-linux",
        "*-market.zip" : "win-osx-linux",
        "*-pc.zip" : "win-linux",
        "*-win.zip" : "win",
        "*-mac.zip" : "osx",
        "*-linux.tar.bz2" : "linux",
        "*-release.apk" : "android",
    }

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

    # Additional or Override keys to add to the Info.plist.
    mac_info_plist = { }

    # Do we want to add the script_version file?
    script_version = True

    # A list of file lists to merge.
    merge = [ ]

    # Do we want to include the i686 binaries?
    include_i686 = True

    # Do we want to change the icon on the i686 binaries?
    change_icon_i686 = True

    # A list of additional android permission names.
    android_permissions = [ ]

    # Should the sdk-fonts directory be renamed to game?
    _sdk_fonts = False

    # Which update formats should be built?
    update_formats = [ "rpu" ]

    # Should the gameonly update be available?
    game_only_update = False

    # The time at which the game was built.
    time = store.renpy.game.build_info.get("time", None)

    # Information about the game that is stored in cache/build_info.json.
    info = store.renpy.game.build_info.get("info", { })

    # This function is called by the json_dump command to dump the build data
    # into the json file.
    def dump():
        import time

        global include_update

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

        if game_only_update:

            include_update = True

            for i in packages:
                if i["name"] == "gameonly":
                    i["hidden"] = False

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

        rv["itch_channels"] = itch_channels

        if mac_identity:
            rv["mac_identity"] = mac_identity
            rv["mac_codesign_command"] = mac_codesign_command
            rv["mac_create_dmg_command"] = mac_create_dmg_command
            rv["mac_codesign_dmg_command"] = mac_codesign_dmg_command

        rv["mac_info_plist"] = mac_info_plist

        rv["merge"] = list(merge)

        if include_i686:
           rv['merge'].append(("linux_i686", "linux"))
           rv['merge'].append(("windows_i686", "windows"))

        rv["include_i686"] = include_i686
        rv["change_icon_i686"] = change_icon_i686

        rv["android_permissions"] = android_permissions

        rv["_sdk_fonts"] = _sdk_fonts

        rv["update_formats"] = update_formats

        rv["info"] = {
            "info" : info,
            "time" : time.time(),
            "name" : config.name,
            "version" : config.version,
            }

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
