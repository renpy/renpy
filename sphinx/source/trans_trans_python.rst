====================================
Transforms and Transitions in Python
====================================

Python can be used to create new transforms and transitions for use by
Ren'Py scripts.

.. _transforms-python:

Transforms
----------

*Main articles:* :doc:`transforms` *and* :doc:`atl`

A transform is a Python callable that, when called with a displayable,
returns another displayable.

For example::

    init python:

        # This is a transform that uses the right and
        # left transforms.
        def right_or_left(d):
            if switch:
                return right(d)
            else:
                return left(d)

The Python equivalent of an ATL transform is a Transform object.

.. class:: Transform(child=None, function=None, **properties)

    A transform applies operations such as cropping, rotation, scaling, and
    alpha-blending to its child. A transform object has fields corresponding
    to the :ref:`transform properties <transform-properties>`, which it applies
    to its child.

    `child`
        The child the transform applies to.

    .. function:: function(trans, st, at, /) -> int|None

        If not None, this function will be called when the transform
        is rendered, with three positional arguments:

        * The transform object.
        * The shown timebase, in seconds.
        * The animation timebase, in seconds.

        The function should return a delay, in seconds, after which it will
        be called again, or None to be called again at the start of the next
        interaction.

        This function should not have side effects other
        than changing the Transform object in the first argument, and may be
        called at any time with any value to enable prediction.

    Additional keyword arguments are values that transform properties are set
    to. These particular transform properties will be set each time the
    transform is drawn, and so may not be changed after the Transform object
    is created. Fields corresponding to other transform properties, however,
    can be set and changed afterwards, either within the function passed as
    the `function` parameter, or immediately before calling the
    :meth:`update` method.

    .. attribute:: hide_request

        This is set to true when the function is called, to indicate that the
        transform is being hidden.

    .. attribute:: hide_response

        If hide request is true, this can be set to false to prevent the
        transform from being hidden.

    .. method:: set_child(child)

        Call this method with a new `child` to change the child of
        this transform.

    .. method:: update()

        This should be called when a transform property field is updated
        outside of the function passed as the `function` argument, to ensure
        that the change takes effect.

.. _transitions-python:

Transitions
-----------

*Main article:* :doc:`transitions`

*See also:* :ref:`atl-transitions`

A transition is a Python callable that, when called with two keyword
arguments, returns a displayable that performs the transition effect.
The two keyword arguments are:

`old_widget`
    A displayable representing the old screen.

`new_widget`
    A displayable representing the new screen.

The returned displayable should have a ``delay`` field, which gives
the number of seconds the transition should run for.

For example::

    init python:

        def dissolve_or_pixellate(old_widget=None, new_widget=None):
            if persistent.want_pixellate:
                return pixellate(old_widget=old_widget, new_widget=new_widget)
            else:
                return dissolve(old_widget=old_widget, new_widget=new_widget)
