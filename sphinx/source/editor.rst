.. _text-editor-integration:

=======================
Text Editor Integration
=======================

Ren'Py uses a text editor to allow the user to edit game scripts from the
launcher, and to report errors to the user. By default, Ren'Py uses jEdit
as the text editor when launched from the launcher and the system default
editor otherwise. This can be customized by the user as necessary.

The editor is customized by creating an Editor class in a .edit.py file. This
class contains methods that are called to manage text editing.

When run directly, Ren'Py first looks at the RENPY_EDIT_PY environment
variable to find an .edit.py file to use. If it can find one, it uses the
Editor class defined in that file. If not, it uses a built-in editor class
that launches the editor in a system-specific manner.

When the Ren'Py Launcher is run, it scans subdirectories of the projects
directory and Ren'Py directory to find files of the form `name`.edit.py. (For
example, it would find launcher/jEdit.edit.py and myeditor/MyEditor.edit.py.)
The latest editor with a given `name` is presented to the creator as part of
the launcher options. The launcher also sets RENPY_EDIT_PY to the selected
file, so that games launched from the launcher will use the selected editor.


Writing an .edit.py File
------------------------

An edit.py file is a Python (not Ren'Py) file that must define a single
class, named Editor. Ren'Py will call methods on this class to cause
editing to occur.

Use of the editor is done as part of an editor transaction, which groups
related operations together. For example, if an editor transaction asks
for a new window, all of the files in that transaction should be opened
in the same new window. An editor transaction starts with a call to the
begin method, may contain one or more calls to operation methods, and ends
with a call to the end method.

The edit.py file should import renpy.editor, and the Editor class should
inherit from renpy.editor.Editor. As additional keyword arguments may be
added to methods, each method you define should ignore unknown keyword
arguments. Since you're expected to define your own
Editor subclass, we present the methods with the `self` parameter.

.. class:: Editor

  .. method:: begin(self, new_window=False, **kwargs)

    Starts an editor transaction.

    If `new_window` is true, the editor should attempt to open a new window.
    Otherwise, it should attempt to perform the transaction in an existing editor
    window.

  .. method:: end(self, **kwargs)

    Ends a transaction.

  .. method:: open(self,  filename, line=None, **kwargs)

    Opens a `filename` in the editor.

    If `line` is not None, attempts to position the editing cursor at `line`.
