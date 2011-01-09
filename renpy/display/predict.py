# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

import renpy

# Called to indicate an image should be loaded or preloaded. This is
# a function that takes an image manipulator, set by reset and predict,
# and winds up bound to either im.cache.get or im.cache.preload_image
image = None

# The set of displayables we've predicted
predicted = set()

def displayable(d):
    if d is None:
        return

    if d not in predicted:
        predicted.add(d)
        d.visit_all(lambda i : i.predict_one())


def reset():
    global image
    image = renpy.display.im.cache.get
    predicted.clear()
    
def prediction_coroutine(root_widget):
    """
    The image prediction co-routine. This predicts the images that can
    be loaded in the near future, and passes them to the image cache's
    preload_image method to be queued up for loading.
    """

    global image
    image = renpy.display.im.cache.preload_image

    renpy.game.context().predict()

    yield False
