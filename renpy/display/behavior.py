# This contains various Displayables that handle events.


import renpy

# import renpy.display.core as core
# import renpy.display.layout as layout
# import renpy.display.text as text
# import renpy.config as config
# import renpy.game as game

import pygame
from pygame.constants import *

class Keymap(renpy.display.layout.Container):
    """
    This is a behavior that maps keys to functions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, **keymap):
        self.keymap = keymap

    def event(self, ev, x, y):

        if ev.type != KEYDOWN:
            return

        for key, action in self.keymap.iteritems():
            if key == ev.unicode or ev.key == getattr(pygame.constants, key, None):
                action()
                raise renpy.display.core.IgnoreEvent()

    def render(self, width, height, st, tt):
        return None

class SayBehavior(renpy.display.layout.Container):
    """
    This is a class that implements the say behavior,
    which is to return True (ending the interaction) if
    the user presses space or enter, or clicks the left
    mouse button.
    """

    def event(self, ev, x, y):
        if ev.type == MOUSEBUTTONDOWN:
            if ev.button == 1:
                return True

        if ev.type == KEYDOWN:
            if ev.key == K_RETURN:
                return True

            if ev.key == K_SPACE:
                return True

        return None

class Menu(renpy.display.layout.VBox):

    def __init__(self, menuitems):
        """
        @param menuitems: A list of menuitem tuples. The first element
        of each tuple is the string that should be displayed to the
        user. The second item is the value that should be returned if
        this item is selected, or None to indicate that this item is a
        caption.
        """

        super(Menu, self).__init__(full=False)

        self.selected = None
        self.results = [ ]

        for i, (caption, result) in enumerate(menuitems):
            self.add(renpy.display.text.Text(caption))

            if not self.selected and result is not None:
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
                child.set_style('menu_caption')
                continue

            # Actual choices change color if they are selected or not.
            if i == self.selected:
                child.set_style('menu_choice_selected')
            else:
                child.set_style('menu_choice_unselected')


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
        if ev.type == MOUSEBUTTONDOWN:
            target = self.child_at_point(x, y)
            if target is None:
                return None

            if self.results[target] is not None:
                return self.results[target]

        # Change selection based on keypress.
        if ev.type == KEYDOWN and ev.key == K_DOWN:

            selected = self.selected

            while selected < len(self.results) - 1:
                selected += 1
                if self.results[selected] is not None:
                    self.selected = selected
                    break

        # Change selection based on keypress.
        if ev.type == KEYDOWN and ev.key == K_UP:

            selected = self.selected

            while selected > 0:
                selected -= 1
                if self.results[selected] is not None:
                    self.selected = selected
                    break

        # Make selection based on keypress.
        if ev.type == KEYDOWN and ev.key == K_RETURN:
            return self.results[self.selected]
            
        # If the selected item changed, update the display.
        if self.selected != old_selected:

            self.children[self.selected].set_style('menu_choice_selected')
            self.children[old_selected].set_style('menu_choice_unselected')

            renpy.game.interface.redraw(0)

        return None
        
class Button(renpy.display.layout.Window):
    

    def __init__(self, child, idle_style='button_idle',
                 hover_style='button_hover',
                 clicked=None):

        self.idle_style = idle_style
        self.hover_style = hover_style
        self.clicked = clicked

        super(Button, self).__init__(child, style=idle_style)

        self.old_hover = False

    def set_hover(self, hover):
        """
        Called when we change from hovered to un-hovered, or
        vice-versa.
        """

        if hover:
            style_name = self.hover_style
        else:
            style_name = self.idle_style

        self.style = renpy.style.Style(style_name, dict())
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

        if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
            if inside:
                return self.clicked


class TextButton(Button):

    def __init__(self, text, idle_style='button_idle',
                 hover_style='button_hover',
                 idle_text_style='button_idle_text',
                 hover_text_style='button_hover_text',
                 clicked=None):

        self.text_widget = renpy.display.text.Text(text, style=idle_text_style)

        super(TextButton, self).__init__(self.text_widget,
                                         idle_style=idle_style,
                                         hover_style=hover_style,
                                         clicked=clicked)

        self.idle_text_style = idle_text_style
        self.hover_text_style = hover_text_style
        

    def set_hover(self, hover):
        super(TextButton, self).set_hover(hover)

        if hover:
            style_name = self.hover_text_style
        else:
            style_name = self.idle_text_style
        
        self.text_widget.style = renpy.style.Style(style_name, dict())
                
            
            
