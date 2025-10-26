.. highlight:: text

======================
Command Line Interface
======================

Ren'Py includes a command line interface (CLI) that can be used to automate
some development tasks, allowing for continuous integration and for scripting
releases. For most purposes, this isn't necessary - all these tasks can be
done through the Ren'Py launcher.

The examples on this page assume you're running the CLI from the Ren'Py SDK
directory (the directory that contains renpy.py, renpy.sh, and renpy.exe). The
examples also assume you're running on Linux or macOS. On Windows, you'll need
to replace ``./renpy.sh`` with ``lib\\py3-windows-x86_64\\python.exe renpy.py``.

The CLI isn't a stable interface - it may change between Ren'Py releases,
as required.

.. describe:: <base>

    In the description of the commands below, <base> is the path to the
    base directory of the project.


Check and Test Commands
=======================

Check Script (Lint)
-------------------

::

    ./renpy.sh <base> lint [ filename ] [ options... ]

This runs a lint report on the game. It's equivalent to the "Check Script (Lint)"
button in the launcher.

.. option:: filename

    If given, the lint report will be written to this file rather than
    printed to standard output.

Lint takes many options, which can change from release to release. To view
them, run:

::

    ./renpy.sh <base> lint --help


.. _cli-test:

Run Testcases
-------------

::

    ./renpy.sh <base> test [ testcase ] [ options... ]

This runs :file:`automated tests <testcases>` on the game.

.. option:: testcase

    The name of the testcase or test suite to run. If not given, the "global"
    test suite will be run.

.. option:: --enable_all

    If provided, all test cases and test suites will be executed, regardless
    of their ``enabled`` property.

.. option:: --overwrite_screenshots

    If provided, existing screenshots will be overwritten when a
    :ref:`screenshot statement <test-screenshot-statement>` is executed.

.. option:: --hide-header

    If provided, the header at the start of the test run will be disabled.

.. option:: --hide-execution [no|hooks|testcases|all]

    If provided, test execution output will be hidden. ``hooks`` hides hooks,
    ``testcases`` hides test cases and hooks, and ``all`` hides everything.

.. option:: --hide-summary

    If provided, the summary at the end of the test run will be disabled.

.. option:: --report-detailed

    If provided, detailed information about each test will be shown during
    the run.

.. option:: --report-skipped

    If provided, information about skipped tests will be shown. This option
    should be used together with ``--report-detailed``.




Build Commands
==============

.. note::

    As part of the build process, Ren'Py will create .rpyc files that contain
    information that load the game. A continuous integration system should
    preserve these .rpyc files after a build, and supply them to the next
    build, either directly or in the old-game directory. Failure to do so
    may result in a game that can't load saves.


Android Build
-------------

::

    ./renpy.sh launcher android_build <base> [ options... ]


This builds a release of the game for Android. It's assumed that the launcher
has been used to install the Android SDK, generate keys, and configure the
project.

.. option:: --destination <directory>

    The directory to place the output in. The default is a directory
    named "`name`-`version`-dists" in the current directory, taking information
    from :var:`build.name` and :var:`build.version`.

.. option:: --bundle

    When given, Ren'Py will produce a .aab bundle. If not given, Ren'Py will
    produce an .apk file.

.. option:: --install

    When given, Ren'Py will install the .apk or .aab file to a connected device.

.. option:: --launch

    When given, Ren'Py will launch the game on a connected device. This implies
    ``--install``.


Add From To Call
----------------

::

    ./renpy.sh <base> add_from

This command adds a ``from`` clause to each ``call`` statement that does not
have one. Generally, this should be done before a release, to help Ren'Py
locate the return point of calls in a modified game.

.. note::

    This will modify your game's script files, and assumes that you will include
    the changes it makes into your game.


Compile
-------

::

    ./renpy.sh <base> compile [ --keep-orphan-rpyc ]

This command compiles the game, creating .rpyc files from .rpy files. The
equialent of the "Force Recompile" button in the Ren'Py launcher.

.. option:: --keep-orphan-rpyc

    By default, Ren'Py will delete .rpyc files that are not associated with
    a .rpy or _ren.py file of the same name. If this option is given, Ren'Py
    will not delete these files.


Distribute
----------

::

    ./renpy.sh launcher distribute <base> [ options... ]

This builds distributions of the game for windows, macOS, and Linux. Some
options this command takes are:

.. option:: --destination <directory>

    The directory to place the distributions in. The default is a directory
    named "`name`-`version`-dists" in the current directory, taking information
    from :var:`build.name` and :var:`build.version`.

.. option:: --no-update

    When given, Ren'Py will not build update files.

.. option:: --package <package>

    This gives the name of the package to build, where package is a package
    name like "pc", "mac", or "markets". This option can be given multiple
    times to build multiple packages. The default is to build all packages.

(There are other options, but these are more useful for building Ren'Py
itself.)

iOS Create
----------

::

    ./renpy.sh launcher ios_create <base> <destination>

This creates an Xcode project that can be used to build an iOS version of
the game. It's assumed that the launcher has been used to install iOS
support once.

.. option:: destination

    The directory to place the Xcode project in.


iOS Populate
------------

::

    ./renpy.sh launcher ios_populate <base> <destination>

This copies the game into an Xcode project created by :command:`ios_create`. This
is used to update a project created with the same version of Ren'Py.

.. option:: destination

    The directory to update.


Update Old Game
---------------

::

    ./renpy.sh launcher update_old_game <base>

This command will copy .rpyc files from <base>/game to <base>/old-game.


Web Build
-------------

::

    ./renpy.sh launcher web_build <base> [ options... ]


This builds a release of the game for web. It's assumed that the
launcher has been used to install web support and that any configuration
files (such as ``progressive_download.txt``) are in place.

.. option:: --destination <directory>

    The directory to place the web root in.


Launcher Commands
=================

These commands are used to control the Ren'Py launcher from the command line.


Set Projects Directory
----------------------

::

    ./renpy.sh launcher set_projects_directory <directory>


This sets the directory that the Ren'Py launcher uses to store projects. It's
intended for use on minimal systems where none of the options for selecting
a projects directory are available.

This can only be done when the launcher is not running.


Set Project
-----------

::

    ./renpy.sh launcher set_project <base>

Sets the current project to the given project. This will change the
projects directory and currently selected project in the launcher
to accomplish this goal.

This can only be done when the launcher is not running.
