.. _transforms:

==========
Transforms
==========

Transforms are used in order to turn a :doc:`displayable <displayables>` into
another displayable. There are several kinds of transforms, and various ways to
create them. The built-in transforms are used to control where an image is
placed on the screen, while user-defined transforms can cause more complex
effects, like motion, zoom, rotation, up to complex color effects.

Quickstart
==========

Transforms can be applied to images by passing them to the ``at`` clause of the
:ref:`show <show-statement>` or scene statements. The following applies the
``right`` transform to the ``eileen happy`` image::

    show eileen happy at right

Multiple transforms can be applied by separating them with commas. These
transforms are applied from left-to-right. ::

    show eileen happy at halfsize, right

Simple ATL transform::

    transform slide_right:
        xalign 0.0
        linear 1.0 xalign 1.0

    label start:
        show eileen happy at slide_right
        pause

Showing transforms with Python::

    label start:
        $ renpy.show("eileen happy", at_list=right)
        pause

Simple Python transform using ``At()``::

    init python:
        def show_eileen_rotated():
            rotated = Transform(rotate=45)
            show_stmt = At("eileen happy", rotated)
            renpy.show("eileen", what=show_stmt)

    label start:
        $ show_eileen_rotated()
        pause

.. Add a "common pitfalls" section here.

Built-in Transforms
===================

Ren'Py ships with a number of transforms defined by default. These transforms
position things on the screen. Here's a depiction of where each built-in
transform will position an image.

.. code-block:: none

                  +-----------------------------------------------------------+
                  | topleft, reset               top                 topright |
                  |                                                           |
                  |                                                           |
                  |                                                           |
                  |                                                           |
                  |                          truecenter                       |
                  |                                                           |
                  |                                                           |
                  |                                                           |
                  |                                                           |
    offscreenleft | left                   center, default              right | offscreenright
                  +-----------------------------------------------------------+

The :var:`offscreenleft` and :var:`offscreenright` transforms position images
off the edges of the screen. These transforms can be used to move things off
the screen (remember to hide them afterwards, to ensure that they do not consume
resources).

The transforms are:

.. var:: center

    Centers horizontally, and aligns to the bottom of the screen.

.. var:: default

    Centers horizontally, and aligns to the bottom of the screen. This can be
    redefined via :var:`config.default_transform` to change the default
    placement of images shown with the show or scene statements.

.. var:: left

    Aligns to the bottom-left corner of the screen.

.. var:: offscreenleft

    Places the displayable off the left side of the screen, aligned to the
    bottom of the screen.

.. var:: offscreenright

    Places the displayable off the right side of the screen, aligned to the
    bottom of the screen.

.. var:: reset

    Resets the transform to the default values of each property, removing any
    properites set before it.

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


.. _atl:

ATL - Animation and Transformation Language
===========================================

The Animation and Transformation Language (ATL) is a high-level language which
can create animations, move displayables across the screen, set their position,
apply transformations, and more. These can be changed over time, and in response
to events.

ATL transform objects, which are created using the :ref:`transform-statement`
down below, are displayables and can be used as such (even though they will be
transparent when their child displayable is not set) : they can be passed to a
screen's :ref:`sl-add` element, or to a :ref:`show-expression-statement`
statement, or to the :func:`renpy.show` function.


Ren'Py script statements
------------------------

There are three Ren'Py script statements which can include ATL code.

.. _transform-statement:

Transform Statement
~~~~~~~~~~~~~~~~~~~

The ``transform`` statement creates a new transform that you can use to animate
and position displayables in your game. The transform is reusable, and can be
applied to images and other displayables throughout your game using the
``at`` clause of the :ref:`show <show-statement>` and scene statements.

Transforms can also act as :doc:`displayables` and be displayed directly.
However, unlike other displayables which exist in the global image namespace
(see :ref:`defining-images`), transforms are created as variables in the appropriate
:ref:`named store <named-stores>` (or the default store).

The transform is created during :ref:`init time <init-phase>` (when the game starts up).

**Syntax**

    Basic form::

        transform <transform_name>:
            <atl_block>

    With parameters::

        transform <transform_name>( <parameters> ):
            <atl_block>

**Usage**

    .. table::
        :widths: auto

        ==============  =========  ===========
        Name            Type       Description
        ==============  =========  ===========
        transform_name  word       Name of the transform.

                                   Must be valid Python identifiers separated by dots

                                   (e.g., ``my_transform`` or ``sprites.bounce``)
        parameters      --         (Optional) Parameters of the transform
        atl_block       block      ATL code block defining the transform
        ==============  =========  ===========

    ..
        update the special child section with this section

    You can add parameters to make your transforms flexible and reusable. Parameters
    work similarly to Python function parameters.

    Currently not supported:

    * Positional-only parameters (using ``/``)
    * Required keyword-only parameters (after ``*`` without defaults)
    * ``*args`` (variadic positional parameters)
    * ``**kwargs`` (variadic keyword parameters)

    .. note ::

        * If your transform has parameters without default values, you must provide
          values for all of them before you can use it as a transform
        * See also: :ref:`atl-partial`


**Example**

    ::

        transform left_to_right:
            xalign 0.
            linear 2 xalign 1.
            repeat

        transform ariana.left:
            xalign .3

        transform animated_ariana_disp(duration=1.0):
            "ariana"
            pause duration
            "ariana_reverse"
            pause duration
            repeat

        label start:
            show eileen happy at left_to_right
            pause
            show animated_ariana_disp
            pause

.. _atl-image-statement:

Image Statement with ATL Block
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second way to include ATL code in a script is as part of an :ref:`image
statement <image-statement>`. As its inline counterpart, it binds an image name
(which may contain spaces) to the given transform. As there is no way to supply
with parameters, it's only useful if the transform defines an animation.

**Syntax**

    ::

        image <image_name>:
            <atl_block>

**Usage**

    .. table::
        :widths: auto

        ============  =========  ===========
        Name          Type       Description
        ============  =========  ===========
        image_name    word(s)    Name of the image
        atl_block     block      ATL code block defining the transform
        ============  =========  ===========

**Example**

    ::

        image animated_ariana_img:
            "ariana"
            pause 1.
            "ariana_reverse"
            pause 1.
            repeat


Scene and Show Statements with ATL Block
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final way to use ATL is as part of a :ref:`show <show-statement>` or scene
statement. This wraps the image that's being shown inside an ATL transformation
which is created on the fly and applied to the image.

**Syntax**

    ::

        show <image_name>:
            <atl_block>

        scene <image_name>:
            <atl_block>

**Usage**

    .. table::
        :widths: auto

        ============  =========  ===========
        Name          Type       Description
        ============  =========  ===========
        image_name    word(s)    Name of the image
        atl_block     block      ATL code block defining the transform
        ============  =========  ===========

**Example**

    ::

        show eileen happy:
            xalign 1.

        scene bg washington:
            zoom 2.

..
    include here, after #4405, how to change the child then get back to it

ATL Syntax and Statements
-------------------------

ATL statements may be inline, or make up a block within the ATL block in which
it is written. With some exceptions described in the relevant statements, the
statements in an ATL block are executed in order, from top to bottom.

If an ATL statement requires an expression to be evaluated, such evaluation
occurs when the transform is first executed (that is when using a ``show``
statement, or displaying the transform as part of a screen), and not when the
particular ATL statement is executed.

The following are the ATL statements.

.. _atl-properties-statement:

Properties Statement
~~~~~~~~~~~~~~~~~~~~

This statement sets the value of a transform property.

**Syntax**

    ::

        <property_name> <property_value>

**Usage**

    .. table::
        :widths: auto

        ==============  ======  ===========
        Name            Type    Description
        ==============  ======  ===========
        property_name   word    Name of transform property (eg. :tpref:`xalign`, :tpref:`alpha`, ...)
        property_value  Varies  Value of property
        ==============  ======  ===========

    The statement first gives a series (at least one) of property names, each
    followed by the new value to set it to. See :ref:`transform-properties` for a
    list of transform properties, their meaning and the values they take.

**Example**

    ::

        transform rightoid:
            xalign .9

        transform ariana.left:
            xanchor .3 xpos 100


Number Statement
~~~~~~~~~~~~~~~~

This statement pauses the execution of the ATL block for the given duration.
The "pause" keyword is optional.

**Syntax**

    ::

        pause <duration>


**Usage**

    .. table::
        :widths: auto

        ========  =================  ===========
        Name      Type               Description
        ========  =================  ===========
        "pause"   keyword            (Optional) Keyword indicating a pause
        duration  float, int (expr)  Time in seconds to pause
        ========  =================  ===========

**Examples**

    ::

        transform pause_example(duration=0.5):
            xalign 0.0

            # Pause for 2.0 seconds.
            pause 2.0
            xalign 1.0

            # Pause for `duration` seconds.
            pause duration
            xalign 0.5

            # Pause for 3.0 seconds.
            3.0

            repeat


Interpolation Statement
~~~~~~~~~~~~~~~~~~~~~~~

The interpolation statement is the main way of getting smoothly animated
transformations. The values change over time from their starting value to the
given value.

A :ref:`warping function <warpers>` is used to control how the
interpolation progresses over time.

**Syntax**

    Basic form::

        <warper_name> <duration> <atl_property> [<atl_property> ...]

    Using a warper function::

        warp <warper_function> <duration> <atl_property> [<atl_property> ...]

    Block form::

        <warper_name> <duration>:
            <atl_property>
            <atl_property>
            ...

**Usage**

    .. table::
        :widths: auto

        ================  ===============================  ===========
        Name              Type                             Description
        ================  ===============================  ===========
        warper_name       word                             Name of a :ref:`built-in warper <warpers>`
        warper_function   str, function (expr)             Warping function
                                                           with signature ``(t: float) -> float``
        duration          float, int (expr)                Time in seconds for the interpolation
        atl_property      :ref:`atl-properties-statement`  Property to interpolate
        ================  ===============================  ===========

    The interpolation will persist for the given duration, and at least one
    frame.

    When :doc:`transform_properties` are given, the value each is given is the value
    it will be set to at the end of the interpolation statement.

    It is also possible to interpolate a :ref:`transform-expression-atl-statement`,
    which should in this case be an ATL transform containing only a single
    properties statement. The properties from the transform will be processed as if
    they were written directly in this interpolation.

**Examples**

    Basic usage::

        show logo base:
            xalign 0.0 yalign 0.0

            # Take 2.0 seconds to move things to the bottom-left corner.
            linear 2.0 yalign 1.0

    Using warper function::

        show logo base(warper_expr="ease_in"):
            xalign 0.0 yalign 0.0

            # Use the warper in the parameter to move to the right side of the screen.
            warp warper_expr 1.0 xalign 1.0

    Multiple properties::

        show logo base:
            xalign 0.0 yalign 0.0

            # Changes xalign and yalign at the same time.
            linear 2.0 xalign 0.5 yalign 0.5

            # The same thing, using a block.
            linear 2.0:
                xalign 0.5
                yalign 0.5

    Creator-defined warper::

        init python:
            def my_warper(t):
                return t**4.4

            my_warpers = [my_warper]

        transform custom_warper_example:
            xpos 0
            warp my_warper 3 xpos 100
            warp my_warpers[0] 5 xpos 520

**Property Interpolation**

With spline motion (curved path):

    ::

        <atl_property> knot <knot_value> [knot <knot_value> ...]

    .. table::
        :widths: auto

        ====================  =====================  ===========
        Name                  Type                   Description
        ====================  =====================  ===========
        knot_value            (float, float) (expr)  Knot value given as ``(time, value)``, where time is between 0.0 and 1.0
        ====================  =====================  ===========

    The ``time`` in the knot value represents the fraction of the way through the interpolation,
    and ``value`` is the value of the property at that time.

    The starting point is the value of the property at the start of the interpolation,
    the end point is the given value, and the knots are used to control the
    spline. A quadratic curve is used for a single knot, Bezier is used when there
    are two and Catmull-Rom is used for three or more knots. In the former two
    cases, the knot or knots are simply control nodes. For Catmull-Rom, the first
    and last knot are control nodes (often outside the displayed path) and the
    other knots are points the path passes through.

    ::

        show logo base:
            xalign 1.0 yalign 0.0

            # Use a spline motion to move us around the screen.
            linear 2.0 align (0.5, 1.0) knot (0.0, .33) knot (1.0, .66)

With circular motion

    ::

        <atl_property> clockwise
        <atl_property> counterclockwise
        <atl_property> circles <number_of_circles>

    .. table::
        :widths: auto

        ====================  ===========  ===========
        Name                  Type         Description
        ====================  ===========  ===========
        number_of_circles     int (expr)   Number of full rotations for circular motion
        ====================  ===========  ===========

    The start and end locations are compared (which are set by :tpref:`pos`, :tpref:`align`,
    :tpref:`angle` and :tpref:`radius`, ...) and the polar coordinate
    center is determined (which is :tpref:`around`). Ren'Py will then compute the number of
    degrees it will take to go from the start angle to the end angle, in the
    specified direction of rotation. If the circles clause is given, Ren'Py will
    ensure that the appropriate number of circles will be made.

    ::

        show logo base:
            xalign 1.0 yalign 0.0

            # Set the location to circle around.
            anchor (0.5, 0.5)

            # Use circular motion to bring us to spiral out to the top of
            # the screen. Take 2 seconds to do so.
            linear 2.0 yalign 0.0 clockwise circles 3

With a transform expression

    ::

        <transform_expression>

    .. table::
        :widths: auto

        ====================  ======================================  ===========
        Name                  Type                                    Description
        ====================  ======================================  ===========
        transform_expression  :ref:`Transform <transform-statement>`
                              (expr)                                  Transform to interpolate to
        ====================  ======================================  ===========

    In this case, the  be an ATL transform containing only a single
    properties statement. The properties from the transform will be processed as if
    they were written directly in this interpolation.

    ::

        show logo base:
            xalign 1.0 yalign 0.0

            # Move to the location specified in the truecenter transform in 1.0 seconds
            ease 1.0 truecenter

Pass Statement
~~~~~~~~~~~~~~

The ``pass`` statement causes nothing to happen: a no-op.

**Syntax**

    ::

        pass

    This can be used when there's a desire to separate statements, like when
    two sets of choice statements (see below) would otherwise be back-to-back. It
    can also be useful when the syntax requires a block to be created but you need
    it to be empty, for example to make one of the choice blocks not do anything.

Repeat Statement
~~~~~~~~~~~~~~~~

The ``repeat`` statement causes the block containing
it to resume execution from the beginning.

**Syntax**

    Basic form::

        repeat

    With count parameter::

        repeat <count>

**Usage**

    .. table::
        :widths: auto

        ==========  ==========  ===========
        Name        Type        Description
        ==========  ==========  ===========
        count       int (expr)  (Optional) Number of times to execute the block
        ==========  ==========  ===========

    A block ending with ``repeat 2`` will execute
    at most twice in total, and ``repeat 1`` does not repeat.

    The repeat statement must be the last statement in a block

**Example**

    ::

        show logo base:
            xalign 0.0
            linear 1.0 xalign 1.0
            linear 1.0 xalign 0.0
            repeat

Block Statement
~~~~~~~~~~~~~~~

The ``block`` statement simply contains a block of ATL statements.
This can be used to group statements that will repeat.

**Syntax**

    ::

        block:
            <atl_block>


**Example**

    ::

        show logo base:
            alpha 0.0 xalign 0.0 yalign 0.0
            linear 1.0 alpha 1.0

            block:
                linear 1.0 xalign 1.0
                linear 1.0 xalign 0.0
                repeat

Parallel Statement
~~~~~~~~~~~~~~~~~~

The ``parallel`` statement defines a set of ATL blocks to execute in parallel.

**Syntax**

    ::

        parallel:
            <atl_block>

**Usage**

    .. table::
        :widths: auto

        ============  =========  ===========
        Name          Type       Description
        ============  =========  ===========
        "parallel"    keyword    One or more parallel blocks
        atl_block     block      ATL block for this parallel branch
        ============  =========  ===========

    When you use multiple parallel blocks, they all run at the same time.
    The parallel statement finishes when the last block finishes.

    Each parallel block should be independent and modify different
    :doc:`transform_properties`. For example, one block might control horizontal
    movement (:tpref:`xalign`) while another controls vertical movement (:tpref:`yalign`).
    If two blocks try to change the same property at the same time, the behavior is
    unpredictable and should be avoided.

    Parallel statements are greedily grouped into a parallel set when more than
    one parallel block appears consecutively in a block.

**Example**

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

Choice Statement
~~~~~~~~~~~~~~~~

The ``choice`` statement defines one of a set of
potential choices. Ren'Py will pick one of the choices in the set, and
execute the ATL block associated with it, and then continue execution after
the last choice in the choice set.

**Syntax**

    Basic form::

        choice:
            <atl_block>

    With weight::

        choice <weight>:
            <atl_block>

**Usage**

    .. table::
        :widths: auto

        ==========  ============  ===========
        Name        Type          Description
        ==========  ============  ===========
        "choice"    keyword       One or more choices
        weight      float (expr)  (Optional) Weight of this choice, defaults to 1.0
        atl_block   block         ATL block for this choice
        ==========  ============  ===========

    Choice statements are greedily grouped into a choice set when more than one
    choice statement appears consecutively in a block. If the `simple_expression`
    is supplied, it is a floating-point weight given to that block, otherwise 1.0
    is assumed.

    The ``pass`` statement can be useful in order to break several sets of choice
    blocks into several choice statements, or to make an empty choice block.

**Example**

    ::

        image eileen random:
            choice:
                "eileen happy"
            choice:
                "eileen vhappy"
            choice 2.0:
                # More likely to be chosen.
                "eileen concerned"

            pause 1.0
            repeat


.. _animation-atl-statement:

Animation Statement
~~~~~~~~~~~~~~~~~~~

The ``animation`` statement must be the first statement in an ATL block, and
tells Ren'Py that the block uses the animation timebase (``at``) rather
than the normal showing timebase (``st``). For more information,
see :ref:`atl-timebases`.

**Syntax**

    ::

        animation

**Usage**

    The animation timebase starts when an image or screen with the same tag is shown.
    This is generally used to have one image replaced by a second one at the
    same apparent time.

**Example**

    ::

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
    finishes, but will not cause her position to change, as both animations share
    the same animation time, and hence will place her sprite in the same place.
    Without the animation statement, the position would reset when the player
    clicks.

On Statement
~~~~~~~~~~~~

The ``on`` statement defines an event handler.

**Syntax**

    For one event ::

        on <event_name>:
            <atl_block>

    For multiple events ::

        on <event_name>, <event_name>, ...:
            <atl_block>

**Usage**

    .. table::
        :widths: auto

        ============  =======  ===========
        Name          Type     Description
        ============  =======  ===========
        event_name    word     Name of one or more :ref:`events <external-atl-events>` to handle
        atl_block     block    ATL block to execute when event occurs
        ============  =======  ===========

    ``on`` blocks are greedily grouped into a single statement. On statement can
    handle a single event name, or a comma-separated list of event names.

    This statement is used to handle events. When an event is handled, handling of
    any other event ends and handing of the new event immediately starts. When an
    event handler ends without another event occurring, the ``default`` event is
    produced (unless the ``default`` event is already being handled).

    Execution of the on statement will never naturally end. (But it can be ended
    by the time statement, or an enclosing event handler.)

**Example**

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

.. _displayable-atl-statement:


Displayable Statement
~~~~~~~~~~~~~~~~~~~~~

The displayable statement sets or replaces the child :doc:`displayable <displayables>`
of the transform when the statement executes.
You can also optionally add a transition effect when changing from one displayable to another.

**Syntax**

    Basic form::

        <displayable>

    With transition::

        <displayable> with <transition>

**Usage**

    .. table::
        :widths: auto

        ===============  ========================================  ===========
        Name             Type                                      Description
        ===============  ========================================  ===========
        displayable      :doc:`Displayable <displayables>` (expr)  The new child image or visual element to display
        transition       :doc:`Transition <transitions>` (expr)    (Optional) Transition when changing displayables

                                                                   (eg. ``dissolve``, ``fade``)
        ===============  ========================================  ===========

    .. note::
        Not all transitions work in this context. In particular, :ref:`dict-transitions`,
        and :var:`move- <move>` and :var:`ease- <ease>` transitions won't work here.

    **Using transforms as displayables:** If you pass another ATL transform that already
    has a child displayable, your current ATL block will pause and wait for that
    included transform's animation to finish before continuing.

    .. warning::

        If you pass a transform without a child, it will make your transform transparent
        and won't display anything. A child-less ATL transforms might be interpreted as
        a :ref:`transform-expression-atl-statement`, which will yield different results.

        **For beginners**: Always make sure your displayable is something visible, like an
        image filename (``"logo.png"``) or a displayable with content.


**Example**

    ::

        image atl example:
            "logo_base.png"

            pause 1.0

            "logo_bw.png" with Dissolve(0.5, alpha=True)

.. _transform-expression-atl-statement:

Transform Expression Statement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This statement includes another ATL transform as part of the current ATL block.

**Syntax**

    ::

        <transform_expression>

**Usage**

    .. table::
        :widths: auto

        ====================  ======================================  ===========
        Name                  Type                                    Description
        ====================  ======================================  ===========
        transform_expression  :ref:`Transform <transform-statement>`
                              (expr)                                  Transform to interpolate to
        ====================  ======================================  ===========

    This only applies if the ATL transform has **not** been supplied a child (see
    the top of the page for how to do that), otherwise it will be interpreted as a
    :ref:`displayable-atl-statement`. The contents of the provided ATL transform
    are included at the location of this statement.

**Example**

    ::

        transform move_right:
            linear 1.0 xalign 1.0

        image atl example:
            # Display logo_base.png
            "logo_base.png"

            # Run the move_right transform.
            move_right


.. _inline-contains-atl-statement:

Contains Inline Statement
~~~~~~~~~~~~~~~~~~~~~~~~~

This statement sets (or replaces) the child of the current ATL transform to the
value of the expression, making it useful for animation.

**Syntax**

    ::

        contains <displayable>

**Usage**

    .. table::
        :widths: auto

        ===========  =============================================  ===========
        Name         Type                                           Description
        ===========  =============================================  ===========
        displayable  :doc:`Displayable <displayables>`,
                     :ref:`Transform <transform-statement>` (expr)  Child displayable or transform
        ===========  =============================================  ===========

    The :ref:`displayable-atl-statement` is less explicit and bears ambiguity with
    the transform expression statement, but it allows for a
    :doc:`transition <transitions>` to be used for replacing the child. This
    statement can be particularly useful when an ATL transform wishes to contain,
    rather than include, a second ATL transform.

    .. note ::

        Use this statement when you want your ATL transform to contain another ATL
        transform as its child. This is particularly helpful when you need the child
        to be a separate transform object rather than just including its code directly.

        Otherwise, the :ref:`displayable-atl-statement` is a simpler way to set the child
        displayable, and it has the advantage of specifying a :doc:`transition <transitions>`
        that plays when replacing the old child with a new one.

**Example**

    ::

        transform an_animation:
            "1.png"
            pause 2
            "2.png"
            pause 2
            repeat

        image move_an_animation:
            contains an_animation

            # If we didn't use contains, we'd still be looping
            # and would never reach here.
            xalign 0.0
            linear 1.0 yalign 1.0


Contains Block Statement
~~~~~~~~~~~~~~~~~~~~~~~~

The contains block, like its
:ref:`inline counterpart <inline-contains-atl-statement>`, sets the child of the
transform but in a different way.

**Syntax**

    ::

        contains:
            <atl_block>

**Usage**

    One or more contains blocks will be greedily grouped together inside a single
    contains statement, wrapped inside a :func:`Fixed`, and set as the child of the
    transform.

    Each block should define a displayable to use, otherwise an error will occur.
    The contains statement executes instantaneously, without waiting for the
    children to complete.

**Example**

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
~~~~~~~~~~~~~~~~~~

The ``function`` statement allows ATL to use Python code.

**Syntax**

    ::

        function <func>

**Usage**

    .. table::
        :widths: auto

        ==========  ===============  ===========
        Name        Type             Description
        ==========  ===============  ===========
        func        function (expr)  Function to call, with signature
                                    ``(trans: Transform, st: float, at: float) -> float | None``
        ==========  ===============  ===========

    The functions have the same signature as those used with :func:`Transform`:

    * The first argument is a transform object. :doc:`transform_properties` can be
      set as attributes on this object.

    * The second argument is the shown :ref:`timebase <atl-timebases>`,
      the number of seconds since the function began executing.

    * The third argument is the animation timebase, which is the number of
      seconds something with the same tag has been on the screen.

    * If the function returns a number, it will be called again after that number of
      seconds has elapsed. (0 seconds means to call the function as soon as
      possible.) If the function returns None, control will pass to the next ATL
      statement.

    This function should not have side effects other than changing the transform
    object in the first argument, and may be called at any time with any value as
    part of prediction.

    Note that ``function`` is not a transform property, and that it doesn't have the
    exact same behavior as :func:`Transform`\ 's `function` parameter.

**Example**

    ::

        init python:
            def slide_vibrate(trans, st, at, /):
                if st > 1.0:
                    trans.xalign = 1.0
                    trans.yoffset = 0
                    return None
                else:
                    trans.xalign = st
                    trans.yoffset = random.randrange(-10, 11)
                    return 0

        label start:
            show logo base:
                function slide_vibrate
                pause 1.0
                repeat

Time Statement
~~~~~~~~~~~~~~

The ``time`` statement is a control statement.

**Syntax**

    ::

        time <value>

**Usage**

    .. table::
        :widths: auto

        =======  ================  ===========
        Name     Type              Description
        =======  ================  ===========
        value    float/int (expr)  Time in seconds from start of block execution
        =======  ================  ===========

    When the value given in the statement is reached, the next statement begins to execute.
    This transfer of control occurs even if a previous statement is still executing, and
    causes any such prior statement to immediately terminate.

    If the time statement is reached before the given value, the transform pauses and
    waits until the time statement would take control.

    When there are multiple time statements in a block, they must strictly
    increase in order.

**Example**

    ::

        image backgrounds:
            "bg band"
            xoffset 0
            block:
                linear 1 xoffset 10
                linear 1 xoffset 0
                repeat # control would never exit this block

            time 2.0
            xoffset 0
            "bg whitehouse"

            time 4.0
            "bg washington"

Event Statement
~~~~~~~~~~~~~~~

The ``event`` statement causes an event with the given name to be produced.

**Syntax**

    ::

        event <event_name>

**Usage**

    .. table::
        :widths: auto

        ============  =======  ===========
        Name          Type     Description
        ============  =======  ===========
        event_name    word     Name of event to produce
        ============  =======  ===========

    When an event is produced inside a block, the block is checked to see if an
    event handler for the given name exists. If it does, control is transferred
    to the event handler. Otherwise, the event propagates to any containing event
    handler.


.. _external-atl-events:

External events
---------------

The following events are triggered automatically within an ATL transform:

``start``
    A pseudo-event, triggered on entering an ``on`` statement, if no event of
    higher priority has happened.

``show``
    Triggered when the transform is shown using the show or scene statement, and
    no image with the given tag exists.

``replace``
    Triggered when transform is shown using the ``show`` statement, replacing an
    image with the given tag.

``hide``
    Triggered when the transform is hidden using the ``hide`` statement or its
    Python equivalent.

    Note that this isn't triggered when the transform is eliminated via the
    :ref:`scene-statement` or exiting the :ref:`context` it exists in, such as
    when exiting the game menu.

``replaced``
    Triggered when the transform is replaced by another. The image will not
    actually hide until the ATL block finishes.

``hover``, ``idle``, ``selected_hover``, ``selected_idle``, ``insensitive``, ``selected_insensitive``
    Triggered when a button containing this transform, or a button contained by
    this transform, enters the named state.

.. _atl-partial:

ATL curry and partial parameter passing
---------------------------------------

An ATL transform defined using the :ref:`transform-statement` can have its
parameters set at different times. When calling an ATL transform like a
function, the resulting value is still a transform, and the parameters that were
passed a value are treated as though the value is the new default value of the
parameter.

For example::

    transform screamer(child, screamee, wait_time=2, flash_time=.1):
        child
        pause wait_time
        screamee
        pause flash_time
        child

    # doing this doesn't raise an error (it would if it were a Python function)
    define shorter_screamer = screamer(wait_time=1)

    define eileen_excited_screamer = screamer(screamee="eileen excited", flash_time=.2)

    label start:
        show hhannahh happy at screamer(screamee="hhannahh surprised", wait_time=1.5)
        "Here is one way"

        show eileen vhappy at eileen_excited_screamer
        "Here is another"

        show patricia sad at eileen_excited_screamer(screamee="patricia wow")
        "And you can also do this"

Note that the ``shorter_screamer`` transform, just as the ``screamer``
transform, cannot be used directly like ``show eileen at screamer``, since their
``screamee`` parameters do not have a value.

Note also that, like labels and screens, the default values of the parameters of
a transform directly created by the :ref:`transform-statement` will be evaluated
at the time when the transform is *called*, not at the time when it is
*defined*.

However, the transform resulting from calling another transform (such as
``shorter_screamer`` in the example above, or also the transform applied to
patricia) has all the default values of its parameters already evaluated,
whether they come from the evaluation of the default values in the original
transform (such as ``shorter_screamer``\ 's `flash_time` parameter, or
patricia's transform's `wait_time` parameter), or from values passed to it in a
call earlier in the line (such as ``shorter_screamer``\ 's `wait_time`
parameter, or patricia's transform's `screamee` and `flash_time` parameters).

.. _atl-child-param:

Special Child Parameter
-----------------------

If an ATL transform has a parameter named "child" and that parameter receives a
value, **regardless of the kind of parameter or the way it receives a value**
(by a positional argument or by keyword, and even if the parameter is
positional-only or keyword-only, and defaulted or required), then in parallel
the child of the transform is set to the value of the parameter.

..
    address the special case of **kwargs if and when allowed

Note that the default value of the parameter doesn't count, the parameter has to
receive a value from the outside.

Conversely, when that ATL transform is used as a transform, the ``child=``
keyword argument will be passed, and so in addition to setting the child, if a
parameter is there to receive it (excluding positional-only parameters, since it
is passed by keyword), it will have the child's value when the transform
executes.

For example, this enables to swap between the supplied child and another
displayable::

    transform lucy_jump_scare(child):
        # the child is implicitly set as the child of the transform
        pause 5

        # Jump scare
        "lucy mad"
        pause .2

        # Go back to the original child
        child

It can also be used to place the original child inside a ``contains`` block::

    transform marquee(width, height=1.0, duration=2.0, child=None):
        xcenter 0.5
        ycenter 0.5

        crop (0, 0, 0.5, 500)

        contains:
            child
            xanchor 0.0 xpos 1.0
            linear duration xanchor 1.0 xpos 0.0

The `old_widget` and `new_widget` keyword-able parameters (meaning that they
should not be positional-only) have a special use as part of
:ref:`atl-transitions`.


.. _warpers:

Warpers
=======

A warper is a function that can change the amount of time an interpolation
statement considers to have elapsed. They are defined as functions from t to t',
where t and t' are floating point numbers, with t ranging from 0.0 to 1.0 over
the given amount of time. (If the statement has 0 duration, then t is 1.0 when
it runs.) t' should start at 0.0 and end at 1.0, but can be greater or less. The
following warpers are defined by default.

``pause``
    Pause, then jump to the new value. If ``t == 1.0``, ``t' = 1.0``. Otherwise,
    ``t' = 0.0``.

``linear``
    Linear interpolation. ``t' = t``

``ease``
    Start slow, speed up, then slow down. ``t' = .5 - math.cos(math.pi * t) / 2.0``

``easein``
    Start fast, then slow down. ``t' = math.cos((1.0 - t) * math.pi / 2.0)``

``easeout``
    Start slow, then speed up. ``t' = 1.0 - math.cos(t * math.pi / 2.0)``

In addition, most of Robert Penner's easing functions are supported. To
make the names match those above, the functions have been renamed
somewhat. Graphs of these standard functions can be found at
https://easings.net/.

.. include:: inc/easings

These warpers can be accessed in the ``_warper`` read-only module, which contains
the functions listed above. It is useful for things in Ren'Py which take a
time-warping function, such as :func:`Dissolve`, which you can use like::

    with Dissolve(1, time_warp=_warper.easein_quad)

New warpers can be defined using the ``renpy.atl_warper`` decorator, in a ``python
early`` block. It should be placed in a file that is parsed before any file
that uses the warper. This looks like::

    python early hide:

        @renpy.atl_warper
        def linear(t):
            return t


.. _replacing-transforms:

Replacing Transforms
====================

When an ATL transform, a built-in transform or a transform defined using the
:class:`Transform` class is replaced by another transform of these categories,
the properties of the outgoing transform are inherited by the incoming
transform. That inheritance doesn't apply for other kinds of transforms.

.. Explain why this is important

When the :ref:`show statement <show-statement>` has multiple transforms in the
``at`` list, the transforms are matched from last to first, until one list runs
out. For example::

    show eileen happy at a, b, c
    "Dialogue !"
    show eileen happy at d, e

The ``c`` transform will be replaced by ``e``, the ``b`` transform will be
replaced by ``d``, and nothing replaces the ``a`` transform.

At the moment of replacement, if both transforms are of suitable kinds, the
values of the properties of the old transform are copied to the new transform.
If the old transform was animated, the current intermediate value is inherited.
For example::

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

In this example, the image will bounce from left to right and back until the
player clicks. When that happens, the ``xalign`` property of the ``bounce``
transform will be used to initialize the ``xalign`` property of the
``headright`` transform, and so the image will move from where it was when the
player first clicked.

The position properties (:tpref:`xpos`, :tpref:`ypos`, :tpref:`xanchor`,
:tpref:`yanchor`, and properties setting them such as :tpref:`xalign` or
:tpref:`radius`\ / :tpref:`angle`) have a special rule for inheritance : a value
set in the child will override a value set in the parent. That is because a
displayable may have only one position, and a position that is actively set
takes precedence.

Finally, when a ``show`` statement does not include an ``at`` clause, the same
transforms are used, so no inheritance is necessary. To reset all transform
properties, hide and then show the displayable again. To break the animations
applied to a displayable (but keep the position), you can use::

    show eileen happy at some_animation
    "Wow, so this is what antigravity feels like !"

    show eileen:
        pass
    "But I'm happy when it settles down."

.. _atl-timebases:

Timebases
=========

Two timebases exist and are commonly confused:

* ``st`` (shown timebase): begins when this displayable is first shown on the screen.
* ``at`` (animation timebase): begins when an image with the same tag was shown,
  without being hidden.

When the displayable is shown without a tag, ``st`` and ``at`` are the same.

.. note::

    By default, transforms use ``st``.
    Use :ref:`animation <animation-atl-statement>` to switch to ``at``.

Transform Class
===============

One equivalent to to the simplest ATL transforms is the Transform class.

.. class:: Transform(child=None, *, function=None, reset=False, **properties)

    Creates a transform which applies operations such as cropping, rotation,
    scaling or alpha-blending to its child. A transform object has fields
    corresponding to the :doc:`transform properties <transform_properties>`,
    which it applies to its child.

    `child`
        The child the transform applies to.

    `reset`
        If True, the transform will reset properties to their default values
        when it is shown, rather than inheriting those properties from the
        transforms it replaces.

    .. function:: function(trans: Transform, st: float, at: float, /) -> float|None

        If not None, this function will be called when the transform is
        rendered, with three positional arguments:

        * The transform object.
        * The shown timebase, in seconds.
        * The animation timebase, in seconds.

        The function should return a delay, in seconds, after which it will be
        called again, or None to be called again at the start of the next
        interaction.

        This function should not have side effects other than changing the
        Transform object in the first argument, and may be called at any time
        with any value as a part of prediction.

    Additional keyword arguments are values that transform properties are set
    to. These particular transform properties will be set each time the
    transform is drawn, and so may not be changed after the Transform object is
    created. Fields corresponding to other transform properties, however, can be
    set and changed afterwards, either within the function passed as the
    `function` parameter, or immediately before calling the :meth:`update`
    method.

    .. attribute:: hide_request

        This attribute is set to true when the function is called, to indicate
        that the transform is being hidden.

    .. attribute:: hide_response

        If ``hide_request`` is true, this can be set to false to prevent the
        transform from being hidden.

    .. attribute:: original_child

        This is the child Displayable that was set when the transform was created,
        before any calls to set_child. This may be None if no child was during creation.

    .. method:: set_child(child)

        Call this method with a new `child` to change the child of this
        transform.

    .. method:: update()

        This should be called when a transform property field is updated outside
        of the function passed as the `function` argument, to ensure that the
        change takes effect.

Applying transforms to displayables in Python
=============================================

There are several ways to apply transform ``t`` to displayable ``d`` in Python:

#. The most universal and most recommended way is ``At(d, t)`` (see below). It
   works with all transforms.

#. ``d(child=t)`` works with all :ref:`ATL transforms <atl>`.

#. ``t(d)`` works with all :ref:`Python transforms <transforms-python>`, as well
   as with ATL transforms that don't have any positional parameters.

.. include:: inc/disp_at

.. note::
    The resulting value may not be able to be displayed, if there remains
    parameters of the transform that have not been given a value, as can be the
    case with transforms defined using the :ref:`transform-statement`.

.. note::
    The resulting value may still be a transform that can be applied to yet
    another displayable (overriding its previous child) ; that's the case with
    ATL transforms which are still usable as transforms even when having their
    child set.

.. _transforms-python:

Callables as transforms
=======================

Finally, simple Python callables can be used as transforms. These callables
should take a single :doc:`displayable <displayables>` as an argument, and
return a new Displayable. For example::

    init python:

        # this transform uses the right and left transforms
        def right_or_left(d):
            if switch:
                return At(d, right)
            else:
                return At(d, left)

That means that certain builtins which take a displayable and return a displayable,
such as :func:`Flatten`, are also transforms and can be used as such.
