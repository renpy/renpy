# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display

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

def screen(_screen_name, **kwargs):
    """
    Called to predict that the named screen is about to be shown
    with the given arguments.
    """

    screens.append((_screen_name, kwargs))

    
def reset():
    global image
    image = renpy.display.im.cache.get
    predicted.clear()
    del screens[:]

    
def prediction_coroutine(root_widget):
    """
    The image prediction co-routine. This predicts the images that can
    be loaded in the near future, and passes them to the image cache's
    preload_image method to be queued up for loading.
    """

    global predicting
    
    # Set up the image prediction method.
    global image
    image = renpy.display.im.cache.preload_image

    # Predict images that are going to be reached in the next few
    # clicks.
    predicting = True

    renpy.game.context().predict()

    predicting = False
    yield True

    # If there's a parent context, predict we'll be returning to it
    # shortly. Otherwise, call the functions in
    # config.predict_callbacks.
    predicting = True
    
    if len(renpy.game.contexts) >= 2:
        sls = renpy.game.contexts[-2].scene_lists

        for l in sls.layers.itervalues():
            for sle in l:
                displayable(sle.displayable)

    else:
        for i in renpy.config.predict_callbacks:
            i()
                
    predicting = False
                
    yield True

    # Predict things (especially screens) that are reachable through
    # an action.
    predicting = True

    root_widget.visit_all(lambda i : i.predict_one_action())

    predicting = False

    # Predict the screens themselves.
    for name, kwargs in screens:
        yield True

        predicting = True
        
        try:
            renpy.display.screen.predict_screen(name, **kwargs)
        except:
            if renpy.config.debug_image_cache:
                renpy.display.ic_log.write("While predicting screen %s %r", name, kwargs)
                renpy.display.ic_log.exception()

        predicting = False
            
    yield False
                
