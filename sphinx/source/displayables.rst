.. _displayables:

Displayables
============

A displayable is an object that can be shown to the user. Ren'Py
displayables can be used in many ways.

* Assignment to an image name using the ``image`` statement.
* Added to a screen using the screen language ``add`` statement.
* Assignment to certain config variables.
* Assignment to certain style properties.

When a Ren'Py function or variable expects a displayable, there are
several things that can be provided:

* An object of type Displayable, created by calling one of the
  functions given below.
* A string with a colon ``:`` in it. These are rare, but see the section on
  :ref:`displayable prefixes <displayable-prefix>` below.
* A string with a dot ``.`` in it. Such a string is interpreted as
  a filename by :func:`Image`.
* A color. A color may either be given as a hexadecimal color string in "#rgb",
  "#rgba", "#rrggbb", or "#rrggbbaa" form, a :class:`Color`, or an (r, g, b, a) tuple,
  where each component is an integer between 0 and 255. Colors are
  passed to :func:`Solid`.
* An image name. Any other string is interpreted as a reference to an
  image, either defined with the image statement or auto-defined from
  the :ref:`images directory <images-directory>`.
* A list. If a list is provided, each item is expanded as described
  below, and checked to see if it matches a filename or image name.
  If so, expansion stops and the matched thing is then processed
  as described above.

Strings may have one or more square-bracket substitutions in them,
such as "eileen [mood]" or "eileen_[outfit]_[mood].png". When such a
string is given, a dynamic image is created. A dynamic image has
:ref:`text interpolation <text-interpolation>` performed at the start
of each interaction (such as say statements and menus). The resulting
string is processed according to the rules above.

When a string has "[prefix\_]" in it, that substitution is replaced with
each of the style prefixes associated with the current displayable.

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

There are four image file formats we recommend you use:

* AVIF
* WEBP
* PNG
* JPG

And one vector image file format we recommend:

* SVG

Non-animated GIF and BMP files are also supported, but should not be
used in modern games.

Loading an Image from a file on disk and decoding it so it can be
drawn to the screen takes a long amount of time. While measured in the
tenths or hundreds of seconds, the duration of the loading process is
long enough that it can prevent an acceptable framerate, and become
annoying to the user.

Since an Image is of a fixed size, and doesn't change in response to
input, game state, or the size of the area available to it, an Image
can be loaded before it is needed and placed into an area of memory
known as the image cache. Once an Image is decoded and in the cache,
it can be quickly drawn to the screen.

Ren'Py attempts to predict the images that will be used in the future,
and loads them into the image cache before they are used. When space
in the cache is needed for other images, Ren'Py will remove images
that are no longer being used.

By default, Ren'Py will predictively cache up to 8 screens worth of
image data. (If your screen is 800x600, then a screen's worth of data
is one 800x600 image, two 400x600 images, and so on.) This can be
changed with the :var:`config.image_cache_size` configuration
variable.

Although the precise amount is dependent on implementation details and
there is significant overhead, as a rule of thumb, each pixel in the
image cache consumes 4 bytes of main memory and 4 bytes of video
memory.

SVG Images
----------

Ren'Py supports many SVG 1.0 images, using the NanoSVG library.
Some unsupported features include:

* Text elements are ignored. If the text is converted into a path, it will
  be rendered.
* Embedded bitmaps are ignored.
* Scripts are ignored.
* Animations are ignored.

A list of features NanoSVG supports may be found
`here <https://core.tcl-lang.org/tips/doc/trunk/tip/507.md>`__.

It's recommended to convert everything in an SVG image that will not
render properly into paths.

Ren'Py will render SVG images as if the virtual screen was 96dpi.
If the window is enlarged or shrunk, the SVG image will be scaled
up or down, respectively, and :ref:`oversampling <oversampling>` will
be used to ensure the image is rendered at the correct virtual
size.

This ensures the SVG will be rendered sharp if it is not scaled.

Image-Like Displayables
-----------------------

We call these displayables image-like because they take up a
rectangular area of the screen, and do not react to input.  These
differ from normal images by varying their size to fill an area
(Frame, Tile, and Solid), or by allowing the user to specify their
size (Composite, Crop, Null). They are not image manipulators.

Image-like displayables take :ref:`position-style-properties`.

.. include:: inc/disp_imagelike

Text Displayables
-----------------

See :ref:`text-displayables`.


Dynamic Displayables
--------------------

Dynamic displayables display a child displayable based on the state of
the game.

Note that these dynamic displayables always display their current state.
Because of this, a dynamic displayable will not participate in a
transition. (Or more precisely, it will display the same thing in both the
old and new states of the transition.)

By design, dynamic displayables are intended to be used for things that
change rarely and when an image defined this way is off screen (Such as
a character customization system). It is not designed for things that
change frequently, such as character emotions.

.. include:: inc/disp_dynamic


Layer Displayables
------------------

Layer displayables display the contents of a layer based on the state of the
game. They are intended for use with :var:`config.detached_layers`.

Note that similar to dynamic displayables, the layers shown within always
display their current state. Because of this, the contents of a layer
displayable will not participate in a transition, unless that transition is
targeted at the layer being displayed.

.. include:: inc/disp_layer

::

    # A new detached layer to hold the contents of a broadcast.
    define config.detached_layers += [ "broadcast" ]

    # A layer displayable to represent a TV and watch the broadcast layer.
    image tv = Window(Layer("broadcast"), background='#000', padding=(10, 10), style="default")

    image living_room = Placeholder('bg', text='living_room')
    image studio = Solid('7c7')
    image eileen = Placeholder('girl')

    label example:
        pause

        # Set up the broadcast scene.
        scene studio onlayer broadcast
        with None

        # Begin a new scene in the living room.
        scene living_room

        # Show the TV in the lower right corner of ths screen.
        show tv:
          align (.75, .75) zoom .3

        # Show Eileen in the broadcast.
        show eileen onlayer broadcast

        # Dissolve into the living room, as Eileen enters the TV from the right.
        with {'master': dissolve, 'broadcast': moveinright}
        pause


Layout Boxes and Grids
----------------------

Layout boxes are displayables that lay out their children on the
screen. They can lay out the children in a horizontal or vertical
manner, or lay them out using the standard positioning algorithm.

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

:doc:`Image manipulators <im>` are an historic kind of displayables that
apply transformations or operations exclusively to other images or image
manipulators - to the exclusion of the other kinds of displayables.

An image manipulator can be used any place a displayable can, but not
vice-versa. An :func:`Image` is a kind of image manipulator, so an
Image can be used whenever an image manipulator is required.

Their use is historic. A number of image manipulators that had been documented
in a distant past should no longer be used, as they suffer from inherent
problems, and in general (except for :func:`im.Data`), the :func:`Transform`
displayable provides similar functionality while fixing the problems.

For the list of image manipulators, see the :doc:`image manipulator <im>`
documentation.

Placeholders
------------

The Placeholder displayable is used to display background or character
images as appropriate. Placeholders are used automatically when an undefined
image is used in developer mode. Placeholder displayables can also be used
manually when the defaults are inappropriate. ::

    # By default, the girl placeholder will be used.
    image sue = Placeholder("boy")

    label start:
        show sue angry
        "Sue" "How do you do? Now you gonna die!"

.. include:: inc/placeholder

.. _displayable-prefix:

Displayable Prefixes
--------------------

Displayable prefixes make it possible for a creator to define their own
displayables, and refer to them anywhere a displayable can be used in
Ren'Py. A prefixed displayable is a string with a colon in it. The prefix
is to the left of the colon, and the argument is anything to the right of
it. The :var:`config.displayable_prefix` variable maps a prefix to a function.
The function takes the argument, and either returns a displayable or None.

For example, this makes the big prefix return an image that is twice as
big as the original. ::

    init -10 python:
        def embiggen(s):
            return Transform(s, zoom=2)

        config.displayable_prefix["big"] = embiggen

The ``init -10`` makes sure the prefix is defined before any images that use it.
The prefix can then be used to define images::

    image eileen big = "big:eileen happy"

or in any other place where a displayable is required.

See also
--------

:doc:`displaying_images` : the basics of how to make all these displayables
appear on the screen.
