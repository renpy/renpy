Color Class
===========

Ren'Py has a Color class that can be used for converting from one color
space to another, or performing various color theory operations. Colors
are immutable, and can be used wherever a color tuple can be used.

Color tuples operate in one of three color spaces.

* RGB - Red, Green, Blue
* HLS - Hue, Lightness, Saturation
* HSV - Hue, Saturation, Value

As an example of some of the calculations that can be performed, all of
the following colors are bright green::

    # Standard Ren'Py Colors.
    Color("#0f0")
    Color("#00ff00")
    Color((0, 255, 0, 255))

    # Convert from other color spaces.
    Color(hls=(.333, 0.5, 1.0))
    Color(hsv=(.333, 1.0, 1.0))

    # Turns red into green via a method that returns a new color.
    Color("#f00").rotate_hue(.333)

.. include:: inc/color
