.. _character-callbacks:

Character Callbacks
===================

Ren'Py includes the ability to execute callbacks when various events
occur during dialogue. This is done by giving the `callback` argument
to :func:`Character`, or setting the :var:`config.character_callback` or
:var:`config.all_character_callbacks` variables.

The character callback is called with a single positional argument, the event
that occurred. Possible events are:

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

The callback is called with at the keyword arguments:

`interact`
    This is true if the dialogue causes an interaction to occur.

`type`
    The type of character (e.g. "nvl", "adv", "bubble").

`what`
    The text that is going to be supplied to the what displayable.

`multiple`
    The `multiple` argument to :func:`Character`.

The "show" and "slow_done" callbacks are also given additional keyword
arguments:

`start`
    The start of the current segment of dialogue, in the `what` string.

`end`
    The end of the current segment of dialogue, in the `what` string.

`delay`
    The amount of time Ren'Py will pause after the current segment of dialogue is shown,
    or None if Ren'Py will pause until the player clicks.

`last_segment`
    True if this is the last segment of dialogue in the say statement, False otherwise.


Other values of the positional argument and additional keyword arguments may
be supplied to the callback. The callback should be written to ignore keyword arguments it
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

To specialize a general callback with for specific characters, you can
pass arguments to the callback function with the `cb_` prefix::

    init python:
        def boopy_voice(event, interact=True, boopfile="normal_boop.ogg", **kwargs):
            if not interact:
                return

            if event == "show_done":
                renpy.sound.play(boopfile)
            elif event == "slow_done":
                renpy.sound.stop()

    define chrisjen = Character("Chrisjen", callback=boopy_voice)
    define nagata = Character("Naomi", callback=boopy_voice, cb_boopfile="sfx-blipmale.ogg")
