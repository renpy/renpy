.. _transforms:

==========
Transforms
==========

A transform can be applied to a displayable to yield another
displayable. The built-in transforms are used to control where an
object is placed on the screen, while user-defined transforms
can cause more complex effects, like motion, zoom, and rotation.

Transforms can be applied by giving the at clause to the scene and
show statements. The following code applies the "right" transform to
the eileen happy displayable.::

    show eileen happy at right

Multiple transforms can be applied by separating them with commas. These
transforms are applied from left-to-right, with the rightmost
transform taking precedence in the case of conflicts. ::

    show eileen happy at halfsize, right

A displayable always has a transform associated with it. If no
transform is given, the prior transform is used. When the transform is
changed, undefined values are taken from the prior transform, or from
``default`` if there is no prior transform.

Default Transforms
==================

Ren'Py ships with a number of transforms defined by default. These
transforms position things on the screen. Here's a depiction of where
each default transform will position an image. ::

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
   |left                   center, default                right|
   +-----------------------------------------------------------+

The offscreenleft and offscreenright transforms position images off the
screen. These transforms can be used to move things off the screen
(remember to hide them afterwards, to ensure that they do not consume
resources).

The transforms are:

.. var:: center

    Centers horizontally, and aligns to the bottom of the screen.

.. var:: default

    Centers horizontally, and aligns to the bottom of the screen. This
    can be redefined to change the default placement of images shown
    with the show or scene statements.

.. var:: left

    Aligns to the bottom-left corner of the screen.

.. var:: offscreenleft

    Places the displayable off the left side of the screen,
    aligned to the bottom of the screen.

.. var:: offscreenright

    Places the displayable off the left side of the screen,
    aligned to the bottom of the screen.

.. var:: reset

    Resets the transform. Places the displayable in the top-left
    corner of the screen, and also eliminates any zoom, rotation, or
    other effects.

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

Creator-Defined Transforms
==========================

A creator can define a transform using the
:ref:`animation and transformation language <atl>`, or the
:class:`Transform` function.
