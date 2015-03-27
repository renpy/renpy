.. _displayables:

Displayables
============

A displayable is an object that can be shown to the user. Ren'Py
displayables can be used in many ways.

* Assignment to an image name using the image statement.
* Added to a screen using the screen language add statement.
* Assignment to certain config variables.
* Assignment to certain style properties.

When a Ren'Py function or variable expects a displayable, there are
four things that can be provided:

* An object of type Displayable, created by calling one of the
  functions given below.
* A string with a dot (.) in it. Such a string is interpreted as
  a filename by :func:`Image`.
* A color. A color may either be given as a hexadecimal color string in "#rgb",
  "#rgba", "#rrggbb", or "#rrggbbaa" form, or an (r, g, b, a) tuple,
  where each component is an integer between 0 and 255. Colors are
  passed to :func:`Solid`.
* An image name. Any other string is interpreted as a reference to an
  image defined with the image statement.

.. _images:

Images
------

The most commonly used displayable is Image, which loads a file from
disk and displays it. Since Image is so commonly used, when a string
giving a filename is used in a context that expects a displayable, an
Image is automatically created. The only time it's necessary to use
Image directly is when you want to create an image with style
properties.

.. include:: inc/im_image

::

    # These two lines are equivalent.
    image logo = "logo.png"
    image logo = Image("logo.png")

    # Using Image allows us to specify a default position as part of
    # an image.
    image logo right = Image("logo.png", xalign=1.0)

Loading an Image from from a file on disk and decoding it so it can be
drawn to the screen takes a long amount of time. While measured in the
tenths or hundreds of seconds, the duration of the loading process is
long enough that it can prevent an acceptable framerate, and become
annoying to the user.

Since an Image is of a fixed size, and doesn't change in response to
input, game state, or the size of the area available to it, an Image
can be loaded before it is needed, and placed into an area of memory
known as the image cache. Once an Image is decoded and in the cache,
it can be quickly drawn to the screen.

Ren'Py attempts to predict the images that will be used in the future,
and loads them into the image cache before they are used. When space
in the cache is needed for other images, Ren'Py will remove images
that are no longer being used.

By default, Ren'Py will predictively cache up to 8 screens worth of
image data. (If your screen is 800x600, then a screen's worth of data
is one 800x600 image, two 400x600 images, and so on.) This can be
changed with the :var:config.image_cache_size configuration
variable.

Although the precise amount is dependent on implementation details and
there is significant overhead, as a rule of thumb, each pixel in the
image cache consumes 4 bytes of main memory and 4 bytes of video
memory.

Image-Like Displayables
-----------------------

We call these displayables image-like because they take up a
rectangular area of the screen, and do not react to input.  These
differ from normal images by varying their size to fill an area
(Frame, LiveTile, and Solid), or by allowing the user to specify their
size (LiveComposite, LiveCrop, Null). They are not image manipulators.

Image-like displayables take :ref:`position-style-properties`.

.. include:: inc/disp_imagelike

Text Displayables
-----------------

See :ref:`text-displayables`.


Dynamic Displayables
--------------------

Dynamic displayables display a child displayable based on the state of
the game. They do not take any properties, as layout is controlled
by the properties of the child displayable they return.

.. include:: inc/disp_dynamic


Applying Transforms to Displayables
-----------------------------------

The At function produces a displayable from a displayable and one or
more :ref:`transforms <transforms>`.

.. include:: inc/disp_at


Layout Boxes and Grids
----------------------

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


The Grid layout displays its children in a grid on the screen. It takes
:ref:`position-style-properties` and the :propref:`spacing` style
property.

.. include:: inc/disp_grid

Effects
-------

These displayables are used to create certain visual effects.

.. include:: inc/disp_effects

Image Manipulators
------------------

An image manipulator is a displayable that takes an image or image
manipulator, performs an operation to it, and stores the result of
that operation in the image cache. Since image manipulators can be
predicted like images, they can perform expensive operations without
incuring a display-time overhead.

Image manipulators are limited to storing image data to the
cache. This means that their result is of a fixed size, known in
advance, and they can't change in response to game state or
input. Generally, image manipulators can only take images or other
image manipulators as input.

An image manipulator can be used any place a displayable can, but not
vice-versa. An :func:`Image` is a kind of image manipulator, so an
Image can be used whenever an image manipulator is required.

Many image manipulators provide the same functionality as other
displayables. Most of these exist so they can be provided as input to
other image manipulators, and so the game-maker can choose between
cache memory usage and work done at render-time. There's also an
element of historical accident here - many of these image manipulators
predate their equivalents.

.. include:: inc/im_im

im.MatrixColor
--------------

The im.MatrixColor image manipulator is an image manipulator that uses
a matrix to control how the colors of an image are transformed. The
matrix used can be an im.matrix object, which encodes a 5x5 matrix in
an object that supports matrix multiplication, and is returned by a
series of functions. im.matrix objects may be multiplied together to
yield a second object that performs both operations. For example, the
code::

    image city blue = im.MatrixColor(
        "city.jpg",
        im.matrix.desaturate() * im.matrix.tint(0.9, 0.9, 1.0))

first desaturates the image, and then tints it blue. When the
intermediate image is not needed, multiplying matrices is far
more efficient, in both time and image cache space, than using
two im.MatrixColors.

.. include:: inc/im_matrixcolor

Placeholders
------------

The Placeholder displayable is used to display background or character
images as appropriate. Placeholders are used automatically when an undefined
image is used in developer mode. Placeholder displayables can also be used
manually when the defaults are inappropriate. ::

    # By default, the girl placeholer will be used.
    image sue = Placeholder("boy")

    label start:
         show sue angry
         "Sue" "How do you do? Now you gonna die!"

.. include:: inc/placeholder
