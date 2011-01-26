# Defines a SnowBlossom object, which uses particle motion to show falling
# cherry blossom petals.
image snowblossom = SnowBlossom(anim.Filmstrip("sakura.png", (20, 20), (2, 1), .15), fast=True)

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

    scene black

    show expression (StarField().sm) as starfield
    show eileen happy at center
    
    "Space, the final frontier."

    return
