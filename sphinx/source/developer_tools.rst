Developer Tools
===============

Ren'Py includes a number of features to make a developer's life easier. Many of
them need the variable :var:`config.developer` to be set to True to operate.

.. _lint:

Lint
----

The Lint tool (available from the launcher) checks the game for potential errors
or misoptimizations, and advises the developing team about how to best improve it.
Since some of these errors will only affect users on other platforms, it’s
recommended to understand and fix all errors, even if the problem can't be
triggered locally.

Lint also includes useful infos and stats about the game.

Note that using Lint is not a substitute for thorough testing.

.. _console:

Shift+O Console
---------------

The debug console makes it possible to interactively run Ren'Py script and
Python statements, and immediately see the results. The console is available in
developer mode or when :var:`config.console` is True, and can be accessed by
pressing Shift+O.

The console can be used to:

* Jump to a label.
* Interactively try out Ren'Py script statements.
* Evaluate a Python expression or statement to see the result.
* Trace Python expressions as the game progresses.

.. include:: inc/console_commands

Shift+E Editor Support
----------------------

Shift+E opens the default text editor, as set in the launcher and customizable
using :doc:`editor`, to open the script file in and line number at which the
current statement is written.

Shift+D Developer Menu
----------------------

When :var:`config.developer` is true, hitting Shift+D will display a developer
menu that provides easy access to some of the features given below.

Shift+R Reloading
-----------------

When :var:`config.developer` is True, hitting Shift+R will save the current
game, reload the game script, and reload the game. This will often place you at
the last unchanged statement encountered before Shift+R was pressed.

After the first reload, the game will be in autoreload mode, and any changes
to files accessed since the last reload will cause the game to be reloaded
again.

This allows the developer to make script changes with an external editor, and
not have to exit and restart Ren'Py to see the effect of the changes.

Note that game state, which includes variable values and scene lists, is
preserved across the reload. This means that if one of those statements is
changed, it is necessary to rollback and re-execute the statement to see its
new effect.

Shift+R reloading does not work in a replay.

The following functions implement the same behavior in pure python. Note that
they are only meant to be used in developer mode.

.. include:: inc/reload

.. _style-inspector:

Shift+I Style Inspecting
------------------------

When :var:`config.developer` is true, pressing Shift+I will cause style
inspection to occur. This will display a list of displayables underneath the
mouse, in the order they are drawn to the screen (that is, the last displayable
is the one on top of the others). For each displayable, it will display the
type, the style used, and the size it is being rendered at.

Clicking on the style name will display the styles the displayable inherits
from, and the properties each style contributes to the final displayable.

> Fast Skipping
---------------

When :var:`config.developer` or :var:`config.fast_skipping` is True, pressing
the `fast_skip` key (by default, ">") causes the game to immediately skip to
the next important interaction.  For this purpose, an important interaction is
one that is not caused by a say statement, transition, or pause command.
Usually, this means skipping to the next menu, but it will also stop when
user-defined forms of interaction occur.

.. _warping_to_a_line:

Warping to a Line
------------------

Ren'Py supports warping to a line in the script, without the developer to play
through the entire game to get there. While this warping technique has a number
of warnings associated with it, it still may be useful in providing a live
preview.

To invoke warping, run Ren'Py with the ``--warp`` command-line argument followed
by a filename:line combination, to specify where you would like to warp to. For
example::

    renpy.exe my_project --warp script.rpy:458

(Where `my_project` is the full path to the base directory of your project.)

When warping is invoked, Ren'Py picks the statement closest to, but before or
at, the given line, and works backwards to infer a path leading to it. Up to
``config.warp_limit`` statements from the end of that path are considered.
Ren'Py executes warp-compatible statements, such as scene, show, and hide,
along the path. Finally, it transfers control to the target statement.

Dialogue by ADV, NVL, and bubble characters is also replayed to reconstruct
state, without waiting for input:

* ADV dialogue adds completed lines to the history.
* NVL dialogue adds completed lines to the history and NVL list. ``nvl clear``
  and a character's ``clear=True`` setting clear the NVL list without clearing
  history.
* Bubble dialogue adds completed lines to the history, reconstructs retained
  bubbles, and updates bubble layout properties. Bubbles are cleared according
  to the bubble database and :var:`bubble.clear_retain_statements`, including
  at skipped menus and ``call screen`` statements. Those statements are not
  otherwise executed.

History and NVL list length limits still apply. Reconstructed history entries
do not represent rollback checkpoints. The target statement is not replayed:
it executes normally after ``after_warp``.

Characters support replay by default; ``Character(..., warp=False)`` disables
it for a particular character. Other say callables are skipped unless their
``warp`` attribute is True. An opted-in callable is called normally and can
use :func:`renpy.is_warping` to avoid interactions and other side effects.
Built-in characters suppress interaction callbacks, voice hooks, and say
transitions during replay, but text filters, substitutions, dynamic names,
history callbacks, and character preparation/completion hooks still run.
Opting in does not make arbitrary application code safe to replay.

If a replayed say statement raises an ordinary exception, Ren'Py logs it,
ignores that statement, and continues warping. This includes failures while
resolving the sayer or evaluating arguments and substitutions. Quit, restart,
and other engine control-flow exceptions are not ignored. Temporary replay
state is restored, but arbitrary side effects performed before an exception
cannot be undone.

There are a number of fairly major caveats to the warp feature. The first is
that it only examines a single path, which means that while the path may be
representative of some route of execution, it's possible that there may be a
bug along some other route. In general, the path doesn't consider game logic,
so it's also possible to have a path that isn't actually reachable. (This is
only really a problem on control-heavy games, especially those that use a lot of
Python.)

The biggest problem, though, is that Python is not executed before the
statement that is warped to. This means that all variables will be
uninitialized, which can lead to crashes when they are used. To overcome this,
one can define a label ``after_warp``, which is called after a warp but before
the warped-to statement executes. This label can set up variables in the
program, and then return to the preview. This setup occurs after dialogue
reconstruction, so it cannot repair preceding lines that failed to replay.
Initialized defaults remain available during replay.

Translations are used when replaying a complete dialogue translation block.
If the target or the warp limit cuts through a multi-statement translation
block, warp replays the available source-language prefix: there is no general
mapping from part of a source block to part of its translation. As with route
selection, this remains best-effort rather than a full playthrough.

The warp feature requires :var:`config.developer` to be True to operate.


Debug Functions
---------------

.. include:: inc/debug


.. _launcher-customization:

Launcher Customization
----------------------

It's possible to customize the Ren'Py launcher to select the files and directories
that are available to click on. To do this, create project.json with the lines below::

    {
        "renpy_launcher":
        {
            "open_directory":
            {
                "game": "game",
                "base": ".",
                "images": "game/images",
                "audio": "game/audio",
                "gui": "game/gui"
            },
            "edit_file":
            {
                "script.rpy": "game/script.rpy",
                "options.rpy": "game/options.rpy",
                "gui.rpy": "game/gui.rpy",
                "screens.rpy": "game/screens.rpy"
            }
        }
    }

If the file already exists, you'll want to edit in the renpy_launcher key and the lines below it.
You can then edit the dictionaries to change the available files and directories.
