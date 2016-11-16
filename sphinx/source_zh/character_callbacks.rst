.. _character-callbacks:

Character Callbacks
===================

Ren'Py includes the ability to execute callbacks when various events
occur during dialogue. This is done by giving the `callback` argument
to :func:`Character`, or setting the :var:`config.character_callback` or
:var:`config.all_character_callbacks` variables.

The character callback is called with a single positional argument, the event
that occured. Possible events are:

"begin"
    Called at the start of a say statement.

"show"
    Called before showing each segment of dialogue. Dialogue may be separated
    into multiple segments by the {w} or {p} text tags, but always consists of
    at least one segment.

"show_done"
    Called after showing each segment of dialogue.

"slow_done"
    Called after slow text finishes showing. Note that this event may occur
    after "end", in cases where dialogue does not cause an interaction
    to occur.

"end"
    Called at the end of a say statement.

The callback is called with at least one keyword argument:

`interact`
    This is true if the dialogue causes an interaction to occur.

Other values of the positional argument and additional keyword arguments may
be supplied in the future. The callback should coded to ignore arguments it
does not understand.

Example
-------

This example plays beeps in place of a character voice, when slow
text is enabled::

    init python:
        def beepy_voice(event, interact=True, **kwargs):
            if not interact:
                return

            if event == "show_done":
                renpy.sound.play("beeps.ogg")
            elif event == "slow_done":
                renpy.sound.stop()

    define pike = Character("Christopher Pike", callback=beepy_voice)

    label start:

        pike "So, hanging out on Talos IV, minding my own business, when..."
