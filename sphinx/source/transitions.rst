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


.. _dict-transitions:

Dict Transitions
================

In many places where Ren'Py takes a transition, it's possible to instead
specify a dictionary that maps layer names to this transition. When this
is the case, Ren'Py applies each transition to the appropriate layer.

When a dict is used, the pause that usually occurs when a transition takes
place does not occur. Instead, the statement taking the dictionary returns
immediately, and the transitions are scheduled to occur at the start of the
next interaction.

This can be used with the master layer to cause transitions to occur while
dialogue is being shown on the screen. For example, if we wrote::

    define dis = { "master" : Dissolve(1.0) }

and::

    show eileen happy
    with dis

    e "Hello, world."

The dissolve will take place while the text is displayed on the screen.

Dict layer transitions can't be used every place a transition can be used,
only places where applying transitions to a layer is possible. It can be
used with the ``with`` statement and ``with`` cause of the scene, show, and
hide statements. It can also be used with :func:`renpy.with_statement` and
:func:`renpy.transition`, the :func:`Show` and :func:`Hide` actions, and
various config variables that take transitions. Dict layer transitions *will not*
work inside things that don't work with layers, such as ATL, :func:`ComposeTransition`
and :func:`MultipleTransition`.

This can interact poorly with statements that cause a transition to occur
themselves, like the transitions caused by ``window auto``. That can often be
solved with a second dict transition that applies to a different layer.
For example, if you are seeing weird blinking when the dialogue window shows
and hides, consider changing options.rpy to have::

    define config.window_show_transition = { "screens" : Dissolve(.25) }
    define config.window_hide_transition = { "screens" : Dissolve(.25) }

This works because the dialogue window exists entirely on the screens layer.

