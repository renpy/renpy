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

# This file contains code contributed by Brian Turcotte, the copyright
# assignment follows:
#
# Copyright for nonlinear ramp code added to ImageDissolve is hereby
# assigned to PyTom <pytom@bishoujo.us>.
# 
# And feel free to change, improve, fold, spindle, or mutilate it,
# obviously.
# 
# Cheers, Brian Turcotte (shaja).

# NOTE:
# Transitions need to be able to work even when old_widget and new_widget
# are None, at least to the point of making it through __init__. This is
# so that prediction of images works.

import renpy
from renpy.display.render import render


class Transition(renpy.display.core.Displayable):
    """
    This is the base class of most transitions. It takes care of event
    dispatching.
    """

    def __init__(self, delay, **properties):
        super(Transition, self).__init__(**properties)
        self.delay = delay
        self.events = True
        
    def event(self, ev, x, y, st):

        if self.events or ev.type == renpy.display.core.TIMEEVENT:
            return self.new_widget.event(ev, x, y, st) # E1101
        else:
            return None

    def visit(self):
        return [ self.new_widget, self.old_widget ] # E1101

def null_render(d, width, height, st, at):

    d.events = True
    surf = renpy.display.render.render(d.new_widget,
                                       width,
                                       height,
                                       st, at)

    rv = renpy.display.render.Render(surf.width, surf.height)
    rv.blit(surf, (0, 0))
    
    return rv
    
class NoTransition(Transition):
    """
    This is a transition that doesn't do anything, and simply displays
    the new_widget for a specified amount of time. It's almost
    certainly not interesting by itself, but it may come in quite
    handy as part of a MultipleTransition.
    """

    def __init__(self, delay, old_widget=None, new_widget=None, **properties):
        super(NoTransition, self).__init__(delay, **properties)

        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = True

    def render(self, width, height, st, at):
        return null_render(self, width, height, st, at)


class MultipleTransition(Transition):
    """
    This is a transition that can sequence between multiple screens,
    showing a different transition between each.

    This must be supplied with a tuple containing an odd number of
    components. The first, third, and so on components are interpreted
    as screens that can be shown to the user, while the even components
    are transitions between those screens.

    A screen can be any displayable, but normally an Image or Solid is
    most appropriate. An screen can also be False to represent the screen
    we are transitioning from, or True to represent the screen we are
    transitioning to. Almost always, the first argument will be False
    and the last will be True.
    """
    
    def __init__(self, args, old_widget=None, new_widget=None):
        
        if len(args) % 2 != 1 or len(args) < 3:
            raise Exception("MultipleTransition requires an odd number of arguments, and at least 3 arguments.")

        self.transitions = [ ]

        # The screens that we use for the transition.
        self.screens = [ renpy.easy.displayable(i) for i in args[0::2] ]

        def oldnew(w):
            if w is False:
                return old_widget
            if w is True:
                return new_widget

            return w

        for old, trans, new in zip(self.screens[0:], args[1::2], self.screens[1:]):
            old = oldnew(old)
            new = oldnew(new)

            self.transitions.append(trans(old_widget=old, new_widget=new))


        super(MultipleTransition, self).__init__(sum([i.delay for i in self.transitions]))

        self.event_target = None
        self.time_offset = 0
        self.new_widget = self.transitions[-1]
        self.events = False

    def visit(self):

        return [ i for i in self.screens if isinstance(i, renpy.display.core.Displayable)] + self.transitions

    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)

        while True:
            trans = self.transitions[0]
            stoff = st - self.time_offset

            if stoff < trans.delay:
                break

            if len(self.transitions) == 1:
                break

            self.time_offset += trans.delay
            self.transitions.pop(0)

            
        if len(self.transitions) == 1:
            self.events = True
            
        self.event_target = trans
        
        surf = renpy.display.render.render(trans, width, height, stoff, at)
        width, height = surf.get_size()
        rv = renpy.display.render.Render(width, height)
        rv.blit(surf, (0, 0))
        
        if stoff > 0:
            renpy.display.render.redraw(self, stoff)

        return rv
            

def Fade(out_time, hold_time, in_time,
         old_widget=None, new_widget=None,
         color=None,
         widget=None,
         ):

    """
    This returns an object that can be used as an argument to a with
    statement to fade the old scene into a solid color, waits for a
    given amount of time, and then fades from the solid color into
    the new scene.
    
    @param out_time:  The amount of time that will be spent
    fading from the old scene to the solid color. A float, given as
    seconds.
    
    @param hold_time:  The amount of time that will be spent
    displaying the solid color. A float, given as seconds.

    @param in_time:  The amount of time that will be spent
    fading from the solid color to the new scene. A float, given as
    seconds.
    
    @param color:  The solid color that will be fade to. A tuple containing
    three components, each between 0 or 255. This can also be None.

    @param widget: This is a widget that will be faded to, if color
    is None. This allows a fade to be to an image rather than just
    a solid color.

    If both color and widget are None, then the fade is to black.
    """

    dissolve = renpy.curry.curry(Dissolve)
    notrans = renpy.curry.curry(NoTransition)

    widget = renpy.easy.displayable_or_none(widget)
    
    if color:
        widget = renpy.display.image.Solid(color)
	
    if not widget:
        widget = renpy.display.image.Solid((0, 0, 0, 255))

    args = [ False, dissolve(out_time), widget ]

    if hold_time:
        args.extend([ notrans(hold_time), widget, ])

    args.extend([dissolve(in_time), True ])

    return MultipleTransition(args, old_widget=old_widget, new_widget=new_widget)


class Pixellate(Transition):
    """
    This pixellates out the old scene, and then pixellates in the new
    scene, taking the given amount of time and the given number of pixellate
    steps in each direction.
    """

    def __init__(self, time, steps, old_widget=None, new_widget=None, **properties):

        time = float(time)

        super(Pixellate, self).__init__(time, **properties)

        self.time = time
        self.steps = steps

        self.old_widget = old_widget
        self.new_widget = new_widget

        self.events = False

        self.quantum = time / ( 2 * steps )

    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)

        if st >= self.time:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        step = st // self.quantum + 1
        visible = self.old_widget

        if step > self.steps:
            step = (self.steps * 2) - step + 1
            visible = self.new_widget
            self.events = True

        rdr = render(visible, width, height, st, at)

        surf = rdr.pygame_surface(False)
        size = surf.get_size()

        newsurf = renpy.display.pgrender.surface(size, surf)

        px = 2 ** step

        renpy.display.module.pixellate(surf, newsurf, px, px, px, px)
        renpy.display.render.mutated_surface(newsurf)

        rv = renpy.display.render.Render(rdr.width, rdr.height)
        rv.blit(newsurf, (0, 0))
        rv.depends_on(rdr)
        
        renpy.display.render.redraw(self, 0)

        return rv

        
class Dissolve(Transition):
    """
    This dissolves from the old scene to the new scene, by
    overlaying the new scene on top of the old scene and varying its
    alpha from 0 to 255.

    @param time: The amount of time the dissolve will take.
    """

    __version__ = 1

    def after_upgrade(self, version):
        if version < 1:
            self.alpha = False
    
    def __init__(self, time, old_widget=None, new_widget=None, alpha=False, **properties):
        super(Dissolve, self).__init__(time, **properties)

        self.time = time
        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = False
        self.alpha = alpha


    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)
        
        if st >= self.time:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        if st < self.time:
            renpy.display.render.redraw(self, 0)

        alpha = min(255, int(255 * st / self.time))

        bottom = render(self.old_widget, width, height, st, at)
        top = render(self.new_widget, width, height, st, at)
        
        bottom_surface = bottom.pygame_surface(self.alpha)
        top_surface = top.pygame_surface(self.alpha)

        width = min(top.width, bottom.width)
        height = min(top.height, bottom.height)

        def draw(dest, x, y):
            
            dw, dh = dest.get_size()

            w = min(dw, width + x)
            h = min(dh, height + y)

            if w <= 0 or h <= 0:
                return

            renpy.display.module.blend(
                bottom_surface.subsurface((-x, -y, w, h)),
                top_surface.subsurface((-x, -y, w, h)),
                dest.subsurface((0, 0, w, h)),
                alpha)
            
        if self.alpha:

            surf = renpy.display.pgrender.surface((width, height), True)
            draw(surf, 0, 0)
            renpy.display.render.mutated_surface(surf)

            rv = renpy.display.render.Render(width, height)
            rv.blit(surf, (0, 0))

        else:
            rv = renpy.display.render.Render(width, height, draw_func=draw, opaque=True)

        rv.depends_on(top, True)
        rv.depends_on(bottom)
        return rv


class ImageDissolve(Transition):
    """
    This dissolves the old scene into the new scene, using an image
    to control the dissolve process.

    A list of values is used to control this mapping. This list of
    values consists 256 fully transparent values, a ramp (of a
    specified number of steps) from full transparency to full opacity,
    and 256 fully opaque values. A 256 entry window is slid over this
    list, and the values found within are used to map the red channel
    of the image onto the opacity of the new scene.

    Basically, this means that while pixels come in first, black last,
    and the ramp controls the sharpness of the transition.
    
    @param image: The image that will be used to control this
    transition. The image should be the same size as the scene being
    dissolved.

    @param time: The amount of time the dissolve will take.

    @param ramplen: The number of pixels of ramp to use. This defaults
    to 8.

    @param ramptype: Type of alpha ramp. Possible types are: linear, cube,
    dcube, mcube. Default is linear. Non-linear types must have
    ramplen >= 8. "cube": Ease in, sharp out. "dcube": Sharp in, sharp out.
    "mcube": Ease in, ease out.

    @param ramp: If given, this is expected to be a sequence of
    integers in the range 0 to 255. This sequence explicitly gives the
    ramp to be used. If given, this overrides ramplen and ramptype.

    @param reverse: This reverses the ramp and the direction of the window
    slide. When True, black pixels dissolve in first, and while pixels come
    in last.    
    """

    __version__ = 1

    def after_upgrade(self, version):
        if version < 1:
            self.alpha = False
    
    def generate_ramp(self, ramplen, ramptype, explicit_ramp, reverse):
        """
        Precomputes the ramp.
        """

        ramp = '\x00' * 256

        if explicit_ramp is not None:

            for i in explicit_ramp:
                ramp += chr(i)

        else:

            if ramptype == 'cube':
                # make sure ramplen is big enough, to avoid div-by-0 errors
                # Not much point in nonlinear if the size is that small, anyway
                if ramplen >= 8:
                    table = []
                    for i in range(ramplen):
                        table.append(i * i * i)
                    scale = max(table) / 255.0
                    for i in range(ramplen):
                        #print i, table[i], table[i] / scale
                        ramp += chr(int(table[i] / scale))
                else:
                    ramptype = 'linear'

            elif ramptype == 'dcube':
                if ramplen >= 8:
                    table = []
                    for i in range(ramplen / 2 - ramplen, ramplen / 2):
                        table.append(i * i * i)
                    adj = abs(min(table))
                    for i in range(len(table)):
                        table[i] += adj
                    scale = max(table) / 255.0
                    #print "scale:", scale
                    for i in range(ramplen):
                        #print i, table[i], table[i] / scale
                        ramp += chr(int(table[i] / scale))
                else:
                    ramptype = 'linear'

            elif ramptype == 'mcube':
                if ramplen >= 8:
                    ramplen = (ramplen / 2) * 2 # make sure it's even
                    table = []
                    for i in range(ramplen / 2):
                        table.append(i * i * i)
                    adj = table[-1]
                    tmptable = []
                    for i in table:
                        tmptable.append(i)
                    for i in range(1, len(table) + 1):
                        tmptable.append(abs(table[len(table) - i] - adj) + adj)
                    table = tmptable
                    scale = max(table) / 255.0
                    #print "scale:", scale
                    for i in range(ramplen):
                        #print i, table[i], table[i] / scale
                        ramp += chr(int(table[i] / scale))
                else:
                    ramptype = 'linear'

            if ramptype == 'linear':
                for i in range(ramplen):
                    ramp += chr(255 * i / ramplen)

        ramp += '\xff' * 256

        if reverse:
            ramp = list(ramp)
            ramp.reverse()
            ramp = ''.join(ramp)

        return ramp
        
        
    def __init__(self, image, time, ramplen=8, ramptype='linear', ramp=None, reverse=False, alpha=False,
                 old_widget=None, new_widget=None, **properties):

        super(ImageDissolve, self).__init__(time, **properties)

        self.time = time
        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = False
        self.alpha = alpha
        
        self.image = renpy.display.im.image(image)

        if ramp is not None:
            ramplen = len(ramp)

        self.ramp = self.generate_ramp(ramplen, ramptype, ramp, reverse)
        
        self.steps = ramplen + 256
        self.reverse = reverse


    def visit(self):
        return super(ImageDissolve, self).visit() + [ self.image ]

    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)

        if st >= self.time:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        image = renpy.display.im.cache.get(self.image)

        if st < self.time:
            renpy.display.render.redraw(self, 0)

        step = int(self.steps * st / self.time)

        if self.reverse:
            step = self.steps - step

        ramp = self.ramp[step:step+256]


        bottom = render(self.old_widget, width, height, st, at)
        top = render(self.new_widget, width, height, st, at)
        
        bottom_surface = bottom.pygame_surface(self.alpha)
        top_surface = top.pygame_surface(self.alpha)

        iw, ih = image.get_size()

        width = min(bottom.width, top.width, iw)
        height = min(bottom.height, top.height, ih)
            
        def draw(dest, x, y):

            dw, dh = dest.get_size()

            w = min(dw, width + x)
            h = min(dh, height + y)

            renpy.display.module.imageblend(
                bottom_surface.subsurface((-x, -y, w, h)),
                top_surface.subsurface((-x, -y, w, h)),
                dest.subsurface((0, 0, w, h)),
                image.subsurface((-x, -y, w, h)),
                ramp)

        if self.alpha:

            surf = renpy.display.pgrender.surface((width, height), True)
            draw(surf, 0, 0)
            renpy.display.render.mutated_surface(surf)

            rv = renpy.display.render.Render(width, height)
            rv.blit(surf, (0, 0))

        else:
            rv = renpy.display.render.Render(width, height, draw_func=draw, opaque=True)

        rv.depends_on(top, True)
        rv.depends_on(bottom)
        return rv


class CropMove(Transition):
    """
    The CropMove transition works by placing the old and the new image
    on two layers, called the top and the bottom. (Normally the new
    image is on the top, but that can be changed in some modes.) The
    bottom layer is always drawn in full. The top image is first
    cropped to a rectangle, and then that rectangle drawn onto
    the screen at a specified position. Start and end crop rectangles
    and positions can be selected by the supplied mode, or
    specified manually. The result is a surprisingly flexible
    transition.

    This transition has many modes, simplifying its use. We can group
    these modes into three groups: wipes, slides, and other.

    In a wipe, the image stays fixed, and more of it is revealed as
    the transition progresses. For example, in "wiperight", a wipe from left to right, first the left edge of the image is
    revealed at the left edge of the screen, then the center of the image,
    and finally the right side of the image at the right of the screen.
    Other supported wipes are "wipeleft", "wipedown", and "wipeup".

    In a slide, the image moves. So in a "slideright", the right edge of the
    image starts at the left edge of the screen, and moves to the right
    as the transition progresses. Other slides are "slideleft", "slidedown",
    and "slideup".

    There are also slideaways, in which the old image moves on top of
    the new image. Slideaways include "slideawayright", "slideawayleft",
    "slideawayup", and "slideawaydown".

    We also support a rectangular iris in with "irisin" and a
    rectangular iris out with "irisout". Finally, "custom" lets the
    user define new transitions, if these ones are not enough.
    """

    def __init__(self, time,
                 mode="fromleft",
                 startcrop=(0.0, 0.0, 0.0, 1.0),
                 startpos=(0.0, 0.0),
                 endcrop=(0.0, 0.0, 1.0, 1.0),
                 endpos=(0.0, 0.0),
                 topnew=True,
                 old_widget=None,
                 new_widget=None,
                 **properties):

        """
        @param time: The time that this transition will last for, in seconds.
 
        @param mode: One of the modes given above.

        The following parameters are only respected if the mode is "custom". 

        @param startcrop: The starting rectangle that is cropped out of the
        top image. A 4-element tuple containing x, y, width, and height. 
        
        @param startpos: The starting place that the top image is drawn
        to the screen at, a 2-element tuple containing x and y.

        @param endcrop: The ending rectangle that is cropped out of the
        top image. A 4-element tuple containing x, y, width, and height. 
        
        @param endpos: The ending place that the top image is drawn
        to the screen at, a 2-element tuple containing x and y.

        @param topnew: If True, the top layer contains the new
        image. Otherwise, the top layer contains the old image.
        """
        
        super(CropMove, self).__init__(time, **properties)
        self.time = time

        if mode == "wiperight":
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 0.0, 1.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "wipeleft":
            startpos = (1.0, 0.0)
            startcrop = (1.0, 0.0, 0.0, 1.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "wipedown":
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "wipeup":
            startpos = (0.0, 1.0)
            startcrop = (0.0, 1.0, 1.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slideright":
            startpos = (0.0, 0.0)
            startcrop = (1.0, 0.0, 0.0, 1.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slideleft":
            startpos = (1.0, 0.0)
            startcrop = (0.0, 0.0, 0.0, 1.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slideup":
            startpos = (0.0, 1.0)
            startcrop = (0.0, 0.0, 1.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True
            
        elif mode == "slidedown":
            startpos = (0.0, 0.0)
            startcrop = (0.0, 1.0, 1.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slideawayleft":
            endpos = (0.0, 0.0)
            endcrop = (1.0, 0.0, 0.0, 1.0)
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = False

        elif mode == "slideawayright":
            endpos = (1.0, 0.0)
            endcrop = (0.0, 0.0, 0.0, 1.0)
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = False

        elif mode == "slideawaydown":
            endpos = (0.0, 1.0)
            endcrop = (0.0, 0.0, 1.0, 0.0)
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = False
            
        elif mode == "slideawayup":
            endpos = (0.0, 0.0)
            endcrop = (0.0, 1.0, 1.0, 0.0)
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = False

        elif mode == "irisout":
            startpos = (0.5, 0.5)
            startcrop = (0.5, 0.5, 0.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True
            
        elif mode == "irisin":
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            endpos = (0.5, 0.5)
            endcrop = (0.5, 0.5, 0.0, 0.0)
            topnew = False
            
            
        elif mode == "custom":
            pass
        else:
            raise Exception("Invalid mode %s passed into boxwipe." % mode)

        self.delay = time
        self.time = time

        self.startpos = startpos
        self.endpos = endpos

        self.startcrop = startcrop
        self.endcrop = endcrop
        
        self.topnew = topnew

        self.old_widget = old_widget
        self.new_widget = new_widget

        self.events = False

        if topnew:
            self.bottom = old_widget
            self.top = new_widget
        else:
            self.bottom = new_widget
            self.top = old_widget

    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)

        time = 1.0 * st / self.time

        # Done rendering.
        if time >= 1.0:
            self.events = True
            return render(self.new_widget, width, height, st, at)
        
        # How we scale each element of a tuple.
        scales = (width, height, width, height)

        def interpolate_tuple(t0, t1):
            return tuple([ int(s * (a * (1.0 - time) + b * time))
                           for a, b, s in zip(t0, t1, scales) ])

        crop = interpolate_tuple(self.startcrop, self.endcrop)
        pos = interpolate_tuple(self.startpos, self.endpos)


        top = render(self.top, width, height, st, at)
        bottom = render(self.bottom, width, height, st, at)
        
        width = min(bottom.width, width)
        height = min(bottom.height, height)
        rv = renpy.display.render.Render(width, height)

        rv.blit(bottom, (0, 0), focus=not self.topnew)

        ss = top.subsurface(crop, focus=self.topnew)
        rv.blit(ss, pos, focus=self.topnew)

        renpy.display.render.redraw(self, 0)
        return rv


# Utility function used by MoveTransition et al.
def position(d):

    xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel = d.get_placement()

    if xpos is None:
        xpos = 0
    if ypos is None:
        ypos = 0
    if xanchor is None:
        xanchor = 0
    if yanchor is None:
        yanchor = 0

    return xpos, ypos, xanchor, yanchor

# These are used by MoveTransition.
def MoveFactory(pos1, pos2, delay, d, **kwargs):
    if pos1 == pos2:
        return d

    return renpy.display.motion.Move(pos1, pos2, delay, d, **kwargs)

def default_enter_factory(pos, delay, d):
    return d

def default_leave_factory(pos, delay, d):
    return None

# These can be used to move things in and out of the screen.
def MoveIn(pos, pos1, delay, d, **kwargs):

    def aorb(a, b):
        if a is None:
            return b
        return a

    pos = tuple([aorb(a, b) for a, b in zip(pos, pos1)])
    return renpy.display.motion.Move(pos, pos1, delay, d, **kwargs)

def MoveOut(pos, pos1, delay, d, **kwargs):

    def aorb(a, b):
        if a is None:
            return b
        return a

    pos = tuple([aorb(a, b) for a, b in zip(pos, pos1)])
    return renpy.display.motion.Move(pos1, pos, delay, d, **kwargs)

def ZoomInOut(start, end, pos, delay, d, **kwargs):

    xpos, ypos, xanchor, yanchor = pos

    FactorZoom = renpy.display.motion.FactorZoom
    
    if end == 1.0:
        return FactorZoom(start, end, delay, d, after_child=d, opaque=False,
                          xpos=xpos, ypos=ypos, xanchor=xanchor, yanchor=yanchor, **kwargs)
    else:
        return FactorZoom(start, end, delay, d, opaque=False,
                          xpos=xpos, ypos=ypos, xanchor=xanchor, yanchor=yanchor, **kwargs)

def RevolveInOut(start, end, pos, delay, d, **kwargs):
    return renpy.display.motion.Revolve(start, end, delay, d, pos=pos, **kwargs)
    
# TODO: Move isn't properly respecting positions when x < 0.
def MoveTransition(delay, old_widget=None,  new_widget=None, factory=None, enter_factory=None, leave_factory=None, old=False, layers=[ 'master' ]):
    """
    This transition attempts to find images that have changed
    position, and moves them from the old position to the new
    transition, taking delay seconds to complete the move.

    Images are considered to be the same if they have the same tag, in
    the same way that the tag is used to determine which image to
    replace or to hide.

    If you use this transition to slide an image off the side of the
    screen, remember to hide it when you are done.

    factory is a function that takes the old position, the new position, the
    delay time, and the displayable, and returns a new displayable that
    performs the move.
    """

    if factory is None:
        factory = MoveFactory

    if enter_factory is None:
        enter_factory = default_enter_factory

    if leave_factory is None:
        leave_factory = default_leave_factory

    use_old = old
    
    def merge_slide(old, new):

        # If new does not have .layers or .scene_list, then we simply
        # insert a move from the old position to the new position, if
        # a move occured.
            
        if (not isinstance(new, renpy.display.layout.MultiBox)
            or (new.layers is None and new.layer_name is None)):

            if use_old:
                child = old
            else:
                child = new

            if position(old) != position(new):

                return factory(position(old),
                               position(new),
                               delay,
                               child,
                               )
            else:
                return child

        # If we're in the layers_root widget, merge the child widgets
        # for each layer.
        if new.layers:

            assert old.layers

            rv = renpy.display.layout.MultiBox(layout='fixed')
            rv.layers = { }

            for layer in renpy.config.layers:

                f = new.layers[layer]

                if (isinstance(f, renpy.display.layout.MultiBox) 
                    and layer in layers
                    and f.scene_list is not None):
                    
                    f = merge_slide(old.layers[layer], new.layers[layer])

                rv.layers[layer] = f
                rv.add(f)

            return rv

        # Otherwise, we recompute the scene list for the two widgets, merging
        # as appropriate.

        # Wraps the displayable found in SLE so that the various timebases
        # are maintained.
        def wrap(sle):
            key, zorder, st, at, d = sle
            return renpy.display.layout.AdjustTimes(d, st, at)
        
        def tag(sle):
            if sle[0] is None:
                tag = sle[4]
            else:
                tag = sle[0]

            return tag

        def merge(sle, d):
            return (sle[0], sle[1], 0, sle[3], d)
        
        # A list of tags on the new layer.
        new_tags = set()

        # The scene list we're creating.
        rv_sl = [ ]

        # The new scene list we're copying from.
        new_scene_list = new.scene_list[:]

        for new_sle in new.scene_list:
            new_tag = tag(new_sle)
            
            if new_tag is not None:
                new_tags.add(new_tag)

        for old_sle in old.scene_list:
            old_tag = tag(old_sle)
            old_d = wrap(old_sle)
            
            # In old, not in new.
            if old_tag not in new_tags:

                move = leave_factory(position(old_d), delay, old_d)
                if move is None:
                    continue
                
                move = renpy.display.layout.IgnoresEvents(move)
                
                rv_sl.append(merge(old_sle, move))
                continue

            # In new, not in old.
            while new_scene_list:
                new_sle = (new_scene_list.pop(0))                
                new_tag = tag(new_sle)
                new_d = wrap(new_sle)
                
                new_tags.discard(new_tag)
                
                if new_tag == old_tag:
                    break

                move = enter_factory(position(new_d), delay, new_d)
                if move is None:
                    continue

                rv_sl.append(merge(new_sle, move))
                continue

            # In both.
            if new_tag == old_tag:

                if use_old:
                    child = old_d
                else:
                    child = new_d
                
                move = factory(position(old_d), position(new_d), delay, child)
                if move is None:
                    continue

                rv_sl.append(merge(new_sle, move))
                
        # In new scene list after we're done processing the stuff in the old
        # scene list.
        while new_scene_list:
            new_sle = (new_scene_list.pop(0))                
            new_tag = tag(new_sle)
            new_d = wrap(new_sle)

            move = enter_factory(position(new_d), delay, new_d)
            if move is None:
                continue

            rv_sl.append(merge(new_sle, move))
            continue

        layer = new.layer_name
        rv = renpy.display.layout.MultiBox(layout='fixed', focus=layer, **renpy.game.interface.layer_properties[layer])
        rv.append_scene_list(rv_sl)
        rv.layer_name = layer

        return rv


    # This calls merge_slide to actually do the merging.

    rv = merge_slide(old_widget, new_widget)
    rv.delay = delay # W0201

    return rv

            

def ComposeTransition(trans, before=None, after=None, new_widget=None, old_widget=None):
    if before is not None:
        old = before(new_widget=new_widget, old_widget=old_widget)
    else:
        old = old_widget
        
    if after is not None:
        new = after(new_widget=new_widget, old_widget=old_widget)
    else:
        new = new_widget

    return trans(new_widget=new, old_widget=old)

def SubTransition(rect, trans, old_widget=None, new_widget=None, **properties):
    x, y, w, h = rect

    old = renpy.display.layout.LiveCrop(rect, old_widget)
    new = renpy.display.layout.LiveCrop(rect, new_widget)

    inner = trans(old_widget=old, new_widget=new)
    delay = inner.delay
    inner = renpy.display.layout.Position(inner, xpos=x, ypos=y, xanchor=0, yanchor=0)
    
    f = renpy.display.layout.MultiBox(layout='fixed')
    f.add(new_widget)
    f.add(inner)

    return NoTransition(delay, old_widget=f, new_widget=f)

