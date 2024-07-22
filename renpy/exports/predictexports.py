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

import fnmatch

import renpy


def cache_pin(*args):
    """
    :undocumented: Cache pinning has been removed.
    """

def cache_unpin(*args):
    """
    :undocumented: Cache pinning has been removed
    """


def expand_predict(d):
    """
    :undocumented:

    Use the fnmatch function to expland `d` for the purposes of prediction.
    """

    if not isinstance(d, basestring):
        return [ d ]

    if not "*" in d:
        return [ d ]

    if "." in d:
        l = renpy.exports.list_files(False)
    else:
        l = renpy.exports.list_images()

    return fnmatch.filter(l, d)


def start_predict(*args):
    """
    :doc: image_func

    This function takes one or more displayables as arguments. It causes
    Ren'Py to predict those displayables during every interaction until
    the displayables are removed by :func:`renpy.stop_predict`.

    If a displayable name is a string containing one or more \\*
    characters, the asterisks are used as a wildcard pattern. If there
    is at least one . in the string, the pattern is matched against
    filenames, otherwise it is matched against image names.

    For example::

        $ renpy.start_predict("eileen *")

    starts predicting all images with the name eileen, while::

        $ renpy.start_predict("images/concert*.*")

    matches all files starting with concert in the images directory.

    Prediction will occur during normal gameplay. To wait for prediction
    to complete, use the `predict` argument to :func:`renpy.pause`.
    """

    new_predict = renpy.revertable.RevertableSet(renpy.store._predict_set)

    for i in args:
        for d in expand_predict(i):
            d = renpy.easy.displayable(d)
            new_predict.add(d)

    renpy.store._predict_set = new_predict


def stop_predict(*args):
    """
    :doc: image_func

    This function takes one or more displayables as arguments. It causes
    Ren'Py to stop predicting those displayables during every interaction.

    Wildcard patterns can be used as described in :func:`renpy.start_predict`.
    """

    new_predict = renpy.revertable.RevertableSet(renpy.store._predict_set)

    for i in args:
        for d in expand_predict(i):
            d = renpy.easy.displayable(d)
            new_predict.discard(d)

    renpy.store._predict_set = new_predict


def start_predict_screen(_screen_name, *args, **kwargs):
    """
    :doc: screens

    Causes Ren'Py to start predicting the screen named `_screen_name`
    with the given arguments. This replaces any previous prediction
    of `_screen_name`. To stop predicting a screen, call :func:`renpy.stop_predict_screen`.

    Prediction will occur during normal gameplay. To wait for prediction
    to complete, use the `predict` argument to :func:`renpy.pause`.
    """

    new_predict = renpy.revertable.RevertableDict(renpy.store._predict_screen)
    new_predict[_screen_name] = (args, kwargs)
    renpy.store._predict_screen = new_predict


def stop_predict_screen(name):
    """
    :doc: screens

    Causes Ren'Py to stop predicting the screen named `name`.
    """

    new_predict = renpy.revertable.RevertableDict(renpy.store._predict_screen)
    new_predict.pop(name, None)
    renpy.store._predict_screen = new_predict


def predicting():
    """
    :doc: other

    Returns true if Ren'Py is currently in a predicting phase.
    """

    return renpy.display.predict.predicting
