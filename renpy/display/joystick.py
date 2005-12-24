# This file is responsible for joystick support in Ren'Py.

import os

import pygame
from pygame.constants import *

import renpy

# Do we have a joystick enabled?
enabled = False

# The old states for each axis.
old_axis_states = { }

def init():
    """
    Initialize the joystick system.
    """

    global enabled

    if not renpy.config.joystick:
        return

    if 'RENPY_DISABLE_JOYSTICK' in os.environ:
        return

    try:
        pygame.joystick.init()
        
        if pygame.joystick.get_count() > 0:
            pygame.joystick.Joystick(0).init()
            enabled = True
    except:        
        if renpy.config.debug:
            raise
        
def event(ev):

    if not enabled:
        return ev

    if ev.type == JOYAXISMOTION:

        if ev.value >= 0.5:
            state = "Positive"
        elif ev.value <= -0.5:
            state = "Negative"
        else:
            state = None

        if state == old_axis_states.get(ev.axis, None):
            return None

        old_axis_states[ev.axis] = state

        if state is None:
            return None

        return pygame.event.Event(renpy.display.core.JOYEVENT,
                                  name="Axis %d %s" % (ev.axis, state))

    if ev.type == JOYBUTTONDOWN:

        return pygame.event.Event(renpy.display.core.JOYEVENT,
                                  name="Button %d" % ev.button)

    return ev

class JoyBehavior(renpy.display.layout.Null):
    """
    This is a behavior intended for joystick calibration. If a joystick
    event occurs, this returns it as a string.
    """

    def event(self, ev, x, y):
        if ev.type == renpy.display.core.JOYEVENT:
            return ev.name
    
    
