.. _layered-images:

Layered Images
==============

When a sprite-set gets to a certain level of complexity, defining every
possible combination may become unwieldy. For example, a sprite with
4 outfits, 4 hairstyles, and 6 emotions already has 96 possible
combinations. Creating static images for each possible combination would
consume a lot of disk space and programmer time.

To address this use case, Ren'Py has a way of defining an image consisting
of multiple layers. (For the purpose of this, consider layers to be the layers
in a paint program like Photoshop or the GIMP, and not the layers used elsewhere
in Ren'Py.) Layers can be shown unconditionally, or can be selected
by attributes provided to the image or conditions that are evaluated at
runtime.

To make defining layered images easier, Ren'Py has the ``layeredimage`` statement,
which introduces a domain-specific language that lets you define a layered
image. There's also the :func:`LayeredImage` object, which isn't an image
but can be assigned to an image statement and used like one.


Defining Layered Images
-----------------------

The layered image domain-specific language consists of only a few statements,
one of which is also a script language statement to introduce the image,
followed by statements to introduce the layers and groups of layers.

To introduce the language, here's a layered image that uses the
available features, with things that could be implied instead
explicitly given. ::

    layeredimage augustina:

        always:
            "augustina_base"

        group outfit:

            attribute dress:
                "augustina_outfit_dress"

            attribute jeans:
                "augustina_outfit_jeans"

        group eyes:

            attribute open default:
                "augustina_eyes_open"
                default True

            attribute wink:
                "augustina_eyes_wink"

        group eyebrows:

            attribute normal default:
                "augustina_eyebrows_normal"

            attribute oneup:
                "augustina_eyebrows_oneup"

        group mouth:

            pos (100, 100)

            attribute smile default:
                "augustina_mouth_smile"

            attribute happy:
                "augustina_mouth_happy"

        if evil:
            "augustina_glasses_evil"
        else:
            "augustina_glasses"


That is a large amount of script, but it's very regular, and below
we'll show how to simplify it.

First off, the ``layeredimage`` statement introduces a layered image
with the name of the sprite. This statement is part of the Ren'Py
script language, and runs at init time.

The block of a layered image can contain always, group, and if
statements. A ``group`` statement can take attributes. The ``always`` and ``if``
statements must be supplied displayables, while the attribute statement
can optionally be supplied one. All statements can be supplied properties.

The ``always`` statement declares a layer that is always displayed, like the
background of a sprite.

The ``group`` statement introduces a group of attributes, where only one of
the attributes can be displayed at a time. So this layered image can only
have one outfit, and one post for each of the eyes, eyebrows, and mouth.
Properties given to the group are passed on to the attributes, and a group
can automatically declare attributes.

The ``attribute`` statement introduces a layer that is displayed if an attribute
is supplied to the image. For example, "augustina_outfit_dress" is only
displayed if if the "dress" attribute is supplied. If given the ``default``
keyword, the attribute is displayed if no conflicting attributes are
provided; in this example, "augustina_eyes_open" is displayed unless the
unless the "wink" attribute is given.

Finally, the ``if`` statement adds a layer that selects between displayables
using a Python statement. This is evaluated constantly, and the first
condition that evaluates to true is the one that's displayed.

Properties consist of a property name and a simple expression, and
can be given to each layer. Some properties change the functioning of
a statement. If one or more :ref:`transform properties <transform-properties>` are
given, a :func:`Transform` is created that wraps the display. The at property
can be given a transform or list of transforms that also wrap the displayable.
For example, the pos property here creates a transform that moves the top-left
corner of each mouth image.

The resulting image is the size of the bounding box of all the layers, so
it probably makes sense to have one layer the full size of the image, which
no other layer goes outside of. The first layer is in the back of the image,
while the last is in front – in this example, the glasses will be on top of
the other layers.

Groups and attributes may appear more than once in a layered image, with
all of the layers with an attribute being displayed.


Using an Layered Image
----------------------

To use this (but not other) layered images, the evil variable must be given
a value, for example with::

    default evil = True

Then the layered image can be shown like any other image. Almost certainly,
one of the outfits should be given – while Ren'Py doesn't enforce this,
this image requires one::

    show augustina jeans

While a sprite is being shown, additional attributes will be added to
those already showing provided they do not conflict. (This is the case
in all of Ren'Py when an image being shown does not match one that's
already defined, something that is never the case with a layered image.) So, ::

    show augustina wink

Will activate the layers associated with the wink attribute. We could stop
winking with::

    show augustina open

As the open eyes conflict with the winking eyes. Or we could simply remove
the wink attribute using::

    show augustina -wink

Which would display the layer with the open attribute, as it is the
default.

Layered images can also be used with the scene statement.



Automatic Attributes
--------------------

There's a lot of repetition our first example, when it comes to the
attribute names and the displayables that define the attribute. To
save you from having to do a lot of redundant typing, Ren'Py can
automatically determine a displayable name from the image name, group name,
and attribute name. This is done by combining the names with underscores.

When doing this, you can also take advantage of another feature of
attributes – it's possible to add any properties to the first line and
omit the block entirely.

Here's our example of having done that::

    layeredimage augustina:

        always:
            "augustina_base"

        group outfit:
            attribute dress
            attribute jeans

        group eyes:
            attribute open default
            attribute wink

        group eyebrows:
            attribute normal default
            attribute oneup

        group mouth:
            pos (100, 100)
            attribute smile default
            attribute happy

        if evil:
            "augustina_glasses_evil"
        else:
            "augustina_glasses"

This example is equivalent to the first one (as we gave the same names for
the displayables in the first example). For example, the dress attribute in
the outfit group uses "augustina_outfit_dress" for the displayable, a
displayable that references the image with  that name.

It's possible to go even further than this, by automatically defining the
attributes in a group. This is done by giving a group the `auto` keyword,
which causes the group to search for defined
images that would match the pattern, then define the attribute if it does
not already exist.

As with ``attribute``, properties can be placed on the first line of the
group and the block omitted. The displayable and properties of the
always statement can be put on the first line the same way.

Here's an example of the final form::

    layeredimage augustina:

        always "augustina_base"

        group outfit auto

        group eyes auto:
            attribute open default

        group eyebrows auto:
            attribute normal default

        group mouth auto:
            pos (100, 100)
            attribute smile default

        if evil:
            "augustina_glasses_evil"
        else:
            "augustina_glasses"


This is about as simply as we can define that image, without changing
what we define. The savings with auto-definition increases as we have
more attributes per group. We could also save lines if we didn't need
default attributes. In that case, all of the groups could be written on
single lines.

There's no way to omit the displayables from the ``always`` or ``if`` statements,
so this is as short as it gets – but with a few more images with proper
names, it's possible to use this to define thousands or even millions
of combinations of layers.


Statement Reference
-------------------

Note that with the conditions in the ``if`` statement, all expressions are
evaluated at init time, when the layered image is first defined.

Layeredimage
^^^^^^^^^^^^

The ``layeredimage`` statement is a statement in the Ren'Py script language
that introduces a layered image. It starts with an image name, and takes
a block that can contain attribute, group, and if statements.

Layeredimage takes the following properties:

`image_format`
    When a given image is a string, and this is supplied, the image name
    is interpolated into `image_format` to make an image file. For example,
    "sprites/eileen/{image}.png" will look for the image in a subdirectory
    of sprites. (This is not used by auto groups, which look for images and
    not image files.)

`format_function`
    A function that is used instead of `layeredimage.format_function` to format
    the image information into a displayable.

:ref:`transform properties <transform-properties>`
    If present, these are used to construct a :func:`Transform` that is applied
    to the displayable.

`at`
    A transform or list of transforms that are applied to the layered image.

Attribute
^^^^^^^^^

The ``attribute`` statement adds a layer that is displayed when the given
attribute is used to display the image. The same attribute can be used with
multiple layers, with all layers corresponding to the attribute being shown
(the `if_also` and `if_not` properties can change this).

An attribute takes an attribute name. It can also take two keywords.
The ``default`` keyword indicates that the attribute should be present
by default if no attribute in its group conflicts. The ``null`` keyword
prevents Ren'Py from automatically searching for a displayable corresponding
to this attribute, which is useful to have an attribute that is intended solely
for use with `if_all`, `if_any`, or `if_not`.

If the displayable is not present, it will be computed from the name of the
layer, group, group variant, and attribute, by replacing all spaces with
underscores and using underscores to combine everything together. So
if we have an image named "augustina", the group "eyes" and the name "closed",
the image "augustina_eyes_closed" will be used. (The layered image's
format function is used to do this, defaulting to :func:`layeredimage.format_function`.)

If an attribute is not inside a group, it's placed in a group with the
same name, but that group is not used to compute the displayable name.
(So it would look for "image_attribute", not "image_attribute_attribute").

The attribute statement takes the following properties:

`if_all`
    A string or list of strings giving the names of attributes. If this is
    present, this layer is only displayed if all of the named attributes
    are present.

`if_any`
    A string or list of strings giving the names of attributes. If this is
    present, this layer is only displayed if any of the named attributes
    are present.

`if_not`
    A string or list of strings giving the names of attributes. If this is
    present, this layer is only displayed if none of the named attributes are
    present.


:ref:`transform properties <transform-properties>`
    If present, these are used to construct a transform that is applied
    to the layer.

`at`
    A transform or list of transforms that are applied to the layer.

Group
^^^^^

The ``group`` statement groups together alternative layers. When an attribute is
inside a group, it is an error to include any of the other attributes in
that group. (But it's fine to include the same attribute twice. The ``multiple``
keyword removes this restriction.)

The ``group`` statement takes a name. The name isn't used for very much, but is
used to generate the default names of attributes inside the group.

The name may be followed by the ``auto`` keyword. If it's present, after any
attributes in the group have been declared, Ren'Py will scan its list of images
for those that match the group's pattern (see below). Any images that are found
that do not correspond to declared attributes are then added to the group as if
declared with the attribute statement.

This can be followed by the ``multiple`` keyword. If present, more than one
member of the group can be selected at the same time. This is useful to have
a group auto-define multiple attributes that are not exclusive. This conflicts
with the default keyword being given to one of the attributes.

Properties can then be declared on the first line of the group, and it can
take a block that contains properties and attributes.

There are two properties that are specific to groups.

`variant`
    If given, this should be a string. If present, it adds a variant element
    that becomes part of automatically-generated image names and the pattern
    used to search for automatically-defined attributes.

`prefix`
    If given, this is a prefix that is concatenated using an underscore with
    the manually or automatically defined attribute names. So if prefix is
    "leftarm", and the attribute name "hip" is encountered, the attribute
    "leftarm_hip" is defined instead.

The group statement also takes the same properties ``attribute`` does.  Properties
supplied to the group are passed to the attributes inside the group, unless
overridden by the same property of the attribute itself.

**Pattern.** The image pattern used consists of:

* The name of the image, with spaces replaced with underscores.
* The name of the group.
* The name of the variant.
* The name of the attribute.

all combined with underscores. For example, if we have a layered image with
the name "augustina work", and the group "eyes", this will match images
that match the pattern augustina_work_eyes\_\ `attribute`. With a `variant`
of `blue`, it would match the pattern augustina_work_eyes_blue\_\ `attribute`.


Always
^^^^^^

The ``always`` statement declares a layer that is always shown. It
must be supplied a displayable, and can take properties also. Both can
be placed on the same line or inside a block.

The always statement takes the following properties:

`if_all`
    A string or list of strings giving the names of attributes. If this is
    present, this layer is only displayed if all of the named attributes
    are present.

`if_any`
    A string or list of strings giving the names of attributes. If this is
    present, this layer is only displayed if any of the named attributes
    are present.

`if_not`
    A string or list of strings giving the names of attributes. If this is
    present, this layer is only displayed if none of the named attributes are
    present.

:ref:`transform properties <transform-properties>`
    If present, these are used to construct a transform that is applied
    to the layer.

`at`
    A transform or list of transforms that are applied to the layer.

If
^^

The ``if`` statement (or more fully the if-elif-else) statement allows you
to supply one or more conditions that are evaluated at runtime. Each
condition is associated with a layer, with the first true condition
being the one that is shown. If no condition is true, the ``else`` layer
is shown if present.

A more complete example of an ``if`` statement might look like::

    if glasses == "evil":
        "augustina_glasses_evil"
    elif glasses == "normal":
        "augustina_glasses"
    else:
        "augustina_nose_mark"

Each layer must have a displayable given. It can also be given these properties:

`if_all`
    A string or list of strings giving the names of attributes. If this is
    present, this condition is only considered if all of the named attributes
    are present.

`if_any`
    A string or list of strings giving the names of attributes. If this is
    present, this condition is only considered if any of the named attributes
    are present.

`if_not`
    A string or list of strings giving the names of attributes. If this is
    present, this condition is only considered if none of the named attributes are
    present.


:ref:`transform properties <transform-properties>`
    If present, these are used to construct a transform that is applied
    to the layer.

`at`
    A transform or list of transforms that are applied to the layer.

The ``if`` statement is transformed to a :func:`ConditionSwitch` when the
``layeredimage`` statement runs.

.. var: layeredimage.predict_all = None

    Sets the value of `predict_all` for the ConditionSwitches produced
    by layered image if statements.

When ``predict_all`` is not true, changing the condition of the if statement
should be avoided while the layered image is shown or about to be shown,
as it would lead to an unpredicted image load. It's intended for use for
character customization options that change rarely.

Poses
-----

It's possible to have a character that has sprites in multiple poses,
where everything – or at least everything of interest – is different.
For example, if a character has standing and sitting poses, all the image
parts will be in different places.

In that case, it makes sense to define multiple layered images for the same
image tag. The ``layeredimage`` statement makes this possible by allowing
you to include attributes as part of the image name. So we can have::

    layeredimage augustina sitting:
        ...

    layeredimage augustina standing:
        ...

This is especially useful when using a layered image to compose a side
image, where the side images of different characters will have nothing
to do with each other. ::

    layeredimage side eileen:
        ...

    layeredimage side lucy:
        ...


Advice
------

**Use underscores in image names.**
By default, Ren'Py's layered images use underscores to separate sections
of image names. It might be tempting to use images with spaces between
sections, but that could lead to problems later on.

Ren'Py has a rule that if you show an image with the exact name as one
that's being shown, it's shown instead. This can bypass the layered image
you defined and show the layer directly, which can lead to weird problems
like a pair of eyes floating in space.

By having each layer have a different tag from the main image, this is no
longer a problem.

**Cropping layers isn't necessary.**
Ren'Py optimizes images by cropping them to the bounding box of the
non-transparent pixels before loading them into RAM. As a result, assuming
the images are being predicted properly, it generally won't improve
performance or image size much to crop the images yourself.


Python
------

Of course, the ``layeredimage`` statements have a Python equivalents. The
group statement does not – the group is supplied to ``attribute``, and the
auto functionality can be implemented using :func:`renpy.list_images`.

.. include:: inc/li

:func:`layeredimage.format_function` is a function that is used to format attributes
and displayables into image files. It's supplied so you can see how it's
documented, and the arguments it takes if you want to supply your own
`format_function` to replace it.

.. include:: inc/li_ff

Proxying Layered Images
-----------------------

Sometimes, it's necessary to proxy a layered image, to use the same
layered image in multiple places. One reason for this would be to have
the same sprite at multiple sizes, while another would be to use it as
a side image.

The :func:`LayeredImageProxy` object does this, taking one layered image and
duplicating it somewhere else.

For example::

    image dupe = LayeredImageProxy("augustina")

creates a duplicate of the image that can be displayed independently. This
also takes a transform argument that makes it useful to position a side
image, like this::

    image side augustina = LayeredImageProxy("augustina", Transform(crop=(0, 0, 362, 362), xoffset=-80))

.. include:: inc/li_proxy
