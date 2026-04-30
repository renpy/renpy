Matrixcolor
===========

Ren'Py supports recoloring images using the :tpref:`matrixcolor` transform
property. This property can take either a :class:`Matrix` or a ColorMatrix
object.

Premultiplied Alpha Color
-------------------------

When an image is loaded, Ren'Py decompresses the image, and then copies it
to the GPU of your computer or mobile device. As part of the copying, each
of the four color channels (red, green, blue, and alpha - with alpha representing
opacity) is scaled to a number between 0.0 and 1.0.
In this system, 1.0 represents the full level of a color or fully opaque, while
0.0 represents the absence of the color or the pixel being fully transparent.

Ren'Py doesn't stop there, though. Once the values have been scaled, the red,
green, and blue channels are multiplied by the alpha channel. This means that
an opaque white pixel will have the value (1.0, 1.0, 1.0, 1.0), a 50% transparent
red pixel will have the value (0.5, 0.0, 0.0, 0.5), and a transparent pixel
will have the value (0.0, 0.0, 0.0, 0.0).

Premultiplied alpha allows Ren'Py to scale images
up and down without causing dark artifacts that come from representing
colors more directly. Scaling images is similar to averaging two pixels
together. Without premultiplied alpha, we might have a solid white pixel
and a transparent pixel - (1.0, 1.0, 1.0, 1.0) and (0.0, 0.0, 0.0, 0.0),
respectively. Average those together gets (0.5, 0.5, 0.5, 0.5), representing
50% opaque gray in the straight alpha system. 

However, since a fully transparent pixel doesn't really have
any color, it shouldn't affect the resulting color, either - only the resulting
transparency. In the premultiplied alpha system, the starting values are the same,
and so is the result - except now, (0.5, 0.5, 0.5, 0.5) has been pre-defined to
be 50% opaque white. By storing colors in this way, Ren'Py can draw them to the
screen correctly, and not get weird artifacts when scaling.

Using a Matrix to Change Colors
-------------------------------

The :class:`Matrix` objects used to change colors can consist of 16
numbers, which can in turn be arranged into a 4x4 grid. Here's a
way of doing this that assigns a letter to each number::

    define mymatrix = Matrix([ a, b, c, d,
                               e, f, g, h,
                               i, j, k, l,
                               m, n, o, p, ])

While they're represented as letters here, realize these are really numbers, either given
directly or computed.

These values are applied to the red (R), green (G), blue (B), and alpha (A)
channels of the original color to make a new color, (R', G', B', A'). The
formulas to do this are:

.. code-block:: none

    R' = R * a + G * b + B * c + A * d
    G' = R * e + G * f + B * g + A * h
    B' = R * i + G * j + B * k + A * l
    A' = R * m + G * n + B * o + A * p

While this might seem complex, there's a pretty simple structure to it -
the first row creates the new red channel, the second the new green channel
and so on. So if we wanted to make a matrix that swapped red and green for
some reason, we'd write::

    transform swap_red_and green:
        matrixcolor Matrix([ 0.0, 1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0, 0.0,
                             0.0, 0.0, 1.0, 0.0,
                             0.0, 0.0, 0.0, 1.0, ])

While this is a simple example, there is a lot of color theory that can be
expressed in this way. Matrices can be combined by multiplying them
together, and when that happens the matrices are combined right to left.

.. _colormatrix:

ColorMatrix
-----------

While Matrix objects are suitable for static color changes, they're not
useful for animating color changes. It's also useful to have a way of
taking common matrices and encapsulating them in a way that allows the
matrix to be parameterized.

The ColorMatrix is a base class that is is extended by a number of
Matrix-creating classes. Instances of ColorMatrix are called by Ren'Py,
and return Matrixes. ColorMatrix is well integrated with ATL, allowing
for matrixcolor animations. ::

    transform red_blue_tint:
        matrixcolor TintMatrix("#f00")
        linear 3.0 matrixcolor TintMatrix("#00f")
        linear 3.0 matrixcolor TintMatrix("#f00")
        repeat

The ColorMatrix class can be subclassed, with the subclasses replacing its
``__call__`` method. This method takes:

* An old object to interpolate off of. This object may be of any class,
  and may be None if no old object exists.
* A value between 0.0 and 1.0, representing the point to interpolate.
  0.0 is entirely the old object, and 1.0 is entirely the new object.

And should return a :class:`Matrix`.

As an example of a ColorMatrix, here is the implementation of Ren'Py's
TintMatrix class. ::

    class TintMatrix(ColorMatrix):
        def __init__(self, color):

            # Store the color given as a parameter.
            self.color = Color(color)

        def __call__(self, other, done):

            if type(other) is not type(self):

                # When not using an old color, we can take
                # r, g, b, and a from self.color.
                r, g, b = self.color.rgb
                a = self.color.alpha

            else:

                # Otherwise, we have to extract from self.color
                # and other.color, and interpolate the results.
                oldr, oldg, oldb = other.color.rgb
                olda = other.color.alpha
                r, g, b = self.color.rgb
                a = self.color.alpha

                r = oldr + (r - oldr) * done
                g = oldg + (g - oldg) * done
                b = oldb + (b - oldb) * done
                a = olda + (a - olda) * done

            # To properly handle premultiplied alpha, the color channels
            # have to be multiplied by the alpha channel.
            r *= a
            g *= a
            b *= a

            # Return a Matrix.
            return Matrix([ r, 0, 0, 0,
                            0, g, 0, 0,
                            0, 0, b, 0,
                            0, 0, 0, a ])


Structural Similarity
^^^^^^^^^^^^^^^^^^^^^^

In ATL, interpolating a the :tpref:`matrixcolor` property requires the
use of ColorMatrixes that have structural similarity. That means the same
types of ColorMatrix, multiplied together in the same order.

As an example, the following will interpolate from normal to a desaturated
blue tint, and then return to normal. ::

    show eileen happy at center:
        matrixcolor TintMatrix("#ffffff") * SaturationMatrix(1.0)
        linear 2.0 matrixcolor TintMatrix("#ccccff") * SaturationMatrix(0.0)
        linear 2.0 matrixcolor TintMatrix("#ffffff") * SaturationMatrix(1.0)

While the first setting of matrixcolor may seem unnecessary, it is required
to provide a base for the first linear interpolation. If it wasn't present, that
interpolation would be skipped.


Built-In ColorMatrix Subclasses
-------------------------------

The following is the list of ColorMatrix subclasses that are built into
Ren'Py.

.. include:: inc/colormatrix
