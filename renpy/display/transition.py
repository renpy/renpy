import renpy
from renpy.display.render import render
import pygame
from pygame.constants import *


class Transition(renpy.display.core.Displayable):
    """
    This is the base class of all transitions. It takes care of event
    dispatching (primarily by passing all events off to a SayBehavior.)
    """

    def __init__(self, delay):
        self.delay = delay
        self.offsets = [ ]
        self.events = True
        
    def event(self, ev, x, y):
        if self.events:
            return self.new_widget.event(ev, x, y)
        else:
            return None

class Fade(Transition):
    """
    This is a transition that involves fading to a certain color, then
    holding that color for a certain amount of time, then fading in the
    new scene.
    """

    def __init__(self, out_time, hold_time, in_time,
                 old_widget, new_widget, color=(0, 0, 0)):

        super(Fade, self).__init__(out_time + hold_time + in_time)

        self.out_time = out_time
        self.hold_time = hold_time
        self.in_time = in_time
        self.old_widget = old_widget
        self.new_widget = new_widget
        self.color = color

        # self.frames = 0

    # def __del__(self):
    #     print "Faded using", self.frames, "frames."

    def render(self, width, height, st):

        # self.frames += 1

        rv = renpy.display.render.Render(width, height)

        events = False

        if st < self.out_time:
            widget = self.old_widget
            alpha = int(255 * (st / self.out_time))

        elif st < self.out_time + self.hold_time:
            widget = None
            alpha = 255

        else:
            widget = self.new_widget
            alpha = 255 - int(255 * ((st - self.out_time - self.hold_time) / self.in_time))
            events = True

        if widget:
            surf = render(widget, width, height, st)
            
            rv.blit(surf, (0, 0))

        self.events = events 

        # Just to be sure.
        if alpha < 0:
            alpha = 0

        if alpha > 255:
            alpha = 255

        rv.fill(self.color[:3] + (alpha,))

        if st < self.in_time + self.hold_time + self.out_time:
            renpy.display.render.redraw(self, 0)

        return rv

class Dissolve(Transition):

    def __init__(self, time, old_widget, new_widget):
        super(Dissolve, self).__init__(time)

        self.time = time
        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = True

    def render(self, width, height, st):

        if st > self.time:
            return render(self.new_widget, width, height, st)
        
        rv = render(self.old_widget, width, height, st)

        top = render(self.new_widget, width, height, st)

        surf = top.pygame_surface(False)
        renpy.display.render.mutable_surface(surf)

        alpha = min(255, int(255 * st / self.time))


        surf.set_alpha(alpha, RLEACCEL)
        rv.blit(surf, (0, 0))

        if st < self.time:
            renpy.display.render.redraw(self, 0)
        
        return rv
    
        
