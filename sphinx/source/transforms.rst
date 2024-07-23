.. _transforms:

==========
Transforms
==========

Transforms are used in order to turn a :doc:`displayable <displayables>` into
another displayable. There are several kinds of transforms, and various ways to
create them. The built-in transforms are used to control where an image is
placed on the screen, while user-defined transforms can cause more complex
effects, like motion, zoom, rotation, up to complex color effects.

Transforms can be applied to images by passing them to the ``at`` clause of the
:ref:`show <show-statement>` or scene statements. The following applies the
``right`` transform to the ``eileen happy`` image::

    show eileen happy at right

Multiple transforms can be applied by separating them with commas. These
transforms are applied from left-to-right. ::

    show eileen happy at halfsize, right


Applying transforms to displayables in Python
=============================================

There are several ways to apply transform ``t`` to displayable ``d`` in Python:

#. The most universal and most recommended way is ``At(d, t)``. It works with
   all transforms. See :func:`At`.

#. ``d(child=t)`` works with all :ref:`ATL transforms <atl>`.

#. ``t(d)`` works with all :ref:`Python transforms <transforms-python>`, as well
   as with ATL transforms that don't have any positional parameters.


Built-in Transforms
===================

Ren'Py ships with a number of transforms defined by default. These transforms
position things on the screen. Here's a depiction of where each built-in
transform will position an image.

.. code-block:: none

                 +-----------------------------------------------------------+
                 |topleft, reset               top                   topright|
                 |                                                           |
                 |                                                           |
                 |                                                           |
                 |                                                           |
                 |                          truecenter                       |
                 |                                                           |
                 |                                                           |
                 |                                                           |
                 |                                                           |
    offscreenleft|left                   center, default                right|offscreenright
                 +-----------------------------------------------------------+

The :var:`offscreenleft` and :var:`offscreenright` transforms position images
off the edges of the screen. These transforms can be used to move things off
the screen (remember to hide them afterwards, to ensure that they do not consume
resources).

The transforms are:

.. var:: center

    Centers horizontally, and aligns to the bottom of the screen.

.. var:: default

    Centers horizontally, and aligns to the bottom of the screen. This can be
    redefined via :var:`config.default_transform` to change the default
    placement of images shown with the show or scene statements.

.. var:: left

    Aligns to the bottom-left corner of the screen.

.. var:: offscreenleft

    Places the displayable off the left side of the screen, aligned to the
    bottom of the screen.

.. var:: offscreenright

    Places the displayable off the left side of the screen, aligned to the
    bottom of the screen.

.. var:: reset

    Resets the transform. Places the displayable in the top-left corner of the
    screen, and also eliminates any zoom, rotation, or other effects.

.. var:: right

    Aligns to the bottom-right corner of the screen.

.. var:: top

    Centers horizontally, and aligns to the top of the screen.

.. var:: topleft

    Aligns to the top-left corner of the screen.

.. var:: topright

    Aligns to the top-right corner of the screen.

.. var:: truecenter

    Centers both horizontally and vertically.


.. _atl:

ATL - Animation and Transformation Language
===========================================

The Animation and Transformation Language (ATL) is a high-level language which
can create animations, move displayables across the screen, set their position,
apply transformations, and more. These can be changed over time, and in response
to events.

ATL transform objects, which are created using the :ref:`transform-statement`
down below, are displayables and can be used as such (even though they will be
transparent when their child displayable is not set) : they can be passed to a
screen's :ref:`sl-add` element, or to a :ref:`show-expression-statement`
statement, or to the :func:`renpy.show` function.

Ren'Py script statements
------------------------

There are three Ren'Py script statements which can include ATL code.

.. _transform-statement:

Transform Statement
~~~~~~~~~~~~~~~~~~~

The ``transform`` statement creates a new transform. The syntax is:

.. productionlist:: script
    atl_transform : "transform" `qualname` ( "(" `parameters` ")" )? ":"
                  :    `atl_block`

The transform statement is run at :ref:`init time <init-phase>`. The transform
may take a list of parameters, which works much the same way as a Python
function definition, except that several kinds of parameters are currently
forbidden, though they may be allowed in the future:

#. Positional-only parameters
#. Keyword-only parameters without a default value
#. Variadic positional parameters (``*args``)
#. Variadic keyword parameters (``**kwargs``)

`qualname`, the name of the transform, must be a set of dot-separated Python
identifiers. The transform created by the ATL block will be bound to that name,
within the provided :ref:`store <named-stores>` if one was provided. ::

    transform left_to_right:
        xalign 0.
        linear 2 xalign 1.
        repeat

    transform ariana.left:
        xalign .3

    transform animated_ariana_disp:
        "ariana"
        pause 1.
        "ariana_reverse"
        pause 1.
        repeat

The created object is both a transform and a displayable, but as opposed to the
``image`` statement, it is created as a variable (or a constant), rather than in
the namespace of :ref:`images <defining-images>`.

.. _atl-image-statement:

Image Statement with ATL Block
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second way to include ATL code in a script is as part of an :ref:` image
statement <image-statement>`. As its inline counterpart, it binds an image name
(which may contain spaces) to the given transform. As there is no way to supply
with parameters, it's only useful if the transform defines an animation. The
syntax is:

.. productionlist:: script
    atl_image : "image" `image_name` ":"
              :    `atl_block`

::

    image animated_ariana_img:
        "ariana"
        pause 1.
        "ariana_reverse"
        pause 1.
        repeat

Scene and Show Statements with ATL Block
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final way to use ATL is as part of a :ref:`show <show-statement>` or scene
statement. This wraps the image that's being shown inside an ATL transformation
which is created on the fly and applied to the image. The syntax is:

.. productionlist:: script
    atl_show  : `stmt_show` ":"
              :    `atl_block`
    atl_scene : `stmt_scene` ":"
              :    `atl_block`

::

    show eileen happy:
        xalign 1.

    scene bg washington:
        zoom 2.

..
    include here, after #4405, how to change the child then get back to it

ATL Syntax and Statements
-------------------------

ATL statements may be inline, or make up a block within the ATL block in which
it is written. With some exceptions described in the relevant statements, the
statements in an ATL block are executed in order, from top to bottom.

If an ATL statement requires an expression to be evaluated, such evaluation
occurs when the transform is first executed (that is when using a ``show``
statement, or displaying the transform as part of a screen), and not when the
particular ATL statement is executed.

The following are the ATL staatements.


TODO: include ATL statements here


TODO: link to transform properties ?


External events
---------------

The following events are triggered automatically within an ATL transform:

``start``
    A pseudo-event, triggered on entering an ``on`` statement, if no event of
    higher priority has happened.

``show``
    Triggered when the transform is shown using the show or scene statement, and
    no image with the given tag exists.

``replace``
    Triggered when transform is shown using the ``show`` statement, replacing an
    image with the given tag.

``hide``
    Triggered when the transform is hidden using the ``hide`` statement or its
    Python equivalent.

    Note that this isn't triggered when the transform is eliminated via the
    :ref:`scene-statement` or exiting the :ref:`context` it exists in, such as
    when exiting the game menu.

``replaced``
    Triggered when the transform is replaced by another. The image will not
    actually hide until the ATL block finishes.

``update``
    Triggered when a screen is updated without being shown or replacing another
    screen. This happens in rare but possible cases, such as when the game is
    loaded and when styles or translations change.

``hover``, ``idle``, ``selected_hover``, ``selected_idle``, ``insensitive``, ``selected_insensitive``
    Triggered when a button containing this transform, or a button contained by
    this transform, enters the named state.


TODO: special ATL kw param (child)



.. _replacing-transforms:

Replacing Transforms
====================

When an ATL transform, a built-in transform or a transform defined using the
:class:`Transform` class is replaced by another transform of these categories,
the properties of the outgoing transform are inherited by the incoming
transform. That inheritance doesn't apply for other kinds of transforms.

When the :ref:`show <show-statement>` statement has multiple transforms in the
``at`` list, the transforms are matched from last to first, until one list runs
out. For example::

    show eileen happy at a, b, c
    "Dialogue !"
    show eileen happy at d, e

The ``c`` transform will be replaced by ``e``, the ``b`` transform will be
replaced by ``d``, and nothing replaces the ``a`` transform.

At the moment of replacement, if both transforms are of suitable kinds, the
values of the properties of the old transform are copied to the new transform.
If the old transform was animated, the current intermediate value is inherited.
For example::

    transform bounce:
        linear 3.0 xalign 1.0
        linear 3.0 xalign 0.0
        repeat

    transform headright:
        linear 15 xalign 1.0

    label example:
        show eileen happy at bounce
        pause
        show eileen happy at headright
        pause

In this example, the image will bounce from left to right and back until the
player clicks. When that happens, the ``xalign`` property of the ``bounce``
transform will be used to initialize the ``xaalign`` property of the
``headright`` transform, and so the image will move from where it was when the
player first clicked.

The position properties (:tpref:`xpos`, :tpref:`ypos`, :tpref:`xanchor`,
:tpref:`yanchor`, and properties setting them such as :tpref:`xalign` or
:tpref:`radius`\ / :tpref:`angle`) have a special rule for inheritance : a value
set in the child will override a value set in the parent. That is because a
displayable may have only one position, and a position that is actively set
takes precedence.

Finally, when a ``show`` statement does not include an ``at`` clause, the same
transforms are used, so no inheritance is necessary. To prevent inheritance,
hide and then show the displayable again.


The Transform Class
===================

One equivalent to to the simplest ATL transforms is the Transform class.

.. class:: Transform(child=None, function=None, **properties)

    Creates a transform which applies operations such as cropping, rotation,
    scaling or alpha-blending to its child. A transform object has fields
    corresponding to the :ref:`transform properties <transform-properties>`,
    which it applies to its child.

    `child`
        The child the transform applies to.

    .. function:: function(trans: Transform, st: float, at: float, /) -> int|None

        If not None, this function will be called when the transform is
        rendered, with three positional arguments:

        * The transform object.
        * The shown timebase, in seconds.
        * The animation timebase, in seconds.

        The function should return a delay, in seconds, after which it will be
        called again, or None to be called again at the start of the next
        interaction.

        This function should not have side effects other than changing the
        Transform object in the first argument, and may be called at any time
        with any value as a part of prediction.

    Additional keyword arguments are values that transform properties are set
    to. These particular transform properties will be set each time the
    transform is drawn, and so may not be changed after the Transform object is
    created. Fields corresponding to other transform properties, however, can be
    set and changed afterwards, either within the function passed as the
    `function` parameter, or immediately before calling the :meth:`update`
    method.

    .. attribute:: hide_request

        This attribute is set to true when the function is called, to indicate
        that the transform is being hidden.

    .. attribute:: hide_response

        If ``hide_request`` is true, this can be set to false to prevent the
        transform from being hidden.

    .. method:: set_child(child)

        Call this method with a new `child` to change the child of this
        transform.

    .. method:: update()

        This should be called when a transform property field is updated outside
        of the function passed as the `function` argument, to ensure that the
        change takes effect.

.. _transforms-python:

Callables as transforms
=======================

Finally, simple Python callables can be used as transforms. These callables
should take a single Displayable as an argument, and return a new Displayable.
For example::

    init python:

        # this transform uses the right and left transforms
        def right_or_left(d):
            if switch:
                return At(d, right)
            else:
                return At(d, left)

That means that certain builtins such as :func:`Flatten` are also transforms and
can be used as such.
