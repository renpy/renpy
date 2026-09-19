# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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
import time
import asyncio

from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *

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
screens = []

# A list of translation ids for the statement being predicted.
tlids = list[str | None]

# The statement currently being predicted, or None outside statement prediction.
statement = None


def displayable(d):
    """
    Called to predict that the displayable `d` will be shown.
    """

    if d is None:
        return

    if d not in predicted:
        predicted.add(d)
        d.visit_all(lambda i: i.predict_one())
        predict_displayable_shaders(d)


def predict_displayable_shaders(d):
    stack = [(d, ())]
    seen = set()

    while stack:
        d, shaders = stack.pop()
        key = (id(d), shaders)

        if key in seen:
            continue

        seen.add(key)
        children = d.predict_shaders(shaders)
        stack.extend(reversed(children))


def predict_registered_shaders():
    for shaders in renpy.store._predict_shader:
        renpy.gl2.gl2shadercache.predict_shader(shaders)


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


async def prediction_coroutine(root_widget: renpy.display.displayable.Displayable):
    """
    The image predictiont coroutine. This predicts the images that can
    be loaded in the near future, and passes them to the image cache's
    preload_image method to be queued up for loading.
    """

    global predicting

    # Start the prediction thread (to clean out the cache).
    renpy.display.im.cache.start_prediction()

    # Wait to be told to start.
    await asyncio.sleep(0)

    # Set up the image prediction method.
    global image
    image = renpy.display.im.cache.preload_image

    predicting = True

    # Predict displayables given to renpy.start_predict.
    for d in renpy.store._predict_set:
        try:
            displayable(d)
        except Exception:
            if renpy.config.debug_prediction:
                raise

        await asyncio.sleep(0)

    # Predict images that are going to be reached in the next few
    # clicks.

    for _i in renpy.game.context().predict():
        await asyncio.sleep(0)

    # If there's a parent context, predict we'll be returning to it
    # shortly. Otherwise, call the functions in
    # config.predict_callbacks.

    predicted_screens = []

    if len(renpy.game.contexts) >= 2:
        sls = renpy.game.contexts[-2].scene_lists

        for l in sls.layers.values():
            for sle in l:
                try:
                    displayable(sle.displayable)
                except Exception:
                    pass

                await asyncio.sleep(0)

    else:
        for i in renpy.config.predict_callbacks:
            i()
            await asyncio.sleep(0)

        # Predict the game menu screen.

        s = getattr(renpy.store, "_game_menu_screen", None)

        if s is not None:

            if renpy.display.screen.has_screen(s):
                renpy.display.screen.predict_screen(s)
                predicted_screens.append((s, (), {}))


            elif s.endswith("_screen"):
                s = s[:-7]
                if renpy.display.screen.has_screen(s):
                    renpy.display.screen.predict_screen(s)
                    predicted_screens.append((s, (), {}))

            await asyncio.sleep(0)

    # Predict that overlay screens will be shown.
    for i in renpy.config.overlay_screens:
        renpy.display.screen.predict_screen(i)
        predicted_screens.append((i, (), {}))
        await asyncio.sleep(0)

    # Predict screens given with renpy.start_predict_screen.
    for name, value in list(renpy.store._predict_screen.items()):
        args, kwargs = value

        predicted_screens.append((name, args, kwargs))

        renpy.display.screen.predict_screen(name, *args, **kwargs)
        await asyncio.sleep(0)


    # Predict things (especially screens) that are reachable through
    # an action.
    predicting = True

    try:
        root_widget.visit_all(lambda i: i.predict_one_action())
    except Exception:
        if renpy.config.debug_prediction:
            import traceback

            print("While predicting actions.")
            traceback.print_exc()
            print()


    # Predict screens reachable through actions
    for t in screens:
        if t in predicted_screens:
            continue

        predicted_screens.append(t)

        name, args, kwargs = t

        if name.startswith("_"):
            continue

        await asyncio.sleep(0)

        renpy.display.screen.predict_screen(name, *args, **kwargs)

    predict_registered_shaders()
    await asyncio.sleep(0)

    # Pre-build shader combinations exposed by prediction.
    while renpy.gl2.gl2shadercache.has_predicted_shaders():
        renpy.gl2.gl2shadercache.preload_predicted_shader()
        await asyncio.sleep(0)

    renpy.gl2.assimp.finish_predict()
