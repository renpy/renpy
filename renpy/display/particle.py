# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This code supports particle animation.

import renpy
import random

# TODO: Random start of particles, all at once.

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
        self.old_st = -1
        
    def render(self, w, h, st, at):

        rv = renpy.display.render.Render(w, h)

        if renpy.game.less_updates:
            return rv
                
        if st < self.old_st:
            self.particles = [ ]

        self.old_st = st

        particles = self.particles
        if particles is None:
            particles = [ ]


        newparts = self.factory.create(self.particles, at)

        if newparts is not None:
            particles.extend(newparts)


        liveparts = [ ]

        for p in particles:

            new = p.update(at)
            if new is None:
                continue

            liveparts.append(p)

            xpos, ypos, t, widget = new            
            widget = renpy.display.im.image(widget, loose=True)
            rend = renpy.display.render.render(widget, w, h, t, t)
            widget.place(rv, 0, 0, w, h, rend, xoff=xpos, yoff=ypos)

        self.particles = liveparts
        renpy.display.render.redraw(self, 0)

        return rv

    def visit(self):
        rv = [ ]

        try:
            pl = self.factory.predict()
            for i in pl:
                i = renpy.display.im.image(i, loose=True)
                rv.append(i)
        except:
            pass

        return rv
    
class SnowBlossomFactory(object):

    rotate = False
    
    def __setstate__(self, state):
        self.start = 0
        vars(self).update(state)
        self.init()

    def __init__(self, image, count, xspeed, yspeed, border, start, fast, rotate=False):
        self.image = image
        self.count = count 
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.border = border        
        self.start = start
        self.fast = fast
        self.rotate = rotate
        self.init()

    def init(self):
        self.starts = [ random.uniform(0, self.start) for i in range(0, self.count) ] # W0201
        self.starts.append(self.start)
        self.starts.sort()
    
    def create(self, particles, st):

        def ranged(n):
            if isinstance(n, tuple):
                return random.uniform(n[0], n[1])
            else:
                return n

        if not particles and self.fast:
            rv = [ ]

            for i in range(0, self.count):
                rv.append(SnowBlossomParticle(self.image,
                                              ranged(self.xspeed),
                                              ranged(self.yspeed),
                                              self.border,
                                              st,
                                              random.uniform(0, 100),
                                              fast=True,
                                              rotate=self.rotate))
            return rv
            
        
        if particles is None or len(particles) < self.count:

            # Check to see if we have a particle ready to start. If not,
            # don't start it.
            if particles and st < self.starts[len(particles)]:
                return None

            return [ SnowBlossomParticle(self.image,
                                         ranged(self.xspeed),
                                         ranged(self.yspeed),
                                         self.border,
                                         st,
                                         random.uniform(0, 100),
                                         fast=False,
                                         rotate=self.rotate) ]

    def predict(self):
        return [ self.image ]
    

class SnowBlossomParticle(object):

    def __init__(self, image, xspeed, yspeed, border, start, offset, fast, rotate):

        # safety.
        if yspeed == 0:
            yspeed = 1

        self.image = image
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.border = border
        self.start = start
        self.offset = offset
        self.rotate = rotate
        
        
        if not rotate:
            sh = renpy.config.screen_height
            sw = renpy.config.screen_width
        else:
            sw = renpy.config.screen_height
            sh = renpy.config.screen_width
            
            
        if self.yspeed > 0:
            self.ystart = -border
        else:
            self.ystart = sh + border
        

        travel_time = (2.0 * border + sh) / abs(yspeed)

        xdist = xspeed * travel_time

        x0 = min(-xdist, 0)
        x1 = max(sw + xdist, sw)

        self.xstart = random.uniform(x0, x1)

        if fast:
            self.ystart = random.uniform(-border, sh + border)
            self.xstart = random.uniform(0, sw)

    def update(self, st):
        to = st - self.start

        xpos = self.xstart + to * self.xspeed
        ypos = self.ystart + to * self.yspeed

        if not self.rotate:
            sh = renpy.config.screen_height
        else:
            sh = renpy.config.screen_width
        
        if ypos > sh + self.border:
            return None

        if ypos < -self.border:
            return None

        if not self.rotate:
            return int(xpos), int(ypos), to + self.offset, self.image
        else:
            return int(ypos), int(xpos), to + self.offset, self.image
        
def SnowBlossom(image,
                count=10,
                border=50,
                xspeed=(20, 50),
                yspeed=(100, 200),
                start=0,
                fast=False,
                horizontal=False):

    # If going horizontal, swap the xspeed and the yspeed.
    if horizontal:
        xspeed, yspeed = yspeed, xspeed

    return Particles(SnowBlossomFactory(image=image,
                                        count=count,
                                        border=border,
                                        xspeed=xspeed,
                                        yspeed=yspeed,
                                        start=start,
                                        fast=fast,
                                        rotate=horizontal))

