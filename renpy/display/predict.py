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

from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *
from renpy.display.displayable import Displayable

import renpy

# Called to indicate an image should be loaded or preloaded. This is
# a function that takes an image manipulator, set by reset and predict,
# and winds up bound to either im.cache.get or im.cache.preload_image
image = None

# The set of displayable ids we've predicted since reset was last called.
predicted: set[int] = set()

# A list of displayables we've predicted, to keep them alive and prevent id reuse.
predicted_displayables: list[Displayable] = []

# A flag that indicates if we're currently predicting.
predicting = False

# A list of (screen name, argument dict) tuples, giving the screens we'd
# like to predict.
screens = []

# A list of translation ids for the statement being predicted.
tlids = list[str | None]

# The statement currently being predicted, or None outside statement prediction.
statement = None


# A list of (displayable, shader) tuples that are pending to be predicted. This is a worklist used
# in predict_pending.
pending: list[tuple[Displayable, tuple]] = []


def displayable(d):
    """
    Called to predict that the displayable `d` will be shown.
    """

    if d is None:
        return

    id_d = id(d)

    if id_d not in predicted:
        predicted.add(id_d)
        predicted_displayables.append(d)
        pending.append((d, ()))


def predict_pending(limited=False):
    """
    Predicts displayable loading and shaders for all of the pending displayables.

    `limited`
        Avoid predicting actions.
    """

    while pending:
        d, shaders = pending.pop()

        try:
            d.predict_one()
            shaders = d.predict_shaders(shaders)
        except Exception:
            if renpy.config.debug_prediction:
                import traceback

                print(f"While predicting {d!r}:")
                traceback.print_exc()
                print()
            continue

        if not limited:
            try:
                d.predict_one_action()
            except Exception:
                if renpy.config.debug_prediction:
                    import traceback

                    print("While predicting actions.")
                    traceback.print_exc()
                    print()

        try:
            children = d.visit()
        except Exception:
            children = []

        for i in reversed(children):
            if i is None:
                continue

            id_i = id(i)

            if id_i not in predicted:
                predicted.add(id_i)
                predicted_displayables.append(i)
                pending.append((i, shaders))

        yield from predict_sleep()


def predict_registered_shaders():
    for shaders in renpy.store._predict_shader:
        renpy.gl2.gl2shadercache.predict_shader(shaders)

        yield from renpy.display.predict.predict_sleep()


def screen(_screen_name, *args, **kwargs):
    """
    Called to predict that the named screen is about to be shown
    with the given arguments.
    """

    screens.append((_screen_name, args, kwargs))


def reset():
    global predicting
    predicting = False
    global image
    image = renpy.display.im.cache.get_texture
    predicted.clear()
    del predicted_displayables[:]
    del pending[:]
    del screens[:]


# The last time we paused prediction. We do so every .1ms.
next_predict_pause_ns: int = 0


def predict_sleep():
    """
    Yield from this to let prediction tasks release control to the scheduler.
    This may also be called from a non-predicting context.
    """
    global predicting
    global next_predict_pause_ns

    # If we're not predicting, we do not pause execution.
    if not predicting:
        return

    now_ns = time.perf_counter_ns()

    if now_ns < next_predict_pause_ns:
        return

    next_predict_pause_ns = now_ns + 100_000

    old_predicting = predicting
    predicting = False

    old_ui_screen = renpy.ui.screen
    renpy.ui.screen = None

    old_current_screen_stack = renpy.display.screen.current_screen_stack
    renpy.display.screen.current_screen_stack = []
    old_current_screen = renpy.display.screen._current_screen
    renpy.display.screen._current_screen = None

    old_ui_stack = renpy.ui.stack
    old_ui_at_stack = renpy.ui.at_stack
    old_ui_imagemap_stack = renpy.ui.imagemap_stack
    old_ui_add_tag = renpy.ui.add_tag

    renpy.ui.reset()

    try:
        yield
    finally:
        renpy.ui.stack = old_ui_stack
        renpy.ui.at_stack = old_ui_at_stack
        renpy.ui.imagemap_stack = old_ui_imagemap_stack
        renpy.ui.add_tag = old_ui_add_tag

        renpy.display.screen.current_screen_stack = old_current_screen_stack
        renpy.display.screen._current_screen = old_current_screen
        renpy.ui.screen = old_ui_screen
        predicting = old_predicting


def prediction_task(root_widget: renpy.display.displayable.Displayable):
    """
    The image prediction task. This predicts the images that can
    be loaded in the near future, and passes them to the image cache's
    preload_image method to be queued up for loading.
    """

    global predicting

    # Start the prediction thread (to clean out the cache).
    renpy.display.im.cache.start_prediction()

    # Wait to be told to start.
    yield from predict_sleep()

    # Set up the image prediction method.
    global image
    image = renpy.display.im.cache.preload_image

    predicting = True

    try:
        if root_widget is not None:
            try:
                displayable(root_widget)
            except Exception:
                if renpy.config.debug_prediction:
                    raise

        # Predict displayables given to renpy.start_predict.
        for d in renpy.store._predict_set:
            try:
                displayable(d)
            except Exception:
                if renpy.config.debug_prediction:
                    raise

            yield from predict_sleep()

        # Predict images that are going to be reached in the next few
        # clicks.

        for _i in renpy.game.context().predict():
            yield from predict_sleep()

        yield from predict_pending()

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

                    yield from predict_sleep()

                    yield from predict_pending()
        else:
            for i in renpy.config.predict_callbacks:
                try:
                    i()
                except Exception:
                    if renpy.config.debug_prediction:
                        raise

                yield from predict_sleep()

            # Predict the game menu screen.

            s = getattr(renpy.store, "_game_menu_screen", None)

            if s is not None:

                if renpy.display.screen.has_screen(s):
                    yield from renpy.display.screen.predict_screen_task(s)
                    predicted_screens.append((s, (), {}))


                elif s.endswith("_screen"):
                    s = s[:-7]
                    if renpy.display.screen.has_screen(s):
                        yield from renpy.display.screen.predict_screen_task(s)
                        predicted_screens.append((s, (), {}))

                yield from predict_sleep()
                yield from predict_pending()

        # Predict that overlay screens will be shown.
        for i in renpy.config.overlay_screens:
            yield from renpy.display.screen.predict_screen_task(i)
            predicted_screens.append((i, (), {}))
            yield from predict_sleep()
            yield from predict_pending()

        # Predict screens given with renpy.start_predict_screen.
        for name, value in list(renpy.store._predict_screen.items()):
            args, kwargs = value

            predicted_screens.append((name, args, kwargs))

            yield from renpy.display.screen.predict_screen_task(name, *args, **kwargs)
            yield from predict_pending()

        # Predict screens reachable through actions
        for t in screens:
            if t in predicted_screens:
                continue

            predicted_screens.append(t)

            name, args, kwargs = t

            if name.startswith("_"):
                continue

            yield from predict_sleep()

            yield from renpy.display.screen.predict_screen_task(name, *args, **kwargs)
            yield from predict_pending(limited=True)

        yield from predict_registered_shaders()

        # Pre-build shader combinations exposed by prediction.
        while renpy.gl2.gl2shadercache.has_predicted_shaders():
            renpy.gl2.gl2shadercache.preload_predicted_shader()
            yield from predict_sleep()

        renpy.gl2.assimp.finish_predict()

    finally:
        predicting = False
