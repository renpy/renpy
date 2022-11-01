.. _extensions:

=================
Ren'Py Extensions
=================

Ren'Py Extensions (RPE) allow you to add advanced features and patch Ren'Py's
code before any other file of your game is interpreted. This makes it possible
to add functionnalities that go beyond what is normally possible in Ren'Py and
makes it easier to share code.

As Ren'Py Extensions are loaded before any other file, they are very usefull
to package :ref:`cds` and complex :ref:`warpers` and guarantee that they'll be
available in every one of your files without naming restrictions.

Usage
-----

Ren'Py Extensions (RPE) must conform to the following rules:

- They must be in the ZIP file format

- Their extension must be ``.rpe``

- They must be directly under the ``game`` directory of your game and may not
  be part of an archive

- They must contain an ``autorun.py`` file (the file may be empty)

Python files other than ``autorun.py`` may be imported as modules in the
extension or in your game's code, however only autorun.py will be executed
when reloading, thus it should be the only file that makes changes to Ren'Py
or your game may crash when reloading.

A notable limitation of Ren'Py Extensions is the fact that they are not
monitored for changes during development, which means that the game must be
fully reloaded whenever a change is made. When possible, one way to limit the
impact of this behavior is to develop in a regular ``.rpy`` file and copy the
python block it contains once all changes are made. If doing so, import
``renpy.store`` as renpy to keep the code working.

Create an extension
-------------------

The following steps demonstrate the creation of a simple extension that
provides a custom warper for a game.

- Create a new directory (the directory does not need to be part of the game)
- Create a new ``autorun.py`` file::

    # This is the autorun.py
    # The warper may be used with the name extension_linear
    import renpy

    @renpy.atl.atl_warper
    def extension_linear(t):
        return t    

- Create the extension file (the following command-line add ``autorun.py`` to
  a zip file and sets its full name to ``my_warper.rpe``)::

    python -m zipfile -c my_warper.rpe autorun.py

- Move ``my_warper.rpe`` to the game's ``game`` directory
- The custom warper may now be used in any Ren'Py file
