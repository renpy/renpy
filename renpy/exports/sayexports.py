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


def do_reshow_say(who, what, interact=False, *args, **kwargs):

    if who is not None:
        who = renpy.python.py_eval(who)

    say(who, what, *args, interact=interact, **kwargs)


curried_do_reshow_say = renpy.curry.curry(do_reshow_say)


def get_reshow_say(**kwargs):
    kw = dict(renpy.store._last_say_kwargs)
    kw.update(kwargs)

    return curried_do_reshow_say(
        renpy.store._last_say_who,
        renpy.store._last_say_what,
        renpy.store._last_say_args,
        **kw)


def reshow_say(**kwargs):
    get_reshow_say()(**kwargs)


def get_say_attributes():
    """
    :doc: other

    Gets the attributes associated with the current say statement, or
    None if no attributes are associated with this statement.

    This is only valid when executing or predicting a say statement.
    """

    return renpy.game.context().say_attributes


def get_side_image(prefix_tag, image_tag=None, not_showing=None, layer=None):
    """
    :doc: side

    This attempts to find an image to show as the side image.

    It begins by determining a set of image attributes. If `image_tag` is
    given, it gets the image attributes from the tag. Otherwise, it gets
    them from the image property suplied to the currently showing character.
    If no attributes are available, this returns None.

    It then looks up an image with the tag `prefix_tag`, and attributes
    consisting of:

    * An image tag (either from `image_tag` or the image property supplied
      to the currently showing character).
    * The attributes.

    If such an image exists, it's returned.

    `not_showing`
        If not showing is True, this only returns a side image if an image
        with the tag that the attributes are taken from is not currently
        being shown. If False, it will always return an image, if possible.
        If None, takes the value from :var:`config.side_image_only_not_showing`.

    `layer`
        If given, the layer to look for the image tag and attributes on. If
        None, uses the default layer for the tag.
    """

    if not_showing is None:
        not_showing = renpy.config.side_image_only_not_showing

    images = renpy.game.context().images

    if image_tag is not None:
        image_layer = default_layer(layer, image_tag)
        attrs = (image_tag,) + images.get_attributes(image_layer, image_tag)

        if renpy.config.side_image_requires_attributes and (len(attrs) < 2):
            return None

    else:

        # Character will compute the appropriate attributes, and stores it
        # in _side_image_attributes.
        attrs = renpy.store._side_image_attributes

    if not attrs:
        return None

    attr_layer = renpy.exports.default_layer(layer, attrs)

    if not_showing and images.showing(attr_layer, (attrs[0],)):
        return None

    required = [ attrs[0] ]
    optional = list(attrs[1:])

    return images.choose_image(prefix_tag, required, optional, None)
