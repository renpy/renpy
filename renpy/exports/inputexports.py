# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy


def web_input(prompt, default='', allow=None, exclude='{}', length=None, mask=False):
    """
    :undocumented:

    This provides input in the web environment, when config.web_input is True.
    """

    renpy.exports.mode('input')

    prompt = renpy.text.extras.filter_text_tags(prompt, allow=set())

    roll_forward = renpy.exports.roll_forward_info()
    if not isinstance(roll_forward, basestring):
        roll_forward = None

    # use previous data in rollback
    if roll_forward is not None:
        default = roll_forward

    wi = renpy.display.behavior.WebInput(renpy.exports.substitute(prompt), default, length=length, allow=allow, exclude=exclude, mask=mask)
    renpy.ui.add(wi)

    renpy.exports.shown_window()

    if renpy.config.autosave_on_input and not renpy.game.after_rollback:
        renpy.loadsave.force_autosave(True)

    rv = renpy.ui.interact(mouse='prompt', type="input", roll_forward=roll_forward)
    renpy.exports.checkpoint(rv)

    with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    return rv


def input(prompt, default='', allow=None, exclude='{}', length=None, with_none=None, pixel_width=None, screen="input", mask=None, copypaste=True, multiline=False, **kwargs): # @ReservedAssignment
    """
    :doc: input
    :args: (default='', allow=None, exclude='{}', length=None, pixel_width=None, screen="input", mask=None, copypaste=True, multiline=False, **kwargs)

    Calling this function pops up a window asking the player to enter some
    text. It returns the entered text.

    `prompt`
        A string giving a prompt to display to the player.

    `default`
        A string giving the initial text that will be edited by the player.

    `allow`
        If not None, a string giving a list of characters that will
        be allowed in the text.

    `exclude`
        If not None, if a character is present in this string, it is not
        allowed in the text.

    `length`
        If not None, this must be an integer giving the maximum length
        of the input string.

    `pixel_width`
        If not None, the input is limited to being this many pixels wide,
        in the font used by the input to display text.

    `screen`
        The name of the screen that takes input. If not given, the ``input``
        screen is used.

    `mask`
        If not None, a single-character string that replaces the input text that
        is shown to the player, such as to conceal a password.

    `copypaste`
        When true, copying from and pasting to this input is allowed.

    `multiline`
        When true, move caret to next line is allowed.

    If :var:`config.disable_input` is True, this function only returns
    `default`.

    Keywords prefixed with ``show_`` have the prefix stripped and
    are passed to the screen.

    Due to limitations in supporting libraries, on Android and the web platform
    this function is limited to alphabetic characters.
    """

    if renpy.config.disable_input:
        return default

    fixed = renpy.exports.in_fixed_rollback()

    if (not PY2) and renpy.emscripten and renpy.config.web_input and not fixed:
        return web_input(prompt, default, allow, exclude, length, bool(mask))

    renpy.exports.mode('input')

    roll_forward = renpy.exports.roll_forward_info()
    if not isinstance(roll_forward, basestring):
        roll_forward = None

    # use previous data in rollback
    if roll_forward is not None:
        default = roll_forward

    # put arguments with show_ prefix aside
    show_properties, kwargs = renpy.easy.split_properties(kwargs, "show_", "")

    if kwargs:
        raise TypeError("renpy.input() got unexpected keyword argument(s): {}".format(", ".join(kwargs.keys())))

    if renpy.exports.has_screen(screen):
        widget_properties = { }
        widget_properties["input"] = dict(default=default, length=length, allow=allow, exclude=exclude, editable=not fixed, pixel_width=pixel_width, mask=mask, copypaste=copypaste, multiline=multiline)

        renpy.exports.show_screen(screen, _transient=True, _widget_properties=widget_properties, prompt=prompt, **show_properties)

    else:

        if screen != "input":
            raise Exception("The '{}' screen does not exist.".format(screen))

        renpy.ui.window(style='input_window')
        renpy.ui.vbox()

        renpy.ui.text(prompt, style='input_prompt')

        inputwidget = renpy.ui.input(default, length=length, style='input_text', allow=allow, exclude=exclude)

        # disable input in fixed rollback
        if fixed:
            inputwidget.disable()

        renpy.ui.close()

    renpy.exports.shown_window()

    if renpy.config.autosave_on_input and not renpy.game.after_rollback:
        renpy.loadsave.force_autosave(True)

    # use normal "say" click behavior if input can't be changed
    if fixed:
        renpy.ui.saybehavior()

    rv = renpy.ui.interact(mouse='prompt', type="input", roll_forward=roll_forward)
    renpy.exports.checkpoint(rv)

    if with_none is None:
        with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    return rv


def get_editable_input_value():
    """
    :undocumented:

    Returns the current input value, and a flag that is true if it is editable.
    and false otherwise.
    """

    return renpy.display.behavior.current_input_value, renpy.display.behavior.input_value_active


def set_editable_input_value(input_value, editable):
    """
    :undocumented:

    Sets the currently active input value, and if it should be marked as
    editable.
    """

    renpy.display.behavior.current_input_value = input_value
    renpy.display.behavior.input_value_active = editable
