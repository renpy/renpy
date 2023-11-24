:orphan:

Image Manipulators
==================

An image manipulator is a displayable that takes an image or image
manipulator, and either loads it or performs an operation on it.
Image manipulators can only take images or other
image manipulators as input.

An image manipulator can be used any place a displayable can, but not
vice-versa. An :func:`Image` is a kind of image manipulator, so an
Image can be used whenever an image manipulator is required.

.. warning::

    The use of image manipulators is
    historic. A number of image manipulators that had been documented in the
    past should no longer be used, as they suffer from inherent problems,
    and in general (except for :func:`im.Data`), the :func:`Transform`
    displayable provides similar functionality while fixing the problems.

.. include:: inc/im_im

im.MatrixColor
--------------

.. warning::

    The im.MatrixColor image manipulator has been replaced by Transforms
    and ATL transforms that specify the matrixcolor property. Each `im.matrix`
    generator has been given a new `Matrix` equivalent, which can be found
    in the :doc:`matrixcolor documentation <matrixcolor>`.

The im.MatrixColor image manipulator is an image manipulator that uses
a matrix to control how the colors of an image are transformed. The
matrix used can be an im.matrix object, which encodes a 5x5 matrix in
an object that supports matrix multiplication, and is returned by a
series of functions. im.matrix objects may be multiplied together to
yield a second object that performs both operations. For example::

    image city blue = im.MatrixColor(
        "city.jpg",
        im.matrix.desaturate() * im.matrix.tint(0.9, 0.9, 1.0))

first desaturates the image, and then tints it blue. When the
intermediate image is not needed, multiplying matrices is far
more efficient, in both time and image cache space, than using
two im.MatrixColors.

.. warning::

    The new Matrix objects multiply in the opposite order as the im.Matrixcolor
    ones. With X being the Matrix corresponding to im.Matrixcolor.x,
    ``C*B*A`` will be the Matrix corresponding to ``im.a*im.b*im.c``.

.. include:: inc/im_matrixcolor
.. include:: inc/im_matrix
