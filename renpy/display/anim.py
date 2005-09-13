# This file contains support for state-machine controlled animations.

import renpy
import pygame
import random

class State(object):
    """
    This creates a state that can be used in a SMAnimation.
    """


    def __init__(self, name, image, *atlist):
        """
        @param name: A string giving the name of this state.

        @param image: The displayable that is shown to the user while
        we are in (entering) this state. For convenience, this can
        also be a string or tuple, which is interpreted with Image.

        image should be None when this State is used with motion,
        to indicate that the image will be replaced with the child of
        the motion.

        @param atlist: A list of functions to call on the image. (In
        general, if something can be used in an at clause, it can be
        used here as well.)
        """

        if image and not isinstance(image, renpy.display.core.Displayable):
            image = renpy.display.image.Image(image)
            
        self.name = name
        self.image = image
        self.atlist = atlist


    def add(self, sma):
        sma.states[self.name] = self

    def get_image(self):
        rv = self.image

        for i in self.atlist:
            rv = i(rv)

        return rv

    def motion_copy(self, child):

        if self.image is not None:
            child = self.mage

        return State(self.name, child, *self.atlist)
    

class Edge(object):
    """
    This creates an edge that can be used with a SMAnimation.
    """

    def __init__(self, old, delay, new, trans=None, prob=1):
        """
        @param old: The name (a string) of the state that this transition is from.

        @param delay: The number of seconds that this transition takes.

        @param new: The name (a string) of the state that this transition is to.

        @param trans: The transition that will be used to show the
        image found in the new state. If None, the image is show
        immediately.

        When used with an SMMotion, the transition should probably be
        move.

        @param prob: The number of times this edge is added. This can
        be used to make a transition more probable then others. For
        example, if one transition out of a state has prob=5, and the
        other has prob=1, then the one with prob=5 will execute 5/6 of
        the time, while the one with prob=1 will only occur 1/6 of the
        time. (Don't make this too large, as memory use is proportional to
        this value.)
        """

        self.old = old
        self.delay = delay
        self.new = new
        self.trans = trans
        self.prob = prob

    def add(self, sma):
        for i in range(0, self.prob):
            sma.edges.setdefault(self.old, []).append(self)


class SMAnimation(renpy.display.core.Displayable):
    """
    This creates a state-machine animation. Such an animation is
    created by randomly traversing the edges between states in a
    defined state machine. Each state corresponds to an image shown to
    the user, with the edges corresponding to the amount of time an
    image is shown, and the transition it is shown with.

    Images are shown, perhaps with a transition, when we are
    transitioning into a state containing that image.
    """
    
    def __init__(self, initial, *args, **properties):
        """
        @param initial: The name (a string) of the initial state we
        start in.

        This accepts as additional arguments the anim.State and
        anim.Edge objects that are used to make up this state
        machine.
        """

        if 'delay' in properties:
            self.delay = properties['delay']
            del properties['delay']
        else:
            self.delay = None

        super(SMAnimation, self).__init__(**properties)

        self.properties = properties

        # The initial state.
        self.initial = initial

        # A map from state name to State object.
        self.states = { }

        # A map from state name to list of Edge objects.
        self.edges = { }

        for i in args:
            i.add(self)

        # The time at which the current edge started. If None, will be
        # set to st by render.
        self.edge_start = None

        # A cache for what the current edge looks like when rendered.
        self.edge_cache = None

        # The current edge.
        self.edge = None

        # The state we're in.
        self.state = None

    def predict(self, callback):
        for i in self.states.itervalues():
            i.image.predict(callback)

    def pick_edge(self, state):
        """
        This randomly picks an edge out of the given state, if
        one exists. It updates self.edge if a transition has
        been selected, or returns None if none can be found. It also
        updates self.image to be the new image on the selected edge.
        """


        if state not in self.edges:
            self.edge = None
            return

        edges = self.edges[state]
        self.edge = random.choice(edges)
        self.state = self.edge.new
        
    def update_cache(self):
        """
        Places the correct Displayable into the edge cache, based on
        what is contained in the given edge. This takes into account
        the old and new states, and any transition that is present.
        """

        im = self.states[self.edge.new].get_image()

        if self.edge.trans:
            im = self.edge.trans(old_widget=self.states[self.edge.old].get_image(),
                                 new_widget=im)

        self.edge_cache = im

    def get_placement(self):

        if self.edge_cache:
            return self.edge_cache.get_placement()

        if self.state:
            return self.states[self.state].get_image().get_placement()

        return self.style

    def render(self, width, height, st):

        if self.edge_start is None or st < self.edge_start:
            self.edge_start = st
            self.edge_cache = None
            self.pick_edge(self.initial)

        while self.edge and st > self.edge_start + self.edge.delay:
            self.edge_start += self.edge.delay

            self.edge_cache = None
            self.pick_edge(self.edge.new)

        # If edge is None, then we have a permanent, static picture. Deal
        # with that.

        if not self.edge:
            im = renpy.display.render.render(self.states[self.state].get_image(),
                                             width, height,
                                             st - self.edge_start)


        # Otherwise, we have another edge.

        else:
            if not self.edge_cache:
                self.update_cache()

            im = renpy.display.render.render(self.edge_cache, width, height, st - self.edge_start)            

            renpy.display.render.redraw(self.edge_cache, self.edge.delay - (st - self.edge_start))


        iw, ih = im.get_size()

        rv = renpy.display.render.Render(iw, ih)
        rv.blit(im, (0, 0))

        return rv
    
    def __call__(self, child=None, new_widget=None, old_widget=None):
        """
        Used when this SMAnimation is used as a SMMotion. This creates
        a duplicate of the animation, with all states containing None
        as the image having that None replaced with the image that is provided here.
        """

        if child is None:
            child = new_widget

        args = [ ]

        for state in self.states.itervalues():
            args.append(state.motion_copy(child))

        for edges in self.edges.itervalues():
            args.extend(edges)

        return SMAnimation(self.initial, delay=self.delay, *args, **self.properties)

def Animation(*args):
    """
    A Displayable that draws an animation, which is a series of images
    that are displayed with time delays between them.

    Odd (first, third, fifth, etc.) arguments to Animation are
    interpreted as image filenames, while even arguments are the time
    to delay between each image. If the number of arguments is odd,
    the animation will stop with the last image (well, actually delay
    for a year before looping). Otherwise, the animation will restart
    after the final delay time.
    """

    sm = [ 0 ]

    for i, arg in enumerate(args):

        if i % 2 == 0:
            sm.append(State(i, arg))

        else:

            if i == len(args) - 1:
                new = 0
            else:
                new = i + 1
                
            sm.append(Edge(i - 1, arg, new))

    return SMAnimation(*sm)


class Blink(renpy.display.core.Displayable):

    def __init__(self, image, on=0.5, off=0.5, rise=0.5, set=0.5,
                 high=1.0, low=0.0, offset=0.0, **properties):

        super(Blink, self).__init__(**properties)

        self.image = renpy.display.im.image(image, loose=True)
        self.on = on
        self.off = off
        self.rise = rise
        self.set = set
        self.high = high
        self.low = low
        self.offset = offset

        self.cycle = on + set + off + rise

    def get_placement(self):
        return self.style

    def render(self, height, width, st):

        time = (self.offset + st) % self.cycle
        alpha = self.high

        if 0 <= time < self.on:
            delay = self.on - time
            alpha = self.high

        time -= self.on

        if 0 <= time < self.set:
            delay = 0            
            frac = time / self.set
            alpha = self.low * frac + self.high * (1.0 - frac)

        time -= self.set

        if 0 <= time < self.off:
            delay = self.off - time
            alpha = self.low

        time -= self.off

        if 0 <= time < self.rise:
            delay = 0
            frac = time / self.rise 
            alpha = self.high * frac + self.low * (1.0 - frac)


        rend = renpy.display.render.render(self.image, height, width, st)

        if not renpy.display.module.can_map:
            return rend

        w, h = rend.get_size()
        rv = renpy.display.render.Render(w, h)

        if alpha:

            oldsurf = rend.pygame_surface()

            if not (oldsurf.get_masks()[3]):
                oldsurf = oldsurf.convert_alpha()

            newsurf = pygame.Surface(oldsurf.get_size(), oldsurf.get_flags(), oldsurf)

            amap = renpy.display.im.ramp(0, int(alpha * 255.0))
            identity = renpy.display.im.identity

            renpy.display.module.map(oldsurf, newsurf,
                                     identity, identity, identity, amap)

            renpy.display.render.mutated_surface(newsurf)

            rv.blit(newsurf, (0, 0))

        rv.depends_on(rend)
        renpy.display.render.redraw(self, delay)

        return rv
