====================
Transform Properties
====================

Transform properties are used by :doc:`transforms` to influence how a
displayable is drawn. They are usually set using :ref:`ATL <atl>` or the
:class:`Transform` class.

.. _transform-properties:

List of Transform Properties
============================

The following transform properties exist.

When the type is given as a :term:`position`, its relative component is
interpreted as a fraction of the size of the containing area (for
:tpref:`pos`) or of the displayable (for :tpref:`anchor`).

Note that not all properties are independent. For example, :tpref:`xalign` and
:tpref:`xpos` both update some of the same underlying data. In a ``parallel``
statement, not more than one block should adjust properties sharing the same data.
The angle and radius properties set both horizontal and vertical positions.

Positioning
-----------

.. transform-property:: pos

    :type: (position, position)
    :default: (0, 0)

    The position, relative to the top-left corner of the containing area.

.. transform-property:: xpos

    :type: position
    :default: 0

    The horizontal position, relative to the left side of the containing area.

.. transform-property:: ypos

    :type: position
    :default: 0

    The vertical position, relative to the top of the containing area.

.. transform-property:: anchor

    :type: (position, position)
    :default: (0, 0)

    The anchor position, relative to the top-left corner of the displayable.

.. transform-property:: xanchor

    :type: position
    :default: 0

    The horizontal anchor position, relative to the left side of the
    displayable.

.. transform-property:: yanchor

    :type: position
    :default: 0

    The vertical anchor position, relative to the top of the displayable.

.. transform-property:: align

    :type: (float, float)
    :default: (0.0, 0.0)

    Equivalent to setting pos and anchor to the same value.

.. transform-property:: xalign

    :type: float
    :default: 0.0

    Equivalent to setting xpos and xanchor to this value.

.. transform-property:: yalign

    :type: float
    :default: 0.0

    Equivalent to setting ypos and yanchor to this value.

.. transform-property:: offset

    :type: (absolute, absolute)
    :default: (0, 0)

    The number of pixels the displayable is offset by in each direction.
    Positive values offset towards the bottom-right.

.. transform-property:: xoffset

    :type: absolute
    :default: 0

    The number of pixels the displayable is offset by in the horizontal
    direction. Positive values offset toward the right.

.. transform-property:: yoffset

    :type: absolute
    :default: 0

    The number of pixels the displayable is offset by in the vertical direction.
    Positive values offset toward the bottom.

.. transform-property:: xycenter

    :type: (position, position)
    :default: (0.0, 0.0)

    Equivalent to setting pos to the value of this property, and anchor to
    (0.5, 0.5).

.. transform-property:: xcenter

    :type: position
    :default: 0.0

    Equivalent to setting xpos to the value of this property, and xanchor to
    0.5.

.. transform-property:: ycenter

    :type: position
    :default: 0.0

    Equivalent to setting ypos to the value of this property, and yanchor to
    0.5.

.. transform-property:: subpixel

    :type: boolean
    :default: False

    If True, causes the child to be placed using subpixel positioning.

    Subpixel positioning effects the colors (including transparency) that are
    drawn into pixels, but not which pixels are drawn. When subpixel positioning
    is used in combination with movement (the usual case), the image should have
    transparent borders in the directions it might be moved in, if those edges
    are visible on the screen.

    For example, if a character sprite is being moved horizontally, it makes
    sense to have transparent borders on the left and right. These might not be
    necessary when panning over a background that extends outside the visible
    area, as the edges will not be seen.

Rotation
--------

.. transform-property:: rotate

    :type: float or None
    :default: None

    If None, no rotation occurs. Otherwise, the image will be rotated by this
    many degrees clockwise. Rotating the displayable causes it to be resized,
    according to the setting of rotate_pad, below. This can cause positioning to
    change if xanchor and yanchor are not 0.5.

.. transform-property:: rotate_pad

    :type: boolean
    :default: True

    If True, then a rotated displayable is padded such that the width and height
    are equal to the hypotenuse of the original width and height. This ensures
    that the transform will not change size as its contents rotate. If False,
    the transform will be given the minimal size that contains the transformed
    displayable. This is more suited to fixed rotations.

.. transform-property:: transform_anchor

   :type: boolean
   :default: False

   If true, the anchor point is located on the cropped child, and is scaled and
   rotated as the child is transformed. Effectively, this makes the anchor the
   point that the child is rotated and scaled around.

Zoom and Flip
-------------

.. transform-property:: zoom

    :type: float
    :default: 1.0

    This causes the displayable to be zoomed by the supplied factor.

.. transform-property:: xzoom

    :type: float
    :default: 1.0

    This causes the displayable to be horizontally zoomed by the supplied
    factor. A negative value causes the image to be flipped horizontally.

.. transform-property:: yzoom

   :type: float
   :default: 1.0

   This causes the displayable to be vertically zoomed by the supplied
   factor. A negative value causes the image to be flipped vertically.

Pixel Effects
-------------

.. transform-property:: nearest

    :type: boolean
    :default: None

    If True, the displayable and its children are drawn using nearest-neighbor
    filtering. If False, the displayable and its children are drawn using
    bilinear filtering. If None, this is inherited from the parent, or
    :var:`config.nearest_neighbor`, which defaults to False.

.. transform-property:: alpha

    :type: float
    :default: 1.0

    This controls the opacity of the displayable.

    The alpha transform is applied to each image comprising the child of the
    transform independently. This can lead to unexpected results when the
    children overlap, such as seeing a character through clothing. The
    :func:`Flatten` displayable can help with these problems.

.. transform-property:: additive

    :type: float
    :default: 0.0

    This controls how much additive blending Ren'Py performs. When 1.0, Ren'Py
    draws using the ADD operator. When 0.0, Ren'Py draws using the OVER
    operator.

    Additive blending is performed on each child of the transform independently.

    Fully additive blending doesn't alter the alpha channel of the destination,
    and additive images may not be visible if they're not drawn directly onto an
    opaque surface. (Complex operations, like viewport, :func:`Flatten`,
    :func:`Frame`, and certain transitions may cause problems with additive
    blending.)

.. transform-property:: matrixcolor

    :type: None or Matrix or MatrixColor
    :default: None

    If not None, the value of this property is used to recolor everything that
    children of this transform draw. Interpolation is only supported when
    MatrixColors are used, and the MatrixColors are structurally similar. See
    :doc:`matrixcolor` for more information.

.. transform-property:: blur

    :type: None or float
    :default: None

    This blurs the child of this transform by `blur` pixels, up to the border
    of the displayable. The precise details of the blurring may change between
    Ren'Py versions, and the blurring may exhibit artifacts, especially when the
    image being blurred is changing.

Polar Positioning
-----------------

.. transform-property:: around

    :type: (position, position)
    :default: (0.0, 0.0)

    This specifies the starting point, relative to the upper-left corner of the
    containing area, from where the polar vector (computed from :tpref:`angle`
    and :tpref:`radius`) will be drawn. The sum of the two gives the resulting
    :tpref:`pos`.

.. transform-property:: angle

    :type: float

    This gives the angle component of a position specified in polar coordinates.
    This is measured in degrees, with 0 being to the top of the screen, and 90
    being to the right.

    Ren'Py clamps this angle to between 0 and 360 degrees, including 0 but
    not 360. If a value is set outside this range, it will be set to the
    equivalent angle in this range before being used. (Setting this to -10 is
    the equivalent of setting it to 350.)

.. transform-property:: radius

    :type: position

    The radius component of the position given in polar coordinates.

    If a float, this will be scaled to the smaller of the width and height
    available to the transform.

Polar Positioning of the Anchor
-------------------------------

.. note::

    While using polar coordinates to position the anchor is possible, it's often
    more convenient to simply set :tpref:`anchor` to (0.5, 0.5), and position
    the center of your displayable.

.. transform-property:: anchoraround

    :type: (position, position)

    This specifies the starting point, relative to the upper-left corner of the
    displayable, from where the polar vector (computed from :tpref:`anchorangle`
    and :tpref:`anchorradius`) will be drawn. The sum of the two gives the
    resulting :tpref:`anchor`.

.. transform-property:: anchorangle

    :type: (float)

    The angle component of the polar coordinates of the anchor. This is
    specified in degrees, with 0 being to the top and 90 being to the right.

    Ren'Py clamps this angle to between 0 and 360 degrees, including 0 but
    not 360. If a value is set outside this range, it will be set to the
    equivalent angle in this range before being used. (Setting this to -10 is
    the equivalent of setting it to 350.)

.. transform-property:: anchorradius

    :type: (position)

    The radius component of the polar coordinates of the anchor.

    If a float, it is scaled horizontally and vertically to the size and shape
    of the displayable: if the height is not equal to the width, a radius that
    is not strictly absolute will result in elliptical motion when varying the
    anchorangle. For that reason, it is recommended to only pass ``int`` or
    :func:`absolute` values to this property.

Cropping and Resizing
---------------------

.. transform-property:: crop

    :type: None or (position, position, position, position)
    :default: None

    If not None, causes the displayable to be cropped to the given box. The box
    is specified as a tuple of (x, y, width, height), with x and y being the
    coordinates of the box's top-left corner relative to the top-left corner of
    the child. All values can expand outside of the bounds of the original
    image, with the area outside being transparent, though width and height must
    be positive.

    If corners and crop are given, crop takes priority over corners.

.. transform-property:: corner1

    :type: None or (position, position)
    :default: None

    If not None, gives the upper-left corner of the crop box. The values can
    expand outside of the bounds of the original image. Crop takes priority over
    corners.

.. transform-property:: corner2

    :type: None or (position, position)
    :default: None

    If not None, gives the lower-right corner of the crop box. The values can
    expand outside of the bounds of the original image, but they should not be
    inferior to :tpref:`corner1`. Crop takes priority over corners.

.. transform-property:: xysize

    :type: None or (position, position)
    :default: None

    If not None, causes the displayable to be scaled to the given size. This is
    equivalent to setting the :tpref:`xsize` and :tpref:`ysize` properties to
    the first and second components.

    This is affected by the :tpref:`fit` property.

.. transform-property:: xsize

    :type: None or position
    :default: None

    If not None, causes the displayable to be scaled to the given width.

    This is affected by the :tpref:`fit` property.

.. transform-property:: ysize

    :type: None or position
    :default: None

    If not None, causes the displayable to be scaled to the given height.

    This is affected by the :tpref:`fit` property.

.. transform-property:: fit

    :type: None or string
    :default: None

    Causes the displayable to be sized according to the table below. In the
    context of the table below, the "dimensions" are:

    * If both :tpref:`xsize` and :tpref:`ysize` are not None, both sizes are
      used as the dimensions.
    * If only one of those properties is not None, it is used as the sole
      dimension.
    * Otherwise, if fit is not None the area that the Transform is contained in
      is used as the dimensions.

    If fit, xsize, and ysize are all None, this property does not apply.

    .. list-table::
       :widths: 15 85
       :header-rows: 1

       * - Value
         - Description
       * - ``contain``
         - As large as possible, without exceeding any dimensions. Maintains
           aspect ratio.
       * - ``cover``
         - As small as possible, while matching or exceeding all dimensions.
           Maintains aspect ratio.
       * - None or ``fill``
         - Stretches/squashes displayable to exactly match dimensions.
       * - ``scale-down``
         - As for ``contain``, but will never increase the size of the
           displayable.
       * - ``scale-up``
         - As for ``cover``, but will never decrease the size of the
           displayable.

Panning and Tiling
------------------

.. transform-property:: xpan

    :type: None or float
    :default: None

    If not None, this interpreted as an angle that is used to pan horizontally
    across a 360 degree panoramic image. The center of the image is used as the
    zero angle, while the left and right edges are -180 and 180 degrees,
    respectively.

.. transform-property:: ypan

    :type: None or float
    :default: None

    If not None, this interpreted as an angle that is used to pan vertically
    across a 360 degree panoramic image. The center of the image is used as the
    zero angle, while the top and bottom edges are -180 and 180 degrees,
    respectively.

.. transform-property:: xtile

    :type: int
    :default: 1

    The number of times to tile the image horizontally.

.. transform-property:: ytile

    :type: int
    :default: 1

    The number of times to tile the image vertically.

Transitions
-----------

See :ref:`atl-transitions`.

.. transform-property:: delay

    :type: float
    :default: 0.0

    If this transform is being used as a transition, then this is the duration
    of the transition. See :ref:`atl-transitions`.

.. transform-property:: events

    :type: boolean
    :default: True

    If True, events are passed to the child of this transform. If False, events
    are blocked. (This can be used in ATL transitions to prevent events from
    reaching the old_widget.)

Other
-----

.. transform-property:: fps

    :type: float or None
    :default: None

    If not None, this alters time inside the transform so that it is discrete.
    For example, if a transform has an fps of 10, then times inside the
    transform will be rounded down to the nearest multiple of 0.1. This can be
    used to simulate a lower frame rate.

.. transform-property:: show_cancels_hide

    :type: boolean
    :default: True

    Normally, when a displayable or screen with the same tag or name as one that
    is hiding is shown, the hiding displayable or screen is removed, cancelling
    the hide transform. If this property is False in the hide transform, this
    cancellation will not occur, and the hide transform will proceed to
    completion.

There are also several sets of transform properties that are documented
elsewhere:

3D Stage properties:
    :tpref:`perspective`, :tpref:`point_to`, :tpref:`orientation`, :tpref:`xrotate`, :tpref:`yrotate`, :tpref:`zrotate`, :tpref:`matrixanchor`, :tpref:`matrixtransform`, :tpref:`zpos`, :tpref:`zzoom`

Model-based rendering properties:
    :tpref:`blend`, :tpref:`mesh`, :tpref:`mesh_pad`, :tpref:`shader`

GL Properties:
    The :ref:`GL properties <gl-properties>`.

Uniforms:
    Properties beginning with ``u_`` are uniforms that can be used by :ref:`custom shaders <custom-shaders>`.

Property Order
==============

Transform properties are applied in the following order:

#. fps
#. mesh, blur
#. tile
#. pan
#. crop, corner1, corner2
#. xysize, size, maxsize
#. zoom, xzoom, yzoom
#. point_to
#. orientation
#. xrotate, yrotate, zrotate
#. rotate
#. zpos
#. matrixtransform, matrixanchor
#. zzoom
#. perspective
#. nearest, blend, alpha, additive, shader
#. matrixcolor
#. GL Properties, Uniforms
#. position properties
#. show_cancels_hide


Deprecated Transform Properties
===============================

.. warning::

    The following properties should not be used in modern games, as they may
    conflict with more recent features. They are only kept here for
    compatibility, along with the new way of achieving the same behavior.

.. transform-property:: alignaround

    :type: (float, float)

    This sets :tpref:`anchor`, :tpref:`around`, and :tpref:`anchoraround` to the
    same value.

.. transform-property:: crop_relative

    :type: boolean
    :default: True

    If False, float components of :tpref:`crop`, :tpref:`corner1` and
    :tpref:`corner2` are interpreted as an absolute number of pixels, instead of
    a fraction of the width and height of the source image.

    If an absolute number of pixel is to be expressed, :func:`absolute`
    instances should be provided to these properties instead of using the
    crop_relative property. If necessary, values of dubious type can be wrapped
    in the :func:`absolute` callable.

.. transform-property:: size

    :type: None or (int, int)
    :default: None

    This is an older version of :tpref:`xysize` interpreting floating-point
    values as an absolute number of pixels.

.. transform-property:: maxsize

    :type: None or (int, int)
    :default: None

    If not None, causes the displayable to be scaled so that it fits within a
    box of this size, while preserving aspect ratio. (Note that this means that
    one of the dimensions may be smaller than the size of this box.)

    To achieve the same result, give the values to the :tpref:`xysize` property,
    and set the :tpref:`fit` property to the value "contain".
