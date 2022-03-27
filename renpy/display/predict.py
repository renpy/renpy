# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains the routines that manage image prediction.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import renpy

# Called to indicate an image should be loaded or preloaded. This is
# a function that takes an image manipulator, set by reset and predict,
# and winds up bound to either im.cache.get or im.cache.preload_image
image = None

# The set of displayables we've predicted since reset was last called.
predicted = set()

# A flag that indicates if we're currently predicting.
predicting = False

# A list of (screen name, argument dict) tuples, giving the screens we'd
# like to predict.
screens = [ ]


def displayable(d):
    """
    Called to predict that the displayable `d` will be shown.
    """

    if d is None:
        return

    if d not in predicted:
        predicted.add(d)
        d.visit_all(lambda i : i.predict_one())


def screen(_screen_name, *args, **kwargs):
    """
    Called to predict that the named screen is about to be shown
    with the given arguments.
    """

    screens.append((_screen_name, args, kwargs))


def reset():
    global image
    image = renpy.display.im.cache.get_texture
    predicted.clear()
    del screens[:]


def prediction_coroutine(root_widget):
    """
    The image prediction co-routine. This predicts the images that can
    be loaded in the near future, and passes them to the image cache's
    preload_image method to be queued up for loading.

    The .send should be called with True to do a expensive prediction,
    and with False to either do an inexpensive prediction or no
    prediction at all.

    Returns True if there's more predicting to be done, or False
    if there's no more predicting worth doing.
    """

    global predicting

    # Start the prediction thread (to clean out the cache).
    renpy.display.im.cache.start_prediction()

    # Wait to be told to start.
    yield True

    # Set up the image prediction method.
    global image
    image = renpy.display.im.cache.preload_image

    predicting = True

    # Predict displayables given to renpy.start_predict.
    for d in renpy.store._predict_set:
        displayable(d)

        predicting = False
        yield True
        predicting = True

    # Predict images that are going to be reached in the next few
    # clicks.

    for _i in renpy.game.context().predict():

        predicting = False
        yield True
        predicting = True

    # If there's a parent context, predict we'll be returning to it
    # shortly. Otherwise, call the functions in
    # config.predict_callbacks.

    if len(renpy.game.contexts) >= 2:
        sls = renpy.game.contexts[-2].scene_lists

        for l in sls.layers.values():
            for sle in l:
                try:
                    displayable(sle.displayable)
                except Exception:
                    pass

    else:
        for i in renpy.config.predict_callbacks:
            i()

    predicting = False

    while not (yield False):
        continue

    predicting = True

    for i in renpy.config.expensive_predict_callbacks:
        done = False
        while not done:
            if not i():
                done = True

            predicting = False
            yield False
            predicting = True

    predicted_screens = [ ]

    # Predict screens given with renpy.start_predict_screen.
    for name, value in list(renpy.store._predict_screen.items()):
        args, kwargs = value

        predicted_screens.append((name, args, kwargs))

        renpy.display.screen.predict_screen(name, *args, **kwargs)

        predicting = False
        yield False
        predicting = True

    # Predict things (especially screens) that are reachable through
    # an action.
    predicting = True

    try:
        root_widget.visit_all(lambda i : i.predict_one_action())
    except Exception:
        if renpy.config.debug_prediction:
            import traceback

            print("While predicting actions.")
            traceback.print_exc()
            print()

    predicting = False

    # Predict the screens themselves.
    for t in screens:

        while not (yield False):
            continue

        if t in predicted_screens:
            continue

        predicted_screens.append(t)

        name, args, kwargs = t

        if name.startswith("_"):
            continue

        predicting = True

        renpy.display.screen.predict_screen(name, *args, **kwargs)

        predicting = False

    yield None
