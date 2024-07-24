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

def notify(message):
    """
    :doc: other

    Causes Ren'Py to display the `message` using the notify screen. By
    default, this will cause the message to be dissolved in, displayed
    for two seconds, and dissolved out again.

    This is useful for actions that otherwise wouldn't produce feedback,
    like screenshots or quicksaves.

    Only one notification is displayed at a time. If a second notification
    is displayed, the first notification is replaced.

    This function just calls :var:`config.notify`, allowing its implementation
    to be replaced by assigning a new function to that variable.
    """

    renpy.config.notify(message)


def display_notify(message):
    """
    :doc: other

    The default implementation of :func:`renpy.notify`.
    """

    renpy.exports.hide_screen('notify')
    renpy.exports.show_screen('notify', message=message)
    renpy.display.tts.notify_text = renpy.text.extras.filter_alt_text(message)

    renpy.exports.restart_interaction()


def confirm(message):
    """
    :doc: other

    This causes the a yes/no prompt screen with the given message
    to be displayed, and dismissed when the player hits yes or no.

    Returns True if the player hits yes, and False if the player hits no.

    `message`
        The message that will be displayed.

    See :func:`Confirm` for a similar Action.
    """
    Return = renpy.store.Return
    renpy.store.layout.yesno_screen(message, yes=Return(True), no=Return(False))
    return renpy.ui.interact()
