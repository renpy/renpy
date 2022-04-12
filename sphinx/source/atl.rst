.. _atl:

=====================================
Animation and Transformation Language
=====================================

The Animation and Transformation Language (ATL) provides a high-level way of
choosing a displayable to show, positioning it on the screen, and applying
transformations such as rotation, zoom, and alpha-modification. These can be
changed over time, and in response to events.

The Python equivalent of an ATL transform is the :func:`Transform`
displayable. There is no way to create an ATL transform programmatically.

Ren'Py Script Statements
========================

ATL can be included as part of three Ren'Py script statements.

.. _transform-statement:

Transform Statement
-------------------

The ``transform`` statement creates a transform that can be supplied as part of an
at clause. The syntax of the transform statement is:

.. productionlist:: script
    atl_transform : "transform" `name` "(" `parameters` ")" ":"
                  :    `atl_block`

The transform statement  must be run at init time. If it is found outside an
``init`` block, then it is automatically placed inside an ``init`` block with a
priority of 0. The transform may have a list of parameters, which must be
supplied when it is called. Default values for the right-most parameters can
be given by adding "=" and the value (e.g. "transform a (b, c=0):").

`Name` must be a Python identifier. The transform created by the ATL block is
bound to this name.::

   transform left_to_right:
       xalign 0.0
       linear 2.0 xalign 1.0
       repeat

.. _atl-image-statement:

Image Statement With ATL Block
------------------------------

The second way to use ATL is as part of an ``image`` statement with ATL block.
This binds an image name to the given transform. As there's no way to supply
parameters to this transform, it's only useful if the transform defines an
animation. The syntax for an image statement with ATL block is:

.. productionlist:: script
    atl_image : "image" `image_name` ":"
              :    `atl_block`

::

    image eileen animated:
        "eileen_happy.png"
        pause 1.0
        "eileen_vhappy.png"
        pause 1.0
        repeat


Scene and Show Statements with ATL Block
----------------------------------------

The final way to use ATL is as part of a ``scene`` or ``show`` statement. This wraps
the image being shown inside an ATL transformation.

.. productionlist:: script
    atl_scene : `stmt_scene` ":"
              :     `atl_block`
    atl_show  : `stmt_show` ":"
              :     `atl_block`


::

    scene bg washington:
        zoom 2.0

    show eileen happy:
        xalign 1.0


ATL Syntax and Semantics
========================

An ATL block consists of one or more logical lines, all at the same
indentation, and indented relative to the statement containing the block.
Each logical line in an ATL block must contain one or more ATL statements.

There are two kinds of ATL statements: simple and complex. Simple statements
do not take an ATL block. A single logical line may contain one or more ATL
statements, separated by commas. A complex statement contains a block, must
be on its own line. The first line of a complex statement always ends with a
colon ``:``.

By default, statements in a block are executed in the order in which they
appear, starting with the first statement in the block. Execution terminates
when the end of the block is reached. Time statements change this, as
described in the appropriate section below.

Execution of a block terminates when all statements in the block have
terminated.

If an ATL statement requires evaluation of an expression, such evaluation
occurs when the transform is first added to the scene list. (Such as when
using a ``show`` statement or ``ui`` function.)

ATL Statements
==============

The following are the ATL statements.

Interpolation Statement
-----------------------

The interpolation statement is the main way that ATL controls transformations.

.. productionlist:: atl
    atl_properties : ( `property` `simple_expression` ( "knot" `simple_expression` )*
                   : | "clockwise"
                   : | "counterclockwise"
                   : | "circles" simple_expression
                   : | simple_expression )*

.. productionlist:: atl
    atl_interp : ( `warper` `simple_expression` | "warp" `simple_expression` `simple_expression` )? `atl_properties`
               : | ( `warper` `simple_expression` | "warp" `simple_expression` `simple_expression` )? ":"
               :    `atl_properties`


The first part of the interpolation statement is used to select a function
that time-warps the interpolation. (That is, a function from linear time to
non-linear time.) This can either be done by giving the name of a warper
registered with ATL, or by giving the keyword "warp" followed by an
expression giving a function. Either case is followed by a number, giving the
number of seconds the interpolation should take.

If no warp function is given, the interpolation is instantaneous. Otherwise,
it persists for the amount of time given, and at least one frame.

The warper and duration are used to compute a completion fraction. This is
done by dividing the time taken by the interpolation by the duration of the
interpolation. This is clamped to the duration, and then passed to the
warper. The result returned by the warper is the completion fraction.

The interpolation statement can then contain a number of other clauses. When a
property and value are present, then the value is the value the property will
obtain at the end of the statement. The value can be obtained in several ways:

* If the value is followed by one or more knots, then spline motion is used.
  The starting point is the value of the property at the start of the
  interpolation, the end point is the property value, and the knots are used
  to control the spline. A quadratic curve is used for a single knot, Bezier
  is used when there are two and Catmull-Rom is used for three or more knots.
  In the former two cases, the knot or knots are simply control nodes. For
  Catmull-Rom, the first and last knot are control nodes (often outside the
  displayed path) and the other knots are points the path passes through.

* If the interpolation statement contains a "clockwise" or
  "counterclockwise" clause, circular motion is used, as described below.

* Otherwise, the value is linearly interpolated between the start and end
  locations, using the completion fraction.

If a simple expression is present, it should evaluate to a transform with only
a single interpolation statement, without a warper, splines, or circular
motion. The properties from the transform are processed as if they were
included in this statement.

A warper may be followed by a colon (:). In this case, it may be followed
by one or more lines containing the clauses available above. This lets
an ATL interpolation apply to multiple lines of properties.

Some sample interpolations are::

    show logo base:
        # Show the logo at the upper right side of the screen.
        xalign 1.0 yalign 0.0

        # Take 1.0 seconds to move things back to the left.
        linear 1.0 xalign 0.0

        # Take 1.0 seconds to move things to the location specified in the
        # truecenter transform. Use the ease warper to do this.
        ease 1.0 truecenter

        # Just pause for a second.
        pause 1.0

        # Set the location to circle around.
        alignaround (.5, .5)

        # Use circular motion to bring us to spiral out to the top of
        # the screen. Take 2 seconds to do so.
        linear 2.0 yalign 0.0 clockwise circles 3

        # Use a spline motion to move us around the screen.
        linear 2.0 align (0.5, 1.0) knot (0.0, .33) knot (1.0, .66)

         # Changes xalign and yalign at thje same time.
         linear 2.0 xalign 1.0 yalign 1.0

         # The same thing, using a block.
         linear 2.0:
            xalign 1.0
            yalign 1.0

An important special case is that the pause warper, followed by a time and
nothing else, causes ATL execution to pause for that amount of time.

Some properties can have values of multiple types. For example, the :propref:`xpos`
property can be an int, float, or absolute. The behavior is undefined when an
interpolation has old and new property values of different types.

Time Statement
--------------

The ``time`` statement is a simple control statement. It contains a single
`simple_expression`, which is evaluated to give a time, expressed as seconds
from the start of execution of the containing block.

.. productionlist:: atl
    atl_time : "time" `simple_expression`

When the time given in the statement is reached, the following statement
begins to execute. This transfer of control occurs even if a previous
statement is still executing, and causes any prior statement to immediately
terminate.

Time statements are implicitly preceded by a pause statement with an infinite
time. This means that if control would otherwise reach the time statement, it
waits until the time statement would take control.

When there are multiple time statements in a block, they must strictly
increase in order.

::

    image backgrounds:
        "bg band"
        time 2.0
        "bg whitehouse"
        time 4.0
        "bg washington"


Expression Statement
--------------------

An expression statement is a simple statement that starts with a simple
expression. It then contains an optional with clause, with a second simple
expression.

.. productionlist:: atl
    atl_expression :  `simple_expression` ("with" `simple_expression`)?

There are three things the first simple expression may evaluate to:

* If it's an ATL transform, and that ATL transform has **not** been supplied
  a child (through being called as a transform or transition, or
  with a `child` or `old_widget` argument), the ATL transform is
  included at the location of the expression. The ``with`` clause is ignored.

* If it's an integer or floating point number,  it's taken as a number of
  seconds to pause execution for. The ``with`` clause is ignored.

* Otherwise, the expression is interpreted to be a displayable. This
  displayable replaces the child of the transform when this clause executes,
  making it useful for animation. If a ``with`` clause is present, the second
  expression is evaluated as a transition, and the transition is applied to
  the old and new displayables.

::

    transform move_right:
        linear 1.0 xalign 1.0

    image atl example:
         # Display logo_base.png
         "logo_base.png"

         # Pause for 1.0 seconds.
         1.0

         # Show logo_bw.png, with a dissolve.
         "logo_bw.png" with Dissolve(0.5, alpha=True)

         # Run the move_right transform.
         move_right

Pass Statement
--------------

.. productionlist:: atl
    atl_pass : "pass"

The ``pass`` statement is a simple statement that causes nothing to happen. This
can be used when there's a desire to separate statements, like when there are
two sets of choice statements that would otherwise be back-to-back.

Repeat Statement
----------------


The ``repeat`` statement is a simple statement that causes the block containing it
to resume execution from the beginning. If the expression is present, then it
is evaluated to give an integer number of times the block will execute. (So a
block ending with ``repeat 2`` will execute at most twice.)

.. productionlist:: atl
    atl_repeat : "repeat" (`simple_expression`)?

The repeat statement must be the last statement in a block.::

    show logo base:
        xalign 0.0
        linear 1.0 xalign 1.0
        linear 1.0 xalign 0.0
        repeat


Block Statement
---------------

The ``block`` statement is a complex statement that contains a block of ATL statements.
This can be used to group statements that will repeat.

.. productionlist:: atl
    atl_block_stmt : "block" ":"
                   :      `atl_block`

::

    show logo base:
        alpha 0.0 xalign 0.0 yalign 0.0
        linear 1.0 alpha 1.0

        block:
            linear 1.0 xalign 1.0
            linear 1.0 xalign 0.0
            repeat

Choice Statement
----------------

The ``choice`` statement is a complex statement that defines one of a set of
potential choices. Ren'Py will pick one of the choices in the set, and
execute the ATL block associated with it, and then continue execution after
the last choice in the choice set.

.. productionlist:: atl
   atl_choice : "choice" (`simple_expression`)? ":"
              :     `atl_block`

Choice statements are greedily grouped into a choice set when more than one
choice statement appears consecutively in a block. If the `simple_expression`
is supplied, it is a floating-point weight given to that block, otherwise 1.0
is assumed.

::

    image eileen random:
        choice:
            "eileen happy"
        choice:
            "eileen vhappy"
        choice:
            "eileen concerned"

        pause 1.0
        repeat

Parallel Statement
------------------

The ``parallel`` statement is used to define a set of ATL blocks to execute in
parallel.

.. productionlist:: atl
    atl_parallel : "parallel" ":"
                 :    `atl_block`

Parallel statements are greedily grouped into a parallel set when more than
one parallel statement appears consecutively in a block. The blocks of all
parallel statements are then executed simultaneously. The parallel statement
terminates when the last block terminates.

The blocks within a set should be independent of each other, and manipulate
different properties. When two blocks change the same property, the result is
undefined.

::

    show logo base:
        parallel:
            xalign 0.0
            linear 1.3 xalign 1.0
            linear 1.3 xalign 0.0
            repeat
        parallel:
            yalign 0.0
            linear 1.6 yalign 1.0
            linear 1.6 yalign 0.0
            repeat

Event Statement
---------------

The ``event`` statement is a simple statement that causes an event with the given
name to be produced.

.. productionlist:: atl
    atl_event : "event" `name`

When an event is produced inside a block, the block is checked to see if an
event handler for the given name exists. If it does, control is transferred
to the event handler. Otherwise, the event propagates to any containing event
handler.

On Statement
------------

The ``on`` statement is a complex statement that defines an event handler. On
statements are greedily grouped into a single statement. On statement can
handle a single event name, or a comma-separated list of event names.

.. productionlist:: atl
   atl_on : "on" `name` [ "," `name` ] * ":"
          :      `atl_block`

The on statement is used to handle events. When an event is handled, handling
of any other event ends and handing of the new event immediately starts. When
an event handler ends without another event occurring, the ``default`` event
is produced (unless were already handing the ``default`` event).

Execution of the on statement will never naturally end. (But it can be ended
by the time statement, or an enclosing event handler.)

::

    show logo base:
        on show:
            alpha 0.0
            linear .5 alpha 1.0
        on hide:
            linear .5 alpha 0.0

    transform pulse_button:
        on hover, idle:
            linear .25 zoom 1.25
            linear .25 zoom 1.0

Contains Statement
------------------

The ``contains`` statement sets the displayable contained by this ATL transform
(the child of the transform). There are two variants of the contains
statement.

The contains expression variant takes an expression, and sets that expression
as the child of the transform. This is useful when an ATL transform wishes to
contain, rather than include, a second ATL transform.

.. productionlist:: atl
    atl_contains : "contains" `expression`

::

    transform an_animation:
        "1.png"
        pause 2
        "2.png"
        pause 2
        repeat

    image move_an_animation:
        contains an_animation

        # If we didn't use contains, we'd still be looping and
        # would never reach here.
        xalign 0.0
        linear 1.0 yalign 1.0


The contains block allows one to define an ATL block that is used for the
child of this ATL transform. One or more contains block statements will be
greedily grouped together, wrapped inside a :func:`Fixed`, and set as the
child of this transform.

.. productionlist:: atl
    atl_counts : "contains" ":"
         `atl_block`

Each block should define a displayable to use, or else an error will occur.
The contains statement executes instantaneously, without waiting for the
children to complete. This statement is mostly syntactic sugar, as it allows
arguments to be easily passed to the children.

::

    image test double:
        contains:
            "logo.png"
            xalign 0.0
            linear 1.0 xalign 1.0
            repeat

        contains:
            "logo.png"
            xalign 1.0
            linear 1.0 xalign 0.0
            repeat

Function Statement
------------------

The ``function`` statement allows ATL to use Python functions to control the ATL
properties.

.. productionlist:: atl
    atl_function : "function" `expression`

The functions have the same signature as those used with :func:`Transform`:

* The first argument is a transform object. Transform properties can be set
  on this object.

* The second argument is the shown timebase, the number of seconds since the
  function began executing.
* The third argument is the the animation timebase, which is the number of
  seconds something with the same tag has been on the screen.

* If the function returns a number, it will be called again after that
  number of seconds has elapsed. (0 seconds means to call the function as
  soon as possible.) If the function returns None, control will pass to the
  next ATL statement.

This function should not have side effects other
than changing the Transform object in the first argument, and may be
called at any time with any value to enable prediction.

::

    init python:
        def slide_function(trans, st, at):
            if st > 1.0:
                trans.xalign = 1.0
                return None
            else:
                trans.xalign = st
                return 0

    label start:
        show logo base:
            function slide_function
            pause 1.0
            repeat


Animation Statement
-------------------

The ``animation`` statement must be the first statement in an ATL block,
and tells Ren'Py this statement uses the animation timebase.

.. productionlist:: atl
    atl_animation : "animation"

As compared to the normal showing timebase, the animation timebase starts
when an image or screen with the same tag is shown. This is generally used
to have one image replaced by a second one at the same apparent time. For
example::

    image eileen happy moving:
        animation
        "eileen happy"
        xalign 0.0
        linear 5.0 xalign 1.0
        repeat

    image eileen vhappy moving:
        animation
        "eileen vhappy"
        xalign 0.0
        linear 5.0 xalign 1.0
        repeat

    label start:

        show eileen happy moving
        pause
        show eileen vhappy moving
        pause

This example will cause Eileen to change expression when the first pause
finishes, but will not cause her postion to change, as both animations
share the same animation time, and hence will place her sprite in the same place.
Without the animation statement, the position would reset when the player
clicks.


.. _warpers:

Warpers
=======

A warper is a function that can change the amount of time an interpolation
statement considers to have elapsed. The following warpers are defined by
default. They are defined as functions from t to t', where t and t' are
floating point numbers, with t ranging from 0.0 to 1.0 over the given
amount of time. (If the statement has 0 duration, then t is 1.0 when it runs.)
t' should start at 0.0 and end at 1.0, but can be greater or less.

``pause``
    Pause, then jump to the new value. If t == 1.0, t = 1.0. Otherwise, t'
    = 0.0.

``linear``
    Linear interpolation. t' = t

``ease``
    Start slow, speed up, then slow down. t' = .5 - math.cos(math.pi
    * t) / 2.0

``easein``
    Start fast, then slow down. t' = math.cos((1.0 - t) * math.pi / 2.0

``easeout``
    Start slow, then speed up. t' = 1.0 - math.cos(t * math.pi / 2.0)

In addition, most of Robert Penner's easing functions are supported. To
make the names match those above, the functions have been renamed
somewhat. Graphs of these standard functions can be found at
http://www.easings.net/.

.. include:: inc/easings

These warpers can be accessed in the ``_warper`` read-only module, which contains
the functions listed above.

New warpers can be defined using the ``renpy.atl_warper`` decorator, in a ``python
early`` block. It should be placed in a file that is parsed before any file
that uses the warper. This looks like::

    python early hide:

        @renpy.atl_warper
        def linear(t):
            return t

.. _transform-properties:

List of Transform Properties
============================

The following transform properties exist.

When the type is given as position, it may be an int, an ``absolute``, or a
float. If it's a float, it's interpreted as a fraction of the size of the
containing area (for :propref:`pos`) or displayable (for :propref:`anchor`).

Note that not all properties are independent. For example, :propref:`xalign` and :propref:`xpos`
both update some of the same underlying data. In a parallel statement, only
one block should adjust horizontal position, and one should adjust vertical
positions. (These may be the same block.) The angle and radius properties set
both horizontal and vertical positions.

.. transform-property:: pos

    :type: (position, position)
    :default: (0, 0)

    The position, relative to the top-left corner of the containing
    area.

.. transform-property:: xpos

    :type: position
    :default: 0

    The horizontal position, relative to the left side of the
    containing area.

.. transform-property:: ypos

    :type: position
    :default: 0

    The vertical position, relative to the top of the containing area.

.. transform-property:: anchor

    :type: (position, position)
    :default: (0, 0)

    The anchor position, relative to the top-left corner of the
    displayable.

.. transform-property:: xanchor

    :type: position
    :default: 0

    The horizontal anchor position, relative to the left side of the
    displayable.

.. transform-property:: yanchor

    :type: position
    :default: 0

    The vertical anchor position, relative to the top of the
    displayable.

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

    :type: (int, int)
    :default: (0, 0)

    The number of pixels the displayable is offset by in each direction.
    Positive values offset towards the bottom-right.

.. transform-property:: xoffset

    :type: int
    :default: 0

    The number of pixels the displayable is offset by in the horizontal
    direction. Positive values offset toward the right.

.. transform-property:: yoffset

    :type: int
    :default: 0

    The number of pixels the displayable is offset by in the vertical
    direction. Positive values offset toward the bottom.

.. transform-property:: xycenter

    :type: (position, position)
    :default: (0.0, 0.0)

    Equivalent to setting pos to the value of this property, and
    anchor to (0.5, 0.5).

.. transform-property:: xcenter

    :type: position
    :default: 0.0

    Equivalent to setting xpos to the value of this property, and
    xanchor to 0.5.

.. transform-property:: ycenter

    :type: position
    :default: 0.0

    Equivalent to setting ypos to the value of this property, and
    yanchor to 0.5.

.. transform-property:: rotate

    :type: float or None
    :default: None

    If None, no rotation occurs. Otherwise, the image will be rotated
    by this many degrees clockwise. Rotating the displayable causes it
    to be resized, according to the setting of rotate_pad, below. This
    can cause positioning to change if xanchor and yanchor are not
    0.5.

.. transform-property:: rotate_pad

    :type: boolean
    :default: True

    If True, then a rotated displayable is padded such that the width
    and height are equal to the hypotenuse of the original width and
    height. This ensures that the transform will not change size as
    its contents rotate. If False, the transform will be given the
    minimal size that contains the transformed displayable. This is
    more suited to fixed rotations.

.. transform-property:: transform_anchor

   :type: boolean
   :default: False

   If true, the anchor point is located on the cropped child, and is scaled
   and rotated as the child is transformed. Effectively, this makes the
   anchor the point that the child is rotated and scaled around.

.. transform-property:: zoom

    :type: float
    :default: 1.0

    This causes the displayable to be zoomed by the supplied
    factor.

.. transform-property:: xzoom

    :type: float
    :default: 1.0

    This causes the displayable to be horizontally zoomed by the
    supplied factor. A negative value causes the image to be
    flipped horizontally.

.. transform-property:: yzoom

   :type: float
   :default: 1.0

   This causes the displayable to be vertically zoomed by the supplied
   factor. A negative value causes the image to be flipped vertically.

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

    The alpha transform is applied to each image comprising the child of
    the transform independently. This can lead to unexpected results when
    the children overlap, such as as seeing a character through clothing.
    The :func:`Flatten` displayable can help with these problems.

.. transform-property:: additive

    :type: float
    :default: 0.0

    This controls how much additive blending Ren'Py performs. When 1.0,
    Ren'Py draws using the ADD operator. When 0.0, Ren'Py draws using
    the OVER operator.

    Additive blending is performed on each child of the transform independently.

    Fully additive blending doesn't alter the alpha channel of the destination,
    and additive images may not be visible if they're not drawn directly onto
    an opaque surface. (Complex operations, like viewport, :func:`Flatten`, :func:`Frame`,
    and certain transitions may cause problems with additive blending.)

    .. warning::

        Additive blending is only supported by hardware-based renderers, such
        as the OpenGL and DirectX/ANGLE renderers. The software renderer will
        draw additive images incorrectly.

        Once the graphics system has started, ``renpy.get_renderer_info()["additive"]``
        will be true if additive blending is supported.


.. transform-property:: around

    :type: (position, position)
    :default: (0.0, 0.0)

    If not None, specifies the polar coordinate center, relative to
    the upper-left of the containing area. Setting the center using
    this allows for circular motion in position mode.

.. transform-property:: alignaround

    :type: (float, float)
    :default: (0.0, 0.0)

    If not None, specifies the polar coordinate center, relative to
    the upper-left of the containing area. Setting the center using
    this allows for circular motion in align mode.

.. transform-property:: angle

    :type: float

    Get the angle component of the polar coordinate position. This is
    undefined when the polar coordinate center is not set.

.. transform-property:: radius

    :type: position

    Get the radius component of the polar coordinate position. This is
    undefined when the polar coordinate center is not set.

.. transform-property:: crop

    :type: None or (position, position, position, position)
    :default: None

    If not None, causes the displayable to be cropped to the given
    box. The box is specified as a tuple of (x, y, width, height).

    If corners and crop are given, crop takes priority over corners.

.. transform-property:: crop_relative

    :type: None or string
    :default: None

    If None or "child", relative components of crop (see
    :ref:`the position types documentation <position-types>`) are
    considered relatively to the width and height of the source image,
    like ``anchor`` does it.

    If "area", they are considered relatively to the available containing
    area in the context where the source image is displayed (typically
    the size of the screen), like ``pos`` does it.

    If all elements of ``crop`` are ints or ``absolute``s, this property
    has no effect.

.. transform-property:: corner1

    :type: None or (int, int)
    :default: None

    If not None, gives the upper-left corner of the crop box. Crop takes
    priority over corners.

.. transform-property:: corner2

    :type: None or (int, int)
    :default: None

    If not None, gives the lower right corner of the crop box. Cropt takes
    priority over corners.

.. transform-property:: xysize

    :type: None or (position, position)
    :default: None

    If not None, causes the displayable to be scaled to the given
    size.

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

   If not None, causes the displayable to be sized according to the
   table below. In this context "dimensions" refers to one or more of ``xsize`` and
   ``ysize`` that are not None.

   .. list-table::
      :widths: 15 85
      :header-rows: 1

      * - Value
        - Description
      * - ``contain``
        - As large as possible, without exceeding any dimensions.
          Maintains aspect ratio.
      * - ``cover``
        - As small as possible, while matching or exceeding all
          dimensions. Maintains aspect ratio.
      * - None or ``fill``
        - Stretches/squashes displayable to exactly match dimensions.
      * - ``scale-down``
        - As for ``contain``, but will never increase the size of the
          displayable.
      * - ``scale-up``
        - As for ``cover``, but will never decrease the size of the
          displayable.

.. transform-property:: size

    :type: None or (int, int)
    :default: None

    If not None, causes the displayable to be scaled to the given
    size.

    This is affected by the :tpref:`fit` property.

    .. warning::

        This property is deprecated. Use :tpref:`xysize` instead.

.. transform-property:: maxsize

    :type: None or (int, int)
    :default: None

    If not None, causes the displayable to be scaled so that it fits
    within a box of this size, while preserving aspect ratio. (Note that
    this means that one of the dimensions may be smaller than the size
    of this box.)

    .. warning::

        This property is deprecated. Consider using :tpref:`xysize` in
        conjuction with :tpref:`fit` and the value ``contain``.

.. transform-property:: subpixel

    :type: boolean
    :default: False

    If True, causes the child to be placed using subpixel positioning.

    Subpixel positioning effects the colors (including transparency)
    that are drawn into pixels, but not which pixels are drawn. When
    subpixel positoning is used in combination with movement (the usual
    case), the image should have transparent borders in the directions
    it might be moved in, if those edges are visible on the screen.

    For example, if a character sprite is being moved horizontally,
    it makes sense to have transparent borders on the left and right.
    These might not be necessary when panning over a background that
    extends outside the visible area, as the edges will not be seen.

.. transform-property:: delay

    :type: float
    :default: 0.0

    If this transform is being used as a transition, then this is the
    duration of the transition.

.. transform-property:: events

    :type: boolean
    :default: True

    If true, events are passed to the child of this transform. If false,
    events are blocked. (This can be used in ATL transforms to prevent
    events from reaching the old_widget.)

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

    The number of times to tile the image horizontally. (This is ignored when
    xpan is given.)

.. transform-property:: ytile

    :type: int
    :default: 1

    The number of times to tile the image vertically. (This is ignored when
    ypan is given.)

.. transform-property:: matrixcolor

    :type: None or Matrix or MatrixColor
    :default: None

    If not None, the value of this property is used to recolor everything
    that children of this transform draw. See :ref:`matrixcolor` for more
    information.

    This requires model-based rendering to be enabled by setting :var:`config.gl2` to
    True.

.. transform-property:: blur

    :type: None or float
    :default: None

    This blurs the child of this transform by `blur` pixels, up to the border
    of the displayable. The precise details of the blurring may change
    between Ren'Py versions, and the blurring may exhibit artifacts,
    especially when the image being blurred is changing.

    This requires model-based rendering to be enabled by setting :var:`config.gl2` to
    True.

There are also several sets of transform properties that are documented elsewhere:

3D Stage properties:
    :tpref:`perspective`, :tpref:`matrixanchor`, :tpref:`matrixtransform`, :tpref:`zpos`, :tpref:`zzoom`

Model-based rendering properties:
    :tpref:`blend`, :tpref:`mesh`, :tpref:`mesh_pad`, :tpref:`shader`

GL Properties:
    The :ref:`GL properties <gl-properties>`.

Uniforms:
    Properties beginning with ``u_`` are uniforms that can be used by :ref:`custom shaders <custom-shaders>`.

These properties are applied in the following order:

#. tile
#. mesh, blur
#. crop, corner1, corner2
#. xysize, size, maxsize
#. zoom, xzoom, yzoom
#. pan
#. rotate
#. zpos
#. matrixtransform, matrixanchor
#. zzoom
#. perspective
#. nearest, blend, alpha, additive, shader.
#. matrixcolor
#. GL Properties, Uniforms
#. position properties

Circular Motion
===============

When an interpolation statement contains the ``clockwise`` or
``counterclockwise`` keywords, the interpolation will cause circular motion.
Ren'Py will compare the start and end locations and figure out the polar
coordinate center. Ren'Py will then compute the number of degrees it will
take to go from the start angle to the end angle, in the specified direction
of rotation. If the circles clause is given, Ren'Py will ensure that the
appropriate number of circles will be made.

Ren'Py will then interpolate the angle and radius properties, as appropriate,
to cause the circular motion to happen. If the transform is in align mode,
setting the angle and radius will set the align property. Otherwise, the pos
property will be set.

External Events
===============

The following events can be triggered automatically:

``start``
    A pseudo-event, triggered on entering an ``on`` statement, if no event of
    higher priority has happened.

``show``
    Triggered when the transform is shown using the show or scene
    statement, and no image with the given tag exists.

``replace``
    Triggered when transform is shown using the ``show`` statement, replacing
    an image with the given tag.

``hide``
    Triggered when the transform is hidden using the ``hide`` statement or its
    Python equivalent.

    Note that this isn't triggered when the transform is eliminated via
    the scene statement or exiting the context it exists in, such as when
    exiting the game menu.

``replaced``
    Triggered when the transform is replaced by another. The image will
    not actually hide until the ATL block finishes.

``update``
    Triggered when a screen is updated without being shown or replacing
    another screen. This happens in rare but possible cases, such as when
    the game is loaded and when styles or translations change.

``hover``, ``idle``, ``selected_hover``, ``selected_idle``
   Triggered when button containing this transform, or a button contained
   by this transform, enters the named state.


.. _replacing-transforms:

Replacing Transforms
====================

When an an ATL transform or transform defined using the :func:`Transform` class
is replaced by another class, the properties of the transform that's being
replaced are inherited by the transform that's replacing it.

When the ``show`` statement has multiple transforms in the at list, the
transforms are matched from last to first, until one list runs out. For
example, in::

    show eileen happy at a, b, c
    "Let's wait a bit."
    show eileen happy at d, e

the ``c`` transform is replaced by ``e``, the ``b`` transform is replaced by
``d``, and nothing replaces the ``a`` transform.

At the moment of replacement, the values of the properties of the old transform
get inherited by the new transform. If the old transform was being animated,
this might mean an intermediate value is inherited. For example::

    transform bounce:
        linear 3.0 xalign 1.0
        linear 3.0 xalign 0.0
        repeat

    transform headright:
        linear 15 xalign 1.0

    label example:
        show eileen happy at bounce
        pause
        show eileen happy at headright
        pause

In this example, the sprite will bounce from left to right and back until
the player clicks. When that happens, the ``xalign`` from ``bounce`` will
be used to initialize the ``xalign`` of headright, and so the sprite
will move from where it was when the player first clicked.

The position properties (:tpref:`xpos`, :tpref:`ypos`, :tpref:`xanchor`, and :tpref:`yanchor`),
have a special rule for inheritance - a value set in the child will override a value set
in the parent. This is because a displayable may have only one position, and
a position that is actively set takes precedence. These properties may be set in
multiple ways - for example, :tpref:`xalign` sets xpos and xanchor.

Finally, when a ``show`` statement does not include an ``at`` clause, the
same displayables are used, so no inheritence is necessary. To prevent inheritance,
show and then hide the displayable.

.. _atl-transititions:

ATL Transitions
===============

It's possible to use an ATL transform to define a transition. These transitions
accept the `old_widget` and `new_widget` arguments, which are given displayables
that are transitioned from and to, respectively.

An ATL transition must set the :tpref:`delay` property to the number of seconds
the transition lasts for. It may user the :tpref:`events` property to prevent
the old displayable from receiving events. ::

    transform spin(duration=1.0, new_widget=None, old_widget=None):

        # Set how long this transform will take to complete.
        delay duration

        # Center it.
        xcenter 0.5
        ycenter 0.5

        # Spin the old displayable.
        old_widget
        events False
        rotate 0.0
        easeout (duration / 2) rotate 360.0

        # Spin the new displayable.
        new_widget
        events True
        easein (duration / 2) rotate 720.0


.. _atl-keyword-parameters:

Special ATL Keyword Parameters
==============================

There are several parameters that Ren'Py will supply to ATL, in certain
contexts, if the parameter is in the parameter list.

`child`
    When ATL is used as a transform, the child parameter is given the original
    child that the transform is applied to. This allows the child to be referred
    to explicitly. For example, it becomes possible to swap between the s
    supplied child and another displayable::

        transform lucy_jump_scare(child):
            child      # Show the original child.
            pause 5
            "lucy mad" # Jump scare.
            pause .2
            child      # Go back to the original child.

    If can also be used to place the original child inside a ``contains``
    block::

        transform marquee(width, height=1.0, duration=2.0, child=None):
            xcenter 0.5
            ycenter 0.5

            crop_relative True
            crop (0, 0, 0.5, 500)

            contains:
                child
                xanchor 0.0 xpos 1.0
                linear duration xanchor 1.0 xpos 0.0


`old_widget`, `new_widget`
    When an ATL block is used as a transition, these are given displayables
    that are transitioned from and to, respectively.
