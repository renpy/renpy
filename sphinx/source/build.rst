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

    A zip file targeting Windows x86, Linux x86, and Linux x86_64.

Linux x86/x86_64

    A tar.bz2 file targeting Linux x86 and Linux x86_64.

Macintosh x86_64

    A zip file containing a Macintosh application targeting Macintosh
    OS X on Intel processors. Game data will be included inside the
    application, which appears to the user as a single file.

Windows x86

   A zip file targeting Windows x86.

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
inside an ``init python`` block.

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
   colons, and semicolons. If not set, it defaults to :var:`build.name`
   a dash, and :var:`config.version`.

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

icon.ico
    The icon that is used on Windows.

icon.icns
    The icon that is used on Macintosh.

These icon files much be in specific formats. You'll need to use a
program or web service (such as http://iconverticons.com/ ) to convert
them.

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
archive
    These files will be included in the archive.rpa archive.

Files that are not otherwise classified are placed in the "all" file
list.

To exclude files from distribution, classify them as None or the
empty string.

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
included twice in a Macintosh application—both inside and outside
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

    build.package("all-premium", "zip", "windows mac linux all bonus")

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

For example, the following will archive images in images.rpa, and
game scripts into scripts.rpa::

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
help others run your game on future platforms—platforms that may not
exist until after you're gone.


Build Functions
---------------

.. include:: inc/build

Advanced Configuration
----------------------

The following variables provide further control of the build process:

.. var:: build.exclude_empty_directories = True

    If true, empty directories (including directories left empty by
    file archiving) will be removed from generated packages. If false,
    empty directories will be included.

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

.. var:: build.allow_integrated_gpu = True

    Allows Ren'Py to run on the integrated GPU on platforms that have both
    integrated and discrete GPUs. Right now, this is only supported on Mac
    OS X.

.. var:: build.include_old_themes = True

    When true, files required to support themes that existed before Ren'Py
    6.99.9 will be included in the build. When false, such files are excluded.

    This is set to False when :func:`gui.init` is called.

.. var:: build.itch_project = None

    Setting this allows the Ren'Py launcher to upload your project to
    itch.io. This should be set to the name of a project registered
    with itch. (For example, "renpytom/the-question").

    Once this is set, after the distributions have been built, you can
    click "Build distributions", "Upload to itch.io" to cause an upload
    to occur.
