Scripts
=======

Tests for these tools live in ``scripts/tests`` and use pytest. Run them from
the repository root with ``uv run pytest scripts/tests``. They do not require
engine initialization or compiled Ren'Py extensions. ``uv run pytest`` runs only
the engine Python tests by default.

add_all.sh
----------

Runs add.py using the Python in lib/, giving it the ``--real`` flag. add.py tags
and publishes a release, and refuses to do so if the updates.json file in dl/
isn't for the current version.
With ``-n`` (``--no-tag``), the current Ren'Py commit must already have a tag.

alter_translations.py
---------------------

This can be used to replace one string translation with another. It's used
when the string changes from `old` to `new`, but the translatoons are
expected to be correct.

check_copyright.py
------------------

Checks the copyright notice is present.

checksums.py
------------

Used by add.py. This computes the checksums of a released Ren'Py, and
signs them using GPG.

distribute_all.sh
-----------------

Builds a release. It checks the git tree, updates and builds the Ren'Py and
renpy-build checkouts, builds the documentation, and then runs distribute.py.
Its arguments are given to distribute.py. The ones most likely to be useful are:

``--allow-dirty``
    Allows a full build from a git tree with uncommitted changes.

``--nosign``
    Doesn't sign the Mac app or build a dmg. The updates are still signed.

distribute.py checks the files it built, and fails if one is missing or doesn't
match the version. Its ``--fast`` flag only builds the SDK, without updates, and
places it in ``dl/<version>-fast``.

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
projects concurrently on each selected target, and prints a combined synopsis to stdout.
Targets can run in the repository, in a private copy of the tree (natively or
under wine), or on another computer using rsync and ssh. They run like normal
games unless they're set to be headless. Use --project to run some of the
projects, which test filters require.

Alongside the projects, each target apart from a source one also runs the updater
test described under run_updater_test.py. It's selected with --project updater,
and reported in the synopsis as updater and updater:the_question. When it's the
only thing selected, it takes the --version, --variant, and --channel of
run_updater_test.py after --, as in
``run_testcases.py -p updater -- --version 8.6.1``.

Without those, it updates the SDK of this repository's version. If that SDK
hasn't been built in dl/, the updater test is reported as XFAIL, an expected
failure that doesn't fail the run. A version named with --version that hasn't
been built is an error.

Failure reports include assertion messages and tracebacks, including errors in
test hooks. Routine test output stays in the logs, and expected failures do not
print diagnostics.

Targets are defined in ~/.renpy/dev/testcases.toml. To create it, copy and edit
run_testcases.example.toml, which documents the format. Logs and artifacts are
kept in tmp/run-testcases/.

run_updater_test.py
-------------------

Tests the updater. run_testcases.py runs this test as well, and this script
runs it alone. On each target of run_testcases.py, apart from source targets,
this unpacks the SDK that was built into dl/<version>, uses its launcher to
update it to a nightly build, and checks that the launcher restarts as the new
version and that the_question's tests pass in it. The version defaults to that
of this repository, and --version picks another one. The update channel
defaults to Nightly Fix for a version in the series that's getting fixes and to
Nightly otherwise, and --channel picks another one.

The update is downloaded from the real update servers, so each target needs to
reach them. On a computer reached with ssh, the SDK is kept in the updater-test
directory inside the target's destination. Logs are kept in
tmp/run-updater-test/.

sign_update.py
---------------

This signs updates used by the Ren'Py updater.

update_copyright.py
-------------------

Updates the copyright line when the year changes.

update_piglatin.sh
------------------

Updates the piglatin translation.

utflf.py
--------

Fixes line endings and adds UTF-8 BOM to all rpy files in a directory.
