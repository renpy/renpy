==========
Text Input
==========

With some limitations, Ren'Py can prompt the user to input a small
amount of text. This prompting is done by the :func:`renpy.input` function,
which returns the entered text, allowing it to be saved in a variable
or otherwise processed.

On Linux, text input is limited to languages that do not require
input method (IME) support. Most Western languages should work, but
Chinese, Japanese, and Korean probably won't.

The renpy.input function is defined as:

.. include:: inc/input

Games that use renpy.input will often want to process the result
further, using standard Python string manipulation functions. For
example, the following will ask the player for his or her
name and remove leading or trailing whitespace. If the name is
empty, it will be replaced by a default name. Finally, it is
displayed to the user. ::

    define pov = Character("[povname]")

    python:
        povname = renpy.input("What is your name?", length=32)
        povname = povname.strip()

        if not povname:
             povname = "Pat Smith"

    pov "My name is [povname]!"

In this, the length of the input is limited to 32 characters. It's important
to test your game with long names, to makes sure that those names do not break
text layout. At the same time, too short fields may prevent people from entering
their preferred name.

.. _input-methods:

Input Methods
=============

When an input method editor (IME) supplies composition text, Ren'Py draws
it inside the input displayable. On platforms where SDL supplies candidate
events, Ren'Py also draws the candidate list rather than relying on the
operating system's candidate window. This allows the candidates to be seen
when the game is fullscreen.

Candidate events are supported on Windows. SDL's Linux IBus and Fcitx
backends do not currently supply candidate events or suppress the native
candidate window, so those backends continue to use the system candidate
interface. Setting ``SDL_IME_IMPLEMENTED_UI`` does not enable candidate
events on an unsupported backend.

When candidate events are supplied, the list is displayed by the
``_ime_candidates`` screen, which Ren'Py shows and hides as required.
The screen is placed next to the text
being entered, and can be customized by changing the following styles:

``_ime_candidates_frame``
    The frame containing the candidate list.

``_ime_candidates_box``
    The box containing the candidates.

``_ime_candidates_item_frame``, ``_ime_candidates_selected_item_frame``
    The frames around an unselected candidate and the selected candidate.

``_ime_candidates_text``, ``_ime_candidates_selected_text``
    The text of an unselected candidate and the selected candidate.

For example::

    style _ime_candidates_frame:
        background "#202040e0"

    style _ime_candidates_selected_text:
        color "#ffff00"
