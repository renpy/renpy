.. _sprites:

Sprites
=======

To support the display of a large number of images at once, Ren'Py supports
a sprite system. This system allows one to create sprites, where each sprite
contains a displayable. The sprites can then have their location on the
screen and vertical ordering changed.

If one ignores performance, the sprite system is conceptually similar
to a :func:`Fixed` wrapping :func:`Transform`\s. Sprites are much
faster than transforms, but also less flexible. The big performance
improvement of sprites is that each Displayable is rendered only once
per frame, even if that Displayable is used by many sprites. The limitation
is that Sprites only allow one to change their xoffset and yoffset, rather
than the many properties that a Transform has.

To use the sprite system, create a SpriteManager object, and then call
its create method to create new particles. As necessary, update the
xoffset, yoffset, and zorder fields of each sprite to move it around
the screen. By supplying `update` and `event` arguments to
SpriteManager, you can have the sprites change over time, and react to
user input.

Sprite Classes
--------------

.. include:: inc/sprites
.. include:: inc/sprites_extra

Sprite Examples
---------------

The SnowBlossom class is an easy-to use way of placing falling things
on the screen.

::

    image snow = SnowBlossom("snow.png", count=100)


This example shows how a SpriteManager can be used to create complex
behaviors. In this case, it shows 400 particles, and has them avoid
the mouse.

::

    init python:
        import math

        def repulsor_update(st):

            # If we don't know where the mouse is, give up.
            if repulsor_pos is None:
                return .01

            px, py = repulsor_pos

            # For each sprite...
            for i in repulsor_sprites:

                # Compute the vector between it and the mouse.
                vx = i.x - px
                vy = i.y - py

                # Get the vector length, normalize the vector.
                vl = math.hypot(vx, vy)
                if vl >= 150:
                    continue

                # Compute the distance to move.
                distance = 3.0 * (150 - vl) / 150

                # Move
                i.x += distance * vx / vl
                i.y += distance * vy / vl

                # Ensure we stay on the screen.
                if i.x < 2:
                    i.x = 2

                if i.x > repulsor.width - 2:
                    i.x = repulsor.width - 2

                if i.y < 2:
                    i.y = 2

                if i.y > repulsor.height - 2:
                    i.y = repulsor.height - 2

            return .01

        # On an event, record the mouse position.
        def repulsor_event(ev, x, y, st):
            store.repulsor_pos = (x, y)


    label repulsor_demo:

        python:
            # Create a sprite manager.
            repulsor = SpriteManager(update=repulsor_update, event=repulsor_event)
            repulsor_sprites = [ ]
            repulsor_pos = None

            # Ensure we only have one smile displayable.
            smile = Image("smile.png")

            # Add 400 sprites.
            for i in range(400):
                repulsor_sprites.append(repulsor.create(smile))

            # Position the 400 sprites.
            for i in repulsor_sprites:
                i.x = renpy.random.randint(2, 798)
                i.y = renpy.random.randint(2, 598)

            del smile
            del i

        # Add the repulsor to the screen.
        show expression repulsor as repulsor

        "..."

        hide repulsor

        # Clean up.
        python:
            del repulsor
            del repulsor_sprites
            del repulsor_pos
