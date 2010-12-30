Displayables
============
...


Image Manipulators
------------------


ColorMatrix
-----------



Image-Like Displayables
-----------------------

We call these displayables image-like because they take up a
rectangular area of the screen, and do not react to input.  These
differ from normal images by varying their size to fill an area
(Frame, LiveTile, and Sold), or by allowing the user to specify their
size (LiveComposite, LiveCrop, Null). They are not image manipulators.

Image-like displayables take :ref:`position-style-properties`.

.. include:: inc/disp_imagelike


Dynamic Displayables
--------------------

Dynamic displayables display a child displayable based on the state of
the game. They do not take any properties, as layout is controlled
by the properties of the child displayable they return.

.. include:: inc/disp_dynamic


Layout Boxes
------------

Layout boxes are displayables that lay out their children on the
screen. They can lay out the children in a horizontal or vertical
manner, or can lay them out using the standard positioning algorithm.

The box displayables take any number of positional and keyword
arguments. Positional arguments should be displayables that are
added to the box as children. Keyword arguments are style properties
that are applied to the box.

Boxes take :ref:`position-style-properties` and :ref:`box-style-properties`.


.. include:: inc/disp_box

::

   # Display two logos, to the left and right of each other.
   image logo hbox = HBox("logo.png", "logo.png")

   # Display two logos, one on top of the other.
   image logo vbox = VBox("logo.png", "logo.png") 

   # Display two logos. Since both default to the upper-left
   # corner of the screen, we need to use Image to place
   # those logos on the screen.
   image logo fixed = Fixed(
       Image("logo.png", xalign=0.0, yalign=0.0),
       Image("logo.png", xalign=1.0, yalign=1.0))


Effects
-------

These displayables are used to create certain visual effects.

.. include:: inc/disp_effects


