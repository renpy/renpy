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

# This code supports sprite and particle animation.

from renpy.display.render import render, BLIT

import renpy
import random


class SpriteCache(renpy.object.Object):
    """
    This stores information about a displayble, including the identity
    of the displayable, and when it was first displayed. It is also
    responsible for caching the displayable surface, so it doesn't
    need to be re-rendered.
    """

    # Private Fields:
    #
    # child - The child displayable.
    # 
    # st - The shown time when this was first displayed, or None if it hasn't
    # been rendered.
    #
    # render - The render of child.
    #
    # If true, then the render is simple enough it can just be appended to
    # the manager's render's children list.
    
class Sprite(renpy.object.Object):
    """
    This represents a sprite that is managed by a sprite manager.
    """

    # Public fields:
    #
    # xoffset - float or int - The offset of the left side of the sprite
    # yoffset - float or int - The offset of the top side of the sprite.
    # zorder - the zorder of the displayable. The bigger the number, the
    # closer to the viewer.
    
    # child - the displayable that is the child of this sprite.
    # cache - the SpriteCache of child.
    # live - True if this sprite is still alive.
    # manager - A reference to the SpriteManager.

    def set_child(self, d):
        """
        Changes the child of this sprite to be `d`.
        """

        id_d = id(d)

                
        sc = self.manager.displayable_map.get(id_d, None)
        if sc is None:
            d = renpy.easy.displayable(d)

            sc = SpriteCache()
            sc.render = None
            sc.child = d
            sc.st = None
            self.manager.displayable_map[id_d] = sc

        self.cache = sc
            
    def destroy(self):
        self.manager.dead_child = True
        self.live = False

    

class SpriteManager(renpy.display.core.Displayable):
    """
    :doc: sprites
    
    This displayable manages a collection of sprites, and displays
    them at the fastest speed possible.
    """
    
    def __init__(self, function=None, ignore_time=False, **kwargs):
        """
        `function`
            If not None,        
            a function that is called each time a sprite is rendered by
            this sprite manager. It is called with two arguments. The first
            is the sprite manager, and the second is the time since the
            sprite manager was first displayed. It is expected to return
            the number of seconds until the function is called again, and
            the SpriteManager is rendered again.


         `ignore_time`
            If True, then time is ignored when rendering displayables. This
            should be used when the sprite manager is used with a relatively
            small pool of images, and those images do not change over time.
            This should only be used with a small number of displayables, as
            it will keep all displayable in memory for the life of the
            SpriteManager.
         """
            

        super(SpriteManager, self).__init__(self)

        self.function = function
        self.ignore_time = ignore_time
        
        # A map from a displayable to the SpriteDisplayable object
        # representing that displayable.
        self.displayable_map = { }

        # A list of children of this displayable, in zorder. (When sorted.)
        # This is a list of Sprites.
        self.children = [ ]

        # True if at least one child has been killed.
        self.dead_child = False

        
    def create(self, d):
        """
        Creates a new sprite for the displayable `d`, and adds it to the
        list of children of this sprite.
        """

        id_d = id(d)
        
        sc = self.displayable_map.get(id_d, None)
        if sc is None:
            d = renpy.easy.displayable(d)

            sc = SpriteCache()
            sc.render = None
            sc.child = d
            sc.st = None
            self.displayable_map[id_d] = sc

        s = Sprite()
        s.xoffset = 0
        s.yoffset = 0
        s.zorder = 0
        s.cache = sc
        s.live = True
        s.manager = self
        
        self.children.append(s)

        return s

    
    def redraw(self):
        """
        Causes this SpriteManager to be redrawn immediately.
        """

        renpy.display.render.redraw(self, 0)
        
    
    def render(self, width, height, st, at):

        if self.function is not None:
            redraw = self.function(st)

            if redraw is not None:
                renpy.display.render.redraw(self, redraw)
            
        if not self.ignore_time:
            self.displayable_map.clear()
        
        if self.dead_child:
            self.children = [ i for i in self.children if i.live ]

        self.children.sort()

        caches = [ ]

        rv = renpy.display.render.Render(width, height)
        
        for i in self.children:

            cache = i.cache
            r = i.cache.render
            if cache.render is None:
                if cache.st is None:
                    cache.st = st

                cst = st - cache.st

                cache.render = r = render(cache.child, width, height, cst, cst)
                cache.fast = (r.operation == BLIT) and (r.forward is None) and (r.alpha == 1.0)
                rv.depends_on(r)
                
                caches.append(cache)
                

            if cache.fast:
                for child, xo, yo, focus, main in r.children:
                    rv.children.append((child,
                                        xo + i.xoffset,
                                        yo + i.yoffset,
                                        False,
                                        False))

            else:
                rv.subpixel_blit(r, (i.xoffset, i.yoffset))

        for i in caches:
            i.render = None
                
        return rv
                
                



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

