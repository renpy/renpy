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
different properties control the position of the speech bubble tail.

Once you've changed the area or properties for a character (or group of
characters with the same image tags), those properties remain set until
changed again, or until the next scene statement.

When the area or properties are being set on the current line of dialogue,
the corresponding line is brighter. If the values are being inherited from
a prior line of dialogue or the default, the button is dimmed out. Right
clicking on a button will prevent the current line from setting the value.

.. _retained-bubbles:

Retained Bubbles
----------------

Ren'Py supports a mode in which bubbles are retained between lines of
dialogue, so they pop up one by one, until the previous bubbles are
cleared from the screen. To enable this mode, set a bubble character's
`retain` property to True::

    define e = Character(None, image="eileen", kind=bubble, retain=True)

Once that's done, the bubbles will keep popping up. Each bubble will
need to be placed individually, so bubbles don't overlap. In the bubble editor,
pressing the "(clear retained bubbles)" button will remove all of the
retained bubbles from the screen, except for the most recent.

Tips
----

The speech bubbles use the same identifiers used by the translation system,
see the :ref:`Translation Tips <translation-tips>` for more information
about them. These identifiers can change if:

* The text of a line changes.
* Another line with the same text inside the same label is added or removed.
* A label before the line is added or removed (however, adding or removing
  a label with the ``hide`` clause will not change the translation identifier).

If you edit a scene, it's suggested that you replay through it to make sure
the changes did not affect speech bubble placement.

It's possible to apply transforms to the speech bubble by editing the :ref:`bubble-screen`.

.. _bubble-ctc:

If you'd like a CTC indicator to be part of the bubble screen, consider giving the
`ctc_position` argument to Character the value of "screen-variable". You may also need
to add::

    showif ctc:
        add ctc

to the end of the bubble screen, if this is not present. You'd then define the character as:

    define e = Character(
        None,
        image="eileen",
        kind=bubble,
        ctc_position="screen-variable",
        ctc=Transform("ctc_image.png", align=(0.5, 1.0))


Configuration Variables
-----------------------

The speech bubble system is controlled by variables in the ``bubble`` namespace,
and by the ``bubble`` screen and its associated styles.

The ``bubble`` namespace contains the following variables:

.. var:: bubble.db_filename = "bubble.json"

    The database file, stored in the game directory, that contains the
    speech bubble information.

.. var:: bubble.clear_retain_statements = [ "call screen", "menu",  "say", "say-centered", "say-nvl", "scene", ]

    This is a list of statements that will automatically cause retained bubbles to be cleared.

.. var:: bubble.cols = 24

    The granularity of the grid that's used to position and size speech bubbles,
    in the horizontal direction.

.. var:: bubble.default_area = (15, 1, 8, 5)

    This is the default area that speech bubbles are placed in, if no other
    area is specified. This is a tuple of the form (x, y, w, h),
    where each value is a number of grid cells.

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

.. var:: bubble.layer = "screens"

    The layer that non-retained bubbles are placed on.

.. var:: bubble.properties = { ... }

    These are properties, apart from the area, that can be used to customize
    the speech bubble. This is a map from the name of a set of properties
    to a dictionary of properties and values. These properties supersede those
    given to the character, and are then supplied to the ``bubble`` screen.

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

.. var:: bubble.properties_callback = None

    If not None, this should be a function that takes an image tag, and returns
    a list or tuple of property names that should be used for that image tag, in
    the order those names should be cycled through. This takes precedence over
    bubble.properties_order, and can be used to customize the list of bubble
    properties by character.

.. var:: bubble.retain_layer = "screens"

    The layer that retained bubbles are placed on.

.. var:: bubble.rows = 24

    The granularity of the grid that's used to position and size speech bubbles,
    in the vertical direction.


.. _bubble-screen:

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

If you'd like to apply effects to the speech bubble, you can do so by
adding a transform to the bubble screen that accepts the show and hide
transform events, like::

    screen bubble(who, what):
        style_prefix "bubble"

        window:
            id "window"

            at transform:
                on show:
                    alpha 0.0
                    linear .5 alpha 1.0

                on hide:
                    linear .5 alpha 0.0

            if who is not None:

                window:
                    id "namebox"
                    style "bubble_namebox"

                    text who:
                        id "who"

            text what:
                id "what"


Adding Bubble Support to a Game
-------------------------------

Games made before the release of Ren'Py 8.1 won't include the default screens
and settings required for the speech bubble system. There are two things you
need to do to fix this. First, download:

* https://raw.githubusercontent.com/renpy/renpy/master/gui/game/gui/bubble.png
* https://raw.githubusercontent.com/renpy/renpy/master/gui/game/gui/thoughtbubble.png

And place the files in the ``game/gui`` directory of your game. Then, add this to
the end of screens.rpy::

    ## Bubble screen ###############################################################
    ##
    ## The bubble screen is used to display dialogue to the player when using
    ## speech bubbles. The bubble screen takes the same parameters as the say
    ## screen, must create a displayable with the id of "what", and can create
    ## displayables with the "namebox", "who", and "window" ids.
    ##
    ## https://www.renpy.org/doc/html/bubble.html#bubble-screen

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

    style bubble_window is empty
    style bubble_namebox is empty
    style bubble_who is default
    style bubble_what is default

    style bubble_window:
        xpadding 30
        top_padding 5
        bottom_padding 5

    style bubble_namebox:
        xalign 0.5

    style bubble_who:
        xalign 0.5
        textalign 0.5
        color "#000"

    style bubble_what:
        align (0.5, 0.5)
        text_align 0.5
        layout "subtitle"
        color "#000"

    define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
    define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

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

        "thought" : {
            "window_background" : bubble.thoughtframe,
        }
    }

    define bubble.expand_area = {
        "bottom_left" : (0, 0, 0, 22),
        "bottom_right" : (0, 0, 0, 22),
        "top_left" : (0, 22, 0, 0),
        "top_right" : (0, 22, 0, 0),
        "thought" : (0, 0, 0, 0),
    }
