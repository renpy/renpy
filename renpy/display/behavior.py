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
                action()
                raise renpy.display.core.IgnoreEvent()
        
    # def render(self, width, height, st):
    #    return None

class KeymouseBehavior(renpy.display.layout.Null):
    """
    This is a class that causes the keyboard to move the mouse. It's
    useful on the game and key menus, as well as in imagemaps and the
    like.
    """

    def event(self, ev, x, y):
        if ev.type == renpy.display.core.DISPLAYTIME:

            pressed = pygame.key.get_pressed()

            x, y = pygame.mouse.get_pos()
            ox, oy = x, y

            if is_pressed(pressed, "keymouse_left"):
                x -= renpy.config.keymouse_distance
            if is_pressed(pressed, "keymouse_right"):
                x += renpy.config.keymouse_distance
            if is_pressed(pressed, "keymouse_up"):
                y -= renpy.config.keymouse_distance
            if is_pressed(pressed, "keymouse_down"):
                y += renpy.config.keymouse_distance

            if (x, y) != (ox, oy):
                pygame.mouse.set_pos((x, y))

            return None

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

    def __init__(self):
        super(SayBehavior, self).__init__()
              

    def event(self, ev, x, y):

        if ev.type == renpy.display.core.DISPLAYTIME and \
           renpy.config.allow_skipping and renpy.config.skipping and \
           ev.duration > renpy.config.skip_delay / 1000.0:

            if renpy.game.preferences.skip_unseen:
                return True
            elif renpy.game.context().seen_current(True):
                return True


        if map_event(ev, "dismiss"):
            return True

        if map_event(ev, "rollforward"):
            if renpy.game.context().seen_current(False):
                return True
            
        return None

class Menu(renpy.display.layout.VBox):

    def __init__(self, menuitems, style='menu', **properties):
        """
        @param menuitems: A list of menuitem tuples. The first element
        of each tuple is the string that should be displayed to the
        user. The second item is the value that should be returned if
        this item is selected, or None to indicate that this item is a
        caption.
        """

        super(Menu, self).__init__(style=style, **properties)

        self.selected = None
        self.results = [ ]

        # self.caption_style = renpy.style.Style('menu_caption', { })
        # self.selected_style = renpy.style.Style('menu_choice', { })
        # self.unselected_style = renpy.style.Style('menu_choice', { })

        # self.selected_style.set_prefix('hover_')
        # self.unselected_style.set_prefix('idle_')

        for i, (caption, result) in enumerate(menuitems):

            if result is not None:
                style = 'menu_choice'
            else:
                style = 'menu_caption'

            self.add(renpy.display.text.Text(caption, style=style))
            
            if self.selected is None and result is not None:
                self.selected = i

            self.results.append(result)

        self.update_styles()

    def update_styles(self):
        """
        This updates the colors of our children to reflect the
        one that has been selected by the user.
        """

        for i, (child, result) in enumerate(zip(self.children, self.results)):

            # Captions should stay the default text color.
            if result is None:
                continue

            # Actual choices change color if they are selected or not.
            if i == self.selected:
                child.set_style_prefix('hover_')
            else:
                child.set_style_prefix('idle_')


    def event(self, ev, x, y):
        """
        Processes events.
        """

#        print ev
#        print x, y

        old_selected = self.selected
        mouse_select = False

        # Change selection based on mouse position.
        if ev.type == MOUSEMOTION or map_event(ev, "menu_mouseselect"):
            target = self.child_at_point(x, y)
            if target is None:
                return None

            if self.results[target] is not None:
                self.selected = target
                mouse_select = True

        # Change selection based on keypress.
        if map_event(ev, "menu_keydown"):

            selected = self.selected

            while selected < len(self.results) - 1:
                selected += 1
                if self.results[selected] is not None:
                    self.selected = selected
                    break

        # Change selection based on keypress.
        if map_event(ev, "menu_keyup"):

            selected = self.selected

            while selected > 0:
                selected -= 1
                if self.results[selected] is not None:
                    self.selected = selected
                    break

        # If the selected item changed, update the display.
        if self.selected != old_selected:

            self.children[self.selected].set_style_prefix("hover_")
            self.children[old_selected].set_style_prefix("idle_")

            renpy.display.audio.play(self.style.hover_sound)
            # renpy.display.render.redraw(self, 0)

        # Make selection based on keypress or mouse click.
        if map_event(ev, "menu_keyselect") or \
           (mouse_select and map_event(ev, "menu_mouseselect")):

            self.children[self.selected].set_style_prefix("activate_")
            
            renpy.display.audio.play(self.style.activate_sound)
            return self.results[self.selected]

        return None
        
class Button(renpy.display.layout.Window):
    

    def __init__(self, child, style='button', clicked=None,
                 hovered=None, **properties):

        super(Button, self).__init__(child, style=style, **properties)
        self.style.set_prefix('idle_')

        self.activated = False

        self.old_hover = False
        self.clicked = clicked
        self.hovered = hovered

    def render(self, width, height, st):

        if self.activated:
            self.set_style_prefix('activate_')
        elif self.old_hover:
            self.set_style_prefix('hover_')
        else:
            self.set_style_prefix('idle_')


        return super(Button, self).render(width, height, st)

    def set_hover(self, hover):
        """
        Called when we change from hovered to un-hovered, or
        vice-versa.
        """

#         if hover:
#             self.style.set_prefix('hover_')
#         else:
#             self.style.set_prefix('idle_')
        
        renpy.display.render.redraw(self, 0)

    def event(self, ev, x, y):

        # We deactivate on an event.
        self.activated = False

        inside = False

        width, height = self.window_size

        if x >= 0 and x < width and y >= 0 and y < height:
            inside = True

        if self.style.enable_hover and ev.type == MOUSEMOTION:

            if self.old_hover != inside:
                self.old_hover = inside
                self.set_hover(inside)

                if inside:
                    if self.hovered:
                        self.hovered()
                        
                    renpy.display.audio.play(self.style.hover_sound)


        if map_event(ev, "button_select"):
            if inside and self.clicked:
                renpy.display.audio.play(self.style.activate_sound)

                self.activated = True
                renpy.display.render.redraw(self, 0)

                rv = self.clicked()

                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()
                    


        return super(Button, self).event(ev, x, y)

# Reimplementation of the TextButton widget as a Button and a Text
# widget.
def TextButton(text, style='button', text_style='button_text',
               clicked=None, **properties):

    text = renpy.display.text.Text(text, style=text_style)
    return Button(text, style=style, clicked=clicked, **properties)



# class TextButton(Button):

#     def __init__(self, text, style='button', text_style='button_text',
#                  clicked=None):

#         self.text_widget = renpy.display.text.Text(text, style=text_style)

#         super(TextButton, self).__init__(self.text_widget,
#                                          style=style,
#                                          clicked=clicked)

#         self.text_widget.style.set_prefix('idle_')
                                                  
#     def set_hover(self, hover):
#         super(TextButton, self).set_hover(hover)

#         if hover:
#             self.text_widget.style.set_prefix("hover_")
#         else:
#             self.text_widget.style.set_prefix("idle_")
        
                
class Input(renpy.display.text.Text):
    """
    This is a Displayable that takes text as input.
    """

    def __init__(self, default, length=None,
                 style='input_text', **properties):
        super(Input, self).__init__(default + "_", style=style, **properties)
        self.content = unicode(default)
        self.length = length

    def event(self, ev, x, y):

        if map_event(ev, "input_backspace"):
            if self.content:
                self.content = self.content[:-1]

            self.set_text(self.content + "_")
            renpy.display.render.redraw(self, 0)


        elif map_event(ev, "input_enter"):
            return self.content

        elif ev.type == KEYDOWN and ev.unicode:
            if ord(ev.unicode[0]) < 32:
                    return None
                
            if self.length and len(self.content) >= self.length:
                return None

            self.content += ev.unicode

            self.set_text(self.content + "_")
            renpy.display.render.redraw(self, 0)
                

class Bar(renpy.display.core.Displayable):
    """
    Implements a bar that can display an integer value, and respond
    to clicks on that value.
    """
    
    def __init__(self, width, height, range, value, clicked=None,
                 style='bar', **properties):

        super(Bar, self).__init__()

        self.style = renpy.style.Style(style, properties)

        self.width = width
        self.height = height
        self.range = range
        self.value = value

        self.clicked = clicked


    def event(self, ev, x, y):

        if not self.clicked:
            return

        if not map_event(ev, 'bar_click'):
            return

        if not (0 <= x < self.width and 0 <= y <= self.height):
            return

        # print x, y

        lgutter = self.style.left_gutter
        rgutter = self.style.right_gutter

        if x < lgutter:
            value = 0
        elif x > self.width - rgutter:
            value = self.range
        else:
            barwidth = self.width - lgutter - rgutter

            # This makes it easier to select 100%.
            x = x - lgutter
            x = x + (barwidth / self.range // 2)

            value = x * self.range / barwidth

            value = max(value, 0)


            rv = self.clicked(value)
            
            if rv is not None:
                return rv
            else:
                raise renpy.display.core.IgnoreEvent()

    def render(self, width, height, st):

        width = self.width
        height = self.height

        # The amount of space taken up by the bars.

        if self.clicked:
            lgutter = self.style.left_gutter
            rgutter = self.style.right_gutter 
        else:
            lgutter = 0
            rgutter = 0

        barwidth = width - lgutter - rgutter

        left_width = barwidth * self.value // self.range
        right_width = barwidth - left_width

        rv = renpy.display.render.Render(width, height)

        lsurf = render(self.style.left_bar, left_width, height, st)
        rsurf = render(self.style.right_bar, right_width, height, st)

        rv.blit(lsurf, (lgutter, 0))
        rv.blit(rsurf, (lgutter + left_width, 0))

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

        self.state = eval(self.condition, renpy.game.store)

    def render(self, width, height, st):
        if self.state:
            return render(self.child, width, height, st)
        else:
            return render(self.null, width, height, st)

    def event(self, ev, x, y):

        state = eval(self.condition, renpy.game.store)

        if state != self.state:
            renpy.display.render.redraw(self, 0)

        self.state = state

        if state:
            return self.child.event(ev, x, y)
        
            
