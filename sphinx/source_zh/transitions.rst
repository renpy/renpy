.. _transitions:

===========
Transitions
===========

Transitions can be used as part of the :ref:`with statement
<with-statement>`, as well as in other parts of Ren'Py, to apply
effects to changes in the scene. Ren'Py comes with a small number of
pre-defined transitions, which can be given directly to the with
statement. It also includes transition classes, which can be used to
create new transitions.

Pre-Defined Transitions
=======================

Pre-defined transitions can be given directly to the with
statement. For example::

    show bg washington
    with dissolve

.. var:: fade

    Takes 0.5 seconds to fade to black, and then 0.5 seconds to
    fade to the new screen. An instance of the :func:`Fade` transition
    class.

.. var:: dissolve

    Takes 0.5 seconds to dissolve from the old to the new screen. An
    instance of the :func:`Dissolve` transition class.

.. var:: pixellate

    Pixellates the old scene for .5 seconds, and the new scene for
    another .5 seconds. An instance of the :func:`Pixellate`
    transition class.

.. var:: move

    Takes 0.5 seconds to the move images that have changed location to
    their new locations. An instance of the :func:`MoveTransition`
    transition class.

.. var:: moveinright

    Also: **moveinleft, moveintop, moveinbottom**

    These move entering images onto the screen from the appropriate
    side, taking 0.5 seconds to do so.

.. var:: moveoutright

    Also: **moveoutleft, moveouttop, moveoutbottom**

    These move leaving images off the screen via the appropriate side,
    taking 0.5 seconds to do so.

.. var:: ease

    Also: **easeinright, easeinleft, easeintop, easeinbottom, easeoutright, easeoutleft, easeouttop, easeoutbottom**

    These are similar to the move- family of transitions, except that
    they use a cosine-based curve to slow down the start and end of
    the transition.

.. var:: zoomin

    This zooms in entering images, taking 0.5 seconds to do so.

.. var:: zoomout

    This zooms out leaving images, taking 0.5 seconds to do so.

.. var:: zoominout

    This zooms in entering images and zooms out leaving images, taking 0.5 seconds to do so.

.. var:: vpunch

    When invoked, this transition shakes the screen vertically for a
    quarter second.

.. var:: hpunch

    When invoked, this transition shakes the screen horizontally for a
    quarter second.

.. var:: blinds

    Transitions the screen in a vertical blinds effect lasting 1
    second. An instance of the :func:`ImageDissolve` transition class.

.. var:: squares

    Transitions the screen in a squares effect lasting 1 second.

.. var:: wipeleft

    Also: **wiperight, wipeup, wipedown**

    Wipes the scene in the given direction. Instances of the
    :func:`CropMove` transition class.

.. var:: slideleft

    Also: **slideright, slideup, slidedown**

    Slides the new scene in the given direction. Instances of the
    :func:`CropMove` transition class.

.. var:: slideawayleft

    Also: **slideawayright, slideawayup, slideawaydown**

    Slides the old scene in the given direction. Instances of the
    :func:`CropMove` transition class.

.. var:: pushright

    Also: **pushleft, pushtop, pushbottom**

    These use the new scene to slide the old scene out the named
    side. Instances of the :func:`PushMove` transition class.

.. var:: irisin

    Also: **irisout**

    Use a rectangular iris to display the new screen, or hide the old
    screen. Instances of the :func:`CropMove` transition class.

Transition Classes
==================

Transition classes are functions that can be called to create new
transitions. These functions are parameterized, allowing entire
families of transitions to be created.

Calling transition classes can be done as part of the with
statement. For example::

    # A very long dissolve.
    with Dissolve(10.0)

If we find ourselves calling the same transition class repeatedly, we
can use the :ref:`define statement <define-statement>` to assign the
transition to a variable::

    define annoytheuser = Dissolve(1.0)

    label start:
         show bg washington
         with annoytheuser


.. include:: inc/transition

Transition Families
===================

Transition families are functions that define a large family of
related transitions.

.. include:: inc/transition_family
