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
