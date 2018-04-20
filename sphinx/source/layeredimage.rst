.. _layeredimage:

Layered Images
--------------

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

To make defining layered images easier, Ren'Py has the layeredimage statement,
which introduces a domain-specific language that lets you define a layer
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

First off, the layeredimage statement introduces a layered image
with the name of the sprite. This statement is part of the Ren'Py
script language, and runs at init time.

The block of a layered image can contain always, group, and if
statements. A group statement can take attributes. The always and if
statements must be supplied displayables, while the attribute statement
can optionally be supplied one. All statements can be supplied properties.

The always statement declares a layer that is always displayed, like the
background of a sprite.

The group statement introduces a group of attributes, where only one of
the attributes can be displayed at a time. So this layered image can only
have one outfit, and one post for each of the eyes, eyebrows, and mouth.
Properties given to the group are passed on to the attributes, and a group
can automatically declare attributes.

The attribute statement introduces a layer that is displayed if an attribute
is supplied to the image. For example, "augustina_outfit_dress" is only
displayed if if the "dress" attribute is supplied. If given the default
keyword, the attribute is displayed if no conflicting attributes are
provided; in this example, "augustina_eyes_open" is displayed unless the
unless the "wink" attribute is given.

Finally, the if statement adds a layer that selects between displayables
using a python statement. This is evaluated constantly, and the first
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
while the last is in front -  in this example, the glasses will be on top of
the other layers.

Groups and attributes may appear more than once in a layered image, with
all of the layers with an attribute being displayed.


Using an Layered Image
----------------------

To use this (but not other) layered images, the evil variable must be given
a value, for example with::

    default evil = True

Then the layered image can be shown like any other image. Almost certainly,
one of the outfits should be given - while Ren'Py doesn't enforce this,
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
attributes - it's possible to add any properties to the first line and
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
attributes in a group. This is done by giving a group the auto keyword,
which causes the group to search for defined
images that would match the pattern, then define the attribute if it does
not already exist.

As with attribute, properties can be placed on the first line of the
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

There's no way to omit the displayables from the always or if statements,
so this is as short as it gets - but with a few more images with proper
names, it's possible to use this to define thousands or even millions
of combinations of layers.
