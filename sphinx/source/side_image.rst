.. _side-images:

Side Images
===========

Many visual novels include a picture of the character that is speaking as
part of their interface. Ren'Py calls this image a side image, and has
support for automatically selecting and displaying a side image as part
of the dialogue.

The side image support assumes that a :func:`Character` is declared with
a linked image tag::

    define e = Character("Eileen", image="eileen")

When a character with a linked image tag speaks, Ren'Py creates a pool of
image attributes. The linked image tag is added to this pool, as are the
current image attributes that are associated with that tag.

To determine the side image associated with a tag, Ren'Py tries to find
an image with the tag "side", and the largest number of attributes from
the pool. If no image can be found, or more than one image has the same
number of attributes, an :class:`Null` is shown instead.

For example, say we have the following script::

    define e = Character("Eileen", image="eileen")

    image eileen happy = "eileen_happy.png"
    image eileen concerned = "eileen_concerned.png"

    image side eileen happy = "side_eileen_happy.png"
    image side eileen = "side_eileen.png"

    label start:

        show eileen happy

        e "Let's call this line Point A."

        e concerned "And this one is point B."

At point A, the character ``e`` is speaking, which is linked to the image
tag "eileen". The "eileen happy" image is showing, so the pool of attributes
is "eileen" and "happy". We look for an image with the "side" tag, and as
many of those attributes as possible - and we match "side eileen happy",
which is the side image Ren'Py will display.

At point B, the "eileen concerned" image is showing. The pool of attributes
is now "eileen" and "concerned". The only matching image is "side eileen",
so that's what Ren'Py selects. If there was a "side concerned" image, there
would be ambiguity, and Ren'Py wouldn't display an image.


Invisible Characters
--------------------

Another use of the side image is to show an image of the player character,
when that character has dialogue. The way to do this is to link an image to
the character, and then use the say with attributes construct to select
the side image to show.

For example::

    define p = Character("Player", image="player")

    image side player happy = "side_player_happy.png"
    image side player concerned = "side_player_concerned.png"

    label start:

        p happy "This is shown with the 'side player happy' image."

        p "This is also shown with 'side player happy'."

        p concerned "This is shown with 'side player concerned'."

Variations
----------

There are two variants of side image support that can be selected - either alone
or together - using config variables:

.. var:: config.side_image_tag = None

    If this is given, then the side image will track the given image tag,
    rather than the image associated with currently speaking character. For example,

    ::

        define e = Character("Eileen", image="eileen")

        init python:
             config.side_image_tag = "eileen"

    Will make the side image track the "eileen" image tag, which is associated
    with the ``e`` character.

.. var:: config.side_image_only_not_showing = False

    When set to true, the side image will only show if an image with that tag
    is not already being shown on the screen.


Leaving Room / Customization
----------------------------

By default, the entire width of the screen is taken up by the text. If one
tries to display a side image, it will be displayed on top of the text. To
fix this, one should include margin or padding on the appropriate side of
the text window, using code like::

    style window:
        left_padding 150

The position of the side image can be changed by customizing the ``say``
or ``nvl`` screens. Both include the line::

    add SideImage() xalign 0.0 yalign 1.0

By changing the xalign and yalign properties, you can control the positioning
of the side image on the screen.

Finally, the :func:`SideImage` function returns, as a displayable, the
current side image. This can be used as part of more advanced screen
customization.

