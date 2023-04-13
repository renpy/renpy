Speech Bubbles
==============

Ren'Py supports dialogue that's displayed in speech bubbles, which can be
interactively positioned on the screen. This provides an alternative to
the textboxes used by ADV-style games, and the full screen dialogue used
by NVL-mode.

To use speech bubbles your game, you'll have to define Characters with
an image tag, a kind of ``bubble``. For example, ::

    define e = Character(None, image="eileen", kind=bubble) # Eileen
    define l = Character(None, image="lucy", kind=bubble)   # Lucy

While a name is supported, in general the speaking character will be
implied by the tails of the bubble, so the name can be omitted.

You may then use these characters to write dialogue normally.

To position the balloons, hit shift+B to display the speech bubble editor.
For each character that has a speech balloon, this will have two buttons
in it.

Pressing the area button will launch the speech bubble editor. This editor
lets you drag to select the area where the speech bubble will be placed,
on a grid. When you complete the drag, the speech bubble will will change
locations.

Pressing the properties buttons will select between sets of properties
associated with the speech bubble. For the default speech bubble, the
different properties control the positionm of the speech bubble tail.

Once you've changed the area or properties for a character (or group of
characters with the same image tage), those properties remain set until
changed again, or until the next scene statement.

When the area or properties are being set on the current line of dialogue,
the corresponding line is brighter. If the values are being inherited from
a prior line of dialogue or the default, the button is dimmed out. Right
clicking on a button will prevent the current line from setting the value.

Tips
----

The speech bubbles use the same identifiers used by the translation system.
These identifiers can change if:

* The text of a line changes.
* A second line with the same text inside the same label is added or removed.
* The label before the line is added or removes (however, adding or removing
  a label with the ``hide`` clause will not change the translation identifier).

If you edit a scene, it's suggested that you replay through it to make sure
the changes did not affect speech bubble placement.


Configuration Variables
-----------------------

The speech bubble system is controlled by variables in th ``bubble`` namespace,
and by the ``bubble`` screen and its associated styles.

The ``bubble`` namespace contains the following variables:

.. var:: bubble.db_filename = "bubble.json"

    The database file, stored in the game directory, that contains the
    speech bubble information.


.. var:: bubble.cols = 24

    The granularity of the grid that's used to position and size speech bubbles,
    in the horizontal direction.

.. var:: bubble.rows = 24

    The granularity of the grid that's used to position and size speech bubbles,
    in the vertical direction.

.. var:: bubble.default_area = (15, 1, 8, 5)

    This is the default area that speech bubbles are placed in, if no other
    area is specified. This is a tuple of the form (x, y, w, h),
    where each value is a number of grid cells.


.. var:: bubble.properties = { ... }

    These are properties, apart from the area, that can be used to customize
    the speech bubble. This is a map from the name of a set of proprerties
    to a dictionary of properties and values. These properties supersede the properties given
    the character, and are then supplied to the ``bubble`` screen.

    This uses the same prefixing system as :func:`Character` does. Properties
    beginning with ``window_`` have the prefix removed, and are passed to the
    displayable with id "window" in the bubble screen, which is the bubble
    itself. Properties with ``what_`` have the prefix removed, and are passed
    to the displayable with id "what" in the bubble screen, which is the text
    of the bubble. Properties with ``who_`` are handled similarly, and given
    to the characters name. Properties with ``show_`` are given as arguments
    to the bubble screen itself.

    In a new game, screens.rpy includes::

        define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)

        define bubble.properties = {
            "bottom_left" : {
                "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
                "window_bottom_padding" : 27,
            },

            "bottom_right" : {
                "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
                "window_bottom_padding" : 27,
            },

            "top_left" : {
                "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
                "window_top_padding" : 27,
            },

            "top_right" : {
                "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
                "window_top_padding" : 27,
            },
        }

    The bubble.frame variable is just used to make defining bubble.properties
    easier. Then for each of the four styles of bubble, the bubble is flipped
    so the tail is in the right place, and the padding is adjusted to leave
    room for the tail.

.. var:: bubble.properties_order = [ ]

    This is a list of the names of the sets of properties, in the order they should
    be cycled through in the speech bubble editor. If the names of the sets of properties
    are not given, the properties are cycled through in alphabetical order.

.. var:: bubble.expand_area = { ... }

    This is a map from the name of a set of properties to a (left, top, right, bottom)
    tuple. If found in this set, the area of the speech bubble is expanded by the
    given number of pixels.

    This makes the speech bubble bigger than the area the creator dragged out.
    The intent is that this can be used to drag out the body of the speech
    bubble without concern for the tail, and also for the text itself to stay
    put when the set of properties is changed and the tail moves.

    By default, this is::

        define bubble.expand_area = {
            "bottom_left" : (0, 0, 0, 22),
            "bottom_right" : (0, 0, 0, 22),
            "top_left" : (0, 22, 0, 0),
            "top_right" : (0, 22, 0, 0),
        }

Bubble Screen
-------------

The default ``bubble`` screen can be found in ``screens.rpy``, and is similar
to the default ``say`` screen::

    screen bubble(who, what):
        style_prefix "bubble"

        window:
            id "window"

            if who is not None:

                window:
                    id "namebox"
                    style "bubble_namebox"

                    text who:
                        id "who"

            text what:
                id "what"

It's separate from the say screen as it uses its own set of styles, including
``bubble_window``, ``bubble_what``, ``bubble_namebox``, and ``bubble_who``.
These styles can be customized directly to avoid having to set a property
in all of the sets of properties in :var:`bubble.properties`.
