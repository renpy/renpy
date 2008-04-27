# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# This contains various Displayables that handle events.


import renpy
from renpy.display.render import render

import pygame
from pygame.constants import *

def compile_event(key, keydown):
    """
    Compiles a keymap entry into a python expression.

    keydown determines if we are dealing with keys going down (press),
    or keys going up (release).
    """
    
    # Lists or tuples get turned into or expressions.
    if isinstance(key, (list, tuple)):
        if not key:
            return "(False)"

        return "(" + " or ".join([compile_event(i, keydown) for i in key]) + ")"

    # If it's in config.keymap, compile what's in config.keymap.
    if key in renpy.config.keymap:
        return compile_event(renpy.config.keymap[key], keydown)

    if key is None:
        return "(False)"
    
    part = key.split("_")

    # Deal with the mouse.
    if part[0] == "mousedown":
        if keydown:
            return "(ev.type == %d and ev.button == %d)" % (pygame.MOUSEBUTTONDOWN, int(part[1]))
        else:
            return "(False)"

    if part[0] == "mouseup":
        if keydown:
            return "(ev.type == %d and ev.button == %d)" % (pygame.MOUSEBUTTONUP, int(part[1]))
        else:
            return "(False)"

    # Deal with the Joystick.
    if part[0] == "joy":
        if keydown:
            return "(ev.type == %d and ev.press and ev.press == renpy.game.preferences.joymap.get(%r, None))" % (renpy.display.core.JOYEVENT, key)
        else:
            return "(ev.type == %d and ev.release and ev.release == renpy.game.preferences.joymap.get(%r, None))" % (renpy.display.core.JOYEVENT, key)

    # Otherwise, deal with it as a key.
    if keydown:
        rv = "(ev.type == %d" % pygame.KEYDOWN
    else:
        rv = "(ev.type == %d" % pygame.KEYUP

    if part[0] == "alt":
        part.pop(0)
        rv += " and (ev.mod & %d)" % pygame.KMOD_ALT
    else:
        rv += " and not (ev.mod & %d)" % pygame.KMOD_ALT

    if part[0] == "shift":
        part.pop(0)
        rv += " and (ev.mod & %d)" % pygame.KMOD_SHIFT

    if part[0] == "noshift":
        part.pop(0)
        rv += " and not (ev.mod & %d)" % pygame.KMOD_SHIFT

    if len(part) == 1:
        if len(part[0]) != 1:
            raise Exception("Invalid key specifier %s" % key)
        rv += " and ev.unicode == %r)" % part[0]        

    else:
        if part[0] != "K":
            raise Exception("Invalid key specifier %s" % key)

        key = "_".join(part)
        
        rv += " and ev.key == %d)" % (getattr(pygame.constants, key)) 

    return rv

# These store a lambda for each compiled key in the system.
event_cache = { }
keyup_cache = { }

def map_event(ev, name):
    """Returns true if the event matches the named keycode being pressed."""

    check_code = event_cache.get(name, None)
    if check_code is None:
        check_code = eval("lambda ev : " + compile_event(name, True), globals())
        event_cache[name] = check_code

    return check_code(ev)
        
def map_keyup(ev, name):
    """Returns true if the event matches the named keycode being released."""
    
    check_code = keyup_cache.get(name, None)
    if check_code is None:
        check_code = eval("lambda ev : " + compile_event(name, False), globals())
        keyup_cache[name] = check_code

    return check_code(ev)
    

def skipping(ev):
    """
    This handles setting skipping in response to the press of one of the
    CONTROL keys. The library handles skipping in response to TAB.
    """

    if not renpy.config.allow_skipping:
        return

    
    if map_event(ev, "skip"):
        renpy.config.skipping = "slow"
        renpy.exports.restart_interaction()
        
    if map_keyup(ev, "skip"):
        renpy.config.skipping = None
        renpy.exports.restart_interaction()

    return


def inspector(ev):
    return map_event(ev, "inspector")


class Keymap(renpy.display.layout.Null):
    """
    This is a behavior that maps keys to functions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, **keymap):
        super(Keymap, self).__init__(style='default')
        self.keymap = keymap

    def event(self, ev, x, y, st):

        for name, action in self.keymap.iteritems():
            if map_event(ev, name):
                rv = action()
                
                if rv is not None:
                    return rv
                
                raise renpy.display.core.IgnoreEvent()


class RollForward(renpy.display.layout.Null):
    """
    This is a behavior that maps keys to functions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, value):
        super(RollForward, self).__init__(style='default')
        self.value = value

        
    def event(self, ev, x, y, st):
        
        if map_event(ev, "rollforward"):
            renpy.game.interface.suppress_transition = True
            renpy.game.after_rollback = True
            return self.value

class PauseBehavior(renpy.display.layout.Null):
    """
    This is a class implementing the Pause behavior, which is to
    return a value after a certain amount of time has elapsed.
    """

    def __init__(self, delay, result=False):
        super(PauseBehavior, self).__init__()

        self.delay = delay
        self.result = result 


    def event(self, ev, x, y, st):

        if self.delay is not None and st >= self.delay:
            return self.result

        renpy.game.interface.timeout(self.delay - st)

class SayBehavior(renpy.display.layout.Null):
    """
    This is a class that implements the say behavior,
    which is to return True (ending the interaction) if
    the user presses space or enter, or clicks the left
    mouse button.
    """

    focusable = True

    def __init__(self, default=True, afm=None, dismiss=[ 'dismiss' ], allow_dismiss=None, **properties):
        super(SayBehavior, self).__init__(default=default, **properties)

        if not isinstance(dismiss, (list, tuple)):
            dismiss = [ dismiss ]

        if afm is not None:
            self.afm_length = len(afm)
        else:
            self.afm_length = None

        # What keybindings lead to dismissal?
        self.dismiss = dismiss

        self.allow_dismiss = allow_dismiss
        
    def set_afm_length(self, afm_length):
        self.afm_length = afm_length
              
    def event(self, ev, x, y, st):

        skip_delay = renpy.config.skip_delay / 1000.0

        if renpy.config.allow_skipping and renpy.config.skipping and \
           st >= skip_delay:

            if renpy.game.preferences.skip_unseen:
                return True
            elif renpy.config.skipping == "fast":
                return True
            elif renpy.game.context().seen_current(True):
                return True

        if renpy.config.allow_skipping and renpy.config.skipping and \
           st < skip_delay:
            renpy.game.interface.timeout(skip_delay - st)

        if self.afm_length and renpy.game.preferences.afm_time and renpy.game.preferences.afm_enable:
                                                          
            afm_delay = ( 1.0 * ( renpy.config.afm_bonus + self.afm_length ) / renpy.config.afm_characters ) * renpy.game.preferences.afm_time

            if renpy.game.preferences.text_cps:
                afm_delay += 1.0 / renpy.game.preferences.text_cps * self.afm_length

            if st > afm_delay:
                if renpy.config.afm_callback:
                    if renpy.config.afm_callback():
                        return True
                    else:
                        renpy.game.interface.timeout(0.1)
                else:
                    return True
            else:
                renpy.game.interface.timeout(afm_delay - st)

        for dismiss in self.dismiss:

            if map_event(ev, dismiss) and self.is_focused():

                if renpy.config.skipping:
                    renpy.config.skipping = None
                    renpy.exports.restart_interaction()
                    raise renpy.display.core.IgnoreEvent()

                if self.allow_dismiss:
                    if not self.allow_dismiss():
                        raise renpy.display.core.IgnoreEvent()

                return True
            
        return None
    
class Button(renpy.display.layout.Window):

    def __init__(self, child, style='button', clicked=None,
                 hovered=None, unhovered=None, role='',
                 time_policy=None, 
                 **properties):

        super(Button, self).__init__(child, style=style, **properties)

        self.activated = False
        self.clicked = clicked
        self.hovered = hovered
        self.unhovered = unhovered
        self.focusable = clicked is not None
        self.role = role

        self.time_policy_data = None
        
        
    def render(self, width, height, st, at):

        if self.style.time_policy:
            st, self.time_policy_data = self.style.time_policy(st, self.time_policy_data, self.style)
        
        rv = super(Button, self).render(width, height, st, at)

        if self.clicked:

            rect = self.style.focus_rect
            if rect is not None:
                fx, fy, fw, fh = rect
            else:
                fx = self.style.left_margin
                fy = self.style.top_margin
                fw = rv.width - self.style.right_margin
                fh = rv.height - self.style.bottom_margin

            mask = self.style.focus_mask

            if mask is True:
                mask = rv
            elif mask is not None:
                mask = renpy.easy.displayable(mask)
                mask = renpy.display.render.render(mask, rv.width, rv.height, st, at)

            if mask is not None:
                fmx = 0
                fmy = 0
            else:
                fmx = None
                fmy = None
                
            rv.add_focus(self, None,
                         fx, fy, fw, fh,
                         fmx, fmy, mask)
            
        return rv


    def focus(self, default=False):
        super(Button, self).focus(default)

        if self.activated:
            return None

        if self.hovered and not default:
            return self.hovered()


    def unfocus(self):
        super(Button, self).unfocus()

        if self.activated:
            return None
        
        if self.unhovered:
            self.unhovered()

    def per_interact(self):
        if not self.clicked:
            self.set_style_prefix(self.role + "insensitive_")

        super(Button, self).per_interact()
            
    def event(self, ev, x, y, st):

        # If not focused, ignore all events.
        if not self.is_focused():
            return None
        
        # If clicked, 
        if map_event(ev, "button_select") and self.clicked:

            self.activated = True
            self.style.set_prefix(self.role + 'activate_')
            
            renpy.audio.sound.play(self.style.sound)
                    
            rv = self.clicked()

            if rv is not None:
                return rv
            else:
                self.activated = False

                if self.is_focused():
                    self.set_style_prefix(self.role + "hover_")
                else:
                    self.set_style_prefix(self.role + "idle_")
                    
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

    def event(self, ev, x, y, st):

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

# A map from adjustment to lists of displayables that want to be redrawn
# if the adjustment changes.
adj_registered = { }

# This class contains information about an adjustment that can change the
# position of content.
class Adjustment(renpy.object.Object):

    def __init__(self, range=1, value=0, step=None, page=0, changed=None, adjustable=True, ranged=None):
        self._value = value
        self._range = range
        self._page = page
        self._step = step
        self.changed = changed
        self.adjustable = changed or adjustable
        self.ranged = ranged
        
    def get_value(self):
        return self._value

    def set_value(self, v):
        self._value = v

    value = property(get_value, set_value)
        
    def get_range(self):
        return self._range

    def set_range(self, v):
        self._range = v
        if self.ranged:
            self.ranged(self)
        
    range = property(get_range, set_range)

    def get_page(self):
        if self._page is not None:
            return self._page

        return self._range / 10

    def set_page(self, v):
        self._page = v

    page = property(get_page, set_page)

    def get_step(self):
        if self._step is not None:
            return self._step

        if self._page is not None:
            return self._page / 10

        if isinstance(self._range, float):
            return self._range / 20
        else:
            return 1

    def set_step(self, v):
        self._step = v

    step = property(get_step, set_step)
        
    # Register a displayable to be redrawn when this adjustment changes.
    def register(self, d):
        adj_registered.setdefault(self, [ ]).append(d)
            
    def change(self, value):

        if value < 0:
            value = 0
        if value > self._range:
            value = self._range

        if value != self._value:
            self._value = value
            for d in adj_registered.setdefault(self, [ ]):
                renpy.display.render.redraw(d, 0)
            if self.changed:
                return self.changed(value)

        return None
            
class Bar(renpy.display.core.Displayable):
    """
    Implements a bar that can display an integer value, and respond
    to clicks on that value.
    """

    __version__ = 1

    def after_upgrade(version):

        if version < 1:
            self.adjustment = Adjustment(self.range, self.value, changed=self.changed)
            self.adjustment.register(self)
            del self.range
            del self.value
            del self.changed
    
    def __init__(self,
                 range=None,
                 value=None,
                 width=None,
                 height=None,
                 changed=None,
                 adjustment=None,
                 step=None,
                 page=None,
                 bar=None,
                 style='bar',
                 **properties):

        if adjustment is None:
            adjustment = Adjustment(range, value, step=step, page=page, changed=changed, adjustable=False)
        
        if width is not None:
            properties['xmaximum'] = width

        if height is not None:
            properties['ymaximum'] = height

        super(Bar, self).__init__(style=style, **properties)

        self.adjustment = adjustment
        self.focusable = adjustment.adjustable
        
    def visit(self):
        return [ self.style.fore_bar, self.style.aft_bar, self.style.thumb, self.style.thumb_shadow ]

    def per_interact(self):
        self.adjustment.register(self)
    
    def render(self, width, height, st, at):

        # Store the width and height for the event function to use.
        self.width = width
        self.height = height

        range = self.adjustment.range
        value = self.adjustment.value
        page = self.adjustment.page

        if self.style.bar_invert ^ self.style.bar_vertical:
            value = range - value

        bar_vertical = self.style.bar_vertical

        if bar_vertical:
            dimension = height
        else:
            dimension = width

        fore_gutter = self.style.fore_gutter
        aft_gutter = self.style.aft_gutter

        active = dimension - fore_gutter - aft_gutter
        if range:
            thumb_dim = active * page / (range + page) 
        else:
            thumb_dim = active

        thumb_offset = abs(self.style.thumb_offset)

        if bar_vertical:
            thumb = render(self.style.thumb, width, thumb_dim, st, at)
            thumb_shadow = render(self.style.thumb_shadow, width, thumb_dim, st, at)
            thumb_dim = thumb.height
        else:
            thumb = render(self.style.thumb, thumb_dim, height, st, at)
            thumb_shadow = render(self.style.thumb_shadow, thumb_dim, height, st, at)
            thumb_dim = thumb.width

        # Remove the offset from the thumb.
        thumb_dim -= thumb_offset * 2
        self.thumb_dim = thumb_dim
        
        active -= thumb_dim

        if range:
            fore_size = active * value / range
        else:
            fore_size = active
            
        aft_size = active - fore_size

        fore_size += fore_gutter
        aft_size += aft_gutter

        rv = renpy.display.render.Render(width, height)
        
        if bar_vertical:

            if self.style.bar_resizing:
                foresurf = render(self.style.fore_bar, width, fore_size, st, at)
                aftsurf = render(self.style.aft_bar, width, aft_size, st, at)
                rv.blit(thumb_shadow, (0, fore_size - thumb_offset))
                rv.blit(foresurf, (0, 0), main=False)
                rv.blit(aftsurf, (0, height-aft_size), main=False)
                rv.blit(thumb, (0, fore_size - thumb_offset))

            else:
                foresurf = render(self.style.fore_bar, width, height, st, at)
                aftsurf = render(self.style.aft_bar, width, height, st, at)

                rv.blit(thumb_shadow, (0, fore_size - thumb_offset))
                rv.blit(foresurf.subsurface((0, 0, width, fore_size)), (0, 0), main=False)
                rv.blit(aftsurf.subsurface((0, height - aft_size, width, aft_size)), (0, height - aft_size), main=False)
                rv.blit(thumb, (0, fore_size - thumb_offset))

        else:
            if self.style.bar_resizing:
                foresurf = render(self.style.fore_bar, fore_size, height, st, at)
                aftsurf = render(self.style.aft_bar, aft_size, height, st, at)
                rv.blit(thumb_shadow, (fore_size - thumb_offset, 0))
                rv.blit(foresurf, (0, 0), main=False)
                rv.blit(aftsurf, (width-aft_size, 0), main=False)
                rv.blit(thumb, (fore_size - thumb_offset, 0))

            else:
                foresurf = render(self.style.fore_bar, width, height, st, at)
                aftsurf = render(self.style.aft_bar, width, height, st, at)

                rv.blit(thumb_shadow, (fore_size - thumb_offset, 0))
                rv.blit(foresurf.subsurface((0, 0, fore_size, height)), (0, 0), main=False)
                rv.blit(aftsurf.subsurface((width - aft_size, 0, aft_size, height)), (width-aft_size, 0), main=False)
                rv.blit(thumb, (fore_size - thumb_offset, 0))
        
        if self.focusable:
            rv.add_focus(self, None, 0, 0, width, height)

        return rv
    
      
    def event(self, ev, x, y, st):

        if not self.focusable:
            return

        if not self.is_focused():
            return

        range = self.adjustment.range
        old_value = self.adjustment.value
        value = old_value

        invert = self.style.bar_invert ^ self.style.bar_vertical
        if invert:
            value = range - value
        
        grabbed = (renpy.display.focus.get_grab() is self)
        just_grabbed = False
            
        if not grabbed and map_event(ev, "bar_activate"):
            renpy.display.focus.set_grab(self)
            just_grabbed = True
            grabbed = True

        if grabbed:

            if map_event(ev, "bar_decrease"):
                value -= self.adjustment.step

            if map_event(ev, "bar_increase"):
                value += self.adjustment.step

            if ev.type in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):

                if self.style.bar_vertical:

                    tgutter = self.style.fore_gutter
                    bgutter = self.style.aft_gutter
                    zone_height = self.height - tgutter - bgutter - self.thumb_dim
                    if zone_height:
                        value = (y - tgutter - self.thumb_dim / 2) * range / zone_height
                    else:
                        value = 0
                        
                else:
                    lgutter = self.style.fore_gutter
                    rgutter = self.style.aft_gutter
                    zone_width = self.width - lgutter - rgutter - self.thumb_dim   
                    if zone_width:
                        value = (x - lgutter - self.thumb_dim / 2) * range / zone_width
                    else:
                        value = 0
                        
            if isinstance(range, int):
                value = int(value)

            if value < 0:
                value = 0

            if value > range:
                value = range

        if invert:
            value = range - value
            
        if grabbed and not just_grabbed and map_event(ev, "bar_deactivate"):
            renpy.display.focus.set_grab(None)

        if value != old_value:
            return self.adjustment.change(value)

        return None
     
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

    def render(self, width, height, st, at):
        if self.state:
            return render(self.child, width, height, st, at)
        else:
            return render(self.null, width, height, st, at)

    def event(self, ev, x, y, st):

        state = eval(self.condition, vars(renpy.store))

        if state != self.state:
            renpy.display.render.redraw(self, 0)

        self.state = state

        if state:
            return self.child.event(ev, x, y, st)
        
            
class Timer(renpy.display.layout.Null):

    def __init__(self, delay, function, repeat=False, args=(), kwargs={}):
        super(Timer, self).__init__()

        if delay <= 0:
            raise Exception("A timer's delay must be > 0.")

        self.delay = delay
        self.function = function
        self.repeat = repeat
        self.next_event = delay
        self.args = args
        self.kwargs = kwargs
        
    def event(self, ev, x, y, st):

        if self.next_event is None:
            return
        
        if st < self.next_event:
            renpy.game.interface.timeout(self.next_event - st)
            return

        if not self.repeat:
            self.next_event = None
        else:
            while self.next_event < st:
                self.next_event += self.delay

            renpy.game.interface.timeout(self.next_event - st)

        return self.function(*self.args, **self.kwargs)

    
        
