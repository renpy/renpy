======================
Command Line Interface
======================

Ren'Py includes a command line interface (CLI) that can be used to automate
some development tasks, allowing for continuous integration and for scripting
releases. For most purposes, this isn't necessary - all these tasks can be
done through the Ren'Py launcher.

The examples on this page assume you're running the CLI from the Ren'Py SDK
directory (the directory that contains renpy.py, renpy.sh, and renpy.exe).
Examples are provided for Linux/macOS, and Windows.

The CLI isn't a stable interface - it may change between Ren'Py releases,
as required. This page is current as of Ren'Py 8.5.3.


Quick Tasks
===========

Use these quick workflows as copy-paste starting points. Replace paths/language codes as needed.

Run project
-----------

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            cd /path/to/renpy
            ./renpy.sh /path/to/project run

    .. tab:: Windows

        .. code-block:: bat

            cd C:\path\to\renpy
            .\lib\py3-windows-x86_64\python.exe renpy.py C:\path\to\project run


Build distributions
-------------------

Build desktop distributions (Windows/macOS/Linux) from the launcher tool.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            cd /path/to/renpy
            ./renpy.sh launcher distribute /path/to/project --destination /path/to/output

    .. tab:: Windows

        .. code-block:: bat

            cd C:\path\to\renpy
            .\lib\py3-windows-x86_64\python.exe renpy.py launcher distribute C:\path\to\project --destination C:\path\to\output


Generate/update translations
----------------------------

Generate or update translation files, then export dialogue/strings for translators.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            cd /path/to/renpy
            ./renpy.sh /path/to/project translate french
            ./renpy.sh /path/to/project dialogue french --strings

    .. tab:: Windows

        .. code-block:: bat

            cd C:\path\to\renpy
            .\lib\py3-windows-x86_64\python.exe renpy.py C:\path\to\project translate french
            .\lib\py3-windows-x86_64\python.exe renpy.py C:\path\to\project dialogue french --strings


Syntax
======

.. note::

    Notation used on this page:

    * ``<name>`` is a value you replace, such as a project path or language code.
    * ``[item]`` is optional and does not need to be included.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh [global options...] [<basedir>] [<command>] [command options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py [global options...] [<basedir>] [command] [command options...]

.. describe:: <basedir>

    :default: The directory containing the Ren'Py executable (the launcher)

    In the description of the commands below, <basedir> is the path to the
    base directory of the project.

.. describe:: <command>

    :default: ``run``

    Specifies the command to execute.

Global options
--------------

The following flags may be used with any command:

.. option:: --savedir <directory>

    Specifies the directory where saves and persistent data are placed.

.. option:: --trace <level>

    Specifies the level of trace Ren'Py will log to trace.txt. (1=per-call, 2=per-line)

.. option:: --version

    Displays the version of Ren'Py in use.

.. option:: --compile

    Forces all .rpy scripts to be recompiled before proceeding.

.. option:: --compile-python

    Forces all Python files to be recompiled, rather than read from
    :file:`game/cache/bytecode-*.rpyb`.

.. option:: --keep-orphan-rpyc

    If compiling, prevents Ren'Py from deleting :file:`.rpyc` files that are not associated with
    a :file:`.rpy` or :file:`_ren.py` file of the same name.

.. option:: --errors-in-editor

    Causes errors to open in a text editor.

.. option:: --safe-mode

    Forces Ren'Py to start in safe mode, allowing the player to configure graphics.

.. option:: --help, -h

    Displays a help message showing commands and syntax, then exits. This returns
    the most up-to-date command information.

Ren'Py can dump information about the game to a JSON file.
These options let you select the file, and choose what is dumped.

.. option:: --json-dump <file>

    Specifies the name of the JSON file.

.. option:: --json-dump-private

    Includes private names in the dump. (Names beginning with an underscore `_`)

.. option:: --json-dump-common

    Includes names defined in the common directory in the dump.

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


Core Workflow Commands
======================

.. _cli-run:

Run Project
-----------

Runs the current project normally. This is the default command that is run if no command is given.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> run [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> run [options...]

.. option:: --profile-display

    Reports the amount of time it takes to draw the screen.

    Equivalent to setting :var:`config.profile` to True.

.. option:: --debug-image-cache

    Writes information about the :ref:`image cache <images>` to image_cache.txt.

    Equivalent to setting :var:`config.debug_image_cache` to True.

.. option:: --warp <filename:linenumber>

    Tries to warp to just before the specified line. This takes as an argument a
    ``filename:linenumber`` pair.

    The :ref:`warp feature <warping_to_a_line>` requires :var:`config.developer` to be True to operate.


.. _cli-quit:

Quit
----

Quits the game immediately.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> quit

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> quit


.. _cli-compile:

Compile
-------

Compiles the game, creating .rpyc files from .rpy files. The
equivalent of the "Force Recompile" button in the Ren'Py launcher.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> compile [--keep-orphan-rpyc]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> compile [--keep-orphan-rpyc]

.. option:: --keep-orphan-rpyc

    Prevents Ren'Py from deleting :file:`.rpyc` files that are not associated with
    a :file:`.rpy` or :file:`_ren.py` file of the same name.


.. _cli-director:

Interactive Director
--------------------

Starts the :doc:`director` and runs the game afterwards.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> director

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> director


.. _cli-rmpersistent:

Remove Persistent Data
----------------------

Deletes :doc:`persistent` data. This can be handy since persistent data is
found in multiple locations:

- the game save folder
- the location specified by :var:`config.save_directory`

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> rmpersistent

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> rmpersistent

.. warning::

    This will reset all game progress, including unlocks, read messages, and preferences.


.. _cli-update:

Update Project
--------------

Download and install updates to a Ren'Py game from a web host.
For more information, see :doc:`updater`.

The parameters are identical to those used in :meth:`updater.update`.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> update <url> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> update <url> [options...]

.. option:: <url>

    Specifies the URL to the updates.json file.

.. option:: --base <directory>

    Specifies the base directory of the game to update. Defaults to the current game.

.. option:: --force

    Forces the update to run even if the version numbers are the same.

.. option:: --key <key>

    A file giving the public key to use of the update.

.. option:: --simulate <option>

    A simulation mode to test update GUIs without actually performing an update.
    One of ``available``, ``not_available``, or ``error``.

.. warning::

    This will modify your game's files. Use with caution.


Validation and Testing
======================

.. _cli-lint:

Check Script (Lint)
-------------------

This runs a :ref:`lint` report on the game. This checks the script for errors and
prints script statistics. It's equivalent to the "Check Script (Lint)" button
in the launcher.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> lint [<filename>] [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> lint [<filename>] [options...]

.. option:: <filename>

    If given, the lint report will be written to this file rather than
    printed to standard output.

.. option:: --error-code

    Exits with an error code of 1 if there was a lint error. This is useful for CI systems to detect when lint fails.

.. option:: --no-orphan-tl

    Does not report orphan translations. Orphaned translations are
    :ref:`Translation Statements <translation_statement>` that do not reference a string
    in the primary language.

.. option:: --reserved-parameters

    Reports Ren'Py or python reserved names in renpy statement parameters.

    In particular it looks for :doc:`label <label>`, :doc:`screen <screens>`, and :ref:`ATL <atl>` statements.

.. option:: --by-character

    Reports the count of blocks, words, and characters for each character.

.. option:: --check-unclosed-tags

    Reports unclosed text tags.

.. option:: --all-problems

    Reports all problems of a kind, not just the first ten issues.


.. _cli-test:

Run Testcases
-------------

This runs :doc:`automated tests <testcases>` on the game.

Examples:
 * `<https://github.com/renpy/renpy/blob/master/tutorial/game/testcases.rpy>`_
 * `<https://github.com/renpy/renpy/blob/master/gui/game/testcases.rpy>`_
 * `<https://github.com/renpy/renpy/blob/master/launcher/game/testcases.rpy>`_

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> test [<testcase>] [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> test [<testcase>] [options...]

.. option:: <testcase>

    Specifies the name of the testcase or test suite to run. If not given, the "global"
    test suite will be run.

.. option:: --enable_all

    Executes all test cases and test suites, regardless of their ``enabled`` property.

.. option:: --overwrite_screenshots

    Overwrite existing screenshots when a
    :ref:`screenshot statement <test-screenshot-statement>` is executed.

.. option:: --hide-header

    Disables the header at the start of the test run.

.. option:: --hide-execution {no|hooks|testcases|all}

    Hides information about test execution. ``--hide-execution hooks`` hides hooks,
    ``--hide-execution testcases`` hides test cases and hooks, and ``--hide-execution all``
    hides everything.

.. option:: --hide-summary

    Disables the summary at the end of the test run.

.. option:: --report-detailed

    Shows detailed information about each test during the run.

.. option:: --report-skipped

    Shows information about skipped tests. This option should be used together
    with ``--report-detailed``.


Build and Distribution
======================

.. note::

    As part of the build process, Ren'Py will create .rpyc files that contain
    information that load the game. A continuous integration system should
    preserve these .rpyc files after a build, and supply them to the next
    build, either directly or in the old-game directory. Failure to do so
    may result in a game that can't load saves.


.. _cli-add-from:

Add From To Calls
-----------------

Adds a ``from`` clause to each :ref:`call statement <call-statement>`
that does not have one. Generally, this should be done before a release, to help
Ren'Py locate the return point of calls in a modified game.

Implies :option:`--compile`.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> add_from

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> add_from

.. warning::

    This will modify your game's script files.


.. _cli-distribute:

Distribute
----------

:doc:`Builds distributions <build>` of the game for Windows, macOS, and Linux.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher distribute <basedir> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher distribute <basedir> [options...]

.. option:: --destination <directory>

    Specifies the directory to place the distributions in. The default is a directory
    named "`name`-`version`-dists" in the current directory, taking information
    from :var:`build.name` and :var:`build.version`.

.. option:: --format <format>

    Forces the format of the distribution to be this.

.. option:: --macapp <app>

    Specifies the path to a macapp that's used to sign mac
    packages instead of the macapp that's included with Ren'Py.

.. option:: --no-archive

    Does not add files to :ref:`archives`.

.. option:: --no-update

    Does not build update files which allow the :doc:`updater` to work.

.. option:: --package <package>

    Specifies the name of the package to build, where package is a package
    name like "pc", "mac", or "markets". This option can be given multiple
    times to build multiple packages. The default is to build all packages.

.. option:: --packagedest <package>

    Specify the output name for a package (without any
    extensions). Requires that exactly one :option:`--package` is specified.


.. _cli-android-build:

Android Build
-------------

This builds a release of the game for :doc:`android`. It's assumed that the launcher
has been used to install the Android SDK, generate keys, and configure the
project.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher android_build <basedir> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher android_build <basedir> [options...]

.. option:: --destination <directory>

    Specifies the directory to place the output in. The default is a directory
    named "`name`-`version`-dists" in the current directory, taking information
    from :var:`build.name` and :var:`build.version`.

.. option:: --bundle

    Produces a :file:`.aab` bundle if given. If not given, Ren'Py will
    produce a :file:`.apk` file.

.. option:: --install

    Installs the :file:`.apk` or :file:`.aab` file to a connected device.

.. option:: --launch

    Launches the game on a connected device. This implies :option:`--install`.

.. option:: --package <package>

    Specifies the package to build. Defaults to building the 'android' package.


.. _cli-ios-create:

iOS Create
----------

Creates an Xcode project that can be used to build an :doc:`ios` version of
the game. It's assumed that the launcher has been used to install iOS
support once.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher ios_create <basedir> <destination>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher ios_create <basedir> <destination>

.. describe:: <basedir>

    Specifies the path to the Ren'Py project.

.. describe:: <destination>

    Specifies the path to the iOS project that will be created.


.. _cli-ios-populate:

iOS Populate
------------

Copies the game into an Xcode project created by :ref:`ios_create <cli-ios-create>`. This
is used to update a project created with the same version of Ren'Py.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher ios_populate <basedir> <destination>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher ios_populate <basedir> <destination>

.. describe:: <basedir>

    Specifies the path to the Ren'Py project.

.. describe:: <destination>

    Specifies the path to the iOS project that will be updated.


.. _cli-web-build:

Web Build
---------

Builds a release of the game for web. It's assumed that the
launcher has been used to install web support and that any configuration
files (such as :file:`progressive_download.txt`) are in place.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher web_build <basedir> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher web_build <basedir> [options...]



.. option:: --destination <directory>

    Specifies the directory where the packaged files should be placed.

.. option:: --launch

    Starts a webserver and launches the game after build.


Translation and Localization
============================

.. seealso::

    * :doc:`translation`


.. _cli-translate:

Translate
---------

Creates or updates translation files in ``tl/<language>`` for the project.
It writes missing dialogue and string entries while leaving existing translated entries unchanged.
Use :option:`--count` to report missing translations without writing files.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> translate <language> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> translate <language> [options...]

.. option:: <language>

    Specifies the language to generate translations for.

.. option:: --count

    Prints a count of missing translations without generating files.

.. option:: --rot13

    Applies rot13 while generating translations.

.. option:: --piglatin

    Applies pig latin while generating translations. Overridden by :option:`--rot13`.

.. option:: --empty

    Produces empty strings while generating translations. Overridden by :option:`--rot13` and :option:`--piglatin`.

.. option:: --min-priority <int>

    Translates strings with priority greater than this value.

.. option:: --max-priority <int>

    :default: 499 if :var:`config.translate_launcher` is True, otherwise 299.

    Translates strings with less than this priority.

.. option:: --strings-only

    Only translates strings (not dialogue).

.. option:: --common-only

    Only translates strings from common code.

.. option:: --no-todo

    Does not include the TODO flag at the top of generated translation files.

.. option:: --string <string>

    Translates a specific string. This option can be given multiple
    times to translate multiple strings.


.. _cli-dialogue:

Dialogue
-----------

Exports dialogue (and optionally translatable strings) to :file:`dialogue.tab`
by default, or :file:`dialogue.txt` when :option:`--text` is used.

If a language is provided, it outputs translated text when available. Otherwise, it outputs
source text.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> dialogue <language> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> dialogue <language> [options...]

.. note::

    This is an export/reporting command. It does not create :file:`tl/<language>`
    translation script files.

.. describe:: <language>

    Specifies the language to extract dialogue for.

.. option:: --text

    Outputs the dialogue as plain text. If not given, outputs a tab-delimited file.

.. option:: --strings

    Outputs all translatable strings, not just dialogue.

    Most of these are defined with the :func:`_` and :func:`__` functions, as well as
    :doc:`menu choices <menus>`.

.. option:: --notags

    Strips text tags from the dialogue.

.. option:: --escape

    Escapes quotes and other special characters.


.. _cli-extract-strings:

Extract Strings
---------------

Exports existing translations from the game to a JSON file.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> extract_strings <language> <destination> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> extract_strings <language> <destination> [options...]

.. option:: <language>

    Specifies the language to extract translated strings from.

.. option:: <destination>

    Specifies the json file to store the translated strings into.

.. option:: --merge

    Merges the current contents of the file with new contents, preserving existing translations.

.. option:: --force

    Does not throw exceptions if the language does not exist.


.. _cli-merge-strings:

Merge Strings
-------------

Imports translations from JSON file back into the game.

Implies :option:`--compile`.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh <basedir> merge_strings <language> <source> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> merge_strings <language> <source> [options...]

.. option:: <language>

    Specifies the language to merge translated strings to.

.. option:: <source>

    Specifies the json file to take translated strings from.

.. option:: --reverse

    Reverses the languages in the json file.

.. option:: --replace

    Replaces non-trivial translations. A trivial translation is
    one that does not exist or if the translation is the same as the primary
    language.


Launcher Commands
=================

These commands are used to control the Ren'Py launcher from the command line.


.. _cli-generate-gui:

Generate GUI
------------

Generates a GUI for an existing Ren'Py game.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher generate_gui <basedir> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher generate_gui <basedir> [options...]

.. option:: --width <width>

    :default: 1280

    Specifies the width of the generated gui.

.. option:: --height <height>

    :default: 720

    Specifies the height of the generated gui.

.. option:: --accent <color>

    :default: #00B8C3

    Specifies the accent color used throughout the gui.

.. option:: --boring <color>

    :default: #000000

    Specifies the boring color used for the gui background.

.. option:: --light

    Considers this a light theme.

.. option:: --template <directory>

    :default: "gui"

    Specifies the template directory containing source code.

.. option:: --language <language>

    :default: None

    Specifies the language to translate strings and comments to.

.. option:: --start

    Starts a new project, replacing images and code.

.. option:: --replace-images

    Overwrites existing images.

.. option:: --replace-code

    Overwrites existing gui.rpy file.

.. option:: --update-code

    Updates existing gui.rpy file.

.. option:: --minimal

    Only updates option.rpy and translations.


.. _cli-gui-images:

GUI Images
----------

Generates images (e.g. for buttons, bars, radio buttons, etc) based on :doc:`GUI variables <gui>`.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher gui_images <basedir> [options...]

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher gui_images <basedir> [options...]

.. _cli-get-projects-directory:

Get Projects Directory
----------------------

Prints the directory that the Ren'Py launcher uses to store projects.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher get_projects_directory

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher get_projects_directory


.. _cli-set-projects-directory:

Set Projects Directory
----------------------

Sets the directory that the Ren'Py launcher uses to store projects. It's
intended for use on minimal systems where none of the options for selecting
a projects directory are available.

This can only be done when the launcher is not running.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher set_projects_directory <projects>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher set_projects_directory <projects>

.. describe:: <projects>

    Specifies the path to the projects directory.


.. _cli-set-project:

Set Project
-----------

Sets the current project to the given project. This will change the
projects directory and currently selected project in the launcher
to accomplish this goal.

This can only be done when the launcher is not running.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher set_project <project>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher set_project <project>

.. describe:: <project>

    Specifies the full path to the project to select.


.. _cli-update-old-game:

Update Old Game
---------------

Copies .rpyc files from :file:`<basedir>/game` to :file:`<basedir>/old-game`.

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh launcher update_old_game <basedir>

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py launcher update_old_game <basedir>

.. seealso::

    * :ref:`old-game`


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

        Specifies the name of the command in the interface.

    .. describe:: function

        :type: function

        Specifies the function that is called when the command is run. `function` is
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

            > .\lib\py3-windows-x86_64\python.exe renpy.py basedir compute_area 3 --square

            Square: 9.0

            > .\lib\py3-windows-x86_64\python.exe renpy.py basedir compute_area 3 2 --rectangle

            Rectangle: 6.0

            > .\lib\py3-windows-x86_64\python.exe renpy.py basedir compute_area 1 --circle

            Circle: 3.14

            > .\lib\py3-windows-x86_64\python.exe renpy.py basedir compute_area --help
