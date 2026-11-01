Scripts
=======

alter_translations.py
---------------------

This can be used to replace one string translation with another. It's used
when the string changes from `old` to `new`, but the translatoons are
expected to be correct.

autobuild.sh
------------

This is called from distribute.py, to build Ren'Py before distribution
happens.

check_copyright.py
------------------

Checks the copyright notice is present.

checksums.py
------------

Used by add.py. This computes the checksums of a released Ren'Py, and
signs them using GPG.

fetch_prism.py
--------------

Fetches the standalone Prism runtime shared libraries for Windows, macOS,
and Linux from GitHub Releases into ``lib/py3-*`` using HTTP Range requests.

fix_translations.py
-------------------

Removes BOMs and TODO comments from translations.

generate_pyi.py
---------------

This must be run using a Python with the Ren'Py, after modules have been
built. This generates .pyi files in typings/ and renpy, allowing
tools to analyze Ren'Py.

generate_update_keys.py
-----------------------

Generate update keys that can be used by the Ren'Py updater.

mac/
----

Scripts used to sign mac apps.

pyi/
----

Pyi files used by generate_pyi.py.

relative_imports.py
--------------------

This generates the relative import sections of __init__.py files. These fake
the imports, allowing typing tools to find all of Ren'Py.

release_changes.py
------------------

Shows how files have changed in size between releases.

rt/
---

Contains a template game for testing.

rt.py
-----

A tool that helps with creating and running test games.

run_testcases.py
----------------

Runs the test suites of the testcases, tutorial, the_question, and launcher
projects on several platforms at once, and prints a combined synopsis to stdout.
Targets can run in the repository, in a private copy of the tree (natively or
under wine), or on another computer using rsync and ssh. They run like normal
games unless they're set to be headless. Use --project to run some of the
projects, which test filters require.

Targets are defined in ~/.renpy/dev/testcases.toml. To create it, copy and edit
run_testcases.example.toml, which documents the format. Logs and artifacts are
kept in tmp/run-testcases/.

sign_update.py
---------------

This signs updates used by the Ren'Py updater.

update_compat_import.py
-----------------------

Updates the ``from renpy.compat import`` line at the start of files that
have one.

update_copyright.py
-------------------

Updates the copyright line when the year changes.

update_piglatin.sh
------------------

Updates the piglatin translation.

utflf.py
--------

Fixes line endings and adds UTF-8 BOM to all rpy files in a directory.
