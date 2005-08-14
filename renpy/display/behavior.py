# This contains various Displayables that handle events.


import renpy
from renpy.display.render import render

# import renpy.display.core as core
# import renpy.display.layout as layout
# import renpy.display.text as text
# import renpy.config as config
# import renpy.game as game

import pygame
from pygame.constants import *

def map_event(ev, name):
    """
    This looks up the name in the keymap, and uses it to determine if
    the given event was caused by one of the keys or mouse buttons
    mapped to the given name in config.keymap. If so, it returns
    True, otherwise it returns False.
    """
    
    keys = renpy.config.keymap[name]

    if ev.type == MOUSEBUTTONDOWN:
        if ( "mousedown_" + str(ev.button) ) in keys:
            return True
        else:
            return False

    if ev.type == MOUSEBUTTONUP:
        if ( "mouseup_" + str(ev.button) ) in keys:
            return True
        else:
            return False

    if ev.type == KEYDOWN:
        for key in keys:
            if key == ev.unicode or ev.key == getattr(pygame.constants, key, None):
                return True

        return False

    return False

def map_keyup(ev, name):

    keys = renpy.config.keymap[name]
    
    if ev.type == KEYUP:
        for key in keys:
            if ev.key == getattr(pygame.constants, key, None):
                return True

    return False
    
        
def is_pressed(pressed, name):
    """
    This looks the given name up in the keymap. For each binding of the
    form K_whatever, it checks to see if the given key is pressed, and if
    so, returns the keycode of the pressed key. Otherwise, returns False.
    """

    keys = renpy.config.keymap[name]

    for key in keys:
        code = getattr(pygame.constants, key)
        if pressed[code]:
            return code

    return False

def skipping(ev):
    """
    This handles setting skipping in response to the press of one of the
    CONTROL keys. The library handles skipping in response to TAB.
    """

    if map_event(ev, "skip"):
        renpy.config.skipping = True

    if map_keyup(ev, "skip"):
        renpy.config.skipping = False

    return

class Keymap(renpy.display.layout.Null):
    """
    This is a behavior that maps keys to functions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, **keymap):
        super(Keymap, self).__init__(style='default')
        self.keymap = keymap

    def event(self, ev, x, y):

        for name, action in self.keymap.iteritems():
            if map_event(ev, name):
                rv = action()
                
                if rv is not None:
                    return rv
                
                raise renpy.display.core.IgnoreEvent()
        
    # def render(self, width, height, st):
    #    return None

class PauseBehavior(renpy.display.layout.Null):
    """
    This is a class implementing the Pause behavior, which is to
    return a value after a certain amount of time has elapsed.
    """

    def __init__(self, delay, result=False):
        super(PauseBehavior, self).__init__()

        self.delay = delay
        self.result = result 


    def event(self, ev, x, y):
              
        if ev.type == renpy.display.core.DISPLAYTIME and \
           self.delay and ev.duration > self.delay:
            return self.result
    

class SayBehavior(renpy.display.layout.Null):
    """
    This is a class that implements the say behavior,
    which is to return True (ending the interaction) if
    the user presses space or enter, or clicks the left
    mouse button.
    """

    focusable = True

    def __init__(self, default=True, afm=None, **properties):
        super(SayBehavior, self).__init__(default=default, **properties)

        if afm is not None:
            self.afm_length = len(afm)
        else:
            self.afm_length = None
              
    def event(self, ev, x, y):

        if ev.type == renpy.display.core.DISPLAYTIME and \
               renpy.config.allow_skipping and renpy.config.skipping and \
               ev.duration > renpy.config.skip_delay / 1000.0:

            if renpy.game.preferences.skip_unseen:
                return True
            elif renpy.game.context().seen_current(True):
                return True

        if ev.type == renpy.display.core.DISPLAYTIME and \
               self.afm_length and renpy.game.preferences.afm_time and \
               ev.duration > ( 1.0 * ( renpy.config.afm_bonus + self.afm_length ) / renpy.config.afm_characters ) * renpy.game.preferences.afm_time:

            return True

        if map_event(ev, "dismiss") and self.is_focused():
            return True

        if map_event(ev, "rollforward"):
            if renpy.game.context().seen_current(False):
                return True
            
        return None
        
class Button(renpy.display.layout.Window):

    def __init__(self, child, style='button', clicked=None,
                 hovered=None, unhovered=None, **properties):

        super(Button, self).__init__(child, style=style, **properties)

        self.activated = False
        self.clicked = clicked
        self.hovered = hovered
        self.unhovered = unhovered
        self.focusable = clicked is not None

    def render(self, width, height, st):

        rv = super(Button, self).render(width, height, st)

        if self.clicked:
            rv.add_focus(self,
                         None,
                         self.style.left_margin,
                         self.style.top_margin,
                         rv.width - self.style.right_margin,
                         rv.height - self.style.bottom_margin)
            
        return rv


    def focus(self, default=False):
        super(Button, self).focus(default)

        if self.hovered:
            self.hovered()

    def unfocus(self):
        super(Button, self).unfocus()

        if self.unhovered:
            self.unhovered()

    def event(self, ev, x, y):

        # We deactivate on an event.
        if self.activated:
            self.activated = False

            if self.focusable:
                if self.is_focused():
                    self.set_style_prefix('hover_')
                else:
                    self.set_style_prefix('idle_')
            else:
                self.set_style_prefix('insensitive_')

        # If not focused, ignore all events.
        if not self.is_focused():
            return None

        # If clicked, 
        if map_event(ev, "button_select") and self.clicked:

            self.activated = True

            self.set_style_prefix('activate_')
            renpy.audio.sound.play(self.style.sound)

            rv = self.clicked()

            if rv is not None:
                return rv
            else:
                raise renpy.display.core.IgnoreEvent()
                    
        return None


# Reimplementation of the TextButton widget as a Button and a Text
# widget.
def TextButton(text, style='button', text_style='button_text',
               clicked=None, **properties):

    text = renpy.display.text.Text(text, style=text_style)
    return Button(text, style=style, clicked=clicked, **properties)

                
class Input(renpy.display.text.Text):
    """
    This is a Displayable that takes text as input.
    """

    def __init__(self, default, length=None,
                 style='input_text',
                 allow=None,
                 exclude=None,
                 **properties):

        super(Input, self).__init__(default.replace("{", "{{") + "_", style=style, **properties)

        self.content = unicode(default)
        self.length = length

        self.allow = allow
        self.exclude = exclude

    def event(self, ev, x, y):

        if map_event(ev, "input_backspace"):
            if self.content:
                self.content = self.content[:-1]

            self.set_text(self.content.replace("{", "{{") + "_")
            renpy.display.render.redraw(self, 0)

        elif map_event(ev, "input_enter"):
            return self.content

        elif ev.type == KEYDOWN and ev.unicode:
            if ord(ev.unicode[0]) < 32:
                return None
                
            if self.length and len(self.content) >= self.length:
                raise renpy.display.core.IgnoreEvent()

            if self.allow and ev.unicode not in self.allow:
                raise renpy.display.core.IgnoreEvent()

            if self.exclude and ev.unicode in self.exclude:
                raise renpy.display.core.IgnoreEvent()

            self.content += ev.unicode

            self.set_text(self.content.replace("{", "{{") + "_")
            renpy.display.render.redraw(self, 0)

            raise renpy.display.core.IgnoreEvent()
                

class Bar(renpy.display.core.Displayable):
    """
    Implements a bar that can display an integer value, and respond
    to clicks on that value.
    """
    
    def __init__(self, range, value, width=None, height=None,
                 style='bar', **properties):

        super(Bar, self).__init__()

        if width is not None:
            properties['xmaximum'] = width

        if height is not None:
            properties['ymaximum'] = height

        self.style = renpy.style.Style(style, properties)

        self.range = range
        self.value = value


    def render(self, width, height, st):

        lgutter = self.style.left_gutter
        rgutter = self.style.right_gutter

        zone_width = width - lgutter - rgutter

        left_width = zone_width * self.value // self.range
        right_width = zone_width - left_width

        left_width += lgutter
        right_width += rgutter

        rv = renpy.display.render.Render(width, height)

        lsurf = render(self.style.left_bar, width, height, st)
        rsurf = render(self.style.right_bar, width, height, st)

        if self.style.thumb_shadow:
            surf = render(self.style.thumb_shadow, width, height, st)
            rv.blit(surf, (left_width + self.style.thumb_offset, 0))

        rv.blit(lsurf.subsurface((0, 0, left_width, height)), (0, 0))
        rv.blit(rsurf.subsurface((left_width, 0, right_width, height)),
                (left_width, 0))

        if self.style.thumb:
            surf = render(self.style.thumb, width, height, st)
            rv.blit(surf, (left_width + self.style.thumb_offset, 0))

        return rv
        
     
class Conditional(renpy.display.layout.Container):
    """
    This class renders its child if and only if the condition is
    true. Otherwise, it renders nothing. (Well, a Null). 

    Warning: the condition MUST NOT update the game state in any
    way, as that would break rollback.
    """

    def __init__(self, condition, *args):
        super(Conditional, self).__init__(*args)

        self.condition = condition
        self.null = renpy.display.layout.Null()

        self.state = eval(self.condition, vars(renpy.store))

    def render(self, width, height, st):
        if self.state:
            return render(self.child, width, height, st)
        else:
            return render(self.null, width, height, st)

    def event(self, ev, x, y):

        state = eval(self.condition, vars(renpy.store))

        if state != self.state:
            renpy.display.render.redraw(self, 0)

        self.state = state

        if state:
            return self.child.event(ev, x, y)
        
            
