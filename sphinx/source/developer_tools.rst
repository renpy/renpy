Developer Tools
===============

Ren'Py includes a number of features to make a developer's life easier. Many of
them need the variable :var:`config.developer` to be set to True to operate.

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

Shift+E Editor Support
----------------------

The :var:`config.editor` variable allows a developer to specify an editor
command that is run when the launch_editor keypress (by default, Shift+E)
occurs.

please see :ref:`Text Editor Integration <text-editor-integration>`

Shift+D Developer Menu
----------------------

When :var:`config.developer` is True, hitting Shift+D will display a developer
menu that provides easy access to some of the features given below.

Shift+R Reloading
-----------------

When :var:`config.developer` is True, hitting Shift+R will save the current
game, reload the game script, and reload the game. This will often place you at
the last unchanged statement encountered before Shift+R was pressed.

This allows the developer to make script changes with an external editor, and
not have to exit and restart Ren'Py to see the effect of the changes.

Note that game state, which includes variable values and scene lists, is
preserved across the reload. This means that if one of those statements is
changed, it is necessary to rollback and re-execute the statement to see its
new effect.

Shift+I Style Inspecting
------------------------

When :var:`config.developer` is True, pressing Shift+I will cause style
inspection to occur. This will display a list of displayables underneath the
mouse. For each displayable, it will display the type, the style used, and the
size it is being rendered at.

Shift+Y Style Dumping
---------------------

When :var:`config.developer` is True, pressing the dump_styles key (by default,
Shift+Y), will write a description of every style Ren'Py knows about to the
file "styles.txt". This description includes every property that is part of the
style, the value of that property, and the style the property is inherited
from.

> Fast Skipping
---------------

When :var:`config.developer` or :var:`config.fast_skipping` is True, pressing
the ``fast_skip`` key (by default, ">") causes the the game to immediately skip to
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
example ::

    renpy.exe my_project --warp script.rpy:458

(Where `my_project` is the full path to the base directory of your project.)

When warping is invoked, Ren'Py does a number of things. It first finds all of
the scene statements in the program. It then tries to find a path from the
scene statements to every reachable statement in the game. It then picks the
reachable statement closest to, but before or at, the given line. It works
backwards from that statement to a scene statement, recording the path it took.
Ren'Py then executes the scene statement and any show or hide statements found
along that path. Finally, it transfers control to the found statement.

There are a number of fairly major caveats to the warp feature. The first is
that it only examines a single path, which means that while the path may be
representative of some route of execution, it's possible that there may be a
bug along some other route. In general, the path doesn't consider game logic,
so it's also possible to have a path that isn't actually reachable. (This is
only really a problem on control-heavy games, especially those that use a lot of
Python.

The biggest problem, though, is that Python is not executed before the
statement that is warped to. This means that all variables will be
uninitialized, which can lead to crashes when they are used. To overcome this,
one can define a label ``after_warp``, which is called after a warp but before
the warped-to statement executes. This label can set up variables in the
program, and then return to the preview.

The warp feature requires :var:`config.developer` to be True to operate.


Debug Functions
---------------

.. include:: inc/debug
