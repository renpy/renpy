# This code supports particle animation.

import renpy
import random

class Particles(renpy.display.core.Displayable):

    nosave = [ 'particles' ]

    def after_setstate(self):
        self.particles = None

    def __init__(self, factory, style='default', **properties):
        super(Particles, self).__init__(style=style, **properties)

        self.factory = factory
        self.particles = None

    def render(self, w, h, st):

        particles = self.particles
        if particles is None:
            particles = [ ]

        newparts = self.factory.create(self.particles, st)

        if newparts is not None:
            particles.extend(newparts)

        rv = renpy.display.render.Render(w, h)

        liveparts = [ ]

        for p in particles:

            new = p.update(st)
            if new is None:
                continue

            liveparts.append(p)

            xpos, ypos, t, widget = new            
            widget = renpy.display.im.image(widget, loose=True)
            rend = renpy.display.render.render(widget, w, h, t)
            widget.place(rv, 0, 0, w, h, rend, xpos=xpos, ypos=ypos)

        self.particles = liveparts
        renpy.display.render.redraw(self, 0)

        return rv

    # TODO: predict
    
class SnowBlossomFactory(object):

    def __init__(self, image, count, xspeed, yspeed, border):
        self.image = image
        self.count = count 
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.border = border        

    def create(self, particles, st):

        if particles is None or len(particles) < self.count:

            def ranged(n):
                if isinstance(n, tuple):
                    return random.uniform(n[0], n[1])
                else:
                    return n

            return [ SnowBlossomParticle(self.image,
                                         ranged(self.xspeed),
                                         ranged(self.yspeed),
                                         self.border,
                                         st,
                                         random.uniform(0, 100)) ]
class SnowBlossomParticle(object):

    def __init__(self, image, xspeed, yspeed, border, start, offset):

        # safety.
        if yspeed == 0:
            yspeed = 1

        self.image = image
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.border = border
        self.start = start
        self.offset = offset

        sh = renpy.config.screen_height
        sw = renpy.config.screen_width

        if self.yspeed > 0:
            self.ystart = -border
        else:
            self.ystart = sh + border
        

        travel_time = (2.0 * border + sh) / abs(yspeed)

        xdist = xspeed * travel_time

        x0 = min(-xdist, 0)
        x1 = max(sw + xdist, sw)

        self.xstart = random.uniform(x0, x1)

    def update(self, st):
        to = st - self.start

        xpos = self.xstart + to * self.xspeed
        ypos = self.ystart + to * self.yspeed

        if ypos > renpy.config.screen_height + self.border:
            return None

        if ypos < -self.border:
            return None

        return int(xpos), int(ypos), to + self.offset, self.image

def SnowBlossom(image, count=10, border=50, xspeed=(20, 50), yspeed=(100, 250)):
    return Particles(SnowBlossomFactory(image=image,
                                        count=count,
                                        border=border,
                                        xspeed=xspeed,
                                        yspeed=yspeed))
                                       
        
