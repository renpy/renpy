# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display
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
    :doc: sprites class

    This represents a sprite that is managed by the SpriteManager. It contains
    fields that control the placement of the sprite on the screen. Sprites
    should not be created directly. Instead, they should be created by
    calling :meth:`SpriteManager.create`.

    The fields of a sprite object are:

    `x`, `y`
        The x and y coordinates of the upper-left corner of the sprite,
        relative to the SpriteManager.

    `zorder`
        An integer that's used to control the order of this sprite in the
        relative to the other sprites in the SpriteManager. The larger the
        number is, the closer to the viewer the sprite is.

    `events`
        If True, then events are passed to child. If False, the default,
        the children ignore events (and hence don't spend time processing
        them).

    The methods of a Sprite object are:
        """

    # Fields:
    #
    # child - the displayable that is the child of this sprite.
    # cache - the SpriteCache of child.
    # live - True if this sprite is still alive.
    # manager - A reference to the SpriteManager.

    def set_child(self, d):
        """
        :doc: sprites method

        Changes the Displayable associated with this sprite to `d`.
        """

        id_d = id(d)

        sc = self.manager.displayable_map.get(id_d, None)
        if sc is None:
            d = renpy.easy.displayable(d)

            sc = SpriteCache()
            sc.render = None
            sc.child = d
            sc.st = None

            if d._duplicatable:
                sc.child_copy = d._duplicate(None)
                sc.child_copy._unique()
            else:
                sc.child_copy = d

            self.manager.displayable_map[id_d] = sc

        self.cache = sc

    def destroy(self):
        """
        :doc: sprites method

        Destroys this sprite, preventing it from being displayed and
        removing it from the SpriteManager.
        """

        self.manager.dead_child = True
        self.live = False
        self.events = False


class SpriteManager(renpy.display.core.Displayable):
    """
    :doc: sprites class

    This displayable manages a collection of sprites, and displays
    them at the fastest speed possible.
    """

    def __init__(self, update=None, event=None, predict=None, ignore_time=False, **properties):
        """
        `update`
            If not None, a function that is called each time a sprite
            is rendered by this sprite manager. It is called with one
            argument, the time in seconds since this sprite manager
            was first displayed.  It is expected to return the number
            of seconds until the function is called again, and the
            SpriteManager is rendered again.

        `event`
            If not None, a function that is called when an event occurs.
            It takes as arguments:
            * A pygame event object.
            * The x coordinate of the event.
            * The y coordinate of the event.
            * The time since the sprite manager was first shown.
            If it returns a non-None value, the interaction ends, and
            that value is returned.

        `predict`
            If not None, a function that returns a list of
            displayables. These displayables are predicted when the
            sprite manager is.

        `ignore_time`
            If True, then time is ignored when rendering displayables. This
            should be used when the sprite manager is used with a relatively
            small pool of images, and those images do not change over time.
            This should only be used with a small number of displayables, as
            it will keep all displayables used in memory for the life of the
            SpriteManager.

        After being rendered once (before the `update` function is called),
        SpriteManagers have the following fields:

        `width`, `height`

             The width and height of this SpriteManager, in pixels.


        SpriteManagers have the following methods:
        """

        super(SpriteManager, self).__init__(self, **properties)

        self.update_function = update
        self.event_function = event
        self.predict_function = predict
        self.ignore_time = ignore_time

        # A map from a displayable to the SpriteDisplayable object
        # representing that displayable.
        self.displayable_map = { }

        # A list of children of this displayable, in zorder. (When sorted.)
        # This is a list of Sprites.
        self.children = [ ]

        # True if at least one child has been killed.
        self.dead_child = False

        # True if at least one child responds to events.
        self.events = False

        # The width and height.
        self.width = None
        self.height = None

    def create(self, d):
        """
        :doc: sprites method

        Creates a new Sprite for the displayable `d`, and adds it to this
        SpriteManager.
        """

        s = Sprite()
        s.x = 0
        s.y = 0
        s.zorder = 0
        s.live = True
        s.manager = self
        s.events = False

        s.set_child(d)

        self.children.append(s)

        return s

    def predict_one(self):
        if self.predict_function is not None:
            for i in self.predict_function():
                renpy.display.predict.displayable(i)

    def redraw(self, delay=0):
        """
        :doc: sprites method

        Causes this SpriteManager to be redrawn in `delay` seconds.
        """

        renpy.display.render.redraw(self, delay)

    def render(self, width, height, st, at):

        self.width = width
        self.height = height

        if self.update_function is not None:

            redraw = self.update_function(st)

            if redraw is not None:
                renpy.display.render.redraw(self, redraw)

        if not self.ignore_time:
            self.displayable_map.clear()

        if self.dead_child:
            self.children = [ i for i in self.children if i.live ]

        self.children.sort(key=lambda sc: sc.zorder)

        caches = [ ]

        rv = renpy.display.render.Render(width, height)

        events = False

        for i in self.children:

            events |= i.events

            cache = i.cache
            r = i.cache.render
            if cache.render is None:
                if cache.st is None:
                    cache.st = st

                cst = st - cache.st

                cache.render = r = render(cache.child_copy, width, height, cst, cst)
                cache.fast = (r.operation == BLIT) and (r.forward is None) and (r.alpha == 1.0) and (r.over == 1.0)
                rv.depends_on(r)

                caches.append(cache)

            if cache.fast:
                for child, xo, yo, _focus, _main in r.children:
                    rv.children.append((child,
                                        xo + i.x,
                                        yo + i.y,
                                        False,
                                        False))

            else:
                rv.subpixel_blit(r, (i.x, i.y))

        for i in caches:
            i.render = None

        return rv

    def event(self, ev, x, y, st):
        for i in xrange(len(self.children) -1, -1, -1):
            s = self.children[i]

            if s.events:
                rv = s.cache.child.event(ev, x - s.x, y - s.y, st - s.cache.st)
                if rv is not None:
                    return rv

        if self.event_function is not None:
            return self.event_function(ev, x, y, st)
        else:
            return None

    def visit(self):
        rv = [ ]

        try:
            if self.predict_function:
                pl = self.predict_function()
                for i in pl:
                    i = renpy.easy.displayable(i)
                    rv.append(i)
        except:
            pass

        return rv

    def destroy_all(self):
        self.children = [ ]


class Particles(renpy.display.core.Displayable, renpy.python.NoRollback):
    """
    Supports particle motion, using the old API.
    """

    __version__ = 1

    nosave = [ 'particles' ]

    def after_upgrade(self, version):
        if version < 1:
            self.sm = SpriteManager(update=self.update_callback, predict=self.predict_callback)

    def after_setstate(self):
        self.particles = None

    def __init__(self, factory, **properties):
        """
        @param factory: A factory object.
        """

        super(Particles, self).__init__(**properties)

        self.sm = SpriteManager(update=self.update_callback, predict=self.predict_callback)

        self.factory = factory
        self.particles = None

    def update_callback(self, st):

        particles = self.particles

        if st == 0 or particles is None:
            self.sm.destroy_all()
            particles = [ ]

        add_parts = self.factory.create(particles, st)

        new_particles = [ ]

        for sprite, p in particles:
            update = p.update(st)

            if update is None:
                sprite.destroy()
                continue

            x, y, _t, d = update

            if d is not sprite.cache.child:
                sprite.set_child(d)

            sprite.x = x
            sprite.y = y

            new_particles.append((sprite, p))

        if add_parts:
            for p in add_parts:
                update = p.update(st)

                if update is None:
                    continue

                x, y, _t, d = update

                if d is None:
                    continue

                sprite = self.sm.create(d)
                sprite.x = x
                sprite.y = y

                new_particles.append((sprite, p))

        self.particles = new_particles

        return 0

    def predict_callback(self):
        return self.factory.predict()

    def render(self, w, h, st, at):
        return renpy.display.render.render(self.sm, w, h, st, at)


class SnowBlossomFactory(renpy.python.NoRollback):

    rotate = False

    def __setstate__(self, state):
        self.start = 0
        vars(self).update(state)
        self.init()

    def __init__(self, image, count, xspeed, yspeed, border, start, fast, rotate=False):
        self.image = renpy.easy.displayable(image)
        self.count = count
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.border = border
        self.start = start
        self.fast = fast
        self.rotate = rotate
        self.init()

    def init(self):
        self.starts = [ random.uniform(0, self.start) for _i in xrange(0, self.count) ]  # W0201
        self.starts.append(self.start)
        self.starts.sort()

    def create(self, particles, st):

        def ranged(n):
            if isinstance(n, tuple):
                return random.uniform(n[0], n[1])
            else:
                return n

        if (st == 0) and not particles and self.fast:
            rv = [ ]

            for _i in xrange(0, self.count):
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


class SnowBlossomParticle(renpy.python.NoRollback):

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


def SnowBlossom(d,
                count=10,
                border=50,
                xspeed=(20, 50),
                yspeed=(100, 200),
                start=0,
                fast=False,
                horizontal=False):
    """
    :doc: sprites_extra

    The snowblossom effect moves multiple instances of a sprite up,
    down, left or right on the screen. When a sprite leaves the screen, it
    is returned to the start.

    `d`
        The displayable to use for the sprites.

    `border`
        The size of the border of the screen. The sprite is considered to be
        on the screen until it clears the border, ensuring that sprites do
        not disappear abruptly.

    `xspeed`, `yspeed`
        The speed at which the sprites move, in the horizontal and vertical
        directions, respectively. These can be a single number or a tuple of
        two numbers. In the latter case, each particle is assigned a random
        speed between the two numbers. The speeds can be positive or negative,
        as long as the second number in a tuple is larger than the first.

    `start`
        The delay, in seconds, before each particle is added. This can be
        allows the particles to start at the top of the screen, while not
        looking like a "wave" effect.

    `fast`
        If true, particles start in the center of the screen, rather than
        only at the edges.

    `horizontal`
        If true, particles appear on the left or right side of the screen,
        rather than the top or bottom.
        """

    # If going horizontal, swap the xspeed and the yspeed.
    if horizontal:
        xspeed, yspeed = yspeed, xspeed

    return Particles(SnowBlossomFactory(image=d,
                                        count=count,
                                        border=border,
                                        xspeed=xspeed,
                                        yspeed=yspeed,
                                        start=start,
                                        fast=fast,
                                        rotate=horizontal))
