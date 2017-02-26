.. _drag-and-drop:

Drag and Drop
=============

Ren'Py includes drag and drop displayables that allow things to be
moved around the screen with the mouse. Some of the uses of dragging
are:

* Allowing windows to be repositioned by the user, storing the window
  positions.
* Card games that require cards to be dragged around the screen. (For
  example, solitaire.)
* Inventory systems.
* Drag-to-reorder systems.

The drag and drop displayables make it possible to implement these and
other uses of drag and drop. There are two classes involved here. The
Drag class represents either something that can be dragged around the
screen, something that can have a draggable dropped onto it, or
something that can do both. The DragGroup class represents a group of
Drags - for a drag and drop to occur, both Drags must be part of the
same drag group.

The drag and drop system can be used either through the :ref:`Screen
Language <screens>` or directly as displayables. It makes sense to use
the screen language when you don't need to refer to the Drags that you
create after they've been created. This might be the case if the
draggable represents a window that the user places on the screen. If
you need to refer to the drags after they've been created, then it's
often better to create Drags directly, and add them to a DragGroup.

Displayables
------------

.. include:: inc/drag_drop

Examples
--------

An example of a say screen that allows the user to choose the location
of the window by dragging it around the screen.::

    screen say:

        drag:
            drag_name "say"
            yalign 1.0
            drag_handle (0, 0, 1.0, 30)

            xalign 0.5

            window id "window":
                # Ensure that the window is smaller than the screen.
                xmaximum 600

                has vbox

                if who:
                    text who id "who"

                text what id "what"

Here's a more complicated example, one that shows how dragging can be
used to influence gameplay. It shows how dragging can be used to
send a character to a location::

    init python:

        def detective_dragged(drags, drop):

            if not drop:
                return

            store.detective = drags[0].drag_name
            store.city = drop.drag_name

            return True

    screen send_detective_screen:

        # A map as background.
        add "europe.jpg"

        # A drag group ensures that the detectives and the cities can be
        # dragged to each other.
        draggroup:

            # Our detectives.
            drag:
                drag_name "Ivy"
                child "ivy.png"
                droppable False
                dragged detective_dragged
                xpos 100 ypos 100
            drag:
                drag_name "Zack"
                child "zack.png"
                droppable False
                dragged detective_dragged
                xpos 150 ypos 100

            # The cities they can go to.
            drag:
                drag_name "London"
                child "london.png"
                draggable False
                xpos 450 ypos 140
            drag:
                drag_name "Paris"
                draggable False
                child "paris.png"
                xpos 500 ypos 280

    label send_detective:
        "We need to investigate! Who should we send, and where should they go?"

        call screen send_detective_screen

        "Okay, we'll send [detective] to [city]."

More complicated systems take significant programming skill to get
right. The `Ren'Py cardgame framework <http://www.renpy.org/wiki/renpy/Frameworks#Cardgame>`_
is both an example of how to use drag and drop in a complex
system, and useful for making card games in its own right.
