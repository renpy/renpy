import renpy
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
        
    def event(self, ev, x, y):
        event_list = self.new_scene_list[:]
        event_list.reverse()

        offsets = self.offsets[:]
        offsets.reverse()

        for (key, st, disp), (xo, yo) in zip(event_list, offsets):
            rv = disp.event(ev, x - xo, y - yo)
            if rv is not None:
                return rv

        return None

class Fade(Transition):
    """
    This is a transition that involves fading to a certain color, then
    holding that color for a certain amount of time, then fading in the
    new scene.
    """

    def __init__(self, out_time, hold_time, in_time,
                 old_scene_list, new_scene_list, color=(0, 0, 0)):

        super(Fade, self).__init__(out_time + hold_time + in_time)

        self.out_time = out_time
        self.hold_time = hold_time
        self.in_time = in_time
        self.old_scene_list = old_scene_list
        self.new_scene_list = new_scene_list
        self.color = color

        # self.frames = 0

    # def __del__(self):
    #     print "Faded using", self.frames, "frames."

    def render(self, width, height, st):

        # self.frames += 1

        rv = renpy.display.surface.Surface(width, height)

        events = False

        if st < self.out_time:
            scene_list = self.old_scene_list
            alpha = int(255 * (st / self.out_time))

        elif st < self.out_time + self.hold_time:
            scene_list = None
            alpha = 255

        else:
            scene_list = self.new_scene_list
            alpha = 255 - int(255 * ((st - self.out_time - self.hold_time) / self.in_time))
            events = True

        if scene_list:
            surf, offsets = renpy.display.core.render_scene_list(scene_list,
                                                                 width,
                                                                 height)
            rv.blit(surf, (0, 0))

            if events:
                self.offsets = offsets

        # Just to be sure.
        if alpha < 0:
            alpha = 0

        if alpha > 255:
            alpha = 255

        rv.fill(self.color[:3] + (alpha,))

        if st < self.in_time + self.hold_time + self.out_time:
            renpy.game.interface.redraw(0)

        return rv

class Dissolve(Transition):

    def __init__(self, time, old_scene_list, new_scene_list):
        super(Dissolve, self).__init__(time)

        self.time = time
        self.old_scene_list = old_scene_list
        self.new_scene_list = new_scene_list

    def render(self, width, height, st):

        rsl = renpy.display.core.render_scene_list

        rv, offsets = rsl(self.old_scene_list, width, height)
        surftree, self.offsets = rsl(self.new_scene_list, width, height)
        surf = surftree.pygame_surface(False)

        alpha = min(255, int(255 * st / self.time))

        surf.set_alpha(alpha, RLEACCEL)
        rv.blit(surf, (0, 0))

        if st < self.time:
            renpy.game.interface.redraw(0)
        
        return rv
    
        
