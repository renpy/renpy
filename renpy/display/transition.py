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
import pygame
from pygame.constants import *

# We used time too many other times. :-(
from time import time as now

# # This is a utility function that attempts to refactor an old and a new
# # Fixed into four Fixeds: below, old, new, and above. Since only the
# # old and new need transitions, this can be a significant win.
# def refactor_fixed(in_old, in_new):

#     Fixed = renpy.display.layout.Fixed

#     out_below = Fixed()
#     out_old = Fixed()
#     out_new = Fixed()
#     out_above = Fixed()

#     if (not isinstance(in_old, Fixed)) or (not isinstance(in_new, Fixed)):
#         return out_below, in_old, in_new, out_above

#     old_list = in_old.get_widget_time_list()
#     new_list = in_new.get_widget_time_list()

#     # Merge the beginnings of the lists.
#     while old_list and new_list:
#         if old_list[0] == new_list[0]:
#             out_below.add(new_list[0][0], new_list[0][1])
#             old_list.pop(0)
#             new_list.pop(0)

#         else:
#             break

#     # Merge the ends of the lists.
#     above_list = [ ]

#     while old_list and new_list:
#         if old_list[-1] == new_list[-1]:
#             above_list.insert(0, new_list[-1])
#             old_list.pop()
#             new_list.pop()
#         else:
#             break

#     for widget, time in above_list:
#         out_above.add(widget, time)

#     for widget, time in old_list:
#         out_old.add(widget, time)

#     for widget, time in new_list:
#         out_new.add(widget, time)

#     return out_below, out_old, out_new, out_above

class Transition(renpy.display.core.Displayable):
    """
    This is the base class of most transitions. It takes care of event
    dispatching.
    """

    def __init__(self, delay):
        super(Transition, self).__init__()
        self.delay = delay
        self.events = True
        
    def event(self, ev, x, y, st):
        if self.events or ev.type == renpy.display.core.TIMEEVENT:
            return self.new_widget.event(ev, x, y, st)
        else:
            return None

    def visit(self):
        return [ self.old_widget, self.new_widget ]

class NoTransition(Transition):
    """
    This is a transition that doesn't do anything, and simply displays
    the new_widget for a specified amount of time. It's almost
    certainly not interesting by itself, but it may come in quite
    handy as part of a MultipleTransition.
    """

    def __init__(self, delay, old_widget=None, new_widget=None):
        super(NoTransition, self).__init__(delay)

        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = True

    def render(self, width, height, st, at):

        rv = renpy.display.render.Render(width, height)

        rv.blit(renpy.display.render.render(self.new_widget,
                                            width,
                                            height,
                                            st, at), (0, 0))

        return rv


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
        self.screens = args[0::2]

        def oldnew(w):
            if w is False:
                return old_widget
            if w is True:
                return new_widget
            return w

        for old, trans, new in zip(args[0::2], args[1::2], args[2::2]):
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

        rv = renpy.display.render.Render(width, height)
        rv.blit(renpy.display.render.render(trans, width, height, stoff, at), (0,0))
        
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

    def __init__(self, time, steps, old_widget=None, new_widget=None):

        time = float(time)

        if not renpy.display.module.can_pixellate:
            time = 0

        super(Pixellate, self).__init__(time)

        self.time = time
        self.steps = steps

        self.old_widget = old_widget
        self.new_widget = new_widget

        self.surface = None
        self.surface_size = None

        self.events = False

        self.quantum = time / ( 2 * steps )

    def render(self, width, height, st, at):

        if st >= self.time:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        step = st // self.quantum + 1
        visible = self.old_widget

        if step > self.steps:
            step = (self.steps * 2) - step + 1
            visible = self.new_widget
            self.events = True

        rv = renpy.display.render.Render(width, height)
        rdr = render(visible, width, height, st, at)

        # No alpha support.
        surf = rdr.pygame_surface(False)
        
        if surf.get_size() != self.surface_size:
            self.surface_size = surf.get_size()
            self.surface = pygame.Surface(self.surface_size, surf.get_flags(), surf)

        px = 2 ** step

        renpy.display.module.pixellate(surf, self.surface, px, px, px, px)
        renpy.display.render.mutated_surface(self.surface)

        rv.blit(self.surface, (0, 0))

        if self.events:
            rv.focuses.extend(rdr.focuses)

        # renpy.display.render.redraw(self, self.quantum - st % self.quantum)

        renpy.display.render.redraw(self, 0)

        return rv

        
class Dissolve(Transition):
    """
    This dissolves from the old scene to the new scene, by
    overlaying the new scene on top of the old scene and varying its
    alpha from 0 to 255.

    @param time: The amount of time the dissolve will take.
    """

    def __init__(self, time, old_widget=None, new_widget=None):
        super(Dissolve, self).__init__(time)

        self.time = time
        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = False

        self.old_bottom = None
        self.old_top = None
        self.old_alpha = 0

    def render(self, width, height, st, at):

        if st >= self.time:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        if st < self.time:
            renpy.display.render.redraw(self, 0)

        alpha = min(255, int(255 * st / self.time))

        rv = renpy.display.render.Render(width, height)

        bottom = render(self.old_widget, width, height, st, at)
        top = render(self.new_widget, width, height, st, at)

        surf = top.pygame_surface(False)
        renpy.display.render.mutated_surface(surf)

        rv.focuses.extend(top.focuses)

        if renpy.config.enable_fast_dissolve and id(top) == self.old_top and id(bottom) == self.old_bottom and hasattr(self.new_widget, 'layers'):
            # Fast rendering path. Only used for full-screen, top-level, renders.

            alpha = alpha / 255.0
            change = ( alpha - self.old_alpha) / ( 1.0 - self.old_alpha)
            change = int(change * 255.0)

            surf.set_alpha(change, RLEACCEL)
            rv.blit(surf, (0, 0))

            change /= 255.0
            self.old_alpha = self.old_alpha * ( 1 - change ) + change
            
        else:

            # Complete rendering path.

            rv.blit(bottom, (0, 0), focus=False)
            surf.set_alpha(alpha, RLEACCEL)
            rv.blit(surf, (0, 0))

            self.old_alpha = alpha / 255.0


        self.old_top = id(top)
        self.old_bottom = id(bottom)

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
                 new_widget=None):

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
        
        super(CropMove, self).__init__(time)
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

        rv = renpy.display.render.Render(width, height)

        rv.blit(render(self.bottom, width, height, st, at), (0, 0), focus=not self.topnew)

        top = render(self.top, width, height, st, at)
        ss = top.subsurface(crop, focus=self.topnew)
        rv.blit(ss, pos, focus=self.topnew)

        renpy.display.render.redraw(self, 0)
        return rv
                

# TODO: Move isn't properly respecting positions when x < 0.
def MoveTransition(delay, old_widget=None, new_widget=None, factory=None):
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
        factory = renpy.display.layout.Move

    def position(d):

        xpos, ypos, xanchor, yanchor = d.get_placement()

        if xpos is None:
            xpos = 0
        if ypos is None:
            ypos = 0
        if xanchor is None:
            xanchor = 0
        if yanchor is None:
            yanchor = 0

        return xpos, ypos, xanchor, yanchor
        

    def merge_slide(old, new, layer_name=None):

            
        # If new does not have .layers or .scene_list, then we simply
        # insert a move from the old position to the new position, if
        # a move occured.

        if not hasattr(new, 'layers') and not hasattr(new, 'scene_list'):

            if position(old) != position(new):

                return factory(position(old),
                               position(new),
                               delay,
                               new,
                               )
            else:
                return new

        # If we're in the layers_root widget, merge the child widgets
        # for each layer.
        if new.layers:
            assert old.layers

            rv = renpy.display.layout.Fixed()
            rv.layers = { }

            for layer in renpy.config.layers:

                f = new.layers[layer]

                if isinstance(f, renpy.display.layout.Fixed) and f.scene_list:
                    f = merge_slide(old.layers[layer], new.layers[layer], layer_name=layer)

                rv.layers[layer] = f
                rv.add(f)

            return rv

        # Otherwise, we recompute the scene list for the two widgets, merging
        # as appropriate.

        tags = { }

        for tag, zo, start, anim, d in old.scene_list:

            if tag is None:
                continue

            tags[tag] = d

        newsl = [ ]

        for tag, zo, time, anim, d in new.scene_list:

            if tag is None or tag not in tags:
                newsl.append((tag, zo, time, anim, d))
                continue

            oldpos = position(tags[tag])
            newpos = position(d)

            if oldpos == newpos:
                newsl.append((tag, zo, time, anim, d))
                continue
                
            move = renpy.display.layout.Move(position(tags[tag]),
                                             position(d),
                                             delay,
                                             d,
                                             )

            newsl.append((tag, zo, None, anim, move))

        rv = renpy.game.interface.make_layer(layer_name, newsl)

        return rv


    rv = merge_slide(old_widget, new_widget)
    rv.delay = delay

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

        old = 0
        for i in ramp:
            i = ord(i)
            if i < old:
                self.can_fast = False
                break

            old = i
        else:
            self.can_fast = True

        if reverse:
            ramp = list(ramp)
            ramp.reverse()
            ramp = ''.join(ramp)

        return ramp
        
        
    def __init__(self, image, time, ramplen=8, ramptype='linear', ramp=None, reverse=False,
                 old_widget=None, new_widget=None):

        super(ImageDissolve, self).__init__(time)

        self.time = time
        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = False

        self.old_bottom = None
        self.old_top = None
        self.old_ramp = '\x00' * 256

        self.image = renpy.display.im.image(image)

        if ramp is not None:
            ramplen = len(ramp)

        self.ramp = self.generate_ramp(ramplen, ramptype, ramp, reverse)
        
        self.steps = ramplen + 256
        self.reverse = reverse


    def visit(self):
        return [ self.image ]

    def render(self, width, height, st, at):

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

        rv = renpy.display.render.Render(width, height)

        bottom = render(self.old_widget, width, height, st, at)
        top = render(self.new_widget, width, height, st, at)

        surf = top.pygame_surface(True)
        renpy.display.render.mutated_surface(surf)

        rv.focuses.extend(top.focuses)

        if renpy.config.enable_fast_dissolve and self.can_fast and id(top) == self.old_top and id(bottom) == self.old_bottom and hasattr(self.new_widget, 'layers'):
            # Fast rendering path. Only used for full-screen, top-level, renders.

            fast_ramp = [ ]

            for new, old in zip(ramp, self.old_ramp):

                new = ord(new)
                old = ord(old)

                if new >= 255:
                    fast_ramp.append('\xff')
                    continue

                change = 255 * ( new - old ) / ( 255 - old )
                fast_ramp.append(chr(int(change)))

            renpy.display.module.alpha_munge(image, surf,
                                             ''.join(fast_ramp))
            
            rv.blit(surf, (0, 0))
                        
        else:

            # Complete rendering path.

            rv.blit(bottom, (0, 0), focus=False)

            renpy.display.module.alpha_munge(image, surf, ramp)
            rv.blit(surf, (0, 0))

        self.old_ramp = ramp

        
        self.old_top = id(top)
        self.old_bottom = id(bottom)

        return rv

