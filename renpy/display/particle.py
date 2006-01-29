# This code supports particle animation.

import renpy
import random

class Particles(renpy.display.core.Displayable):
    """
    Supports particle motion.
    """

    nosave = [ 'particles' ]

    def after_setstate(self):
        self.particles = None

    def __init__(self, factory, style='default', **properties):
        """
        @param factory: A factory object.
        """

        super(Particles, self).__init__(style=style, **properties)

        self.factory = factory
        self.particles = None

    def render(self, w, h, st, at):

        particles = self.particles
        if particles is None:
            particles = [ ]

        newparts = self.factory.create(self.particles, at)

        if newparts is not None:
            particles.extend(newparts)

        rv = renpy.display.render.Render(w, h)

        liveparts = [ ]

        for p in particles:

            new = p.update(at)
            if new is None:
                continue

            liveparts.append(p)

            xpos, ypos, t, widget = new            
            widget = renpy.display.im.image(widget, loose=True)
            rend = renpy.display.render.render(widget, w, h, t, t)
            widget.place(rv, 0, 0, w, h, rend, xpos=xpos, ypos=ypos)

        self.particles = liveparts
        renpy.display.render.redraw(self, 0)

        return rv

    def predict(self, callback):

        try:
            pl = self.factory.predict()
            for i in pl:
                i = renpy.display.im.image(i, loose=True)
                i.predict(callback)
        except:
            pass
    
class SnowBlossomFactory(object):

    def __setstate__(self, state):
        self.start = 0
        vars(self).update(state)
        self.init()

    def __init__(self, image, count, xspeed, yspeed, border, start):
        self.image = image
        self.count = count 
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.border = border        
        self.start = start
        self.init()

    def init(self):
        self.starts = [ random.uniform(0, self.start) for i in range(0, self.count) ]
        self.starts.append(self.start)
        self.starts.sort()
    
    def create(self, particles, st):

        if particles is None or len(particles) < self.count:

            # Check to see if we have a particle ready to start. If not,
            # don't start it.
            if particles and st < self.starts[len(particles)]:
                return None

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

    def predict(self):
        return [ self.image ]
    

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
    
def SnowBlossom(image, count=10, border=50, xspeed=(20, 50), yspeed=(100, 200), start=0):
    """
    This implements the snowblossom effect, which is a simple linear
    motion up or down the screen. This effect can be used for falling
    cherry blossoms, falling snow, and rising bubbles, along with
    other things.

    @param image: The image that is to be used for the particles. This can
    actually be any displayable, so it's okay to use an Animation as
    an argument to this parameter.

    @param count: The number of particles to maintain at any given
    time. (Realize thant not all of the particles may be on the screen
    at once.)

    @param border: How many pixels off the screen to maintain a particle
    for. This is used to ensure that a particle is not displayed on the
    screen when it is created, and that it is completely off the screen
    when it is destroyed.

    @param xspeed: The horizontal speed of the particles, in pixels per second.
    This may be a single integer, or it may be a tuple of two integers. In the latter
    case, the two numbers are used as a range from which to pick the horizontal
    speed for each particle. The numbers can be positive or negative, as long
    as the second is larger then the first.

    @param yspeed: The vertical speed of the particles, in pixels per
    second.  This may be a single integer, but it should almost
    certainly be a pair of integers which are used as a range from
    which to pick the vertical speed of each particle. (Using a single
    number will lead to every particle being used in a wave... not
    what is wanted.) The second number in the tuple should be larger then
    the first. The numbers can be positive or negative, but you shouldn't
    mix the two in the same tuple. If positive numbers are given, the
    particles fall from the top of the screen to the bottom, as with
    snow or cherry blossoms. If negative numbers are given, the particles
    rise from the bottom of the screen to the top, as with bubbles.    

    @param start: This is the number of seconds it will take to start all
    particles moving. Setting this to a non-zero number prevents an initial
    wave of particles from overwhelming the screen. Each particle will start
    in a random amount of time less than this number of seconds.
    """


    return Particles(SnowBlossomFactory(image=image,
                                        count=count,
                                        border=border,
                                        xspeed=xspeed,
                                        yspeed=yspeed,
                                        start=start))
                                       
        
