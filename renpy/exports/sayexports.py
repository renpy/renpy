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
from renpy.exports.commonexports import renpy_pure



class TagQuotingDict(object):

    def __getitem__(self, key):

        store = renpy.store.__dict__

        if key in store:
            rv = store[key]

            if isinstance(rv, basestring):
                rv = rv.replace("{", "{{")

            return rv
        else:
            if renpy.config.debug:
                raise Exception("During an interpolation, '%s' was not found as a variable." % key)
            return "<" + key + " unbound>"


tag_quoting_dict = TagQuotingDict()


def predict_say(who, what):
    """
    :undocumented:

    This is called to predict the results of a say command.
    """

    if who is None:
        who = renpy.store.narrator # type: ignore

    if isinstance(who, basestring):
        return renpy.store.predict_say(who, what)

    predict = getattr(who, 'predict', None)
    if predict:
        predict(what)


def scry_say(who, what, scry):
    """
    :undocumented:

    Called when scry is called on a say statement. Needs to set
    the interacts field.
    """

    try:
        scry.interacts = who.will_interact()
    except Exception:
        scry.interacts = True

    try:
        scry.extend_text = who.get_extend_text(what)
    except Exception:
        scry.extend_text = renpy.ast.DoesNotExtend


def say(who, what, *args, **kwargs):
    """
    :doc: se_say

    The equivalent of the say statement.

    `who`
        Either the character that will say something, None for the narrator,
        or a string giving the character name. In the latter case, the
        :var:`say` store function is called.

    `what`
        A string giving the line to say. Percent-substitutions are performed
        in this string.

    `interact`
        If true, Ren'Py waits for player input when displaying the dialogue. If
        false, Ren'Py shows the dialogue, but does not perform an interaction.
        (This is passed in as a keyword argument.)

    This function is rarely necessary, as the following three lines are
    equivalent. ::

        e "Hello, world."
        $ renpy.say(e, "Hello, world.")
        $ e("Hello, world.") # when e is not a string
        $ say(e, "Hello, world.") # when e is a string
    """

    if renpy.config.old_substitutions:
        # Interpolate variables.
        what = what % tag_quoting_dict

    if who is None:
        who = renpy.store.narrator # type: ignore

    if renpy.config.say_arguments_callback:
        args, kwargs = renpy.config.say_arguments_callback(who, *args, **kwargs)

    if isinstance(who, basestring):
        renpy.store.say(who, what, *args, **kwargs)
    else:
        who(what, *args, **kwargs)
