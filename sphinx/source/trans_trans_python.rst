====================================
Transforms and Transitions in Python
====================================

Python can be used to create new transforms and transitions for use by
Ren'Py scripts.

Transforms
----------

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

    `function`
        If not none, this is a function that is called when the transform
        is rendered. The function is called with three arguments:

        * The transform object.
        * The shown timebase, in seconds.
        * The animation timebase, in seconds.

        The function should return a delay, in seconds, after which it will
        be called again, or None to be called again at the start of the next
        interaction.

    Additional arguments are taken as values to set transform properties to.

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

        This should be called when a transform property field is
        updated outside of the callback method, to ensure that the
        change takes effect.



Transitions
-----------

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
