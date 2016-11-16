Gestures
========

Ren'Py includes a gesture recognizer that is enabled when a touchscreen
is used. This makes it possible for gestures to functions that would
otherwise require a keyboard and mouse.

The gesture recognizer first classifies swipes into 8 compass directions,
"n", "ne", "e", "se", "s", "sw", "w", "nw". North is considered to be
towards the top of the screen. It then concatenates the swipes into a string
using the "_" as a delimiter. For example, if the player swipes down and
to the right, the string "s_e" will be produced.

Assuming :var:`config.dispatch_gesture` is None, what happens next is that
gesture is mapped to an event using :var:`config.gestures`. If it is found,
it is queued using :func:`renpy.queue_event`. Otherwise, the gesture is
ignored.

Gesture recognition is only enabled when "touch" is present in
:var:`config.variants`, which should be the case when running on
a touchscreen device.

.. var:: config.gestures = { "n_s_w_e_w_e" : "progress_screen" }

    A map from gesture to the event activated by the gesture.

.. var:: config.dispatch_gesture = None

    The function that is used to dispatch gestures. This function is
    passed the raw gesture string. If it returns non-None, the
    interaction ends. If this variable is None, a default dispatch
    function is used.

.. include:: inc/gesture
