.. _matrixcolor:

Matrixcolor
===========

Ren'Py supports recoloring images using the :tpref:`matrixcolor` transform
property. This property can take either a static matrix produced by
:func:`im.matrix` or one of its methods, or a :func:`MatrixColor` object.

The matrixcolor can be supplied as a property of :func:`Transform`, provided
it is given an im.matrix::

    image eileen dark = Transform("eileen concerned", matrixcolor=im.matrix.brightness(-0.5))

when used with an ATL, either an im.matrix object can be used::

    image eileen gray:
        "eileen happy"
        matrixcolor im.matrix.desaturate()

or a MatrixColor object, which allows one to specify a matrixcolor that
changes with time. For example::

    transform rotate_hue:
        matrixcolor HueMatrixColor(0.0)
        linear 5.0 matrixcolor HueMatrixColor(360.0)
        repeat


im.matrix
---------

An im.matrix object encodes a 5x5 matrix in an object that supports matrix
multiplication, and is returned by a series of functions. These objects may be
multiplied together to yield a second object that performs both operations.
For example::

    image city blue:
        "city.jpg"
        matrixcolor im.matrix.desaturate() * im.matrix.tint(0.9, 0.9, 1.0)


first desaturates the image, and then tints it blue.

... include:: inc/im_matrix

