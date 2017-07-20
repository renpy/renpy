Interactive Director
====================

The Interactive Director is a too that allows you to edit the script of
your game from inside Ren'Py itself, with a live preview of the results
of your editing. The director is not not meant as a complete
replacement for the use of  a text editor, which is still required for
writing the dialogue, choices, and logic of the visual novel.

Rather, it's intended to help you direct your game's script, by adding:

* Image (say, show, and hide) statements.
* Transition (with) statements.
* Audio (play, queue, stop, and voice) statements.


Using the Director
------------------

You can access the director after starting your game by pressing the D
(without shift) key on your keyboard. If this is your first time in
a session running the director, Ren'Py will reload your game to ensure
it has the data required to edit it.

The first director screen you'll see shows a list of lines that ran before
the current line. Click outside the lines window to advance the script, or
rollback outside it to roll back. Click the + between a lines to add a line, or the ✎ before a
line to edit that line.

When editing a line, the statement type can be selected, along with
appropriate parameters. Choose "Add" to add the new line, "Change" to change
an existing line, "Cancel" to cancel editing, and "Remove" to remove an
existing line.

Click "Done" when finished editing.

Variables
---------

There are a number of variables defined in the ``director`` namespace that control
how the interactive director functions. These can be set using the define statement,
or modified using Python.


Scene, Show, and Hide
^^^^^^^^^^^^^^^^^^^^^

.. var:: director.tag_blacklist = { "black", "text", "vtext" }
    A blacklist of tags that will not be shown for the show, scene, or hide
    statements.

.. var:: director.scene_tags = { "bg" }
    The set of tags that will be presented for the scene statement, and hidden
    from the show statement.

.. var:: director.show_tags = set()
    If not empty, only the tags present in this set will be presented for the
    show statement.

.. var:: director.transforms = [ "left", "center", "right" ]
    A list of transforms that will be presented as part of the editor.
    In addition to these, any transform defined using the transform
    statement outside of Ren'Py itself will be added to the list of
    transforms, which is then sorted.

With
^^^^

.. var:: director.transitions = [ "dissolve", "pixellate" ]
    A list of transitions that are available to the with statement. Since
    transitions can't be auto-detected, these must be added manually.

Play, Queue, Stop, and Voice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. var:: director.audio_channels = [ "music", "sound", "audio" ]
    The name of the audio channels that can be used with the play, show
    and stop statements.

.. var:: director.voice_channel = "voice"
    The name of the audio channel used by voice.

.. var:: director.audio_patterns = [ "*.opus", "*.ogg", "*.mp3" ]
    The default list of audio patterns that are used to match the files
    available in an audio channel.

.. var:: director.audio_channel_patterns = { }
    A map from a channel name to the list of audio patterns that are
    available in that audio channel. For example, if this is set to
    ``{ 'sound' : [ 'sound/*.opus' ], 'music' : [ 'music/*.opus' ] }`` the
    music and sound channels get their own lists of patterns.

Access
^^^^^^

.. var:: director.button = True
    If True, the director displays a screen with a button to access the
    director window. If False, the game can provide it's own access, by
    making available the director.Start action.

Line Spacing
^^^^^^^^^^^^

.. var:: director.spacing = 1
    The spacing between a director (scene, show, hide, with, play, queue, and voice) line
    and a non-director line, or vice versa. These spacings should be 0 or 1 lines, a higher spacing
    may not work.

.. var:: director.director_spacing = 0
    The spacing between two consecutive director lines.

.. var:: director.other_spacing = 0
    The spacing between two consecutive non-director lines.

Viewport
^^^^^^^^

.. var:: director.viewport_height = 280
    The maximum height of scrolling viewports used by the director.

Audio Filename Functions
------------------------

There are a number of audio filename functions that can be used to convert
filenames on disk to filenames in Python source code. This can be used to
match Ren'Py functionality that maps filenames. For example, if one has::

    define config.voice_filename_format = "v/{filename}.ogg"

one can define the functions::

    init python in director:

        def audio_code_to_filename(channel, code):
            """
            This converts the name of an audio filename as seen in the code,
            to the filename as seen on disk.
            """

            if channel == "voice":
                return "v/" + code + ".ogg"

            return code

        def audio_filename_to_code(channel, fn):
            """
            This converts the name of an audio filename on disk to the filename
            as seen in code.
            """

            if channel == "voice":
                return fn.replace("v/", "").replace(".ogg", "")

            return fn

        def audio_filename_to_display(channel, fn):
            """
            This converts the audio filename as seen on disk so it can be
            presented to the creator.
            """

            if channel == "voice":
                return fn.replace("v/", "").replace(".ogg", "")

            return fn

to match it.

