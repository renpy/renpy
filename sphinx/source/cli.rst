======================
Command Line Interface
======================

Ren'Py includes a command line interface (CLI) that can be used to automate
some development tasks, allowing for continuous integration and for scripting
releases. For most purposes, this isn't necessary - all these tasks can be
done through the Ren'Py launcher.

The examples on this page assume you're running the CLI from the Ren'Py SDK
directory (the directory that contains renpy.py, renpy.sh, and renpy.exe). The
examples also assume you're running on Linux or macOS.

The CLI isn't a stable interface - it may change between Ren'Py releases,
as required. The following is current as of Ren'Py 8.4.0.

Syntax
======

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> <command> [ flags... ] [ command options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> <command> [ flags... ] [ command options... ]

.. describe:: <basedir>

    In the description of the commands below, <basedir> is the path to the
    base directory of the project. This defaults to the directory containing the Ren'Py executable.

.. describe:: <command>

    The command to execute. Defaults to ``run``.

    Available commands are:

    * :ref:`add_from <cli_add_from>`
    * :ref:`android_build <cli_android_build>`
    * :ref:`compile <cli_compile>`
    * :ref:`dialogue <cli_dialogue>`
    * :ref:`director <cli_director>`
    * :ref:`distribute <cli_distribute>`
    * :ref:`extract_strings <cli_extract_strings>`
    * :ref:`generate_gui <cli_generate_gui>`
    * :ref:`get_projects_directory <cli_get_projects_directory>`
    * :ref:`gui_images <cli_gui_images>`
    * :ref:`ios_create <cli_ios_create>`
    * :ref:`ios_populate <cli_ios_populate>`
    * :ref:`lint <cli_lint>`
    * :ref:`merge_strings <cli_merge_strings>`
    * :ref:`quit <cli_quit>`
    * :ref:`rmpersistent <cli_rmpersistent>`
    * :ref:`run <cli_run>`
    * :ref:`set_project <cli_set_project>`
    * :ref:`set_projects_directory <cli_set_projects_directory>`
    * :ref:`test <cli_test>`
    * :ref:`translate <cli_translate>`
    * :ref:`update <cli_update>`
    * :ref:`update_old_game <cli_update_old_game>`
    * :ref:`web_build <cli_web_build>`

The following flags may be used with ANY command:

Optional arguments
------------------

.. option:: --savedir <directory>

    The directory where saves and persistent data are placed.

.. option:: --trace <level>

    The level of trace Ren'Py will log to trace.txt. (1=per-call, 2=per-line)

.. option:: --version

    If given, displays the version of Ren'Py in use.

.. option:: --compile

    If given, forces all .rpy scripts to be recompiled before proceeding.

.. option:: --compile-python

    If given, forces all Python to be recompiled, rather than read from game/cache/bytecode-*.rpyb.

.. option:: --keep-orphan-rpyc

    By default, Ren'Py will delete :file:`.rpyc` files that are not associated with
    a :file:`.rpy` or :file:`_ren.py` file of the same name. If this option is given, Ren'Py
    will not delete these files.

.. option:: --errors-in-editor

    If given, causes errors to open in a text editor.

.. option:: --safe-mode

    If given, forces Ren'Py to start in safe mode, allowing the player to configure graphics.

.. option:: --help, -h

    If given, displays a help message showing commands and syntax, then exits.

.. note::

    The CLI may change between different releases. To see the latest commands
    and flags, run:

    .. tabs::

        .. tab:: Linux / macOS

            .. code-block:: bash

                ./renpy.sh --help

        .. tab:: Windows

            .. code-block:: bash

                .\lib\py3-windows-x86_64\python.exe renpy.py --help

    To see the latest options for a particular command, run:

    .. tabs::

        .. tab:: Linux / macOS

            .. code-block:: bash

                ./renpy.sh <basedir> <command> --help

        .. tab:: Windows

            .. code-block:: bash

                .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> <command> --help


JSON dump arguments
-------------
Ren'Py can dump information about the game to a JSON file. These options let you select the file, and choose what is dumped.

.. option:: --json-dump <file>

    The name of the JSON file.

.. option:: --json-dump-private

    If given, include private names. (Names beginning with an underscore `_`)

.. option:: --json-dump-common

    If given, include names defined in the common directory.


Basic Commands
==============

.. _cli_run:

Run
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> run [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> run [ options... ]

Runs the current project normally. This is the default command that is run if no command is given.

.. option:: --profile-display

    If given, Ren'Py will report the amount of time it takes to draw the screen.

    Equivalent to setting :var:`config.profile` to True.

.. option:: --debug-image-cache

    If given, Ren'Py will write information about the :ref:`image cache <images>` to image_cache.txt.

    Equivalent to setting :var:`config.debug_image_cache` to True.

.. option:: --warp <filename:linenumber>

    This takes as an argument a ``filename:linenumber`` pair, and tries to warp to the statement before that line number.

    The :ref:`warp feature <warping_to_a_line>` requires :var:`config.developer` to be True to operate.


.. _cli_add_from:

Add From To Calls
-----------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> add_from

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> add_from

This command adds a ``from`` clause to each :ref:`call statement <call-statement>`
that does not have one. Generally, this should be done before a release, to help
Ren'Py locate the return point of calls in a modified game.

.. note::

    This will modify your game's script files, and assumes that you will include
    the changes it makes into your game.


.. _cli_lint:

Check Script (Lint)
-------------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> lint [ filename ] [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> lint [ filename ] [ options... ]

This runs a :ref:`lint` report on the game. This checks the script for errors and
prints script statistics. It's equivalent to the "Check Script (Lint)" button
in the launcher.

.. option:: filename

    If given, the lint report will be written to this file rather than
    printed to standard output.

.. option:: --error-code

    If given and there was a lint error, the program will exit with an error code of 1.

.. option:: --no-orphan-tl

    If given, orphan translations are not reported. Orphaned translations are
    :ref:`Translation Statements <translation_statement>` that do not reference a string
    in the primary language.

.. option:: --reserved-parameters

    If given, Ren'Py or python reserved names in renpy statement parameters are reported.

    In particular it looks for :doc:`label <label>`, :doc:`screen <screens>`, and :ref:`ATL <atl>` statements.

.. option:: --by-character

    If given, the count of blocks, words, and characters for each character is reported.

.. option:: --check-unclosed-tags

    If given, unclosed text tags are reported.

.. option:: --all-problems

    If given, all problems of a kind are reported, not just the first ten.


.. _cli_compile:

Compile
-------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> compile [ --keep-orphan-rpyc ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> compile [ --keep-orphan-rpyc ]

This command compiles the game, creating .rpyc files from .rpy files. The
equivalent of the "Force Recompile" button in the Ren'Py launcher.

.. option:: --keep-orphan-rpyc

    By default, Ren'Py will delete :file:`.rpyc` files that are not associated with
    a :file:`.rpy` or :file:`_ren.py` file of the same name. If this option is given, Ren'Py
    will not delete these files.


.. _cli_director:

Interactive Director
--------------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> director

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> director

This command starts the :doc:`director` and runs the game afterwards.


.. _cli_rmpersistent:

Remove Persistent Data
----------------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> rmpersistent

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> rmpersistent

This command is used to delete :doc:`persistent`. This can be handy since persistent data is found both in
the game save folder, AND the location specified by :var:`config.save_directory`.


.. _cli_test:

Test
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> test <testcase>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> test <testcase>

Runs a testcase to automatically test a user interface or gameplay flow.

Examples:
 * `<https://github.com/renpy/renpy/blob/master/tutorial/game/testcases.rpy>`_
 * `<https://github.com/renpy/renpy/blob/master/gui/game/testcases.rpy>`_
 * `<https://github.com/renpy/renpy/blob/master/launcher/game/testcases.rpy>`_

.. option:: <testcase>

    The name of the testcase to run


.. _cli_update:

Update
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> update <url> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> update <url> [ options... ]

Download and install updates to a Ren'Py game from a web host. For more information, see :doc:`updater`.

The parameters are identical to those used in :meth:`updater.update`.

.. option:: <url>

    The URL to the updates.json file.

.. option:: --base <directory>

    The base directory of the game to update. Defaults to the current game.

.. option:: --force

    If given, force the update to run even if the version numbers are the same.

.. option:: --key <key>

    A file giving the public key to use of the update.

.. option:: --simulate <option>

    A simulation mode to test update GUIs without actually performing an update.
    One of ``available``, ``not_available``, or ``error``.


Launcher Commands
=================

These commands are used to control the Ren'Py launcher from the command line.


.. _cli_generate_gui:

Generate GUI
------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher generate_gui <basedir> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher generate_gui <basedir> [ options... ]

Generates a GUI for an existing Ren'Py game.

.. option:: --width <width>

    :default: 1280
    The width of the generated gui.

.. option:: --height <height>

    :default: 720
    The height of the generated gui.

.. option:: --accent <color>

    :default: #00B8C3
    The accent color used throughout the gui.

.. option:: --boring <color>

    :default: #000000
    The boring color used for the gui background.

.. option:: --light

    If given, this is considered a light theme.

.. option:: --template <directory>

    :default: "gui"
    The template directory containing source code.

.. option:: --language <language>

    :default: None
    The language to translate strings and comments to.

.. option:: --start

    If given, starts a new project, replacing images and code.

.. option:: --replace-images

    If given, existing images should be overwritten.

.. option:: --replace-code

    If given, existing gui.rpy file should be overwritten.

.. option:: --update-code

    If given, existing gui.rpy file should be updated.

.. option:: --minimal

    If given, only update option.rpy and translations.


.. _cli_gui_images:

GUI Images
-----------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher gui_images <basedir> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher gui_images <basedir> [ options... ]

Generates images (eg. for buttons, bars, radio buttons, etc) based on :doc:`GUI variables <gui>`.


.. _cli_get_projects_directory:

Get Projects Directory
----------------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher get_projects_directory

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher get_projects_directory

This prints the directory that the Ren'Py launcher uses to store projects.


.. _cli_set_projects_directory:

Set Projects Directory
----------------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher set_projects_directory <projects>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher set_projects_directory <projects>

This sets the directory that the Ren'Py launcher uses to store projects. It's
intended for use on minimal systems where none of the options for selecting
a projects directory are available.

This can only be done when the launcher is not running.

.. describe:: <projects>

    The path to the projects directory.


.. _cli_set_project:

Set Project
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher set_project <project>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher set_project <project>

Sets the current project to the given project. This will change the
projects directory and currently selected project in the launcher
to accomplish this goal.

This can only be done when the launcher is not running.

.. describe:: <project>

    The full path to the project to select.


.. _cli_update_old_game:

Update Old Game
---------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher update_old_game <basedir>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher update_old_game <basedir>

This command will copy .rpyc files from :file:`<basedir>/game` to :file:`<basedir>/old-game`.

.. seealso::

    * :ref:`old-game`


Build Commands
==============

.. note::

    As part of the build process, Ren'Py will create .rpyc files that contain
    information that load the game. A continuous integration system should
    preserve these .rpyc files after a build, and supply them to the next
    build, either directly or in the old-game directory. Failure to do so
    may result in a game that can't load saves.


.. _cli_android_build:

Android Build
-------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher android_build <basedir> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher android_build <basedir> [ options... ]

This builds a release of the game for :doc:`android`. It's assumed that the launcher
has been used to install the Android SDK, generate keys, and configure the
project.

.. option:: --destination <directory>

    The directory to place the output in. The default is a directory
    named "`name`-`version`-dists" in the current directory, taking information
    from :var:`build.name` and :var:`build.version`.

.. option:: --bundle

    If given, Ren'Py will produce a :file:`.aab` bundle. If not given, Ren'Py will
    produce a :file:`.apk` file.

.. option:: --install

    If given, Ren'Py will install the :file:`.apk` or :file:`.aab` file to a connected device.

.. option:: --launch

    If given, Ren'Py will launch the game on a connected device. This implies
    :option:`--install`.

.. option:: --package <package>

    If given, a package to build. Defaults to building the 'android' package.


.. _cli_distribute:

Distribute
----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher distribute <basedir> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher distribute <basedir> [ options... ]

This :doc:`builds distributions <build>` of the game for Windows, macOS, and Linux.

.. option:: --destination <directory>

    The directory to place the distributions in. The default is a directory
    named "`name`-`version`-dists" in the current directory, taking information
    from :var:`build.name` and :var:`build.version`.

.. option:: --format <format>

    If given, forces the format of the distribution to be this.

.. option:: --macapp <app>

    If given, the path to a macapp that's used to sign mac
    packages instead of the macapp that's included with Ren'Py.

.. option:: --no-archive

    If given, files will not be added to :ref:`archives`.

.. option:: --no-update

    If given, Ren'Py will not build update files which allows the :doc:`updater` to work.

.. option:: --package <package>

    This gives the name of the package to build, where package is a package
    name like "pc", "mac", or "markets". This option can be given multiple
    times to build multiple packages. The default is to build all packages.

.. option:: --packagedest <package>

    Specify the output name for a package (without any
    extensions). Requires that exactly one :option:`--package` is specified.


.. _cli_ios_create:

iOS Create
----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher ios_create <basedir> <destination>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher ios_create <basedir> <destination>

This creates an Xcode project that can be used to build an :doc:`ios` version of
the game. It's assumed that the launcher has been used to install iOS
support once.

.. describe:: <basedir>

    The path to the Ren'Py project.

.. describe:: <destination>

    The path to the iOS project that will be created.


.. _cli_ios_populate:

iOS Populate
------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher ios_populate <basedir> <destination>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher ios_populate <basedir> <destination>

This copies the game into an Xcode project created by :ref:`ios_create <cli_ios_create>`. This
is used to update a project created with the same version of Ren'Py.

.. describe:: <basedir>

    The path to the Ren'Py project.

.. describe:: <destination>

    The path to the iOS project that will be updated.


.. _cli_web_build:

Web Build
-------------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher web_build <basedir> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher web_build <basedir> [ options... ]

This builds a release of the game for web. It's assumed that the
launcher has been used to install web support and that any configuration
files (such as :file:`progressive_download.txt`) are in place.

.. option:: --destination <directory>

    The directory where the packaged files should be placed.

.. option:: --launch

    Starts a webserver and launches the game after build.


Translation Commands
====================

.. seealso::

    * :doc:`translation`

.. _cli_dialogue:

Dialogue
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> dialogue <language> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> dialogue <language> [ options... ]

This command updates :file:`dialogue.txt`, a file giving all the dialogue in the game. This generates or updates translations.

.. describe:: <language>

    The language to extract dialogue for.

.. option:: --text

    If given, output the dialogue as plain text. If not given, output a tab-delimited file.

.. option:: --strings

    If given, output all translatable strings, not just dialogue.

    Most of these are defined with the :func:`_` and :func:`__` functions, as well as
    :doc:`menu choices <menus>`.

.. option:: --notags

    If given, strip text tags from the dialogue.

.. option:: --escape

    If given, escape quotes and other special characters.


.. _cli_extract_strings:

Extract Strings
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> extract_strings <language> <destination> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> extract_strings <language> <destination> [ options... ]

Extracts translated strings.

.. option:: <language>

    The language to extract translated strings from.

.. option:: <destination>

    The json file to store the translated strings into.

.. option:: --merge

    If given, the current contents of the file are preserved, and new contents are merged into the file.

.. option:: --force

    If given, no exceptions are thrown if the language does not exist.


.. _cli_merge_strings:

Merge Strings
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> merge_strings <language> <source> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> merge_strings <language> <source> [ options... ]

Merges translated strings with the game script.

.. option:: <language>

    The language to merge translated strings to.

.. option:: <source>

    The json file to take translated strings from.

.. option:: --reverse

    If given, reverses the languages in the json file.

.. option:: --replace

    If given, replaces non-trivial translations. A trivial translation is
    one that does not exist or if the translation is the same as the primary
    language.


.. _cli_translate:

Translate
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> translate <language> [ options... ]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> translate <language> [ options... ]

This command generates translations of the specified language.

.. option:: <language>

    The language to generate translations for.

.. option:: --count

    If given, instead of generating files, print a count of missing translations.

.. option:: --rot13

    If given, apply rot13 while generating translations.

.. option:: --piglatin

    If given, apply pig latin while generating translations. Overridden by :option:`--rot13`.

.. option:: --empty

    If given, produce empty strings while generating translations. Overridden by :option:`--rot13` and :option:`--piglatin`.

.. option:: --min-priority <int>

    Translate strings with more than this priority.

.. option:: --max-priority <int>

    :default: 499 if :var:`config.translate_launcher` is True, otherwise 299.

    Translate strings with less than this priority.

.. option:: --strings-only

    If given, only translate strings (not dialogue).

.. option:: --common-only

    Only translate string from the common code.

.. option:: --no-todo

    Do not include the TODO flag at the top of generated translation files.

.. option:: --string <string>

    Translate a specific string. This option can be given multiple
    times to translate multiple strings.


Custom Commands
===============

In addition to the commands defined above, it is possible to create commands
for a particular project using :func:`renpy.arguments.register_command`.

When running a command, the :doc:`game will first initialize <lifecycle>`, then
run the command.

.. function:: renpy.arguments.register_command(name, function, uses_display=False)

    Registers a command that can be invoked when Ren'Py is run on the command
    line. When the command is run, `function` is called with no arguments.

    .. describe:: name

        :type: str

        The name of the command in the interface.

    .. describe:: function

        :type: function

        The function that is called when the command is run. `function` is
        called with no arguments.

        If `function` needs to take additional command-line arguments, it should
        instantiate a :class:`renpy.arguments.ArgumentParser`, and then call :func:`parse_args`
        on it. Otherwise, it should call :func:`renpy.arguments.takes_no_arguments`.

        If `function` returns True, Ren'Py startup proceeds normally. Otherwise,
        Ren'Py will terminate when ``function()`` returns.

        .. seealso::

            For more information about command line parsing, look at the
            `ArgumentParser documentation <https://docs.python.org/3/library/argparse.html>`_.

    .. describe:: uses_display

        :type: bool

        If True, Ren'Py will initialize the display. If False, Ren'Py will
        use dummy video and audio drivers.


Example
-------

.. code-block:: renpy

    init python:

        def compute_area_command():
            ap = renpy.arguments.ArgumentParser(description='Compute the area of various shapes.')
            ap.add_argument("dimensions", nargs="*", type=float, help="The dimension of the shape.")
            ap.add_argument("--square", action="store_true", help="If given, compute the area as a square.")
            ap.add_argument("--rectangle", action="store_true", help="If given, compute the area as a rectangle.")
            ap.add_argument("--circle", action="store_true", help="If given, compute the area as a circle.")

            args = ap.parse_args()

            if args.square:
                print(f"Square: {args.dimensions[0] ** 2}")

            elif args.rectangle:
                print(f"Rectangle: {args.dimensions[0] * args.dimensions[1]}")

            elif args.circle:
                print(f"Circle: {3.14 * args.dimensions[0] ** 2}")

            # Terminate and do not run Ren'Py normally
            return False

        renpy.arguments.register_command("compute_area", compute_area_command)

The command can then be called as follows:

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            > ./renpy.sh <basedir> compute_area 3 --square

            Square: 9.0

            > ./renpy.sh <basedir> compute_area 3 2 --rectangle

            Rectangle: 6.0

            > ./renpy.sh <basedir> compute_area 1 --circle

            Circle: 3.14

            > ./renpy.sh <basedir> compute_area --help

    .. tab:: Windows

        .. code-block:: bat

            > .\lib\py3-windows-x86_64\python.exe <basedir> compute_area 3 --square

            Square: 9.0

            > .\lib\py3-windows-x86_64\python.exe <basedir> compute_area 3 2 --rectangle

            Rectangle: 6.0

            > .\lib\py3-windows-x86_64\python.exe <basedir> compute_area 1 --circle

            Circle: 3.14

            > .\lib\py3-windows-x86_64\python.exe <basedir> compute_area --help
