# Defines a SnowBlossom object, which uses particle motion to show falling
# cherry blossom petals.
image sakura filmstrip = anim.Filmstrip("sakura.png", (20, 20), (2, 1), .15)
image snowblossom = SnowBlossom("sakura filmstrip")

init python:

    class StarField(object):

        def __init__(self):

            self.sm = SpriteManager(update=self.update)

            # A list of (sprite, starting-x, speed).
            self.stars = [ ]

            # Note: We store the displayable in a variable here.
            # That's important - it means that all of the stars at
            # a given speed have the same displayable. We render that
            # displayable once, and cache the result.

            d = Transform("star.png", zoom=.02)
            for i in range(0, 50):
                self.add(d, 20)

            d = Transform("star.png", zoom=.025)
            for i in range(0, 25):
                self.add(d, 80)

            d = Transform("star.png", zoom=.05)
            for i in range(0, 25):
                self.add(d, 160)

            d = Transform("star.png", zoom=.075)
            for i in range(0, 25):
                self.add(d, 320)

            d = Transform("star.png", zoom=.1)
            for i in range(0, 25):
                self.add(d, 640)

            d = Transform("star.png", zoom=.125)
            for i in range(0, 25):
                self.add(d, 1280)

        def add(self, d, speed):
            s = self.sm.create(d)

            start = renpy.random.randint(0, 840)
            s.y = renpy.random.randint(0, 600)

            self.stars.append((s, start, speed))

        def update(self, st):
            for s, start, speed in self.stars:
                s.x = (start + speed * st) % 840 - 20

            return 0


label tutorial_sprite:

    e "Ren'Py supports a sprite system, which allows many similar objects to be shown on the screen at once."

    scene black
    show expression (StarField().sm) as starfield
    show eileen happy
    with wipeleft

    e "The background behind me consists of one hundred and seventy-five stars, being moved at several different speeds, to give a starflight effect."

    e "The OpenGL system should be able to animate this smoothly, but you might see a bit of stuttering if your computer is using software."

    e "You'll need to decide which older systems to support."

    scene bg washington
    show eileen happy
    with wipeleft

    e "The sprite manager requires you to write a python function to move the sprites around."

    show snowblossom

    e "In many cases, all you need is something moving around the screen - like cherry blossoms, or snow."

    e "That's what the snowblossom function gives you - a simple way to have things falling from the top of the screen."

    hide snowblossom
    with dissolve

    e "And that's it for sprites."


    return
