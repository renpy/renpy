.. _transitions:

===========
Transitions
===========

Transitions can be used as part of the :ref:`with statement <with-statement>`,
as well as in other parts of Ren'Py, to apply effects to changes in the scene
(or sometimes to turn a displayable into another). Ren'Py comes with a small
number of pre-defined transitions, which can be given directly to the with
statement. For example::

    show bg washington
    with dissolve

Pre-Defined Transitions
=======================

.. var:: dissolve

    Takes 0.5 seconds to dissolve from the old to the new screen. An instance of
    the :func:`Dissolve` transition class.

.. var:: fade

    Takes 0.5 seconds to fade to black, and then 0.5 seconds to fade to the new
    screen. An instance of the :func:`Fade` transition class.

.. var:: pixellate

    Pixellates the old scene for .5 seconds, and the new scene for another .5
    seconds. An instance of the :func:`Pixellate` transition class.

.. var:: move

    Takes 0.5 seconds to the move images that have changed location to their new
    locations. An instance of the :func:`MoveTransition` transition class.

    Move transitions, and similar transitions like ease, can only be applied to
    a single layer or all layers at once, using the
    :ref:`with statement <with-statement>`. It will not work in other contexts
    such as :ref:`ATL <displayable-atl-statement>`, :func:`ComposeTransition`,
    or other ways of applying transitions.

.. var:: moveinright

    Also: **moveinleft, moveintop, moveinbottom**

    These move entering images onto the screen from the appropriate side, taking
    0.5 seconds to do so.

.. var:: moveoutright

    Also: **moveoutleft, moveouttop, moveoutbottom**

    These move leaving images off the screen via the appropriate side, taking
    0.5 seconds to do so.

.. var:: ease

    Also: **easeinright, easeinleft, easeintop, easeinbottom, easeoutright, easeoutleft, easeouttop, easeoutbottom**

    These are similar to the move- family of transitions, except that they use a
    cosine-based curve to slow down the start and end of the transition.

.. var:: zoomin

    This zooms in entering images, taking 0.5 seconds to do so.

.. var:: zoomout

    This zooms out leaving images, taking 0.5 seconds to do so.

.. var:: zoominout

    This zooms in entering images and zooms out leaving images, taking 0.5
    seconds to do so.

.. var:: vpunch

    When invoked, this transition shakes the screen vertically for a quarter
    second. Imitating and customizing this transition and :var:`hpunch` is best
    done using :ref:`atl-transitions`.

.. var:: hpunch

    When invoked, this transition shakes the screen horizontally for a quarter
    second.

.. var:: blinds

    Transitions the screen in a vertical blinds effect lasting 1 second. An
    instance of the :func:`ImageDissolve` transition class.

.. var:: squares

    Transitions the screen in a squares effect lasting 1 second.

.. var:: wipeleft

    Also: **wiperight, wipeup, wipedown**

    Wipes the scene in the given direction. Instances of the :func:`CropMove`
    transition class.

.. var:: slideleft

    Also: **slideright, slideup, slidedown**

    Slides the new scene in the given direction. Instances of the
    :func:`CropMove` transition class.

.. var:: slideawayleft

    Also: **slideawayright, slideawayup, slideawaydown**

    Slides the old scene in the given direction. Instances of the
    :func:`CropMove` transition class.

.. var:: pushright

    Also: **pushleft, pushup, pushdown**

    These use the new scene to slide the old scene out the named side. Instances
    of the :func:`PushMove` transition class.

.. var:: irisin

    Also: **irisout**

    Use a rectangular iris to display the new screen, or hide the old screen.
    Instances of the :func:`CropMove` transition class.


Transition Classes
==================

Transition classes are functions that can be called to create new transitions.
These functions are parameterized, allowing entire families of transitions to be
created. Unlike what the term may imply, they are usually not classes in the
Python sense and should not be treated as such.

Calling transition classes can be done as part of the with statement. For
example::

    # A very long dissolve.
    with Dissolve(10.0)

If the same transition class is used repeatedly, the :ref:`define statement
<define-statement>` can be used to assign the transition to a variable::

    define dissolve1 = Dissolve(1.0)

    label start:
        show bg washington
        with dissolve1

The `time_warp` argument taken by many transition classes can be given built-in
warpers found in the ``_warper`` module, see :ref:`warpers <warpers>`.

.. include:: inc/transition


Transition Families
===================

Transition families are functions that define a large family of related
transitions.

.. include:: inc/transition_family


.. _dict-transitions:

Dict Transitions
================

In many places where Ren'Py takes a transition, it's possible to instead specify
a dictionary that maps layer names to this transition. When this is the case,
Ren'Py applies each transition to the appropriate layer.

When a dict is used, the pause that usually occurs when a transition takes place
does not occur. Instead, the statement taking the dictionary returns
immediately, and the transitions are scheduled to occur at the start of the next
interaction.

This can be used with the master layer to cause transitions to occur while
dialogue is being shown on the screen. For example::

    define dis = { "master" : Dissolve(1.0) }

    label start:
        show eileen happy
        with dis

        e "Hello, world."

The dissolve will take place while the text is displayed on the screen.

Dict layer transitions can't be used every place a transition can be used, only
in places where applying transitions to a layer is possible. It can be used with
the :ref:`with-statement` and ``with`` cause of the
:ref:`scene <scene-statement>`, :ref:`show <show-statement>`, and
:ref:`hide <hide-statement>` statements. It can also be used with
:func:`renpy.with_statement` and :func:`renpy.transition`, the :func:`Show` and
:func:`Hide` actions, and various config variables that take transitions. Dict
layer transitions *will not* work inside things that don't work with layers,
such as :ref:`atl`, :func:`ComposeTransition` and :func:`MultipleTransition`.

This can interact poorly with statements that cause a transition to occur
themselves, like the transitions caused by ``window auto``. That can often be
solved with a second dict transition that applies to a different layer.
For example, if you are seeing weird blinking when the dialogue window shows
and hides, consider changing :file:`options.rpy` to have::

    define config.window_show_transition = { "screens" : Dissolve(.25) }
    define config.window_hide_transition = { "screens" : Dissolve(.25) }

This works because the dialogue window exists entirely on the screens layer.


.. _atl-transitions:

ATL Transitions
===============

*See also:* :ref:`atl`

It's possible to use an ATL transform to define a transition. These transitions
need to accept the `old_widget` and `new_widget` arguments, which will receive
displayables representing the screens that are transitioned from and to,
respectively.

An ATL transition must set itself the :tpref:`delay` property to the number of
seconds the transition lasts for. It may use the :tpref:`events` property to
prevent the old displayable from receiving events. ::

    transform spin(duration=1.0, *, new_widget=None, old_widget=None):

        # Set how long this transform will take to complete.
        delay duration

        # Center it.
        xcenter .5
        ycenter .5

        # Spin the old displayable.
        old_widget
        events False
        rotate 0.
        easeout (duration / 2) rotate 360.0

        # Spin the new displayable.
        new_widget
        events True
        easein (duration / 2) rotate 720.0


.. _transitions-python:

Python Transitions
==================

A Python callable may be used as a transition. For that, it must take two
keyword arguments described below, and return a displayable that performs the
transition effect - usually by delegating that to another transition. The two
keyword arguments are `old_widget`, which represents the old screen, and
`new_widget`, which represents the new screen.

The displayable returned by the callable should have a ``delay`` attribute,
set to the number of seconds that the transition should run for.

For example::

    init python:
        def dissolve_or_pixellate(old_widget=None, new_widget=None):
            if persistent.want_pixellate:
                return pixellate(old_widget=old_widget, new_widget=new_widget)
            else:
                return dissolve(old_widget=old_widget, new_widget=new_widget)

Accordingly, all kinds of transitions can be called and passed these two keyword
arguments, resulting in a displayable animating the transition between the two
passed displayables.


.. _scene-show-hide-transition:

Automatic Transitions after Scene, Show, and Hide
=================================================

Ren'Py can automatically show a transition after a series of scene, show, and
hide statements. This transition can be enabled by setting the
:var:`_scene_show_hide_transition` variable to the transition to be used.

The transition will occur after one or more :ref:`scene <scene-statement>`,
:ref:`show <show-statement>`, and :ref:`hide <hide-statement>` statements,
provided the statement are not followed by a :ref:`with <with-statement>`
statement, or a transition caused by :ref:`dialogue-window-management`, like the
various ``window`` statements. It's also disabled when in a menu context.

For example::

    define _scene_show_hide_transition = Dissolve(0.25)

    label start:
        scene bg washington
        show eileen happy

        "The transition won't show here, because the dialogue window transitioned in."

        show lucy mad at right

        "The transition will happen here."

        hide lucy mad
        show eileen vhappy

        "And it will happen here, as well."
