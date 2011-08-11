====================================
Transforms and Transitions in Python
====================================

Python can be used to create new transforms and transitions for use by
Ren'Py scripts.

Transforms
----------

A transform is a python callable that, when called with a displayable,
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

Transitions
-----------

A transition is a python callable that, when called with two keyword
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

            
       
