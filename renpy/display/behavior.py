# This contains various Displayables that handle events.


import renpy

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
        if ( "mouse_" + str(ev.button) ) in keys:
            return True
        else:
            return False

    if ev.type == KEYDOWN:
        for key in keys:
            if key == ev.unicode or ev.key == getattr(pygame.constants, key, None):
                return True

        return False

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


class Keymap(renpy.display.layout.Container):
    """
    This is a behavior that maps keys to functions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, **keymap):
        self.keymap = keymap

    def event(self, ev, x, y):

        for name, action in self.keymap.iteritems():
            if map_event(ev, name):
                action()
                raise renpy.display.core.IgnoreEvent()
        
    def render(self, width, height, st):
        return None

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

class SayBehavior(renpy.display.layout.Null):
    """
    This is a class that implements the say behavior,
    which is to return True (ending the interaction) if
    the user presses space or enter, or clicks the left
    mouse button.
    """

    def __init__(self, delay=None):
        super(SayBehavior, self).__init__()

        self.delay = delay
              

    def event(self, ev, x, y):

        if ev.type == renpy.display.core.DISPLAYTIME and \
           self.delay and \
           ev.duration > self.delay:
            return False

        if map_event(ev, "dismiss"):
            return True

        if map_event(ev, "rollforward"):
            if renpy.game.context().seen_current(False):
                return True
            
        if map_event(ev, "skip"):
            if renpy.game.preferences.skip_unseen:
                return True
            elif renpy.game.context().seen_current(True):
                return True
            
        return None

class Menu(renpy.display.layout.VBox):

    def __init__(self, menuitems, **properties):
        """
        @param menuitems: A list of menuitem tuples. The first element
        of each tuple is the string that should be displayed to the
        user. The second item is the value that should be returned if
        this item is selected, or None to indicate that this item is a
        caption.
        """

        super(Menu, self).__init__(**properties)

        self.selected = None
        self.results = [ ]

        self.caption_style = renpy.style.Style('menu_caption', { })
        self.selected_style = renpy.style.Style('menu_choice', { })
        self.unselected_style = renpy.style.Style('menu_choice', { })

        self.selected_style.set_prefix('hover_')
        self.unselected_style.set_prefix('idle_')

        for i, (caption, result) in enumerate(menuitems):
            self.add(renpy.display.text.Text(caption))

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
                child.set_style(self.caption_style)
                continue

            # Actual choices change color if they are selected or not.
            if i == self.selected:
                child.set_style(self.selected_style)
            else:
                child.set_style(self.unselected_style)


    def event(self, ev, x, y):
        """
        Processes events.
        """

#        print ev
#        print x, y

        old_selected = self.selected

        # Change selection based on mouse position.
        if ev.type == MOUSEMOTION:
            target = self.child_at_point(x, y)
            if target is None:
                return None

            if self.results[target] is not None:
                self.selected = target

        # Make selection based on mouse click position.
        if map_event(ev, "menu_mouseselect"):
            target = self.child_at_point(x, y)
            if target is None:
                return None

            if self.results[target] is not None:
                renpy.sound.play(self.selected_style.activate_sound)
                return self.results[target]

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

        # Make selection based on keypress.
        if map_event(ev, "menu_keyselect"):
            renpy.sound.play(self.selected_style.activate_sound)
            return self.results[self.selected]
            
        # If the selected item changed, update the display.
        if self.selected != old_selected:

            self.children[self.selected].set_style(self.selected_style)
            self.children[old_selected].set_style(self.unselected_style)

            renpy.sound.play(self.selected_style.hover_sound)

            renpy.game.interface.redraw(0)

        return None
        
class Button(renpy.display.layout.Window):
    

    def __init__(self, child, style='button', clicked=None,
                 hovered=None, **properties):

        super(Button, self).__init__(child, style=style, **properties)
        self.style.set_prefix('idle_')

        self.old_hover = False
        self.clicked = clicked
        self.hovered = hovered

    def set_hover(self, hover):
        """
        Called when we change from hovered to un-hovered, or
        vice-versa.
        """

        if hover:
            self.style.set_prefix('hover_')
        else:
            self.style.set_prefix('idle_')
        
        renpy.game.interface.redraw(0)

    def event(self, ev, x, y):

        inside = False

        width, height = self.window_size

        if x >= 0 and x < width and y >= 0 and y < height:
            inside = True

        if ev.type == MOUSEMOTION:

            if self.old_hover != inside:
                self.old_hover = inside
                self.set_hover(inside)

                if inside:
                    if self.hovered:
                        self.hovered()
                        
                    renpy.sound.play(self.style.hover_sound)


        if map_event(ev, "button_select"):
            if inside:
                renpy.sound.play(self.style.activate_sound)
                return self.clicked()

        return None


class TextButton(Button):

    def __init__(self, text, style='button', text_style='button_text',
                 clicked=None):

        self.text_widget = renpy.display.text.Text(text, style=text_style)

        super(TextButton, self).__init__(self.text_widget,
                                         style=style,
                                         clicked=clicked)

        self.text_widget.style.set_prefix('idle_')
                                                  
    def set_hover(self, hover):
        super(TextButton, self).set_hover(hover)

        if hover:
            self.text_widget.style.set_prefix("hover_")
        else:
            self.text_widget.style.set_prefix("idle_")
        
                
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
            renpy.game.interface.redraw(0)


        elif map_event(ev, "input_enter"):
            return self.content

        elif ev.type == KEYDOWN and ev.unicode:
            if ord(ev.unicode[0]) < 32:
                    return None
                
            if self.length and len(self.content) >= self.length:
                return None

            self.content += ev.unicode

            self.set_text(self.content + "_")
            renpy.game.interface.redraw(0)
                
