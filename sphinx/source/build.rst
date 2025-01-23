Building Distributions
======================

Ren'Py includes support for building game distributions. Upon choosing
"Build Distributions" in the launcher, Ren'Py will scan itself and the
project to determine the files to include in the distribution, will
create any archives that are necessary, and will build package and
update files.

With no configuration, Ren'Py is able to build the following kinds of
packages:

PC: Windows and Linux
    A zip file targeting Windows x86_64 and Linux x86_64

Linux
    A tar.bz2 file targeting Linux x86_64. This will also include
    the 32-bit and 64-bit ARM version of Ren'Py, if present. (These
    are found in the sdkarm Ren'Py package.)

Macintosh
    A zip file containing a Macintosh application targeting macOS
    OS X on Intel and Apple Silicon processors. Game data will be
    included inside the application, which appears to the user
    as a single file. The updater does not work with this package.

Windows
    A zip file targeting Windows x86_64.

Windows, Mac, and Linux for Markets
    A distribution that contains the information required to run on
    software markets like itch.io and Steam. This isn't meant to be
    run directly (and probably won't work on the Mac), but should be
    fed to the app store upload process.

.. warning::

    The zip and tar.bz2 files that Ren'Py produces contain permissions
    information that must be present for Ren'Py to run on Linux and
    Macintosh.

    Unpacking and re-packing a zip file on Windows and then running it
    on Linux or Macintosh is not supported.

Basic Configuration
-------------------

The build process can be configured by setting variables and calling
function that live in the build namespace. This must be done from
inside an ``init python`` block. The default settings for these configurations are
set in :file:`options.rpy`.

There are a few basic variables and functions that many games will
use.

.. var:: build.name = "..."

    This is used to automatically generate build.directory_name
    and build.executable_name, if neither is set. This should not
    contain spaces, colons, or semicolons.

.. var:: build.directory_name = "..."

    This is used to create the names of directories in the archive
    files. For example, if this is set to "mygame-1.0", the Linux
    version of the project will unpack to "mygame-1.0-linux".

    This is also used to determine the name of the directory in
    which the package files are placed. For example, if you set
    build.directory_name to mygame-1.0, the archive files will
    be placed in mygame-1.0-dists in the directory above the base
    directory.

    This variable should not contain special characters like spaces,
    colons, and semicolons. If not set, it defaults to :var:`build.name`,
    a dash, and the version. The version is taken from :var:`build.version`,
    if set, or :var:`config.version`.

.. var:: build.executable_name = "..."

    This variable controls the name of the executables that the user
    clicks on to start the game.

    This variable should not contain special characters like spaces,
    colons, and semicolons. If not set, it defaults to :var:`build.name`.

    For example, if this is set to "mygame", the user will be able
    to run mygame.exe on Windows, mygame.app on Macintosh, and
    mygame.sh on Linux.

.. _special-files:

Special Files
-------------

There are two files that can be included in your game's base directory
to customize the build.

:file:`icon.ico`
    The icon that is used on Windows.

:file:`icon.icns`
    The icon that is used on Macintosh.

These icon files must be in specific formats. You'll need to use a
program or web service (such as https://anyconv.com/png-to-ico-converter/ and
https://anyconv.com/png-to-icns-converter/ ) to convert them.

Classifying and Ignoring Files
------------------------------

The build process works by first classifying files in the Ren'Py
distribution and your game into file lists. These file lists are then
added to package files.

The classification is done by the build.classify function. It takes a
patterns and a space-separated list of filenames. Patterns are matched
from first to last, with the first match taking precedence (even if a
more-specific pattern follows.) Patterns are matched with and without
a leading /. Patterns may include the following special characters:

/
   The directory separator.
\*
   Matches all characters except for the directory separator.
\*\*
   Matches all characters.

For example:

\*\*.txt
    Matches all txt files.
game/\*.txt
    Matches txt files in the game directory.

There are seven file lists that files can be classified into by
default. (Ren'Py places its own files into the first six of these.)

all
    These files will be included in all packages, and in Android
    builds.
linux
    These files will be included in packages targeting Linux.
mac
    These files will be included in packages targeting Macintosh.
windows
    These files will be included in packages targeting Windows.
renpy
    These files will be included in packages that require the Ren'Py
    engine files. (Linux, Macintosh, and Windows.)
android
    These files will be included in Android builds.

This set of valid file lists can be expanded by passing
:func:`build.classify` new names as its ``file_list`` argument.

Files can also be classified in archives. By default, the "archive"
archive is declared:

archive
    These files will be included in the archive.rpa archive.

The set of archives can also be expanded, using the :func:`build.archive`
function.

Files that are not otherwise classified are placed in the "all" file
list.

To exclude files from distribution, classify them as None or the
empty string. In this case, \* and \*\* at the end of the pattern
must match at least one character.

For example::

    # Include README.txt
    build.classify("README.txt", "all")

    # But exclude all other txt files.
    build.classify("**.txt", None)

    # Add png and jpg files in the game directory into an archive.
    build.classify("game/**.png", "archive")
    build.classify("game/**.jpg", "archive")

Documentation
-------------

Calling the build.documentation function with patterns marks files
matching those patterns as documentation. Documentation files are
included twice in a Macintosh application – both inside and outside
of the application itself.

For example, to mark all txt and html files in the base directory as
documentation, call::

    build.documentation("*.txt")
    build.documentation("*.html")

.. _packages:

Packages
--------

It's also possible to add new types of packages to the Ren'Py build
process. This is done by calling the build.package function with a
package name, type, and a string containing the file lists to
include.

Say we wanted to build a normal version of our game, and one
containing bonus material. We could classify the bonus files in to a
"bonus" file list, and then declare an all-premium package with::

    # Declare a new archive belonging to a new "bonus" file list.
    build.archive("bonus_archive", "bonus")

    # Put the bonus files into the new archive.
    build.classify("game/bonus/**", "bonus_archive")

    # Declare the package.
    build.package("all-premium", "zip", "windows mac linux renpy all bonus")

Supported package types are "zip" and "tar.bz2" to generate files in
those formats, and "directory" to create a directory filled with
files.

Archives
--------

Ren'Py supports combining files into a simple archive format. While
not very secure, this protects files from casual copying.

By default, all files classified into the "archive" file list will be
placed in an archive.rpa archive, which is included in the all file
list.

By calling build.archive, it's possible to declare a new archives and
the file lists they will be included in. (It's rare to use anything
but the all file list, however.) To use an archive, classify files
into a list with its name.

For example, the following will archive images in :file:`images.rpa`, and
game scripts into :file:`scripts.rpa`::

    # Declare two archives.
    build.archive("scripts", "all")
    build.archive("images", "all")

    # Put script files into the scripts archive.
    build.classify("game/**.rpy", "scripts")
    build.classify("game/**.rpyc", "scripts")

    # Put images into the images archive.
    build.classify("game/**.jpg", "images")
    build.classify("game/**.png", "images")

If an archive file is empty, it will not be built.

Please think twice about archiving your game. Keeping files open will
help others run your game on future platforms – platforms that may not
exist until after you're gone.

.. _old-game:

The Old-game Directory
----------------------

When making multiple releases, like when a game is distributed through
early access or platforms like Patreon, it's necessary to keep the
old .rpyc files around. The .rpyc files contain information that is
necessary to ensure that saves can be loaded, and omitting these
files can cause problems.

At the same time, Ren'Py will update the .rpyc files in the game
directory when these files are changed, making the files unsuitable
for inclusion in version control.

To solve this problem, Ren'Py allows you to place the .rpyc files from
a previous distribution into the old-game directory, which is alongside
the game directory. The directory structure of :file:`old-game/` should match
the directory structure of :file:`game/`. For example, :file:`game/scripts/day1.rpyc`
should be moved to :file:`old-game/scripts/day1.rpyc`. Files in old-game that are
not .rpyc files are ignored.

The advantage of using old-game is that the old-game .rpyc files can be
checked in, and that Ren'Py will always start from a known source when
generating .rpyc files. While this might not be necessary for a
single-developer game with minor changes, old-game is useful for large
multiple developer games.

More information about how .rpyc files help with loading saves into changed
games can be found at:

* `Under the hood: .rpyc files <https://www.patreon.com/posts/under-hood-rpyc-23035810>`_
* `Ren'Py developer update: February 2021 <https://www.patreon.com/posts/renpy-developer-48146908>`_


Requirements
------------

Some stores ask the requirements for Ren'Py applications to run. While
this varies from game to game, here's a set of minimums for a generic
visual novel.

**Windows**

* Version: Windows 7 or higher.
* CPU: 2.0 Ghz 64-bit Intel-compatible
* RAM: 2.0 GB
* Graphics: OpenGL 3.0 or DirectX 11

**macOS**

* Version: 10.10+
* CPU: 2.0 Ghz 64-bit Intel-compatible (Apple silicon supported through Rosetta 2)
* RAM: 2.0 GB
* Graphics: OpenGL 3.0

**Linux**

* Version: Ubuntu 16.04+
* CPU: 2.0 Ghz 64-bit Intel-compatible
* RAM: 2.0 GB
* Graphics: OpenGL 3.0

The amount of disk space required is entirely determined by the assets in your
game, and the amount of CPU and RAM needed may also vary. Ren'Py will also run
under OpenGL 2 with certain extensions available.


Build Functions
---------------

.. include:: inc/build

Build Info
----------

There are two variables that can be used to provide information about
the build. This information is used to generate the game/cache/build_info.json
file, which is loaded as Ren'Py starts.

.. var:: build.time = None

    This variable defaults to None, but if your game has been built,
    it will be set to the time the game was built, in seconds since
    January 1, 1970.

.. var:: build.info = { }

    This variable lets you store information that will be placed into
    the game/cache/build_info.json file in the built game. When the built
    game starts, game/cache/build_info.json is loaded and the contents
    placed into this variable.

    Generally, you'll want to check that a field does not exist, and
    set it, using setdefault.

    For example, this stores the name of the computer that built the
    game in the build_info.json file::

        python hide:
            import socket
            build.info.setdefault("build_host", socket.gethostname())

    The information in this variable needs to be of types that can be
    placed in JSON files. (That is, None, booleans, strings,
    numbers, lists, and dictionaries)


Advanced Configuration
----------------------

The following variables provide further control of the build process:

.. var:: build.allow_integrated_gpu = True

    Allows Ren'Py to run on the integrated GPU on platforms that have both
    integrated and discrete GPUs. Right now, this is only supported on Mac
    OS X.

.. var:: build.destination = "{directory_name}-dists"

    Gives the path to the directory the archive files will be placed in. This
    may be an absolute or a relative path. A relative path is considered to
    be relative to the projects directory.

    The following values are substituted in using Python's ``str.format`` function.

    ``{directory_name}``
        The value of build.directory_name.

    ``{executable_name}``
        The value of build.executable_name.

    ``{version}``
        The value of build.version.

.. var:: build.change_icon_i686 = True

    If True, and icon.ico exists, the icon of the 32-bit Windows executable
    will be changed. If False, the icon will not be changed. Setting this
    to False may prevent some antivirus programs from producing a false
    positive for your game.

.. var:: build.exclude_empty_directories = True

    If true, empty directories (including directories left empty by
    file archiving) will be removed from generated packages. If false,
    empty directories will be included.


.. var:: build.game_only_update = False

    If true, :var:`build.include_update` is enabled, and
    the "Game-Only Update for Mobile" package becomes available.


.. var:: build.include_i686 = True

    If true, files necessary to run on 32-bit x86 processors will be included
    in the Linux and Mac builds. If False, these files will not be included.

.. var:: build.include_old_themes = True

    When true, files required to support themes that existed before Ren'Py
    6.99.9 will be included in the build. When false, such files are excluded.

    This is set to False when :func:`gui.init` is called.

.. var:: build.include_update = False

    When true, Ren'Py will produce the files required for the :doc:`updater <updater>`
    to work.

.. var:: build.itch_project = None

    Setting this allows the Ren'Py launcher to upload your project to
    itch.io. This should be set to the name of a project registered
    with itch. (For example, "renpytom/the-question").

    Once this is set, after the distributions have been built, you can
    click "Build distributions", "Upload to itch.io" to cause an upload
    to occur.

.. var:: build.itch_channels = { ... }

    This maps a filename pattern (such as "\*-win.zip") to a string giving
    the itch channel the file should be uploaded to. This defaults to::

        {
            "*-all.zip" : "win-osx-linux",
            "*-market.zip" : "win-osx-linux",
            "*-pc.zip" : "win-linux",
            "*-win.zip" : "win",
            "*-mac.zip" : "osx",
            "*-linux.tar.bz2" : "linux",
            "*-release.apk" : "android",
        }

.. var:: build.mac_info_plist = { }

    This is a dictionary mapping strings to strings, that can be used to
    add or override keys in the mac's Info.plist file.

.. var:: build.update_formats = [ "rpu" ]

    This is a list of formats that the updater will build. The default,
    "rpu" is supported from Ren'Py 7.7 and 8.2 on. If you need to support
    updating using the earlier zsync-based updates, add "zsync' to the
    list.

.. var:: build.version = None

    Gives a version of the build used by the build process. If None, this defaults to config.version. The main use
    of this is to allow config.version to have characters that are not valid in file or directory names.
